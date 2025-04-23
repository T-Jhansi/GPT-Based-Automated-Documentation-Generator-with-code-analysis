import os
import time
from typing import Dict, Any
import openai
from openai.error import AuthenticationError, RateLimitError, OpenAIError

class DocumentGenerator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OpenAI API key. Set it as the OPENAI_API_KEY environment variable.")
        openai.api_key = api_key

    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        prompt = f"""Generate detailed technical documentation for the following code:

{code}

Analysis:
{analysis}
"""
        attempt = 0
        while attempt < 3:
            try:
                response = openai.Completion.create(
                    model="gpt-3.5-turbo",
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=1024
                )
                return response.choices[0].text.strip()

            except AuthenticationError:
                return "🛑 Invalid OpenAI API key. Please check your credentials."

            except RateLimitError:
                attempt += 1
                if attempt < 3:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    return "⚠️ OpenAI rate limit exceeded. Please try again later."

            except OpenAIError as e:
                return f"❌ OpenAI API error: {str(e)}"
