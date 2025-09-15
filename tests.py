import unittest

from functions.get_files_info import get_files_info, get_file_content

class TestGetFileInfo(unittest.TestCase):

    def test_get_current_dir(self):
        result = get_files_info("calculator", ".")
        self.assertTrue("main.py: file_size=" in result)
        self.assertTrue("tests.py: file_size=" in result)
        self.assertTrue("pkg: file_size=" in result)

    def test_get_pkg(self):
        result = get_files_info("calculator", "pkg")
        self.assertTrue("calculator.py: file_size=" in result)
        self.assertTrue("render.py: file_size" in result)

    def test_get_bin(self):
        result = get_files_info("calculator", "/bin")
        self.assertEqual(result, "Error: Cannot list \"/bin\" as it is outside the permitted working directory")
    
    def test_get_outside_working_dir(self):
        result = get_files_info("calculator", "../")
        self.assertEqual(result, "Error: Cannot list \"../\" as it is outside the permitted working directory")

    def test_get_get_file_calculator_main(self):
        result = get_file_content("calculator", "main.py")
        print(result)
        self.assertTrue("def main():" in result)

    def test_get_get_file_calculator_pkg_calculator(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)
        self.assertTrue(result.startswith("class Calculator:"))

    def test_get_get_file_calculator_bin_cat(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)
        self.assertEqual(result, "Error: Cannot read \"/bin/cat\" as it is outside the permitted working directory")

    def test_get_get_file_calculator_does_not_exist(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        print(result)
        self.assertEqual(result, "Error: File not found or is not a regular file: \"pkg/does_not_exist.py\"")

if __name__ == "__main__":
    unittest.main()