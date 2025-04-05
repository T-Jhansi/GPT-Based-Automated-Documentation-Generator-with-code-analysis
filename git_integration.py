import os
import logging
from git import Repo, InvalidGitRepositoryError, NoSuchPathError, GitCommandError

# 🔧 Set up logging (optional: configure this more globally if needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 📦 Custom exception for Git integration failures
class GitIntegrationError(Exception):
    """Custom exception for errors during Git repository initialization."""
    pass

# 🚀 Main class to manage Git operations
class GitManager:
    def __init__(self, repo_path="."):
        """
        Initialize GitManager.

        Parameters:
        repo_path (str): Path to the Git repository (default: current directory).
        """
        self.repo_path = repo_path
        self.repo = self._initialize_repository()

    def _initialize_repository(self):
        """
        Attempt to load an existing Git repository from the given path.

        Returns:
        Repo: A GitPython Repo object if successful.

        Raises:
        GitIntegrationError: If the repository cannot be initialized.
        """
        try:
            # 📍 Debug info (useful in cloud environments like Streamlit)
            print(f"Initializing Git repository at: {self.repo_path}")
            print("Directory contents:", os.listdir(self.repo_path))

            # Attempt to initialize the repo
            repo = Repo(self.repo_path)
            print("✅ Git repository initialized successfully.")
            return repo

        except (InvalidGitRepositoryError, NoSuchPathError, GitCommandError, Exception) as e:
            # 🔍 Log detailed traceback to help with debugging
            logging.error(f"Git initialization failed: {e}", exc_info=True)

            # 🛑 Raise a clean error message for the front-end
            raise GitIntegrationError(f"Failed to initialize Git repository: {str(e)}")
