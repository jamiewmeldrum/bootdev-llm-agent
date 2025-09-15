import os
import subprocess
from subprocess import TimeoutExpired

from os.path import isfile

def run_python_file(working_directory, file_path, args=[]):

    abs_working_dir = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not isfile(absolute_path):
        return f'Error: File "{file_path}" not found.'
    
    if not absolute_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            args=["python", absolute_path] + args, 
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    
    except TimeoutExpired as t:
        return f"Error: timeout executing Python file: {t}"
    except Exception as e:
        return f"Error: executing Python file: {e}"