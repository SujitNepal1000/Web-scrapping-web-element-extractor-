import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Template for the prompt
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Function to call the OpenAI API
def call_openai_api(prompt_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are an assistant for extracting specific information."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=500,
            n=1,
            temperature=0.5,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return ""

# Function to parse DOM chunks using OpenAI API
def parse_with_openai(dom_chunks, parse_description):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        # Generate the prompt using the template
        prompt_text = template.format(dom_content=chunk, parse_description=parse_description)
        
        # Call OpenAI API to get the extracted information
        response = call_openai_api(prompt_text)

        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
