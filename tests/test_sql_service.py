from types import SimpleNamespace
from unittest.mock import Mock, patch
import pytest
from src.agent.sql_agent import AgentResponse, SQLAgent
from src.services.sql_service import SQLService
from src.utils.exceptions import QueryExecutionError, SQLAgentError

@pytest.fixture
def service():

    with patch("src.services.sql_service.SQLAgent") as agent_class:
        agent_class.return_value = Mock()
        yield SQLService()

def test_sql_service_returns_answer(service):

    service.agent.ask.return_value = AgentResponse(
        answer="There are 5 customers.",
        queries=["SELECT COUNT(*) FROM customers"]
    )

    result = service.ask("  How many customers are there?  ")

    assert result.answer == "There are 5 customers."
    assert result.final_query == "SELECT COUNT(*) FROM customers"
    service.agent.ask.assert_called_once_with("How many customers are there?")

@pytest.mark.parametrize("question", ["", "   ", None])
def test_sql_service_rejects_empty_question(service, question):

    with pytest.raises(QueryExecutionError):
        service.ask(question)

    service.agent.ask.assert_not_called()

def test_sql_service_propagates_agent_errors(service):

    service.agent.ask.side_effect = SQLAgentError("Unable to process SQL request.")

    with pytest.raises(SQLAgentError):
        service.ask("How many customers are there?")

def test_sql_service_wraps_unexpected_errors(service):

    service.agent.ask.side_effect = ValueError("unexpected")

    with pytest.raises(QueryExecutionError):
        service.ask("How many customers are there?")

def test_extract_queries_keeps_only_executed_sql():

    steps = [
        (SimpleNamespace(tool="sql_db_list_tables", tool_input={}), "customers"),
        (SimpleNamespace(tool="sql_db_query", tool_input={"query": " SELECT 1 "}), "[(1,)]"),
        (SimpleNamespace(tool="sql_db_query", tool_input="SELECT 2"), "[(2,)]")
    ]

    assert SQLAgent._extract_queries(steps) == ["SELECT 1", "SELECT 2"]
