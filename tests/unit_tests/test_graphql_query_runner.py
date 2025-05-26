import pytest
from unittest.mock import patch, Mock
from search_verification.services.graphql_query_runner import GraphQLQueryRunner

@pytest.fixture
def runner():
    return GraphQLQueryRunner("http://fake-url/graphql")

@patch("search_verification.services.graphql_query_runner.requests.post")
def test_execute_query_success(mock_post, runner):
    mock_response = Mock()
    mock_response.json.return_value = {"data": {"foo": "bar"}}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = runner.execute_query("query { foo }")
    assert result == {"data": {"foo": "bar"}}

@patch("search_verification.services.graphql_query_runner.requests.post")
def test_execute_query_graphql_error(mock_post, runner):
    mock_response = Mock()
    mock_response.json.return_value = {"errors": ["Some error"]}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    with pytest.raises(ValueError):
        runner.execute_query("query { foo }")

@patch("search_verification.services.graphql_query_runner.requests.post")
def test_execute_query_network_error(mock_post, runner):
    mock_post.side_effect = Exception("Network error")
    with pytest.raises(Exception):
        runner.execute_query("query { foo }")

@patch("search_verification.services.graphql_query_runner.requests.post")
def test_search_providers_calls_execute_query(mock_post, runner):
    mock_response = Mock()
    mock_response.json.return_value = {"data": {"searchProviders": {}}}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = runner.search_providers("test search")
    assert "data" in result