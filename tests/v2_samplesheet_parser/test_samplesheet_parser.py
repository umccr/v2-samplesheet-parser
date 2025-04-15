import json
import re
from pathlib import Path

from unittest import TestCase
from v2_samplesheet_parser.functions.parser import parse_samplesheet
from v2_samplesheet_parser.functions.reverter import revert_samplesheet_to_csv
class TestSampleSheetParser(TestCase):
    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def tearDown(self):
        super().tearDown()

    def test_parse_standard_sheet_with_settings(self):
        """
        python manage.py test tests.v2_samplesheet_parser.test_samplesheet_parser.TestSampleSheetParser.test_parse_standard_sheet_with_settings
        """
        
        # read files from ./examples/standard-sheet-with-settings.csv
        with open(Path(__file__).parent / "examples/standard-sheet-with-settings.csv", "r") as f:
            samplesheet = f.read()
        result = parse_samplesheet(samplesheet)
        # read expected result from ./examples/standard-sheet-with-settings.json
        with open(Path(__file__).parent / "examples/standard-sheet-with-settings.json", "r") as f:
            expected_result = json.load(f)
        self.compare_dicts(result, expected_result)
        self.assertEqual(result, expected_result)

    def test_parse_tso500_cloud_settings(self):
        """
        python manage.py test tests.v2_samplesheet_parser.test_samplesheet_parser.TestSampleSheetParser.test_parse_tso500_cloud_settings
        """
        # read files from ./examples/tso500-cloud-settings.csv
        with open(Path(__file__).parent / "examples/tso500-cloud-settings.csv", "r") as f:
            samplesheet = f.read()
        result = parse_samplesheet(samplesheet)
        # read expected result from ./examples/tso500-cloud-settings.json
        with open(Path(__file__).parent / "examples/tso500-cloud-settings.json", "r") as f:
            expected_result = json.load(f)
        self.compare_dicts(result, expected_result)
        self.assertEqual(result, expected_result)
    
    def test_parse_original_samplesheet(self):
        """
        python manage.py test tests.v2_samplesheet_parser.test_samplesheet_parser.TestSampleSheetParser.test_parse_original_samplesheet
        """
        # read files from ./examples/original-sheet-from-excel.csv
        with open(Path(__file__).parent / "examples/original-sheet-from-excel.csv", "r") as f:
            samplesheet = f.read()
        result = parse_samplesheet(samplesheet)
        # read expected result from ./examples/original-sheet-from-excel.json
        with open(Path(__file__).parent / "examples/original-sheet-from-excel.json", "r") as f:
            expected_result = json.load(f)
        self.compare_dicts(result, expected_result)
        self.assertEqual(result, expected_result)

    def compare_dicts(self, actual: dict, expected: dict, path: str = ""):
        """Compare dictionaries and print differences"""
        for key in set(actual.keys()) | set(expected.keys()):
            current_path = f"{path}.{key}" if path else key
            if key not in actual:
                print(f"Missing key in actual: {current_path}")
            elif key not in expected:
                print(f"Extra key in actual: {current_path}")
            elif actual[key] != expected[key]:
                print(f"Value mismatch at {current_path}:")
                print(f"  Actual: {actual[key]}")
                print(f"  Expected: {expected[key]}")
    
    def compare_csv_sections(self, actual: str, expected: str):
        """
        Compare CSV sections ignoring line order within each section.
        
        Args:
            actual: The actual CSV string
            expected: The expected CSV string
            
        Returns:
            bool: True if the sections match, False otherwise
        """
        # Split both strings into sections
        actual_sections = self._split_into_sections(actual)
        expected_sections = self._split_into_sections(expected)
        
        # Extract section headers
        actual_headers = [section.split('\n')[0] for section in actual_sections]
        expected_headers = [section.split('\n')[0] for section in expected_sections]
        
        # Find common sections
        common_headers = set(actual_headers) & set(expected_headers)
        
        # Check if we have any common sections
        if not common_headers:
            print("No common sections found between actual and expected results")
            return False
        
        # Compare each common section
        for header in common_headers:
            # Find the section in both actual and expected
            actual_section = next(section for section in actual_sections if section.startswith(header))
            expected_section = next(section for section in expected_sections if section.startswith(header))
            
            # Compare section content ignoring line order
            actual_content = set(actual_section.split('\n')[1:])
            expected_content = set(expected_section.split('\n')[1:])
            
            # Remove empty lines
            actual_content = {line for line in actual_content if line.strip()}
            expected_content = {line for line in expected_content if line.strip()}
            
            if actual_content != expected_content:
                print(f"Content mismatch in section {header}:")
                print(f"  Missing in actual: {expected_content - actual_content}")
                print(f"  Extra in actual: {actual_content - expected_content}")
                return False
        
        # Print information about sections that are only in one of the results
        only_in_actual = set(actual_headers) - set(expected_headers)
        only_in_expected = set(expected_headers) - set(actual_headers)
        
        if only_in_actual:
            print(f"Sections only in actual result: {only_in_actual}")
        
        if only_in_expected:
            print(f"Sections only in expected result: {only_in_expected}")
        
        # Return True if all common sections match
        return True
    
    def _split_into_sections(self, csv_string: str) -> list:
        """
        Split a CSV string into sections based on section headers.
        
        Args:
            csv_string: The CSV string to split
            
        Returns:
            list: A list of sections, each as a string
        """
        # Use regex to find section headers
        section_pattern = r'\[(.*?)\]\n(.*?)(?=\n\[|$)'
        sections = re.findall(section_pattern, csv_string, re.DOTALL)
        
        # Format sections as [Header]\nContent
        return [f"[{header}]\n{content}" for header, content in sections]
                
    def test_revert_standard_sheet_with_settings_to_csv(self):
        """
        python manage.py test tests.v2_samplesheet_parser.test_samplesheet_parser.TestSampleSheetParser.test_revert_standard_sheet_with_settings_to_csv
        """
        # read files from ./examples/standard-sheet-with-settings.json
        with open(Path(__file__).parent / "examples/standard-sheet-with-settings.json", "r") as f:
            samplesheet = json.load(f)
        result = revert_samplesheet_to_csv(samplesheet)
        # read expected result from ./examples/standard-sheet-with-settings.csv
        with open(Path(__file__).parent / "examples/standard-sheet-with-settings.csv", "r") as f:
            expected_result = f.read()
        
        # Compare sections ignoring line order
        self.assertTrue(self.compare_csv_sections(result, expected_result), 
                       "CSV sections do not match (ignoring line order)")
        
    def test_revert_tso500_cloud_settings_to_csv(self):
        """
        python manage.py test tests.v2_samplesheet_parser.test_samplesheet_parser.TestSampleSheetParser.test_revert_tso500_cloud_settings_to_csv
        """
        # read files from ./examples/tso500-cloud-settings.json
        with open(Path(__file__).parent / "examples/tso500-cloud-settings.json", "r") as f:
            samplesheet = json.load(f)
        result = revert_samplesheet_to_csv(samplesheet)
        # read expected result from ./examples/tso500-cloud-settings.csv
        with open(Path(__file__).parent / "examples/tso500-cloud-settings.csv", "r") as f:
            expected_result = f.read()
        
        # Compare sections ignoring line order
        self.assertTrue(self.compare_csv_sections(result, expected_result), 
                       "CSV sections do not match (ignoring line order)")
        