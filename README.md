# search-verification-framework
A search service vertification tool that uses AI to generate mock search terms, query PSS and evaluate relevance of search results.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/todd-bwell/search-verification-framework.git
   pip3 install -r requirements.txt
   ```
## Run tests

In PyCharm, right-click the tests folder and select `"Run 'Python tests in tests...'".`

Or run tests from the terminal with console logging:

`pytest --log-cli-level=INFO`

## Run `main.py` from command line - must be in project root

`python -m search_verification.main`


## Tooling
The project uses a sequential langchain to generate search terms, query a search service and evaluate the results.

## Overview
For an overview of the approach and breakdown of the approach, feed the following prompt to GitHub Copilot:
```
Explain what the code in `search-verification/main.py` does, including the purpose of each class and method, and how the overall workflow operates.
```
