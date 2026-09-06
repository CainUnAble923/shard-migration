# Account export source verification

Verified 2026-09-06 against:

- ModernUO `7c9215d97cb25c56b0b5cb35034944ccdaa0a485`
- ServUO pub57 `d76bf4443cf76d081ddaf8f57c87ff33749256af`

ModernUO sources inspected:

- `Projects/UOContent/Accounting/Account.cs`
- `Projects/UOContent/Accounting/Accounts.cs`
- `Projects/UOContent/Accounting/AccountComment.cs`
- `Projects/UOContent/Accounting/AccountTag.cs`
- `Projects/UOContent/Accounting/Security/AccountSecurity.cs`
- `Projects/UOContent/Accounting/Security/HashAlgorithmPasswordProtection.cs`
- `Projects/Server/IAccount.cs`

ServUO sources inspected:

- `Scripts/Accounting/Account.cs`
- `Scripts/Accounting/Accounts.cs`
- `Scripts/Accounting/AccountComment.cs`
- `Scripts/Accounting/AccountTag.cs`

Verified mappings implemented by `tools/modernuo/ExportServUOAccounts.cs`:

- Both engines compute SHA2 passwords as SHA-512 over ASCII `username + password`, capped
  to the first 256 characters. ModernUO stores contiguous hexadecimal; ServUO's
  `newSecureCryptPassword` stores `BitConverter.ToString` hexadecimal with hyphens.
- Username, access level, flags, created/last-login timestamps, total game time, character
  serial/index pairs, comments, tags, and login IPs have matching ServUO XML fields.
- The exporter fails closed before writing if any live account is not SHA2 or does not have
  a 128-character hexadecimal SHA-512 digest.
- The file is written to a temporary sibling and moved into place only after XML writing
  succeeds.

Source-verified incompatibilities:

- ModernUO stores exact integer gold and platinum balances. ServUO pub57 serializes both
  through a `double totalCurrency` value. At sufficiently large platinum values, IEEE-754
  precision cannot represent every individual gold value.
- ModernUO persists `Email`; ServUO's `Account` declares an Email property but its XML
  constructor and `Save` method do not load or save it.
- ModernUO has no account fields corresponding to ServUO sovereigns, IP restrictions, or
  secure per-character account balances. The export initializes sovereigns to zero and
  leaves the others absent.

The exporter includes `modernUOEmail`, `modernUOTotalGold`, and `modernUOTotalPlat`
extension elements so the source data survives the intermediate XML.
`tools/servuo/Account-modernuo-email.patch` loads the email extension and saves it as an
`email` element, which the patch also reloads. Exact high-balance currency preservation
remains unresolved because ServUO's in-memory account model uses `double`.

Verification performed:

- The exporter was copied into a disposable checkout at the pinned ModernUO commit.
- `dotnet build Projects/UOContent/UOContent.csproj --no-restore -v minimal` completed with
  zero warnings and zero errors.
- The email patch was applied by hand to the pristine pub57 `Account.cs` in the ServUO
  scratch tree; a full Release build completed with zero warnings and zero errors.
- Running the command against the live shard, inspecting a real exported file, preserving
  filesystem permissions, and loading it in ServUO remain unverified.
