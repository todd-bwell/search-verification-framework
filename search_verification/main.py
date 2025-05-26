import logging
import os
from dotenv import load_dotenv

from search_verification.services.graphql_query_runner import GraphQLQueryRunner
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
        pss_base_url = os.getenv("PSS_BASE_URL")

        if not openai_api_key or not openai_url or not openai_model:
            logger.error("Missing required environment variables.")
            return

        # Instantiate and invoke SearchTermGenerator
        generator = SearchTermGenerator(model=openai_model)
        terms = generator.generate_terms(num_terms=1)
        logger.info("Generated search terms:\n %s", terms)

        # Instantiate GraphQLQueryRunner
        runner = GraphQLQueryRunner(pss_base_url + "/graphql")

        # For each search term, search providers and log the content field
        for term in terms:
            logger.info(f"Searching providers for term: {term}")
            result = runner.search_providers(term)
            results = result.get("data", {}).get("searchProviders", {}).get("results", [])
            for res in results:
                content = res.get("content")
                logger.info(f"Result content: {content}")

    except Exception as e:
        logger.exception("An error occurred while running the main process.")

if __name__ == "__main__":
    main()