import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_URL = "https://api.gemini.ai/v1/inference"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def call_gemini_api(prompt_text):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt_text,
        # You can adjust parameters as required by the API.
        # You may need to provide additional parameters depending on Gemini's API specs.
    }

    response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""

def parse_with_gemini(dom_chunks, parse_description):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        prompt_text = template.format(dom_content=chunk, parse_description=parse_description)

        response = call_gemini_api(prompt_text)

        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)

# Usage:
dom_chunks = ["This is a sample text.", "Another piece of text."]
parse_description = "Extract the main topic of each text."
parsed_results = parse_with_gemini(dom_chunks, parse_description)
print(parsed_results)