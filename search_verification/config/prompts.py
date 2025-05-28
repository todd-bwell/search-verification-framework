from langchain.prompts import PromptTemplate

search_term_prompt = PromptTemplate(
    input_variables=["num_terms"],
    template=(
"""
You are a person searching for your health records using my healthcare search service. As a user, you've accessed my search service from an app that lets you connect your health records using PROA, and in order to find your health records you need to search for a doctor, practice, organization, insurance or lab where your health records are stored.
You are NOT searching for a department, so search terms should not include terms like 'Records Department' - just the name of the provider or organization.
Generate {num_terms} diverse and realistic search terms. With each term you, as the patient, should have intent to find a doctor, practice, organization, insurance or lab where your health records are stored. You are not searching for healthcare products or services, just the place where your health records are stored. Ensure the terms are specific and representative of real user queries.
Important Guidelines:
- Terms must represent genuine patient search intent
- Focus ONLY on finding record storage locations
- Do NOT generate searches for healthcare products or general services
- Ensure terms are specific and varied. Avoid using the same doctor names, insurance companies or hospitals repeatedly

Generate {num_terms} comma-separated search terms for finding healthcare records.

Rules:
- Focus strictly on doctors, practices, organizations, insurers, or labs storing health records
- Terms must be specific, realistic patient search queries
- Do NOT include searches for healthcare products or general services

Output ONLY the comma-delimited terms, with NO additional explanation
"""
    )
)

relevance_scoring_prompt = PromptTemplate(
    input_variables=["SEARCH_TERM", "SEARCH_RESULTS"],
    template=(
"""
<Inputs>
{SEARCH_TERM}
{SEARCH_RESULTS}
</Inputs>

<Instructions Structure>
1. First, define the context and goal of the task
2. Specify the exact JSON structure required
3. Provide clear instructions about scoring and relevance
4. Emphasize the need for a pure JSON response without additional text
</Instructions>

<Instructions>
You are a sophisticated search result relevance analyzer for a health care record search service. 
Your task is to process a search term and a list of search results, and generate a structured JSON response that captures the search intent and relevance of each result.

For the search term, you must infer/determine the user's likely search intent (e.g., were they trying to find a doctor, practice, insurance company, or lab)

For each search result, you must:
1. Assign the search rank. Starting at 1, where did this result rank in the search results?
2. Assign a relevance score from 1-10 
3. Provide a concise rationale for the relevance score, 2 sentences or less.

JSON Response Structure:
```json
{{
    "searchTerm": "{SEARCH_TERM}",
    "inferredIntent": "...",
    "searchResults": [
        {{
            "rank": "1-100",
            "content": "...",
            "relevanceScore": 0-10,
            "relevanceRationale": "..."
        }}
    ]
}}
```

Scoring Guidelines:
- 1-3: Minimal or no relevance to search intent
- 4-6: Partial relevance or tangential connection
- 7-9: Strong relevance with most key details matching
- 10: Exact, perfect match to search intent

Important Rules:
- Provide ONLY the JSON response
- Do not include any additional text, explanation, or commentary
- Ensure the JSON is valid and well-formatted
- Be precise and objective in your scoring and rationales

Process:
1. Carefully analyze the search term
2. Determine the most likely search intent
3. Evaluate each search result against that intent
4. Score and rationalize each result's relevance
5. Compile the results into the specified JSON structure

<example>
{{
    "searchTerm": "Dr. Smith Cardiology",
    "inferredIntent": "Find a specific doctor",
    "searchResults": [
        {{
            "rank": "1",
            "content": "Dr. John Smith, Cardiologist, St. Mary's Hospital",
            "relevanceScore": 9,
            "relevanceRationale": "Matches name, specialty, and likely practice location"
        }},
        {{
            "rank": "2",
            "content": "Cardiac Care Center",
            "relevanceScore": 6,
            "relevanceRationale": "Related to cardiology but not a specific provider match"
        }}
    ]
}}
</example>
</Instructions>
"""
    )
)