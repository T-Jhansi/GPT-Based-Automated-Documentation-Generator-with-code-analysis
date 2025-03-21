import openai
import os
import logging
import streamlit as st
from typing import Dict, Any

# Set up logging
logger = logging.getLogger(__name__)

class DocumentGenerator:
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        
        # 🔹 Load API Key: Paste it here OR set it as an environment variable
        self.api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY", "paste here")
        
        if self.api_key == "paste here":
            raise ValueError("❌ API Key is missing! Please replace 'paste here' with your OpenAI API Key OR set it in environment variables.")

    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        """
        Generate comprehensive documentation using OpenAI's GPT model.

        Args:
            code (str): Source code
            analysis (Dict): Code analysis results

        Returns:
            str: AI-generated documentation
        """
        try:
            openai.api_key = self.api_key  # 🔹 API Key used here
            prompt = self._create_prompt(code, analysis)

            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )

            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}")
            return "❌ Error generating documentation. Please try again."

    def _create_prompt(self, code: str, analysis: Dict[str, Any]) -> str:
        """Creates a structured prompt for AI documentation."""
        return f"""
        Generate comprehensive documentation for the following Python code.
        Include:
        - Overview
        - Functions: {', '.join(analysis.get('functions', []))}
        - Classes: {', '.join(analysis.get('classes', []))}
        - Dependencies: {', '.join(analysis.get('relationships', {}).get('imports', []))}

        Code:
        {code}

        Please provide detailed documentation with examples and usage patterns.
        """
