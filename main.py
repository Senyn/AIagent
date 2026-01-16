import os
from urllib import response
from dotenv import load_dotenv
import argparse
from google.genai import types

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

response = client.models.generate_content(model='gemini-2.5-flash',
    contents=messages)



def main():
    if response.usage_metadata is not None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Response:\n{response.text}")
    else:
        raise RuntimeError("No usage metadata found in response")


if __name__ == "__main__":
    main()
