"""
Interface abstrata para tribunais - Strategy Pattern
Todos os tribunais devem implementar esta interface
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class SearchType(str, Enum):
    """Tipos de busca suportados"""
    CPF = "cpf"
    NAME = "name"
    CASE_NUMBER = "case_number"
    CNPJ = "cnpj"
    OAB = "oab"


class CaseStatus(str, Enum):
    """Status de um processo"""
    ATIVO = "ativo"
    ARQUIVADO = "arquivado"
    SUSPENSO = "suspenso"
    BAIXADO = "baixado"
    EXTINTO = "extinto"


class Party(BaseModel):
    """Representa uma parte do processo"""
    name: str
    role: str  # autor, réu, advogado, etc.
    cpf_cnpj: Optional[str] = None
    oab: Optional[str] = None


class Movement(BaseModel):
    """Movimentação processual"""
    date: datetime
    description: str
    details: Optional[str] = None


class Case(BaseModel):
    """Modelo padronizado de um processo judicial"""
    case_number: str = Field(..., description="Número do processo")
    tribunal: str = Field(..., description="Tribunal de origem")
    court: Optional[str] = Field(None, description="Vara/Comarca")
    status: CaseStatus
    subject: Optional[str] = Field(None, description="Assunto do processo")
    start_date: Optional[datetime] = Field(None, description="Data de distribuição")
    parties: List[Party] = Field(default_factory=list)
    movements: List[Movement] = Field(default_factory=list)
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Dados brutos da API")

    class Config:
        json_schema_extra = {
            "example": {
                "case_number": "1000001-01.2024.8.26.0100",
                "tribunal": "TJSP",
                "court": "1ª Vara Cível",
                "status": "ativo",
                "subject": "Ação de Cobrança",
                "start_date": "2024-01-15T00:00:00",
                "parties": [
                    {
                        "name": "João da Silva",
                        "role": "autor",
                        "cpf_cnpj": "12345678900"
                    }
                ]
            }
        }


class SearchResult(BaseModel):
    """Resultado de uma busca"""
    query: str
    search_type: SearchType
    tribunal: str
    cases: List[Case]
    total_found: int
    search_date: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "query": "12345678900",
                "search_type": "cpf",
                "tribunal": "TJSP",
                "cases": [],
                "total_found": 0
            }
        }


class BaseTribunal(ABC):
    """
    Classe abstrata que define a interface para todos os tribunais.

    Cada tribunal deve implementar todos os métodos abstratos para garantir
    compatibilidade com o sistema.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa o cliente do tribunal

        Args:
            config: Configurações específicas do tribunal
        """
        self.config = config or {}
        self.tribunal_code = self._get_tribunal_code()

    @abstractmethod
    def _get_tribunal_code(self) -> str:
        """Retorna o código identificador do tribunal (ex: 'TJSP', 'TJRJ')"""
        pass

    @abstractmethod
    async def search_by_cpf(self, cpf: str) -> SearchResult:
        """
        Busca processos por CPF

        Args:
            cpf: CPF a ser pesquisado (apenas números)

        Returns:
            SearchResult com os processos encontrados
        """
        pass

    @abstractmethod
    async def search_by_name(self, name: str) -> SearchResult:
        """
        Busca processos por nome

        Args:
            name: Nome da pessoa a ser pesquisada

        Returns:
            SearchResult com os processos encontrados
        """
        pass

    @abstractmethod
    async def search_by_case_number(self, case_number: str) -> SearchResult:
        """
        Busca processo pelo número

        Args:
            case_number: Número do processo

        Returns:
            SearchResult com o processo encontrado
        """
        pass

    @abstractmethod
    async def get_case_details(self, case_number: str) -> Optional[Case]:
        """
        Obtém detalhes completos de um processo específico

        Args:
            case_number: Número do processo

        Returns:
            Case com todos os detalhes ou None se não encontrado
        """
        pass

    async def search(self, query: str, search_type: SearchType) -> SearchResult:
        """
        Método genérico de busca que roteia para o método específico

        Args:
            query: Termo de busca
            search_type: Tipo de busca a ser realizada

        Returns:
            SearchResult apropriado
        """
        if search_type == SearchType.CPF:
            return await self.search_by_cpf(query)
        elif search_type == SearchType.NAME:
            return await self.search_by_name(query)
        elif search_type == SearchType.CASE_NUMBER:
            return await self.search_by_case_number(query)
        else:
            raise ValueError(f"Tipo de busca não suportado: {search_type}")

    async def validate_connection(self) -> bool:
        """
        Valida se a conexão com o tribunal está funcionando

        Returns:
            True se a conexão está OK, False caso contrário
        """
        try:
            # Implementação básica - cada tribunal pode sobrescrever
            return True
        except Exception:
            return False
