import csv
import json
from pathlib import Path
import unittest
from demo.report import baseline


class ReportTests(unittest.TestCase):
    def test_committed_evidence_matches_reproduced_domain_results(self):
        folder = Path(__file__).resolve().parents[1] / "reports" / "baseline"
        expected = baseline()
        self.assertEqual(json.loads((folder / "snapshot.json").read_text(encoding="utf-8")), expected)
        with (folder / "records.csv").open(newline="", encoding="utf-8") as source:
            exported = list(csv.DictReader(source))
        self.assertEqual(len(exported), len(expected["records"]))
        self.assertEqual([row["id"] for row in exported], [row["id"] for row in expected["records"]])
        self.assertTrue(all(r["version"] == 1 for r in expected["records"]))
