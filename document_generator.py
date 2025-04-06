import openai
import os
import logging
import streamlit as st
from typing import Dict, Any
from openai import AuthenticationError, RateLimitError, OpenAIError


# Set up logging
logger = logging.getLogger(__name__)

class DocumentGenerator:
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("❌ API Key is missing! Set 'OPENAI_API_KEY' in Streamlit secrets or environment variables.")

    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        """Generate comprehensive documentation using OpenAI's GPT model."""
        try:
            openai.api_key = self.api_key
            prompt = self._create_prompt(code, analysis)

            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )

            return response["choices"][0]["message"]["content"]

        except openai.error.AuthenticationError:
            return "❌ Invalid API key! Check your OpenAI API key."
        except openai.error.RateLimitError:
            return "❌ Rate limit exceeded! Try again later."
        except openai.error.OpenAIError as e:
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
