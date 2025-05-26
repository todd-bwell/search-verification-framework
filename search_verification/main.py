import logging
import os
from dotenv import load_dotenv

from search_verification.services.search_term_generator import SearchTermGenerator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Load environment variables
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_url = os.getenv("OPENAI_URL")
        openai_model = os.getenv("OPENAI_MODEL")

        if not openai_api_key or not openai_url or not openai_model:
            logger.error("Missing required environment variables.")
            return

        # Instantiate and invoke SearchTermGenerator
        generator = SearchTermGenerator(model=openai_model)
        terms = generator.generate_terms(num_terms=3)
        logger.info("Generated search terms:\n %s", terms)

    except Exception as e:
        logger.exception("An error occurred while running the main process.")

if __name__ == "__main__":
    main()