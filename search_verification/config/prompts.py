from langchain.prompts import PromptTemplate

search_term_prompt = PromptTemplate(
    input_variables=["num_terms"],
    template=(
"""
You are a person searching for your health records using my healthcare search service. As a user, you've accessed my search service from an app that lets you connect your health records using PROA, and in order to find your health records you need to search for a provider, practice, organization, insurance or lab where your health records are stored.
Generate {num_terms} diverse and realistic search terms. With each term you, as the patient, should have intent to find a provider, practice, organization, insurance or lab where your health records are stored. You are not searching for healthcare products or services, just the place where your health records are stored. Ensure the terms are specific and representative of real user queries.
Important Guidelines:
- Terms must represent genuine patient search intent
- Focus ONLY on finding record storage locations
- Do NOT generate searches for healthcare products or general services
- Ensure terms are specific and varied

Generate {num_terms} comma-separated search terms for finding healthcare records.

Rules:
- Focus strictly on providers, practices, organizations, insurers, or labs storing health records
- Terms must be specific, realistic patient search queries
- Do NOT include searches for healthcare products or general services

Output ONLY the comma-delimited terms, with NO additional explanation
"""
    )
)

intent_prompt = PromptTemplate(
    input_variables=["search_term"],
    template=(
        "Analyze the search term '{search_term}' and infer the most likely user intent. "
        "Provide a concise explanation of what the user is probably seeking."
    )
)

relevance_scoring_prompt = PromptTemplate(
    input_variables=["search_term", "intent", "results"],
    template=(
        "Evaluate the relevance of search results for the term '{search_term}'.\n"
        "User Intent: {intent}\n"
        "Search Results: {results}\n\n"
        "Score the relevance from 0-1, where:\n"
        "0 = Completely irrelevant\n"
        "0.5 = Partially relevant\n"
        "1 = Highly relevant to the user's intent"
    )
)