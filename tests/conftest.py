"""
Configuração de testes pytest
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture do cliente de teste"""
    return TestClient(app)


@pytest.fixture
def sample_cpf():
    """CPF válido para testes"""
    return "12345678900"


@pytest.fixture
def sample_case_number():
    """Número de processo para testes"""
    return "1000001-01.2024.8.26.0100"


@pytest.fixture
def mock_search_result():
    """Resultado de busca mockado"""
    from app.tribunals.base import SearchResult, SearchType
    from datetime import datetime

    return SearchResult(
        query="12345678900",
        search_type=SearchType.CPF,
        tribunal="TJSP",
        cases=[],
        total_found=0,
        search_date=datetime.now()
    )
