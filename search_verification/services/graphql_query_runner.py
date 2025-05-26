from typing import Dict, Any, Optional, List
import requests
import json


class GraphQLQueryRunner:
  def __init__(self, url: str):
    """
    Initialize the GraphQL query runner with a specific endpoint URL.

    Args:
        url (str): The GraphQL endpoint URL
    """
    self.url = url

  def execute_query(
          self,
          query: str,
          variables: Optional[Dict[str, Any]] = None
  ) -> Dict[str, Any]:
    """
    Execute a GraphQL query with optional variables.

    Args:
        query (str): The GraphQL query string
        variables (dict, optional): Variables for the query

    Returns:
        dict: The parsed JSON response from the GraphQL endpoint

    Raises:
        requests.RequestException: For network or request-related errors
        ValueError: For invalid responses
    """
    # Prepare the request payload
    payload = {
      "query": query,
      "variables": variables or {}
    }

    try:
      # Send POST request to GraphQL endpoint
      response = requests.post(
        self.url,
        json=payload,
        headers={
          "Content-Type": "application/json",
          "Accept": "application/json"
        }
      )

      # Raise an exception for bad HTTP responses
      response.raise_for_status()

      # Parse the JSON response
      result = response.json()

      # Check for GraphQL errors
      if "errors" in result:
        raise ValueError(f"GraphQL Errors: {result['errors']}")

      return result

    except requests.RequestException as e:
      print(f"Network error occurred: {e}")
      raise
    except json.JSONDecodeError as e:
      print(f"JSON parsing error: {e}")
      raise ValueError("Invalid response from server")

  def search_providers(
          self,
          search_term: str,
          additional_vars: Optional[Dict[str, Any]] = None
  ) -> Dict[str, Any]:
    """
    Specialized method to search providers with predefined query.

    Args:
        search_term (str): The search term for providers
        additional_vars (dict, optional): Additional variables to override defaults

    Returns:
        dict: The search providers result
    """
    # Default variables with search term
    default_vars = {
      "limit": 10,
      "page_size": 4,
      "client": {
        "id": "OTHER",
        "config": "proa_practitioners",
        "dataSets": ["NPPES"]
      },
      "query_source": "PROA",
      "search": search_term
    }

    # Update with any additional variables
    if additional_vars:
      default_vars.update(additional_vars)

    query = '''
        query GetProviders(
            $client: [ClientInput], 
            $id_: [String], 
            $index: [IndexEnum], 
            $limit: Int, 
            $offset: Int, 
            $order_by: [OrderByInput], 
            $organization_type: [OrganizationTypeEnum], 
            $query_source: SourceEnum, 
            $search: String, 
            $search_position: SearchPosition, 
            $user: UserInput
        ) {
            searchProviders(
                searchProvidersInput: {
                    client: $client, 
                    id: $id_, 
                    index: $index, 
                    limit: $limit, 
                    offset: $offset, 
                    orderBy: $order_by, 
                    organizationType: $organization_type, 
                    querySource: $query_source, 
                    search: $search, 
                    searchPosition: $search_position, 
                    user: $user
                }
            ) {
                totalCount
                results {
                    content
                    id
                    score
                    scores {
                        value
                        description
                        calculation
                    }
                }    
            }
        }
        '''

    return self.execute_query(query, default_vars)


# Example usage
# def main():
#   # Replace with your actual GraphQL endpoint
#   graphql_url = "https://provider-search.dev.bwell.zone/graphql"
#
#   runner = GraphQLQueryRunner(graphql_url)
#
#   try:
#     result = runner.search_providers("Wilbur Kuo")
#     print(json.dumps(result, indent=2))
#   except Exception as e:
#     print(f"Error executing query: {e}")
#
#
# if __name__ == "__main__":
#   main()