import json
import datetime
import logging
from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from search_verification.config import prompts

class SearchResultScorer:
  _logger = logging.getLogger(__name__)

  def __init__(self, *, model: str):
    if not model:
      self._logger.error("The 'model' parameter must be specified.")
      raise ValueError("The 'model' parameter must be specified.")
    self._logger.info("Initializing SearchTermGenerator with model: %s", model)
    self._llm = ChatOpenAI(model_name=model)

  def score_search_results(
          self,
          *,
          pss_envt: str,
          search_term: str,
          search_results: List[Dict]) -> str:
    self._logger.info("Scoring search results for term: %s", search_term)
    prompt = prompts.relevance_scoring_prompt
    self._logger.debug(f"Prompt: {prompt}")

    chain = prompt | self._llm
    try:
      result = chain.invoke({"SEARCH_TERM": search_term, "SEARCH_RESULTS": search_results})
    except Exception as e:
      self._logger.error("Error invoking LLM chain: %s", e)
      raise RuntimeError("Failed to evaluate search results") from e

    if not result or not hasattr(result, "content"):
      self._logger.error("LLM result is invalid or missing 'content': %s", result)
      raise RuntimeError("LLM result is invalid or missing 'content'")

    # result["content_json"] = json.loads(result.content)
    result_json = json.loads(result.content)
    result_json["pss_envt"] = pss_envt
    result_json["dateTime"] = datetime.datetime.now().isoformat()
    result_json["pssEnv"] = pss_envt
    setattr(result, "content_json", result_json)

    # self._logger.info("Raw LLM result: %s", result)
    return result
