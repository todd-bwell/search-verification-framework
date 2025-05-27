import pytest
from dotenv import load_dotenv
import os
from unittest.mock import patch, MagicMock

from search_verification.services.search_result_scorer import SearchResultScorer

load_dotenv()  # Loads variables from .env

def test_score_search_results_e2e():
    openai_model = os.getenv("OPENAI_MODEL")
    if not openai_model:
        pytest.skip("OPENAI_MODEL environment variable not set")

    search_term = "Dr. Smith"
    search_results = [
        {"content": "Dr. John Smith"},
        {"content": "Cardiac Care Center"}
    ]

    scorer = SearchResultScorer(model=openai_model)

    result = scorer.score_search_results(search_term=search_term, search_results=search_results)

    assert "Dr. Smith" in result.content #Provider name
    assert "1" in result.content # Rank
    assert any(score in result.content for score in ['"relevanceScore": 10', '"relevanceScore": 9']) # Relevance score
    assert hasattr(result, "content_json")
    assert "searchTerm" in result.content_json