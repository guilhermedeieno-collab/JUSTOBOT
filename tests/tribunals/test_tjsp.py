"""
Testes do cliente TJSP
"""
import pytest
from app.tribunals.tjsp.client import TJSPClient
from app.tribunals.base import SearchType


class TestTJSPClient:
    """Testes do cliente TJSP"""

    @pytest.fixture
    def client(self):
        """Fixture do cliente"""
        return TJSPClient()

    def test_tribunal_code(self, client):
        """Testa código do tribunal"""
        assert client._get_tribunal_code() == "TJSP"

    @pytest.mark.asyncio
    async def test_search_by_cpf_invalid(self, client):
        """Testa busca com CPF inválido"""
        result = await client.search_by_cpf("123")
        assert result.total_found == 0
        assert len(result.cases) == 0

    @pytest.mark.asyncio
    async def test_search_by_case_number_invalid(self, client):
        """Testa busca com número de processo inválido"""
        result = await client.search_by_case_number("123")
        assert result.total_found == 0


class TestTJSPRegistry:
    """Testes de registro do tribunal"""

    def test_tjsp_registered(self):
        """Testa se TJSP está registrado"""
        from app.tribunals.registry import TribunalRegistry

        assert TribunalRegistry.is_available("TJSP")

    def test_get_tjsp_instance(self):
        """Testa obtenção de instância"""
        from app.tribunals.registry import TribunalRegistry

        client = TribunalRegistry.get_tribunal("TJSP")
        assert client is not None
        assert client.tribunal_code == "TJSP"
