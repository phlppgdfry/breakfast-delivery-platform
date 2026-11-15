import csv
import io
import unittest
from demo.server import csv_cell


class CsvExportTests(unittest.TestCase):
    def test_negative_measurements_keep_their_numeric_representation(self):
        stream = io.StringIO(newline="")
        writer = csv.writer(stream)
        writer.writerow([csv_cell(-12.5), csv_cell(0), csv_cell(23.1)])
        self.assertEqual(
            next(csv.reader(io.StringIO(stream.getvalue()))), ["-12.5", "0", "23.1"]
        )

    def test_untrusted_formula_text_stays_inert(self):
        for value in ["=1+1", "+SUM(1,2)", "-1+2", "@SUM(A1:A2)", "\t=1", "\r=1"]:
            with self.subTest(value=value):
                self.assertEqual(csv_cell(value), "'" + value)
        self.assertEqual(csv_cell("Fictional customer note"), "Fictional customer note")
