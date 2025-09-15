import unittest
import os

from os.path import isfile

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

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


    def test_overwrite_file(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertEqual(result, "Successfully wrote to \"lorem.txt\" (28 characters written)")
        self.assertEqual(get_file_content("calculator", "lorem.txt"), "wait, this isn't lorem ipsum")


    def test_write_new_file(self):

        path = "pkg/morelorem.txt"
        absolute_path = os.path.abspath(os.path.join("calculator", path))
        if isfile(absolute_path):
            os.remove(absolute_path)

        result = write_file("calculator", path, "lorem ipsum dolor sit amet")
        print(result)
        self.assertEqual(result, f"Successfully wrote to \"{path}\" (26 characters written)")
        self.assertEqual(get_file_content("calculator", path), "lorem ipsum dolor sit amet")

        if isfile(absolute_path):
            os.remove(absolute_path)


    def test_write_new_file_and_directory(self):

        path = "pkg/temp/morelorem.txt"
        absolute_path = os.path.abspath(os.path.join("calculator", path))
        if isfile(absolute_path):
            os.remove(absolute_path)
            os.removedirs(os.path.dirname(absolute_path))

        result = write_file("calculator", path, "lorem ipsum dolor sit amet")
        print(result)
        self.assertEqual(result, f"Successfully wrote to \"{path}\" (26 characters written)")
        self.assertEqual(get_file_content("calculator", path), "lorem ipsum dolor sit amet")

        if isfile(absolute_path):
            os.remove(absolute_path)
            os.removedirs(os.path.dirname(absolute_path))


    def test_write_file_not_allowed(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)
        self.assertEqual(result, f'Error: Cannot read "/tmp/temp.txt" as it is outside the permitted working directory')
        

if __name__ == "__main__":
    unittest.main()