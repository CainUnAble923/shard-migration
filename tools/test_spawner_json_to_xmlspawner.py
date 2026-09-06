import importlib.util
import io
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("spawner_json_to_xmlspawner.py")
SPEC = importlib.util.spec_from_file_location("spawner_converter", MODULE_PATH)
converter = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = converter
SPEC.loader.exec_module(converter)


def sample(**overrides):
    value = {
        "type": "Spawner",
        "guid": "11111111-2222-3333-4444-555555555555",
        "location": [100, 200, -5],
        "map": "Trammel",
        "count": 3,
        "walkingRange": 8,
        "entries": [
            {"name": "Rat", "probability": 100, "maxCount": 2},
            {"name": "SewerRat", "probability": 100, "maxCount": 1},
        ],
    }
    value.update(overrides)
    return value


class ConverterTests(unittest.TestCase):
    def test_basic_spawner_preserves_counts_and_defaults(self):
        tree, issues = converter.convert_document([sample()])
        self.assertEqual([], issues)
        row = tree.getroot().find("Points")
        self.assertEqual("3", row.findtext("MaxCount"))
        self.assertEqual("8", row.findtext("Range"))
        self.assertEqual("5", row.findtext("MinDelay"))
        self.assertEqual("False", row.findtext("DelayInSec"))
        self.assertEqual(
            "Rat:MX=2" + converter.OBJECT_SUFFIX + ":OBJ=SewerRat:MX=1" + converter.OBJECT_SUFFIX,
            row.findtext("Objects2"),
        )

    def test_bounds_compensate_for_inclusive_servuo_end(self):
        bounds = {"start": {"x": 10, "y": 20, "z": -30},
                  "end": {"x": 15, "y": 27, "z": 40}}
        tree, _ = converter.convert_document([sample(spawnBounds=bounds)], allow_z_loss=True)
        row = tree.getroot().find("Points")
        self.assertEqual(("10", "20", "4", "6"), tuple(
            row.findtext(name) for name in ("X", "Y", "Width", "Height")
        ))

    def test_seconds_are_selected_when_either_delay_is_not_whole_minutes(self):
        tree, _ = converter.convert_document([
            sample(minDelay="00:00:30", maxDelay="00:02:00")
        ])
        row = tree.getroot().find("Points")
        self.assertEqual("True", row.findtext("DelayInSec"))
        self.assertEqual("30", row.findtext("MinDelay"))
        self.assertEqual("120", row.findtext("MaxDelay"))

    def test_legacy_home_range_becomes_inclusive_xmlspawner_square(self):
        tree, _ = converter.convert_document([sample(homeRange=5, walkingRange=-1)])
        row = tree.getroot().find("Points")
        self.assertEqual(("95", "195", "10", "10"), tuple(
            row.findtext(name) for name in ("X", "Y", "Width", "Height")
        ))
        self.assertEqual("5", row.findtext("Range"))

    def test_spawn_location_as_home_maps_to_relative_home(self):
        tree, _ = converter.convert_document([sample(spawnLocationIsHome=True)])
        self.assertEqual("True", tree.findtext("./Points/IsHomeRangeRelative"))

    def test_region_spawner_uses_region_name(self):
        tree, _ = converter.convert_document(
            [sample(type="RegionSpawner", region="Britain", map="Felucca")],
            allow_z_loss=True,
        )
        row = tree.getroot().find("Points")
        self.assertEqual("Britain", row.findtext("RegionName"))
        self.assertEqual("0", row.findtext("Width"))

    def test_non_default_probability_fails_closed(self):
        value = sample(entries=[{"name": "Rat", "probability": 50, "maxCount": 1}])
        with self.assertRaisesRegex(converter.ConversionError, "no per-entry XmlSpawner equivalent"):
            converter.convert_document([value])

    def test_z_loss_requires_explicit_opt_in(self):
        with self.assertRaisesRegex(converter.ConversionError, "cannot preserve spawnBounds Z"):
            converter.convert_document([
                sample(spawnBounds={"x1": 10, "y1": 20, "x2": 15, "y2": 25})
            ])

    def test_skip_unsupported_reports_and_keeps_supported_rows(self):
        invalid = sample(type="ProximitySpawner", guid="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
        tree, issues = converter.convert_document([invalid, sample()], skip_unsupported=True)
        self.assertEqual(1, len(tree.getroot()))
        self.assertEqual(1, len(issues))

    def test_generated_xml_round_trips(self):
        tree, _ = converter.convert_document([sample(name="A & B")])
        output = io.BytesIO()
        tree.write(output, encoding="utf-8", xml_declaration=True)
        parsed = ET.fromstring(output.getvalue())
        self.assertEqual("A & B", parsed.findtext("./Points/Name"))


if __name__ == "__main__":
    unittest.main()
