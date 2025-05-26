import pytest
import logging
from unittest.mock import patch, MagicMock
from search_verification.services.search_term_generator import SearchTermGenerator

@patch("search_verification.services.search_term_generator.LLMChain")
@patch("search_verification.services.search_term_generator.ChatOpenAI")
def test_generate_terms(mock_chat_openai, mock_llm_chain):
    # Arrange
    mock_chain_instance = MagicMock()
    mock_chain_instance.run.return_value = "term1, term2, term3"
    mock_llm_chain.return_value = mock_chain_instance

    generator = SearchTermGenerator(model="fake-model")

    # Act
    terms = generator.generate_terms(num_terms=3)

    # Assert
    assert terms == ["term1", "term2", "term3"]

    mock_llm_chain.assert_called_once()
    mock_chain_instance.run.assert_called_once_with(num_terms=3)