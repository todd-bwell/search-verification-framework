import pytest
from search_verification_framework.config import prompts

def test_search_term_prompt_variables():
    assert "num_terms" in prompts.search_term_prompt.input_variables

def test_intent_prompt_variables():
    assert "search_term" in prompts.intent_prompt.input_variables

def test_relevance_scoring_prompt_variables():
    for var in ["search_term", "intent", "results"]:
        assert var in prompts.relevance_scoring_prompt.input_variables