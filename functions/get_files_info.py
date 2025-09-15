import os

from os import listdir
from os.path import isfile, isdir, join

from config import MAX_CHARS

def build_response_string(directory_object):
    if isfile(directory_object) or isdir(directory_object):
        return f"{directory_object.split("/")[-1]}: file_size={os.path.getsize(directory_object)} bytes, is_dir={not isfile(directory_object)}"
    else:
        print("Unknown object type")
        raise Exception("Unknown object type")


def get_files_info(working_directory, directory="."):

    try:
        absolute_path = os.path.abspath(os.path.join(working_directory, directory))
        if not os.path.isdir(absolute_path):
            return f'Error: "{absolute_path}" is not a directory'

        if not absolute_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        contents = list(map(lambda x: f"{absolute_path}/{x}", listdir(absolute_path)))
        return "\n".join(list(map(build_response_string, contents)))
    
    except Exception as e:
        print(e)
        return "Error: An unexpected error has occured"
    

def get_file_content(working_directory, file_path):

    try:
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not absolute_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not isfile(absolute_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(absolute_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if len(file_content_string) == MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content_string

    except Exception as e:
        print(e)
        return "Error: An unexpected error has occured"