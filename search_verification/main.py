import json
import logging
import os
import argparse
from dotenv import load_dotenv

from search_verification.services.graphql_query_runner import GraphQLQueryRunner
from search_verification.services.search_term_generator import SearchTermGenerator
from search_verification.services.csv_writer import CsvWriter
from search_verification.services.search_result_scorer import SearchResultScorer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(
        num_search_terms:int =5,
        output_file:str ='results.csv',
        pss_envt:str ='DEV'):
    try:
        # Load environment variables
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_url = os.getenv("OPENAI_URL")
        openai_model = os.getenv("OPENAI_MODEL")
        match pss_envt.upper():
            case 'LOCALHOST':
                pss_base_url = os.getenv("PSS_BASE_URL_LOCALHOST")
            case 'DEV':
                pss_base_url = os.getenv("PSS_BASE_URL_DEV")
            case 'STAGING':
                pss_base_url = os.getenv("PSS_BASE_URL_STAGING")
            case _:
                logger.error(f"PSS environment: {pss_envt} not supported")
                return

        logger.info(f"Evaluating PSS {pss_envt} search results for {num_search_terms} terms")

        if not openai_api_key or not openai_url or not openai_model:
            logger.error("Missing required environment variables.")
            return

        # Generate a set of test search terms
        generator = SearchTermGenerator(model=openai_model)
        terms = generator.generate_terms(num_terms=num_search_terms)
        logger.info("Generated search terms:\n %s", terms)

        # Instantiate GraphQLQueryRunner
        runner = GraphQLQueryRunner(pss_base_url + "/graphql")

        # For each search term, search providers and log the content field
        scorer = SearchResultScorer(model=openai_model)
        for search_term in terms:
            logger.info(f"Searching PSS {pss_envt} for term: {search_term}")
            raw_search_results = runner.search_providers(search_term)
            search_results = raw_search_results.get("data", {}).get("searchProviders", {}).get("results", [])

            scored_results = scorer.score_search_results(
                pss_envt=pss_envt,
                search_term=search_term,
                search_results=search_results
            )

            # Write search results to csv
            logger.info(f"Writing search result analysis to {output_file}")
            csv_path = os.path.join("./output", output_file)
            csv_writer = CsvWriter(json.dumps(scored_results.content_json))
            csv_writer.convert(csv_path)


    except Exception as e:
        logger.exception("An error occurred while running the main process.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_search_terms", type=int, default=1)
    parser.add_argument("--output_file", type=str, default='results.csv',)
    parser.add_argument("--pss_envt", type=str, default='DEV',)
    args = parser.parse_args()
    main(
        num_search_terms=args.num_search_terms,
        output_file=args.output_file,
        pss_envt=args.pss_envt
    )