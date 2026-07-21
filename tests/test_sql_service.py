from unittest.mock import Mock
from src.services.sql_service import SQLService

def test_sql_service_returns_answer():

    service = SQLService()

    service.agent = Mock()

    service.agent.ask.return_value = ("There are 5 customers.")

    result = service.ask("How many customers are there?")

    assert result == ("There are 5 customers.")