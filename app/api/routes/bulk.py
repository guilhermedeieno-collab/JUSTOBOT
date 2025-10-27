"""
Rotas para processamento em lote
"""
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status
from fastapi.responses import StreamingResponse
from loguru import logger
from io import BytesIO

from app.api.schemas import JobCreatedResponse, JobStatusResponse, ErrorResponse
from app.services.bulk_service import BulkService, JobStatus
from app.tribunals.base import SearchType

router = APIRouter(prefix="/bulk", tags=["bulk"])
bulk_service = BulkService()


@router.post(
    "/upload",
    response_model=JobCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload de planilha para processamento",
    description="Faz upload de planilha Excel ou CSV para busca em lote"
)
async def upload_bulk_file(
    file: UploadFile = File(..., description="Arquivo Excel (.xlsx, .xls) ou CSV"),
    tribunal: str = Form(..., description="Código do tribunal (ex: TJSP)"),
    search_type: SearchType = Form(..., description="Tipo de busca (cpf, name, case_number)")
):
    """
    Upload de arquivo para processamento em lote

    - **file**: Arquivo Excel ou CSV com dados para busca
    - **tribunal**: Tribunal onde buscar
    - **search_type**: Tipo de busca a realizar

    O arquivo deve conter uma coluna com os dados de busca.
    Colunas reconhecidas automaticamente:
    - Para CPF: 'cpf', 'documento', 'doc'
    - Para nome: 'nome', 'name', 'parte'
    - Para processo: 'processo', 'numero', 'number'
    """
    try:
        logger.info(f"API: Upload de arquivo - {file.filename}, tribunal={tribunal}")

        # Valida tipo de arquivo
        if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de arquivo não suportado. Use .xlsx, .xls ou .csv"
            )

        # Lê conteúdo
        content = await file.read()

        # Cria job
        job = await bulk_service.create_job_from_file(
            file_content=content,
            filename=file.filename,
            tribunal=tribunal.upper(),
            search_type=search_type
        )

        return JobCreatedResponse(
            job_id=job.job_id,
            message=f"Job criado com sucesso. {job.total_items} itens serão processados.",
            status_url=f"/api/v1/bulk/status/{job.job_id}"
        )

    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro ao processar upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar arquivo"
        )


@router.get(
    "/status/{job_id}",
    response_model=JobStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Verificar status do job",
    description="Obtém status atual de um job de processamento"
)
async def get_job_status(job_id: str):
    """
    Verifica status de processamento

    - **job_id**: ID do job retornado no upload
    """
    try:
        status_data = bulk_service.get_job_status(job_id)

        if not status_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job não encontrado"
            )

        return status_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter status do job"
        )


@router.get(
    "/download/{job_id}",
    status_code=status.HTTP_200_OK,
    summary="Download dos resultados",
    description="Baixa planilha Excel com resultados do processamento"
)
async def download_results(job_id: str):
    """
    Download dos resultados em formato Excel

    - **job_id**: ID do job

    O arquivo contém duas abas:
    - Resultados: Processos encontrados
    - Erros: Consultas que falharam
    """
    try:
        # Verifica status primeiro
        status_data = bulk_service.get_job_status(job_id)

        if not status_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job não encontrado"
            )

        if status_data["status"] not in ["completed", "partial"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Job ainda não está pronto. Status: {status_data['status']}"
            )

        # Gera arquivo
        excel_bytes = await bulk_service.get_job_results(job_id)

        if not excel_bytes:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar arquivo de resultados"
            )

        # Retorna como download
        return StreamingResponse(
            BytesIO(excel_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=justobot_results_{job_id}.xlsx"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao baixar resultados: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao baixar resultados"
        )


@router.get(
    "/jobs",
    status_code=status.HTTP_200_OK,
    summary="Listar todos os jobs",
    description="Lista todos os jobs de processamento"
)
async def list_jobs():
    """
    Lista todos os jobs criados

    Retorna informações básicas de cada job
    """
    try:
        jobs = bulk_service.list_jobs()
        return {"jobs": jobs, "total": len(jobs)}

    except Exception as e:
        logger.error(f"Erro ao listar jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar jobs"
        )
