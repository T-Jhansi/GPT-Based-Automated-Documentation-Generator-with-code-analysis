# document_generator.py

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
        prompt = f"Generate detailed technical documentation for the following code:\n\n{code}\n\nAnalysis:\n{analysis}"

        attempt = 0
        while attempt < 3:  # Retry up to 3 times
            try:
                # Using the new method for generating completions in SDK v1.x
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
                    wait_time = 2 ** attempt  # Exponential backoff (2, 4, 8 seconds)
                    time.sleep(wait_time)  # Sleep before retrying
                else:
                    return "Let's gooo! 🔥 Below is a clean, professional **API-style documentation** for the Python script you just shared. This doc is structured in a way that aligns with **RESTful or SDK-level API docs**, useful for dev teams, open source contributors, or even CI engineers reviewing your automation flow.

---

# 📄 API Documentation – `test_full_workflow.py`

## 🧠 Overview
This script is a **workflow test utility** designed to validate the end-to-end functionality of a GPT-based documentation generation pipeline. It simulates the process from code ingestion to documentation output and verifies key checkpoints in the process.

---

## 📁 Module: `test_full_workflow`

### ➕ Dependencies
```python
import os
import time
from my_docgen_project.workflow import run_pipeline
```

---

## 🔧 Configuration

### 🔗 Constants

| Name            | Description                               | Type   | Default Value           |
|-----------------|-------------------------------------------|--------|--------------------------|
| `TEST_CODE_DIR` | Directory containing test source code     | `str`  | `"test_samples/"`        |
| `TEST_FILE`     | Filename of the test input code           | `str`  | `"calculator.py"`        |
| `CHECKPOINTS`   | List of expected process logs             | `list` | See below                |

```python
CHECKPOINTS = [
    "Code successfully loaded",
    "Analysis complete",
    "GPT response received",
    "Documentation generated",
    "Output written to"
]
```

---

## 🔁 Function: `test_full_workflow()`

### ✅ Purpose
Runs the full test pipeline for the documentation generator, verifying:
- File reading
- Code analysis
- GPT processing
- Output file generation
- Log checkpointing

### 📥 Parameters
_None_

### 📤 Returns
_None_  
Raises exceptions on failure.

### 🔍 Workflow

| Step                      | Description                                                              |
|---------------------------|--------------------------------------------------------------------------|
| 1. **Load Code File**     | Reads the test file from the configured directory.                      |
| 2. **Run Pipeline**       | Invokes the `run_pipeline` function with the code as input.             |
| 3. **Check Logs**         | Asserts that all expected checkpoints are present in the returned logs. |
| 4. **Validate Output**    | Confirms that the documentation output file was successfully created.    |

### 💣 Exceptions

| Exception Type | Raised When                                           |
|----------------|--------------------------------------------------------|
| `RuntimeError` | - Test file can't be read<br>- Pipeline crashes<br>- Output file missing<br>- Log checkpoint missing |

---

## 🚀 Entry Point

```python
if __name__ == "__main__":
    test_full_workflow()
```

Runs the test when the script is executed directly.

---

## 📝 Example Usage
```bash
$ python test_full_workflow.py
```

---

## 🧠 Notes
- Assumes the function `run_pipeline(code: str)` exists in the `my_docgen_project.workflow` module.
- The test code file (`calculator.py`) must exist in the specified `test_samples/` directory.

---

Would
