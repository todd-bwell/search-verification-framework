import pytest
from unittest.mock import patch, MagicMock
from search_verification.services.search_term_generator import SearchTermGenerator

@patch("search_verification.services.search_term_generator.ChatOpenAI")
def test_generate_terms_success(mock_chat_openai):
    mock_llm = MagicMock()
    mock_chain = MagicMock()
    # Simulate the result object with a 'content' attribute
    mock_result = MagicMock()
    mock_result.content = "term1, term2, term3"
    mock_chain.invoke.return_value = mock_result
    # The prompt | llm returns the chain
    mock_prompt = MagicMock()
    with patch("search_verification.services.search_term_generator.prompts") as mock_prompts:
        mock_prompts.search_term_prompt = mock_prompt
        mock_prompt.__or__.return_value = mock_chain
        mock_chat_openai.return_value = mock_llm

        generator = SearchTermGenerator(model="fake-model")
        terms = generator.generate_terms(num_terms=3)
        assert terms == ["term1", "term2", "term3"]
        mock_chain.invoke.assert_called_once_with({"num_terms": 3})

@patch("search_verification.services.search_term_generator.ChatOpenAI")
def test_generate_terms_invalid_result(mock_chat_openai):
    mock_llm = MagicMock()
    mock_chain = MagicMock()
    # Simulate result with no 'content'
    mock_chain.invoke.return_value = None
    mock_prompt = MagicMock()
    with patch("search_verification.services.search_term_generator.prompts") as mock_prompts:
        mock_prompts.search_term_prompt = mock_prompt
        mock_prompt.__or__.return_value = mock_chain
        mock_chat_openai.return_value = mock_llm

        generator = SearchTermGenerator(model="fake-model")
        with pytest.raises(RuntimeError, match="LLM result is invalid or missing 'content'"):
            generator.generate_terms(num_terms=3)

@patch("search_verification.services.search_term_generator.ChatOpenAI")
def test_generate_terms_invoke_exception(mock_chat_openai):
    mock_llm = MagicMock()
    mock_chain = MagicMock()
    mock_chain.invoke.side_effect = Exception("LLM error")
    mock_prompt = MagicMock()
    with patch("search_verification.services.search_term_generator.prompts") as mock_prompts:
        mock_prompts.search_term_prompt = mock_prompt
        mock_prompt.__or__.return_value = mock_chain
        mock_chat_openai.return_value = mock_llm

        generator = SearchTermGenerator(model="fake-model")
        with pytest.raises(RuntimeError, match="Failed to generate search terms"):
            generator.generate_terms(num_terms=3)

def test_init_missing_model():
    with pytest.raises(ValueError, match="The 'model' parameter must be specified."):
        SearchTermGenerator(model=None)