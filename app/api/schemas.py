"""
Schemas Pydantic para requisições e respostas da API
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.tribunals.base import SearchType, CaseStatus


# Request Schemas

class SearchRequest(BaseModel):
    """Requisição de busca"""
    tribunal: str = Field(..., description="Código do tribunal (ex: TJSP)")
    search_type: SearchType = Field(..., description="Tipo de busca")
    query: str = Field(..., description="Termo de busca")

    class Config:
        json_schema_extra = {
            "example": {
                "tribunal": "TJSP",
                "search_type": "cpf",
                "query": "12345678900"
            }
        }


class CaseDetailsRequest(BaseModel):
    """Requisição de detalhes de processo"""
    tribunal: str = Field(..., description="Código do tribunal")
    case_number: str = Field(..., description="Número do processo")

    class Config:
        json_schema_extra = {
            "example": {
                "tribunal": "TJSP",
                "case_number": "1000001-01.2024.8.26.0100"
            }
        }


# Response Schemas

class PartyResponse(BaseModel):
    """Resposta de parte do processo"""
    name: str
    role: str
    cpf_cnpj: Optional[str] = None
    oab: Optional[str] = None


class MovementResponse(BaseModel):
    """Resposta de movimentação"""
    date: datetime
    description: str
    details: Optional[str] = None


class CaseResponse(BaseModel):
    """Resposta de processo"""
    case_number: str
    tribunal: str
    court: Optional[str] = None
    status: CaseStatus
    subject: Optional[str] = None
    start_date: Optional[datetime] = None
    parties: List[PartyResponse] = []
    movements: List[MovementResponse] = []


class SearchResponse(BaseModel):
    """Resposta de busca"""
    query: str
    search_type: SearchType
    tribunal: str
    cases: List[CaseResponse]
    total_found: int
    search_date: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "query": "12345678900",
                "search_type": "cpf",
                "tribunal": "TJSP",
                "cases": [],
                "total_found": 0,
                "search_date": "2024-01-15T10:30:00"
            }
        }


class TribunalInfo(BaseModel):
    """Informações sobre tribunal"""
    code: str
    name: str
    available: bool


class TribunalsResponse(BaseModel):
    """Lista de tribunais disponíveis"""
    tribunals: List[TribunalInfo]


class JobStatusResponse(BaseModel):
    """Status de job de processamento"""
    job_id: str
    tribunal: str
    status: str
    total_items: int
    processed_items: int
    successful_items: int
    failed_items: int
    progress_percentage: float
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class JobCreatedResponse(BaseModel):
    """Resposta de criação de job"""
    job_id: str
    message: str
    status_url: str


class ErrorResponse(BaseModel):
    """Resposta de erro"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
