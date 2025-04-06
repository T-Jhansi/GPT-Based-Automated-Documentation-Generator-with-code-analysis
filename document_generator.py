import os
import logging
import streamlit as st
import openai
from typing import Dict, Any
from openai import OpenAI
from openai._exceptions import OpenAIError, AuthenticationError, RateLimitError

# Set up logging
logger = logging.getLogger(__name__)

class DocumentGenerator:
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("❌ API Key is missing! Set 'OPENAI_API_KEY' in Streamlit secrets or environment variables.")

        # ✅ Initialize OpenAI client instance (required in v1+)
        self.client = OpenAI(api_key=self.api_key)

    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        """Generate comprehensive documentation using OpenAI's GPT model."""
        try:
            prompt = self._create_prompt(code, analysis)

            # ✅ Use the new API pattern (v1.0+)
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.choices[0].message.content

        except AuthenticationError:
            return "❌ Invalid API key! Check your OpenAI API key."
        except RateLimitError:
            return "❌ Rate limit exceeded! Try again later."
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
            return f"❌ OpenAI API error: {str(e)}"
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}", exc_info=True)
            return "❌ Error generating documentation. Please try again."

    def _create_prompt(self, code: str, analysis: Dict[str, Any]) -> str:
        """Creates a structured prompt for AI documentation."""
        functions = ', '.join(analysis.get('functions', []) or ["None"])
        classes = ', '.join(analysis.get('classes', []) or ["None"])
        dependencies = ', '.join(analysis.get('relationships', {}).get('imports', []) or ["None"])

        return f"""
        Generate comprehensive documentation for the following Python code.
        
        Overview:
        - Functions: {functions}
        - Classes: {classes}
        - Dependencies: {dependencies}
        
        Code:
        {code}

        Provide structured documentation with examples.
        """
