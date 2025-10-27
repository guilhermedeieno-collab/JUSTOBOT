"""
Cliente para interação com as APIs do TJSP
"""
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import httpx
from loguru import logger

from app.core.config import settings
from app.tribunals.base import BaseTribunal, SearchResult, Case, SearchType, Party, Movement, CaseStatus
from app.tribunals.registry import TribunalRegistry
from app.utils.validators import validate_cpf, clean_cpf, validate_case_number, format_case_number
from app.tribunals.tjsp.parser import TJSPParser


@TribunalRegistry.register("TJSP")
class TJSPClient(BaseTribunal):
    """
    Cliente para consultas no TJSP (Tribunal de Justiça de São Paulo)

    Utiliza web scraping das páginas públicas do ESAJ
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.base_url = config.get("base_url", settings.TJSP_BASE_URL) if config else settings.TJSP_BASE_URL
        self.timeout = config.get("timeout", settings.TJSP_TIMEOUT) if config else settings.TJSP_TIMEOUT
        self.max_retries = config.get("max_retries", settings.TJSP_MAX_RETRIES) if config else settings.TJSP_MAX_RETRIES
        self.rate_limit = config.get("rate_limit", settings.TJSP_RATE_LIMIT) if config else settings.TJSP_RATE_LIMIT

        self.parser = TJSPParser()
        self._last_request_time = 0.0
        self._semaphore = asyncio.Semaphore(self.rate_limit)

    def _get_tribunal_code(self) -> str:
        return "TJSP"

    async def _rate_limited_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Faz requisição HTTP com rate limiting e retry

        Args:
            method: Método HTTP (GET, POST, etc)
            url: URL da requisição
            **kwargs: Argumentos adicionais para httpx

        Returns:
            Response da requisição
        """
        async with self._semaphore:
            # Rate limiting simples
            current_time = asyncio.get_event_loop().time()
            time_since_last = current_time - self._last_request_time
            if time_since_last < 1.0 / self.rate_limit:
                await asyncio.sleep(1.0 / self.rate_limit - time_since_last)

            # Retry logic
            last_exception = None
            for attempt in range(self.max_retries):
                try:
                    async with httpx.AsyncClient(timeout=self.timeout) as client:
                        response = await client.request(method, url, **kwargs)
                        self._last_request_time = asyncio.get_event_loop().time()

                        if response.status_code == 200:
                            return response
                        elif response.status_code == 429:
                            # Too many requests
                            wait_time = 2 ** attempt
                            logger.warning(f"Rate limit hit, waiting {wait_time}s")
                            await asyncio.sleep(wait_time)
                        else:
                            response.raise_for_status()

                except httpx.HTTPError as e:
                    last_exception = e
                    if attempt < self.max_retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}), retrying in {wait_time}s: {e}")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"Request failed after {self.max_retries} attempts: {e}")

            raise last_exception or Exception("Request failed")

    async def search_by_cpf(self, cpf: str) -> SearchResult:
        """
        Busca processos por CPF no TJSP

        Args:
            cpf: CPF a ser pesquisado

        Returns:
            SearchResult com processos encontrados
        """
        cpf_clean = clean_cpf(cpf)

        if not validate_cpf(cpf_clean):
            logger.warning(f"CPF inválido: {cpf}")
            return SearchResult(
                query=cpf,
                search_type=SearchType.CPF,
                tribunal=self.tribunal_code,
                cases=[],
                total_found=0
            )

        logger.info(f"Buscando processos por CPF: {cpf_clean}")

        try:
            # URL de consulta de participantes do TJSP
            url = f"{self.base_url}/cpopg/search.do"

            # Parâmetros de busca
            params = {
                "conversationId": "",
                "dadosConsulta.localPesquisa.cdLocal": "-1",
                "cbPesquisa": "DOCPARTE",
                "dadosConsulta.tipoNuProcesso": "UNIFICADO",
                "dadosConsulta.valorConsulta": cpf_clean,
                "uuidCaptcha": ""
            }

            response = await self._rate_limited_request("GET", url, params=params)

            # Parse do HTML
            cases = await self.parser.parse_search_results(response.text, self.tribunal_code)

            logger.info(f"Encontrados {len(cases)} processos para CPF {cpf_clean}")

            return SearchResult(
                query=cpf,
                search_type=SearchType.CPF,
                tribunal=self.tribunal_code,
                cases=cases,
                total_found=len(cases)
            )

        except Exception as e:
            logger.error(f"Erro ao buscar por CPF {cpf}: {e}")
            return SearchResult(
                query=cpf,
                search_type=SearchType.CPF,
                tribunal=self.tribunal_code,
                cases=[],
                total_found=0
            )

    async def search_by_name(self, name: str) -> SearchResult:
        """
        Busca processos por nome no TJSP

        Args:
            name: Nome a ser pesquisado

        Returns:
            SearchResult com processos encontrados
        """
        logger.info(f"Buscando processos por nome: {name}")

        try:
            url = f"{self.base_url}/cpopg/search.do"

            params = {
                "conversationId": "",
                "dadosConsulta.localPesquisa.cdLocal": "-1",
                "cbPesquisa": "NMPARTE",
                "dadosConsulta.tipoNuProcesso": "UNIFICADO",
                "dadosConsulta.valorConsulta": name,
                "uuidCaptcha": ""
            }

            response = await self._rate_limited_request("GET", url, params=params)
            cases = await self.parser.parse_search_results(response.text, self.tribunal_code)

            logger.info(f"Encontrados {len(cases)} processos para nome '{name}'")

            return SearchResult(
                query=name,
                search_type=SearchType.NAME,
                tribunal=self.tribunal_code,
                cases=cases,
                total_found=len(cases)
            )

        except Exception as e:
            logger.error(f"Erro ao buscar por nome {name}: {e}")
            return SearchResult(
                query=name,
                search_type=SearchType.NAME,
                tribunal=self.tribunal_code,
                cases=[],
                total_found=0
            )

    async def search_by_case_number(self, case_number: str) -> SearchResult:
        """
        Busca processo específico por número no TJSP

        Args:
            case_number: Número do processo

        Returns:
            SearchResult com o processo encontrado
        """
        logger.info(f"Buscando processo: {case_number}")

        if not validate_case_number(case_number):
            logger.warning(f"Número de processo inválido: {case_number}")
            return SearchResult(
                query=case_number,
                search_type=SearchType.CASE_NUMBER,
                tribunal=self.tribunal_code,
                cases=[],
                total_found=0
            )

        try:
            case = await self.get_case_details(case_number)

            cases = [case] if case else []

            return SearchResult(
                query=case_number,
                search_type=SearchType.CASE_NUMBER,
                tribunal=self.tribunal_code,
                cases=cases,
                total_found=len(cases)
            )

        except Exception as e:
            logger.error(f"Erro ao buscar processo {case_number}: {e}")
            return SearchResult(
                query=case_number,
                search_type=SearchType.CASE_NUMBER,
                tribunal=self.tribunal_code,
                cases=[],
                total_found=0
            )

    async def get_case_details(self, case_number: str) -> Optional[Case]:
        """
        Obtém detalhes completos de um processo

        Args:
            case_number: Número do processo

        Returns:
            Case com todos os detalhes ou None
        """
        logger.info(f"Obtendo detalhes do processo: {case_number}")

        try:
            # Remove formatação
            case_clean = case_number.replace(".", "").replace("-", "")

            url = f"{self.base_url}/cpopg/show.do"

            params = {
                "processo.codigo": case_clean,
                "processo.foro": "1",
                "conversationId": ""
            }

            response = await self._rate_limited_request("GET", url, params=params)

            # Parse detalhado
            case = await self.parser.parse_case_details(response.text, case_number, self.tribunal_code)

            return case

        except Exception as e:
            logger.error(f"Erro ao obter detalhes do processo {case_number}: {e}")
            return None

    async def validate_connection(self) -> bool:
        """
        Valida conexão com o TJSP

        Returns:
            True se conectado
        """
        try:
            response = await self._rate_limited_request("GET", self.base_url)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Erro ao validar conexão com TJSP: {e}")
            return False
