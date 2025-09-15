import unittest

from functions.get_files_info import get_files_info

class TestGetFileInfo(unittest.TestCase):

    def test_get_current_dir(self):
        result = get_files_info("calculator", ".")
        self.assertTrue("main.py: file_size=" in result)
        self.assertTrue("tests.py: file_size=" in result)
        self.assertTrue("pkg: file_size=" in result)

        print(result)

    def test_get_pkg(self):
        result = get_files_info("calculator", "pkg")
        self.assertTrue("calculator.py: file_size=" in result)
        self.assertTrue("render.py: file_size" in result)

        print(result)

    def test_get_bin(self):
        result = get_files_info("calculator", "/bin")
        self.assertEqual(result, "Error: Cannot list \"/bin\" as it is outside the permitted working directory")

        print(result)
    
    def test_get_outside_working_dir(self):
        result = get_files_info("calculator", "../")
        self.assertEqual(result, "Error: Cannot list \"../\" as it is outside the permitted working directory")

        print(result)

if __name__ == "__main__":
    unittest.main()