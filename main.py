import os
from urllib import response
from dotenv import load_dotenv
import argparse
from google.genai import types
import call_function
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_files import schema_write_file
from functions.run_python_file import schema_run_python_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("AI Key for GEMINI not found")

from google import genai

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="AI Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
)


    

def main():
    for _ in range(20):  # Limit to 20 iterations to prevent infinite loops

        # Generate content with function calling
        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt, 
        temperature=0)
        )

        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls is not None:
            function_call_list = []
            for function_call in response.function_calls:
                function_call_result = call_function.call_function(function_call, args)
                if function_call_result.parts[0].function_response.response is not None:
                    function_call_list.append(function_call_result.parts[0])
                    print(f"Function call result:\n{function_call_result.parts[0].function_response.response['result']}")                            
                else:
                    print("Function call resulted in no response.") 
                    break
                messages.append(types.Content(role="user", parts=function_call_list))         
        else:
            if response.usage_metadata is not None:             
                if args.verbose:
                    print(f"User prompt: {args.user_prompt}")
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print(f"Response:\n{response.text}")
                break
            else:
                raise RuntimeError("No usage metadata found in response")
            
        


if __name__ == "__main__":
    main()
