from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

working_directory = "./calculator"

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")


    result = None
    match function_name:
        case "get_files_info":
            result = get_files_info(working_directory=working_directory, **function_args)
        case "get_file_content":
            result = get_file_content(working_directory=working_directory, **function_args)
        case "run_python_file":
            result = run_python_file(working_directory=working_directory, **function_args)
        case "write_file":
            result = write_file(working_directory=working_directory, **function_args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )