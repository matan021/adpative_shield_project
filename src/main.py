import logging
from src.manager.workflow_manager import WorkflowManager
from src.utils.logging_config import setup_logging
from dotenv import load_dotenv


setup_logging()
logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    url = "https://en.wikipedia.org/wiki/List_of_animal_names"
    base_wikipedia = "https://en.wikipedia.org"
    manager = WorkflowManager(url, base_wikipedia)
    manager.run()


if __name__ == "__main__":
    main()
