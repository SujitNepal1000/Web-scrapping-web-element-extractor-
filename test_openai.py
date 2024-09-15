import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def test_openai_api():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, world!"}
            ],
            max_tokens=5
        )
        print("API Key is working. Response:")
        print(response['choices'][0]['message']['content'].strip())
    except openai.error.RateLimitError:
        print("Error: Rate limit exceeded.")
    except openai.error.InvalidRequestError:
        print("Error: Invalid request.")
    except openai.error.AuthenticationError:
        print("Error: Authentication failed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_openai_api()
