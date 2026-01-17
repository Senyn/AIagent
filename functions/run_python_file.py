import os
import subprocess


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