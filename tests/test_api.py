"""
Testes da API REST
"""
import pytest
from fastapi import status


class TestHealthEndpoints:
    """Testes de endpoints de health check"""

    def test_root_endpoint(self, client):
        """Testa endpoint raiz"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["status"] == "online"

    def test_health_check(self, client):
        """Testa health check"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"


class TestCasesEndpoints:
    """Testes dos endpoints de casos"""

    def test_list_tribunals(self, client):
        """Testa listagem de tribunais"""
        response = client.get("/api/v1/cases/tribunals")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "tribunals" in data
        assert len(data["tribunals"]) > 0
        assert any(t["code"] == "TJSP" for t in data["tribunals"])

    def test_search_missing_fields(self, client):
        """Testa busca com campos faltando"""
        response = client.post("/api/v1/cases/search", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_search_invalid_tribunal(self, client):
        """Testa busca com tribunal inválido"""
        response = client.post("/api/v1/cases/search", json={
            "tribunal": "INVALID",
            "search_type": "cpf",
            "query": "12345678900"
        })
        # Deve retornar erro 400 ou 500 dependendo da validação
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR]


class TestBulkEndpoints:
    """Testes dos endpoints de bulk"""

    def test_list_jobs_empty(self, client):
        """Testa listagem de jobs vazia"""
        response = client.get("/api/v1/bulk/jobs")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "jobs" in data
        assert "total" in data

    def test_get_nonexistent_job(self, client):
        """Testa buscar job inexistente"""
        response = client.get("/api/v1/bulk/status/nonexistent-job-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_upload_without_file(self, client):
        """Testa upload sem arquivo"""
        response = client.post("/api/v1/bulk/upload", data={
            "tribunal": "TJSP",
            "search_type": "cpf"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
