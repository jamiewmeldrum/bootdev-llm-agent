import os

from os import listdir
from os.path import isfile, isdir

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