import pytest
from dotenv import load_dotenv
import os
from unittest.mock import patch, MagicMock

from search_verification.services.search_result_scorer import SearchResultScorer

load_dotenv()  # Loads variables from .env

# @pytest.fixture
# def scorer():
#     return SearchResultScorer(model="fake-model")

# @patch("search_verification.services.search_result_scorer.ChatOpenAI")
# @patch("search_verification.services.search_result_scorer.prompts")
def test_score_search_results_e2e():
    # Mock LLM and prompt
    # mock_llm_instance = MagicMock()
    # mock_llm_instance.invoke.return_value = MagicMock(content='{"searchTerm": "Dr. Smith", "inferredIntent": "Find a provider", "searchResults": [{"content": "Dr. John Smith", "relevanceScore": 10, "relevanceRationale": "Exact match"}]}')
    # mock_chat_openai.return_value = mock_llm_instance
    # mock_prompts.relevance_scoring_prompt = MagicMock()

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

    assert "Dr. Smith" in result.content
    assert any(score in result.content for score in ['"relevanceScore": 10', '"relevanceScore": 9'])
    # mock_llm_instance.invoke.assert_called_once()