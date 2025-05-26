import logging
from typing import List
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from search_verification_framework.config import prompts

class SearchTermGenerator:
    logger = logging.getLogger(__name__)

    def __init__(self, *, model: str):
        if not model:
            self.logger.error("The 'model' parameter must be specified.")
            raise ValueError("The 'model' parameter must be specified.")
        self.logger.info("Initializing SearchTermGenerator with model: %s", model)
        self.llm = ChatOpenAI(model_name=model)

    def generate_terms(
            self,
            num_terms: int = 10
    ) -> List[str]:
        self.logger.info("Generating %d search terms", num_terms)
        prompt = prompts.search_term_prompt
        self.logger.info(f"Prompt: {prompt}")

        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = chain.run(num_terms=num_terms)
        self.logger.debug("Raw LLM result: %s", result)

        terms = [term.strip() for term in result.split(',')]
        self.logger.info("Generated terms: %s", terms)
        return terms