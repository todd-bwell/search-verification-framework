import pytest
import logging
from dotenv import load_dotenv
import os
from search_verification_framework.services.search_term_generator import SearchTermGenerator

load_dotenv()  # Loads variables from .env

def test_generate_terms_e2e():
    # Logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    openai_model = os.getenv("OPENAI_MODEL")
    if not openai_model:
        pytest.skip("OPENAI_MODEL environment variable not set")

    generator = SearchTermGenerator(model=openai_model)
    terms = generator.generate_terms(num_terms=3)

    logger.info("Terms:")
    logger.info(terms)

    assert isinstance(terms, list)
    assert len(terms) == 3
    assert all(isinstance(term, str) and term.strip() for term in terms)