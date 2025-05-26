import logging
from typing import List
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from search_verification.config import prompts

class SearchTermGenerator:
    _logger = logging.getLogger(__name__)

    def __init__(self, *, model: str):
        if not model:
            self._logger.error("The 'model' parameter must be specified.")
            raise ValueError("The 'model' parameter must be specified.")
        self._logger.info("Initializing SearchTermGenerator with model: %s", model)
        self._llm = ChatOpenAI(model_name=model)

    def generate_terms(
        self,
        num_terms: int = 10
    ) -> List[str]:
        self._logger.info("Generating %d search terms", num_terms)
        prompt = prompts.search_term_prompt
        self._logger.info(f"Prompt: {prompt}")

        chain = prompt | self._llm
        try:
            result = chain.invoke({"num_terms": num_terms})
        except Exception as e:
            self._logger.error("Error invoking LLM chain: %s", e)
            raise RuntimeError("Failed to generate search terms") from e

        if not result or not hasattr(result, "content"):
            self._logger.error("LLM result is invalid or missing 'content': %s", result)
            raise RuntimeError("LLM result is invalid or missing 'content'")

        self._logger.info("Raw LLM result: %s", result)
        terms = [term.strip() for term in result.content.split(',')]
        self._logger.info("Generated terms: %s", terms)
        return terms