import functions.get_file_content
import functions.get_files_info
import functions.write_files
import functions.run_python_file
from google.genai import types



function_map = {
    "get_files_info": functions.get_files_info.get_files_info,
    "get_file_content": functions.get_file_content.get_file_content,
    "write_file": functions.write_files.write_file,
    "run_python_file": functions.run_python_file.run_python_file,
}


def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Calling function: {function_call.name}")

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)
    else:
        args = dict(function_call.args) if function_call.args else {}
        args["working_directory"] = "./calculator" #Test purpose only, should be passed from main
        function_result = function_map[function_name](**args)
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)


