import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
    valid_target_file = os.path.commonpath([abs_working_directory, target_file_path]) == abs_working_directory
    if not valid_target_file:
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.isfile(target_file_path):
         return f"Error: \"{file_path}\" does not exist or is not a regular file"
    if not target_file_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file"
    
    else:

        command = ["python", target_file_path]
        if args:
            command.extend(args)
        
        try:
            subprocess_output = subprocess.run(command, capture_output=True, text=True, timeout=30)
            if subprocess_output.returncode != 0:
                return f"Process exited with code {subprocess_output.returncode}"
            else:
                if subprocess_output.stdout or subprocess_output.stderr:
                    return f"STDOUT:{subprocess_output.stdout}\nSTDERR:{subprocess_output.stderr}"
                else:
                    return "No output produced."
        except Exception as e:
            return f"Error: executing Python file: {e}"
        

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified file path relative to the working directory, with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute, relative to the working directory (default is the working directory itself. Also, Current directory should be represented as '.')",
            ), "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python file during execution",
                items=types.Schema(type=types.Type.STRING),
            ), 
        },
     ),
)