import csv
import unittest
from pathlib import Path


DATASET = Path(__file__).resolve().parents[1] / "Data" / "Salaries.csv"
REQUIRED_COLUMNS = {
    "Year",
    "Experience_Level",
    "Employment_Type",
    "Company_Size",
    "Salary_In_Usd",
    "Job_Title",
    "Remote_Ratio",
    "Employee_Residence_Iso3",
}


class SalaryDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DATASET.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source)
            cls.fieldnames = set(reader.fieldnames or [])
            cls.rows = list(reader)

    def test_dataset_is_not_empty(self):
        self.assertGreater(len(self.rows), 0)

    def test_required_columns_are_present(self):
        self.assertTrue(REQUIRED_COLUMNS.issubset(self.fieldnames))

    def test_salary_values_are_positive_numbers(self):
        sample = self.rows[:100]
        self.assertTrue(sample)
        self.assertTrue(all(float(row["Salary_In_Usd"]) > 0 for row in sample))

    def test_remote_ratio_values_use_supported_labels(self):
        values = {row["Remote_Ratio"] for row in self.rows}
        self.assertTrue(values.issubset({"On-site", "Hybrid", "Remote"}))


if __name__ == "__main__":
    unittest.main()
