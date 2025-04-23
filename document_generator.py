# document_generator.py

import os
from typing import Dict, Any
import openai
from openai.error import AuthenticationError, RateLimitError, OpenAIError

class DocumentGenerator:
    def __init__(self):
        # Set API key from environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY as an environment variable.")
        openai.api_key = self.api_key

    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        prompt = f"Generate high-quality technical documentation for the following code:\n\n{code}\n\nCode analysis:\n{analysis}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            return response.choices[0].message.content.strip()

        except AuthenticationError:
            return "🛑 Authentication failed. Please verify your OpenAI API key."

        except RateLimitError:
            return "⏳ Rate limit hit. Try again later."

        except OpenAIError as e:
            return f"⚠️ OpenAI API error: {str(e)}"

        except Exception as e:
            return f"🚨 Unexpected error: {str(e)}"
