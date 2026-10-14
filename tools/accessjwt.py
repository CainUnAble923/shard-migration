"""Cloudflare Access, checked by the play-test service itself (cc-P105, Haven step H1; off unless configured).

Cloudflare Access puts a signed token on every request it lets through: the Cf-Access-Jwt-Assertion header (and the
CF_Authorization cookie). The service checks it, so a request that reached the container any other way (not through
Access) gets no answer. Notes: notes/cc-P105-haven-h1-host-agnostic.md; design: notes/cc-P89-haven-pages-plan.md 5.

What is checked (Cloudflare's "Validate JWTs" rules):
- the token is three base64url parts and its header says alg RS256 with a kid;
- the signature verifies against that kid's public key from https://<team>/cdn-cgi/access/certs (fetched, cached an
  hour, fetched again at most once a minute when a kid is unknown, as after Cloudflare rotates its keys);
- aud holds the Access application's tag, iss is https://<team>, exp is in the future and nbf is not, with a minute
  of leeway either way;
- it carries an email, which becomes the writer identity ("by").

RS256 is RSA PKCS#1 v1.5 with SHA-256. The standard library has no RSA, but verifying is only a modular power and a
fixed padding compare, so it is done here (verify_rs256) rather than adding a dependency to python:3-alpine.

Standard library only. ASCII only.
"""
import base64
import hashlib
import hmac
import json
import threading
import time
import urllib.request

# DER of DigestInfo{sha256} (RFC 8017 section 9.2, note 1), followed by the 32-byte hash.
SHA256_DIGESTINFO = bytes.fromhex("3031300d060960864801650304020105000420")
LEEWAY = 60


class AccessDenied(Exception):
    pass


def b64url(s):
    s = s.encode("ascii") if isinstance(s, str) else s
    return base64.urlsafe_b64decode(s + b"=" * (-len(s) % 4))


def verify_rs256(n, e, signature, message):
    """True if signature is a valid RSASSA-PKCS1-v1_5 SHA-256 signature of message under the key (n, e)."""
    k = (n.bit_length() + 7) // 8
    if len(signature) != k:
        return False
    s = int.from_bytes(signature, "big")
    if s >= n:
        return False
    em = pow(s, e, n).to_bytes(k, "big")
    t = SHA256_DIGESTINFO + hashlib.sha256(message).digest()
    if k < len(t) + 11:
        return False
    expected = b"\x00\x01" + b"\xff" * (k - len(t) - 3) + b"\x00" + t
    return hmac.compare_digest(em, expected)


def _fetch_json(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read().decode("utf-8"))


class AccessVerifier:
    def __init__(self, team_domain, aud, fetch=None, now=None, cache_seconds=3600, certs_url=""):
        team_domain = team_domain.strip().rstrip("/")
        if team_domain.startswith("https://"):
            team_domain = team_domain[len("https://"):]
        if not team_domain or not aud:
            raise ValueError("Access needs both a team domain and an application tag (aud)")
        self.issuer = "https://" + team_domain
        # certs_url is only ever set by the tests (a local key server); Cloudflare's is the default.
        self.certs_url = certs_url or (self.issuer + "/cdn-cgi/access/certs")
        self.aud = aud.strip()
        self._fetch = fetch or _fetch_json
        self._now = now or time.time
        self._cache_seconds = cache_seconds
        self._keys = {}
        self._fetched = 0.0
        self._lock = threading.Lock()

    def _load_keys(self, force=False):
        with self._lock:
            age = self._now() - self._fetched
            if self._keys and not force and age < self._cache_seconds:
                return self._keys
            if force and age < 60 and self._keys:
                return self._keys
            doc = self._fetch(self.certs_url)
            keys = {}
            for k in doc.get("keys", []):
                if k.get("kty") == "RSA" and k.get("kid") and k.get("n") and k.get("e"):
                    keys[k["kid"]] = (int.from_bytes(b64url(k["n"]), "big"), int.from_bytes(b64url(k["e"]), "big"))
            self._keys = keys
            self._fetched = self._now()
            return keys

    def verify(self, token):
        """The token's claims if it is good; AccessDenied with a short reason if not."""
        if not token or not isinstance(token, str):
            raise AccessDenied("no Access token")
        parts = token.strip().split(".")
        if len(parts) != 3:
            raise AccessDenied("not a JWT")
        try:
            header = json.loads(b64url(parts[0]))
            claims = json.loads(b64url(parts[1]))
            sig = b64url(parts[2])
        except (ValueError, TypeError):
            raise AccessDenied("not a JWT")
        if not isinstance(header, dict) or not isinstance(claims, dict):
            raise AccessDenied("not a JWT")
        if header.get("alg") != "RS256" or not header.get("kid"):
            raise AccessDenied("not an RS256 token with a key id")
        try:
            keys = self._load_keys()
            if header["kid"] not in keys:
                keys = self._load_keys(force=True)
        except (OSError, ValueError) as e:
            raise AccessDenied("cannot fetch the Access keys: %s" % e)
        key = keys.get(header["kid"])
        if key is None:
            raise AccessDenied("unknown key id")
        if not verify_rs256(key[0], key[1], sig, (parts[0] + "." + parts[1]).encode("ascii")):
            raise AccessDenied("bad signature")
        aud = claims.get("aud")
        if self.aud not in (aud if isinstance(aud, list) else [aud]):
            raise AccessDenied("wrong audience")
        if claims.get("iss") != self.issuer:
            raise AccessDenied("wrong issuer")
        now = self._now()
        try:
            if float(claims["exp"]) < now - LEEWAY:
                raise AccessDenied("expired")
            if "nbf" in claims and float(claims["nbf"]) > now + LEEWAY:
                raise AccessDenied("not valid yet")
        except (KeyError, TypeError, ValueError):
            raise AccessDenied("no expiry")
        if not str(claims.get("email") or "").strip():
            raise AccessDenied("no email in the token")
        return claims


def token_from(headers):
    """The Access token from a request: the header Cloudflare adds, else the CF_Authorization cookie."""
    t = headers.get("Cf-Access-Jwt-Assertion") or ""
    if t:
        return t.strip()
    for part in (headers.get("Cookie") or "").split(";"):
        name, _, value = part.strip().partition("=")
        if name == "CF_Authorization":
            return value.strip()
    return ""
