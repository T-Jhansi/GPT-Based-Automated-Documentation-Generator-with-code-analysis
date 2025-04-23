# document_generator.py

import os
from typing import Dict, Any
import openai
from openai._exceptions import AuthenticationError, RateLimitError, OpenAIError  # updated import path

class DocumentGenerator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OpenAI API key. Set it as the OPENAI_API_KEY environment variable.")
        openai.api_key = api_key

    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        prompt = f"Generate technical documentation for the following Python code:\n\n{code}\n\nAnalysis:\n{analysis}"

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
            return "⚠️ Rate limit hit. Try again in a few minutes."

        except OpenAIError as e:
            return f"🔧 OpenAI error: {str(e)}"

        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
