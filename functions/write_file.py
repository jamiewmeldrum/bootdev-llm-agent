import os

def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not absolute_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(absolute_path):
            os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
            
        with open(absolute_path, "w") as f:
            f.write(content)
    
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        print(e)
        return "Error: An unexpected error has occured"