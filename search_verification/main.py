import json
import logging
import os
from dotenv import load_dotenv

from search_verification.services.graphql_query_runner import GraphQLQueryRunner
from search_verification.services.search_term_generator import SearchTermGenerator
from search_verification.services.csv_writer import CsvWriter
from search_verification.services.search_result_scorer import SearchResultScorer

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

        # Generate a set of test search terms
        generator = SearchTermGenerator(model=openai_model)
        terms = generator.generate_terms(num_terms=1)
        logger.info("Generated search terms:\n %s", terms)

        # Instantiate GraphQLQueryRunner
        runner = GraphQLQueryRunner(pss_base_url + "/graphql")

        # For each search term, search providers and log the content field
        scorer = SearchResultScorer(model=openai_model)
        for search_term in terms:
            logger.info(f"Searching providers for term: {search_term}")
            result = runner.search_providers(search_term)
            search_results = result.get("data", {}).get("searchProviders", {}).get("results", [])
            # for res in results:
            #     content = res.get("content")
            #     logger.info(f"Result content: {content}")

            scored_result = scorer.score_search_results(search_term=search_term, search_results=search_results)

            # Write search results to csv
            csv_path = os.path.join("./", "results.csv")
            csv_writer = CsvWriter(json.dumps(scored_result.content_json))
            csv_writer.convert(csv_path)


    except Exception as e:
        logger.exception("An error occurred while running the main process.")

if __name__ == "__main__":
    main()