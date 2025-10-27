"""
Serviço para processamento em lote de consultas
"""
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import uuid
import pandas as pd
from io import BytesIO
from loguru import logger

from app.core.config import settings
from app.tribunals.base import SearchType, SearchResult
from app.services.case_service import CaseService


class JobStatus(str, Enum):
    """Status de um job de processamento"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class BulkJob:
    """Representa um job de processamento em lote"""

    def __init__(self, job_id: str, tribunal: str, total_items: int):
        self.job_id = job_id
        self.tribunal = tribunal
        self.total_items = total_items
        self.processed_items = 0
        self.successful_items = 0
        self.failed_items = 0
        self.status = JobStatus.PENDING
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.results: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []

    def to_dict(self) -> Dict[str, Any]:
        """Converte job para dicionário"""
        return {
            "job_id": self.job_id,
            "tribunal": self.tribunal,
            "status": self.status,
            "total_items": self.total_items,
            "processed_items": self.processed_items,
            "successful_items": self.successful_items,
            "failed_items": self.failed_items,
            "progress_percentage": (self.processed_items / self.total_items * 100) if self.total_items > 0 else 0,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class BulkService:
    """
    Serviço para processamento em lote de consultas

    Permite upload de planilhas e processa múltiplas consultas de forma eficiente
    """

    def __init__(self):
        self.case_service = CaseService()
        self.jobs: Dict[str, BulkJob] = {}
        self.max_concurrent = settings.BULK_MAX_CONCURRENT_REQUESTS
        self.batch_size = settings.BULK_BATCH_SIZE

    async def create_job_from_file(
        self,
        file_content: bytes,
        filename: str,
        tribunal: str,
        search_type: SearchType
    ) -> BulkJob:
        """
        Cria um job de processamento a partir de arquivo

        Args:
            file_content: Conteúdo do arquivo
            filename: Nome do arquivo
            tribunal: Tribunal para busca
            search_type: Tipo de busca

        Returns:
            BulkJob criado

        Raises:
            ValueError: Se arquivo inválido
        """
        logger.info(f"Criando job a partir de arquivo: {filename}")

        # Lê arquivo
        df = await self._read_file(file_content, filename)

        if df.empty:
            raise ValueError("Arquivo vazio ou inválido")

        # Cria job
        job_id = str(uuid.uuid4())
        job = BulkJob(
            job_id=job_id,
            tribunal=tribunal,
            total_items=len(df)
        )

        self.jobs[job_id] = job

        # Inicia processamento em background
        asyncio.create_task(self._process_job(job, df, search_type))

        logger.info(f"Job {job_id} criado com {len(df)} itens")

        return job

    async def _read_file(self, content: bytes, filename: str) -> pd.DataFrame:
        """
        Lê arquivo Excel ou CSV

        Args:
            content: Conteúdo do arquivo
            filename: Nome do arquivo

        Returns:
            DataFrame com dados

        Raises:
            ValueError: Se formato não suportado
        """
        try:
            file_obj = BytesIO(content)

            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(file_obj)
            elif filename.endswith('.csv'):
                df = pd.read_csv(file_obj)
            else:
                raise ValueError(f"Formato não suportado: {filename}")

            logger.info(f"Arquivo lido: {len(df)} linhas, {len(df.columns)} colunas")

            return df

        except Exception as e:
            logger.error(f"Erro ao ler arquivo: {e}")
            raise ValueError(f"Erro ao processar arquivo: {e}")

    async def _process_job(
        self,
        job: BulkJob,
        df: pd.DataFrame,
        search_type: SearchType
    ):
        """
        Processa job em background

        Args:
            job: Job a ser processado
            df: DataFrame com dados
            search_type: Tipo de busca
        """
        job.status = JobStatus.PROCESSING
        job.started_at = datetime.now()

        logger.info(f"Iniciando processamento do job {job.job_id}")

        try:
            # Identifica coluna de busca (primeira coluna ou coluna específica)
            search_column = self._identify_search_column(df, search_type)

            if search_column not in df.columns:
                raise ValueError(f"Coluna '{search_column}' não encontrada")

            # Processa em lotes
            queries = df[search_column].dropna().astype(str).tolist()

            # Divide em batches
            batches = [
                queries[i:i + self.batch_size]
                for i in range(0, len(queries), self.batch_size)
            ]

            for batch in batches:
                await self._process_batch(job, batch, search_type)

            # Finaliza job
            job.completed_at = datetime.now()

            if job.failed_items == 0:
                job.status = JobStatus.COMPLETED
            elif job.successful_items > 0:
                job.status = JobStatus.PARTIAL
            else:
                job.status = JobStatus.FAILED

            logger.info(
                f"Job {job.job_id} finalizado: "
                f"{job.successful_items} sucesso, "
                f"{job.failed_items} falhas"
            )

        except Exception as e:
            logger.error(f"Erro ao processar job {job.job_id}: {e}")
            job.status = JobStatus.FAILED
            job.completed_at = datetime.now()

    def _identify_search_column(self, df: pd.DataFrame, search_type: SearchType) -> str:
        """
        Identifica coluna de busca baseada no tipo

        Args:
            df: DataFrame
            search_type: Tipo de busca

        Returns:
            Nome da coluna
        """
        # Mapeamento de nomes comuns
        column_mapping = {
            SearchType.CPF: ['cpf', 'documento', 'doc', 'CPF'],
            SearchType.NAME: ['nome', 'name', 'parte', 'NOME'],
            SearchType.CASE_NUMBER: ['processo', 'numero', 'number', 'case', 'PROCESSO'],
            SearchType.CNPJ: ['cnpj', 'CNPJ']
        }

        # Procura por coluna correspondente
        possible_names = column_mapping.get(search_type, [])

        for col in df.columns:
            if col in possible_names or col.lower() in [name.lower() for name in possible_names]:
                return col

        # Retorna primeira coluna como fallback
        return df.columns[0]

    async def _process_batch(
        self,
        job: BulkJob,
        queries: List[str],
        search_type: SearchType
    ):
        """
        Processa um lote de consultas concorrentemente

        Args:
            job: Job sendo processado
            queries: Lista de queries
            search_type: Tipo de busca
        """
        # Limita concorrência
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def process_single(query: str):
            async with semaphore:
                try:
                    result = await self.case_service.search(
                        tribunal=job.tribunal,
                        search_type=search_type,
                        query=query
                    )

                    job.processed_items += 1
                    job.successful_items += 1

                    # Armazena resultado
                    job.results.append({
                        "query": query,
                        "cases_found": result.total_found,
                        "cases": [case.dict() for case in result.cases]
                    })

                except Exception as e:
                    logger.error(f"Erro ao processar query '{query}': {e}")
                    job.processed_items += 1
                    job.failed_items += 1

                    job.errors.append({
                        "query": query,
                        "error": str(e)
                    })

        # Executa todas as queries do batch
        await asyncio.gather(*[process_single(q) for q in queries])

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém status de um job

        Args:
            job_id: ID do job

        Returns:
            Dicionário com status ou None
        """
        job = self.jobs.get(job_id)
        return job.to_dict() if job else None

    async def get_job_results(self, job_id: str) -> Optional[bytes]:
        """
        Gera arquivo Excel com resultados do job

        Args:
            job_id: ID do job

        Returns:
            Bytes do arquivo Excel ou None
        """
        job = self.jobs.get(job_id)

        if not job or job.status not in [JobStatus.COMPLETED, JobStatus.PARTIAL]:
            return None

        try:
            # Cria DataFrame com resultados
            results_data = []

            for result in job.results:
                for case in result.get("cases", []):
                    results_data.append({
                        "Query": result["query"],
                        "Número do Processo": case.get("case_number"),
                        "Status": case.get("status"),
                        "Tribunal": case.get("tribunal"),
                        "Comarca": case.get("court"),
                        "Assunto": case.get("subject"),
                    })

            df_results = pd.DataFrame(results_data)

            # Adiciona erros em sheet separado
            df_errors = pd.DataFrame(job.errors)

            # Gera Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_results.to_excel(writer, sheet_name='Resultados', index=False)
                if not df_errors.empty:
                    df_errors.to_excel(writer, sheet_name='Erros', index=False)

            output.seek(0)
            return output.getvalue()

        except Exception as e:
            logger.error(f"Erro ao gerar resultados: {e}")
            return None

    def list_jobs(self) -> List[Dict[str, Any]]:
        """Lista todos os jobs"""
        return [job.to_dict() for job in self.jobs.values()]
