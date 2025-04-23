import time
from typing import Dict, Any
from openai.error import AuthenticationError


class DocumentGenerator:
    # ... (other methods remain unchanged)

    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        """Generate comprehensive documentation using OpenAI's GPT model."""
        max_retries = 5
        retry_delay = 1  # Start with a 1 second delay

        for attempt in range(max_retries):
            try:
                prompt = self._create_prompt(code, analysis)

                response = openai.ChatCompletion.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a professional Python documentation writer."},
                        {"role": "user", "content": prompt}
                    ]
                )

                if response.choices:
                    return response.choices[0].message.content.strip()
                else:
                    return "❌ No response from OpenAI API."

            except AuthenticationError:
                return "❌ Invalid API key! Check your OpenAI API key."
            except RateLimitError:
                if attempt < max_retries - 1:  # Don't wait on the last attempt
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    return "❌ Rate limit exceeded! Please try again later."
            except OpenAIError as e:
                logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
                return f"❌ OpenAI API error: {str(e)}"
            except Exception as e:
                logger.error(f"Unexpected error: {type(e).__name__} - {str(e)}", exc_info=True)
                return "❌ Error generating documentation. Please try again."
