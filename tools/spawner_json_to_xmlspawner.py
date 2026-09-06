#!/usr/bin/env python3
"""Convert ModernUO exported spawners to ServUO XmlSpawner DataSet XML.

The converter is intentionally strict: unsupported ModernUO behavior is reported and
prevents output unless --skip-unsupported is supplied.  The XML shape and field
values follow ServUO pub57's XmlSpawner2 SaveSpawnList/LoadSpawnList implementation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SUPPORTED_MAPS = {"Felucca", "Trammel", "Ilshenar", "Malas", "Tokuno", "TerMur"}
SUPPORTED_TYPES = {"Spawner", "RegionSpawner"}
KNOWN_KEYS = {
    "type", "guid", "location", "map", "count", "entries", "name",
    "minDelay", "maxDelay", "team", "homeRange", "walkingRange", "spawnBounds", "region",
    "spawnLocationIsHome", "spawnPositionMode", "maxSpawnAttempts",
}
OBJECT_SUFFIX = ":SB=0:RT=0:TO=0:KL=0:RK=0:CA=1:DN=-1:DX=-1:SP=1:PR=-1"
TIME_SPAN_RE = re.compile(
    r"^(?P<sign>-)?(?:(?P<days>\d+)\.)?(?P<hours>\d{1,2}):"
    r"(?P<minutes>\d{2}):(?P<seconds>\d{2})(?:\.(?P<fraction>\d{1,7}))?$"
)


class ConversionError(ValueError):
    pass


@dataclass(frozen=True)
class Issue:
    index: int
    guid: str
    message: str

    def __str__(self) -> str:
        return f"spawner[{self.index}] ({self.guid}): {self.message}"


def _require_int(value: Any, label: str, minimum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConversionError(f"{label} must be an integer")
    if minimum is not None and value < minimum:
        raise ConversionError(f"{label} must be at least {minimum}")
    return value


def _point(value: Any, label: str) -> tuple[int, int, int]:
    if isinstance(value, list) and len(value) == 3:
        parts = value
    elif isinstance(value, dict) and {"x", "y", "z"} <= value.keys():
        parts = [value["x"], value["y"], value["z"]]
    else:
        raise ConversionError(f"{label} must be [x, y, z] or an x/y/z object")
    return tuple(_require_int(part, label) for part in parts)  # type: ignore[return-value]


def _bounds(value: Any) -> tuple[int, int, int, int, int, int]:
    if isinstance(value, list) and len(value) == 6:
        x, y, z, width, height, depth = (
            _require_int(part, "spawnBounds component") for part in value
        )
        return x, y, z, x + width, y + height, z + depth

    if not isinstance(value, dict):
        raise ConversionError("spawnBounds must be an object or six-element array")
    if {"start", "end"} <= value.keys():
        return (*_point(value["start"], "spawnBounds.start"),
                *_point(value["end"], "spawnBounds.end"))
    if {"x1", "y1", "x2", "y2"} <= value.keys():
        return (
            _require_int(value["x1"], "spawnBounds.x1"),
            _require_int(value["y1"], "spawnBounds.y1"),
            _require_int(value.get("z1", -128), "spawnBounds.z1"),
            _require_int(value["x2"], "spawnBounds.x2"),
            _require_int(value["y2"], "spawnBounds.y2"),
            _require_int(value.get("z2", 127), "spawnBounds.z2"),
        )
    if {"x", "y", "width", "height"} <= value.keys():
        x = _require_int(value["x"], "spawnBounds.x")
        y = _require_int(value["y"], "spawnBounds.y")
        z = _require_int(value.get("z", -128), "spawnBounds.z")
        width = _require_int(value["width"], "spawnBounds.width", 1)
        height = _require_int(value["height"], "spawnBounds.height", 1)
        depth = _require_int(value.get("depth", 255), "spawnBounds.depth", 1)
        return x, y, z, x + width, y + height, z + depth
    raise ConversionError("unrecognized spawnBounds representation")


def _time_span_seconds(value: Any, label: str) -> int:
    if not isinstance(value, str):
        raise ConversionError(f"{label} must be a .NET TimeSpan string")
    match = TIME_SPAN_RE.fullmatch(value)
    if not match or match.group("sign"):
        raise ConversionError(f"{label} must be a non-negative .NET TimeSpan")
    hours = int(match.group("hours"))
    minutes = int(match.group("minutes"))
    seconds = int(match.group("seconds"))
    if hours > 23 or minutes > 59 or seconds > 59:
        raise ConversionError(f"{label} has an out-of-range component")
    if match.group("fraction") and int(match.group("fraction")) != 0:
        raise ConversionError(f"{label} has sub-second precision XmlSpawner cannot store")
    return int(match.group("days") or 0) * 86400 + hours * 3600 + minutes * 60 + seconds


def _entry_spec(entry: Any, label: str) -> str:
    if not isinstance(entry, dict):
        raise ConversionError(f"{label} must be an object")
    unknown = set(entry) - {"name", "probability", "maxCount", "properties", "parameters"}
    if unknown:
        raise ConversionError(f"{label} has unknown fields: {', '.join(sorted(unknown))}")
    name = entry.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ConversionError(f"{label}.name must be a non-empty string")
    if any(token in name for token in (":MX=", ":OBJ=")):
        raise ConversionError(f"{label}.name contains an XmlSpawner delimiter")
    probability = _require_int(entry.get("probability", 100), f"{label}.probability")
    if probability != 100:
        raise ConversionError(f"{label}.probability={probability} has no per-entry XmlSpawner equivalent")
    max_count = _require_int(entry.get("maxCount", 1), f"{label}.maxCount", 1)
    if entry.get("properties") is not None:
        raise ConversionError(f"{label}.properties conversion is unverified")
    if entry.get("parameters") is not None:
        raise ConversionError(f"{label}.parameters conversion is unverified")
    return f"{name}:MX={max_count}{OBJECT_SUFFIX}"


def _add(row: ET.Element, name: str, value: Any) -> None:
    element = ET.SubElement(row, name)
    if isinstance(value, bool):
        element.text = "True" if value else "False"
    elif value is not None:
        element.text = str(value)


def convert_one(spawner: Any, index: int, allow_z_loss: bool = False) -> ET.Element:
    if not isinstance(spawner, dict):
        raise ConversionError("spawner must be an object")
    unknown = set(spawner) - KNOWN_KEYS
    if unknown:
        raise ConversionError(f"unknown fields: {', '.join(sorted(unknown))}")

    spawner_type = spawner.get("type")
    if spawner_type not in SUPPORTED_TYPES:
        raise ConversionError(f"type {spawner_type!r} is unsupported")
    guid_text = spawner.get("guid")
    try:
        guid_text = str(uuid.UUID(str(guid_text)))
    except (ValueError, AttributeError):
        raise ConversionError("guid must be a valid UUID") from None
    location = _point(spawner.get("location"), "location")
    map_name = spawner.get("map")
    if map_name not in SUPPORTED_MAPS:
        raise ConversionError(f"map {map_name!r} is not registered by ServUO pub57 MapDefinitions")
    count = _require_int(spawner.get("count"), "count", 0)
    team = _require_int(spawner.get("team", 0), "team")
    walking_range = _require_int(spawner.get("walkingRange", 0), "walkingRange")
    if walking_range < -1:
        raise ConversionError("walkingRange must be -1 or greater")
    spawn_location_is_home = spawner.get("spawnLocationIsHome", False)
    if not isinstance(spawn_location_is_home, bool):
        raise ConversionError("spawnLocationIsHome must be a boolean")
    position_mode = spawner.get("spawnPositionMode", "Automatic")
    if position_mode not in ("Automatic", 0, None):
        raise ConversionError(f"spawnPositionMode={position_mode!r} has no XmlSpawner equivalent")
    if spawner.get("maxSpawnAttempts", 10) != 10:
        raise ConversionError("non-default maxSpawnAttempts has no XmlSpawner equivalent")

    min_seconds = _time_span_seconds(spawner.get("minDelay", "00:05:00"), "minDelay")
    max_seconds = _time_span_seconds(spawner.get("maxDelay", "00:10:00"), "maxDelay")
    if min_seconds > max_seconds:
        raise ConversionError("minDelay cannot exceed maxDelay")
    delay_in_seconds = min_seconds % 60 != 0 or max_seconds % 60 != 0
    min_delay = min_seconds if delay_in_seconds else min_seconds // 60
    max_delay = max_seconds if delay_in_seconds else max_seconds // 60

    entries = spawner.get("entries")
    if not isinstance(entries, list):
        raise ConversionError("entries must be an array")
    objects = ":OBJ=".join(
        _entry_spec(entry, f"entries[{entry_index}]")
        for entry_index, entry in enumerate(entries)
    )

    region_name = ""
    if spawner_type == "RegionSpawner":
        if not allow_z_loss:
            raise ConversionError(
                "RegionSpawner Z-selection parity is unverified; rerun with --allow-z-loss to accept this"
            )
        region_name = spawner.get("region")
        if not isinstance(region_name, str) or not region_name:
            raise ConversionError("RegionSpawner requires a non-empty region")
        if "spawnBounds" in spawner:
            raise ConversionError("RegionSpawner cannot also define spawnBounds")
        x, y, width, height = location[0], location[1], 0, 0
        spawn_home_range = _require_int(spawner.get("homeRange", 4), "homeRange", 0)
    else:
        if "region" in spawner:
            raise ConversionError("Spawner cannot define region")
        if "spawnBounds" in spawner:
            if not allow_z_loss:
                raise ConversionError(
                    "XmlSpawner cannot preserve spawnBounds Z limits; rerun with --allow-z-loss to accept this"
                )
            x1, y1, _z1, x2, y2, _z2 = _bounds(spawner["spawnBounds"])
            min_x, max_x = sorted((x1, x2))
            min_y, max_y = sorted((y1, y2))
            if min_x == max_x or min_y == max_y:
                raise ConversionError("spawnBounds must contain at least one X/Y tile")
            x, y = min_x, min_y
            # ModernUO's End is exclusive; XmlSpawner's X+Width/Y+Height is inclusive.
            width, height = max_x - min_x - 1, max_y - min_y - 1
            spawn_home_range = min(
                abs(location[0] - x1), abs(x2 - location[0]),
                abs(location[1] - y1), abs(y2 - location[1]),
            )
        elif "homeRange" in spawner:
            legacy_home_range = _require_int(spawner["homeRange"], "homeRange", 0)
            x, y = location[0] - legacy_home_range, location[1] - legacy_home_range
            # ModernUO builds a 2r+1 half-open square; XmlSpawner uses inclusive ends.
            width = height = legacy_home_range * 2
            spawn_home_range = legacy_home_range
        else:
            # BaseSpawner.InitSpawn assigns HomeRange=4 when JSON has no bounds.
            x, y, width, height = location[0] - 4, location[1] - 4, 8, 8
            spawn_home_range = 4

    home_range = walking_range if walking_range > 0 else spawn_home_range

    row = ET.Element("Points")
    values = {
        "Name": spawner.get("name") or "Spawner", "UniqueId": guid_text,
        "Map": map_name, "X": x, "Y": y, "Width": width, "Height": height,
        "CentreX": location[0], "CentreY": location[1], "CentreZ": location[2],
        "Range": home_range, "MaxCount": count, "MinDelay": min_delay,
        "MaxDelay": max_delay, "DelayInSec": delay_in_seconds,
        "Duration": 0, "DespawnTime": 0, "ProximityRange": -1,
        "ProximityTriggerSound": 0x1F4, "ProximityTriggerMessage": "",
        "TriggerProbability": 1, "InContainer": False, "MinRefractory": 0,
        "MaxRefractory": 0, "TODStart": 0, "TODEnd": 0, "TODMode": 0,
        "KillReset": 1, "ExternalTriggering": False, "SequentialSpawning": -1,
        "RegionName": region_name, "AllowGhostTriggering": False,
        "AllowNPCTriggering": False, "SpawnOnTrigger": False, "SmartSpawning": False,
        "TickReset": False, "Team": team, "Amount": 1, "IsGroup": False,
        "IsRunning": True, "IsHomeRangeRelative": spawn_location_is_home,
        "Objects2": objects,
    }
    for key, value in values.items():
        _add(row, key, value)
    return row


def convert_document(
    data: Any, skip_unsupported: bool = False, allow_z_loss: bool = False
) -> tuple[ET.ElementTree, list[Issue]]:
    if not isinstance(data, list):
        raise ConversionError("top-level JSON value must be an array")
    root = ET.Element("Spawns")
    issues: list[Issue] = []
    for index, spawner in enumerate(data):
        guid = str(spawner.get("guid", "unknown")) if isinstance(spawner, dict) else "unknown"
        try:
            root.append(convert_one(spawner, index, allow_z_loss))
        except ConversionError as error:
            issues.append(Issue(index, guid, str(error)))
    if issues and not skip_unsupported:
        raise ConversionError("\n".join(str(issue) for issue in issues))
    ET.indent(root, space="  ")
    return ET.ElementTree(root), issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="ModernUO ExportSpawners JSON file")
    parser.add_argument("output", type=Path, help="ServUO XmlSpawner XML file")
    parser.add_argument(
        "--skip-unsupported", action="store_true",
        help="write supported rows and report skipped spawners (lossy; off by default)",
    )
    parser.add_argument(
        "--allow-z-loss", action="store_true",
        help="accept that XmlSpawner cannot preserve ModernUO bounds/region Z selection",
    )
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8-sig"))
        tree, issues = convert_document(data, args.skip_unsupported, args.allow_z_loss)
        if len(tree.getroot()) == 0:
            raise ConversionError("no supported spawners remain; output was not written")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        tree.write(args.output, encoding="utf-8", xml_declaration=True)
    except (OSError, json.JSONDecodeError, ConversionError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    for issue in issues:
        print(f"warning: skipped {issue}", file=sys.stderr)
    print(f"wrote {len(tree.getroot())} spawner(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
