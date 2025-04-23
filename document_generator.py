import os
import time
from typing import Dict, Any
import openai
from openai._exceptions import AuthenticationError, RateLimitError, OpenAIError

class DocumentGenerator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OpenAI API key. Set it as the OPENAI_API_KEY environment variable.")
        openai.api_key = api_key

    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        prompt = f"Generate detailed technical documentation for the following code:\n\n{code}\n\nAnalysis:\n{analysis}"

        attempt = 0
        while attempt < 3:  # Retry up to 3 times
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1024
                )
                return response.choices[0].message.content.strip()

            except AuthenticationError:
                return "🛑 Invalid OpenAI API key. Please check your credentials."

            except RateLimitError:
                attempt += 1
                if attempt < 3:
                    wait_time = 2 ** attempt  # Exponential backoff (2, 4, 8 seconds)
                    time.sleep(wait_time)  # Sleep before retrying
                else:
                    return "⚠️ Rate limit exceeded multiple times. Please try again later."

            except OpenAIError as e:
                return f"🔧 OpenAI error: {str(e)}"

            except Exception as e:
                return f"❌ Unexpected error: {str(e)}"
