"""
Rotas para consulta de processos
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from app.api.schemas import (
    SearchRequest,
    SearchResponse,
    CaseDetailsRequest,
    CaseResponse,
    TribunalsResponse,
    TribunalInfo,
    ErrorResponse
)
from app.services.case_service import CaseService
from app.tribunals.base import SearchResult, Case

router = APIRouter(prefix="/cases", tags=["cases"])
case_service = CaseService()


@router.post(
    "/search",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar processos",
    description="Realiza busca de processos em um tribunal específico"
)
async def search_cases(request: SearchRequest):
    """
    Busca processos judiciais

    - **tribunal**: Código do tribunal (ex: TJSP)
    - **search_type**: Tipo de busca (cpf, name, case_number)
    - **query**: Termo de busca
    """
    try:
        logger.info(f"API: Busca solicitada - {request.dict()}")

        result = await case_service.search(
            tribunal=request.tribunal.upper(),
            search_type=request.search_type,
            query=request.query
        )

        return result

    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro ao processar busca: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar busca"
        )


@router.post(
    "/details",
    response_model=CaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter detalhes de processo",
    description="Obtém informações detalhadas de um processo específico"
)
async def get_case_details(request: CaseDetailsRequest):
    """
    Obtém detalhes completos de um processo

    - **tribunal**: Código do tribunal
    - **case_number**: Número do processo
    """
    try:
        logger.info(f"API: Detalhes solicitados - {request.dict()}")

        case = await case_service.get_case_details(
            tribunal=request.tribunal.upper(),
            case_number=request.case_number
        )

        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Processo não encontrado"
            )

        return case

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro ao obter detalhes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter detalhes do processo"
        )


@router.get(
    "/tribunals",
    response_model=TribunalsResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar tribunais disponíveis",
    description="Lista todos os tribunais que podem ser consultados"
)
async def list_tribunals():
    """
    Lista tribunais disponíveis no sistema

    Retorna lista com código e nome de cada tribunal
    """
    try:
        available = case_service.list_available_tribunals()

        # Mapeamento de nomes
        tribunal_names = {
            "TJSP": "Tribunal de Justiça de São Paulo",
            "TJRJ": "Tribunal de Justiça do Rio de Janeiro",
            "STJ": "Superior Tribunal de Justiça",
        }

        tribunals = [
            TribunalInfo(
                code=code,
                name=tribunal_names.get(code, code),
                available=True
            )
            for code in available
        ]

        return TribunalsResponse(tribunals=tribunals)

    except Exception as e:
        logger.error(f"Erro ao listar tribunais: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar tribunais"
        )


@router.get(
    "/tribunals/{tribunal}/validate",
    status_code=status.HTTP_200_OK,
    summary="Validar tribunal",
    description="Verifica se um tribunal está disponível e acessível"
)
async def validate_tribunal(tribunal: str):
    """
    Valida se tribunal está acessível

    - **tribunal**: Código do tribunal
    """
    try:
        is_valid = await case_service.validate_tribunal(tribunal.upper())

        if not is_valid:
            return {
                "tribunal": tribunal.upper(),
                "available": False,
                "message": "Tribunal não disponível ou inacessível"
            }

        return {
            "tribunal": tribunal.upper(),
            "available": True,
            "message": "Tribunal disponível"
        }

    except Exception as e:
        logger.error(f"Erro ao validar tribunal: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao validar tribunal"
        )
