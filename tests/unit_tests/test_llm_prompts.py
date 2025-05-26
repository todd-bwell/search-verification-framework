import pytest
from search_verification.config import prompts

def test_search_term_prompt_variables():
    assert "num_terms" in prompts.search_term_prompt.input_variables

def test_relevance_scoring_prompt_variables():
    for var in ["SEARCH_TERM", "SEARCH_RESULTS"]:
        assert var in prompts.relevance_scoring_prompt.input_variables