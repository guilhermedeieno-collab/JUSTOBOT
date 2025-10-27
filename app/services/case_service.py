"""
Serviço de negócio para consultas de processos
"""
from typing import Optional, Dict, Any
from loguru import logger

from app.tribunals.base import SearchResult, Case, SearchType
from app.tribunals.registry import TribunalRegistry


class CaseService:
    """
    Serviço para gerenciar consultas de processos

    Abstrai a lógica de negócio e orquestra chamadas aos tribunais
    """

    def __init__(self):
        self.registry = TribunalRegistry

    async def search(
        self,
        tribunal: str,
        search_type: SearchType,
        query: str,
        config: Optional[Dict[str, Any]] = None
    ) -> SearchResult:
        """
        Realiza busca em um tribunal específico

        Args:
            tribunal: Código do tribunal (ex: 'TJSP')
            search_type: Tipo de busca
            query: Termo de busca
            config: Configurações opcionais

        Returns:
            SearchResult com resultados

        Raises:
            ValueError: Se tribunal não estiver disponível
        """
        logger.info(f"Iniciando busca: tribunal={tribunal}, type={search_type}, query={query}")

        try:
            # Obtém cliente do tribunal
            tribunal_client = self.registry.get_tribunal(tribunal, config)

            # Executa busca
            result = await tribunal_client.search(query, search_type)

            logger.info(f"Busca concluída: {result.total_found} processos encontrados")

            return result

        except Exception as e:
            logger.error(f"Erro na busca: {e}")
            raise

    async def get_case_details(
        self,
        tribunal: str,
        case_number: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Optional[Case]:
        """
        Obtém detalhes de um processo específico

        Args:
            tribunal: Código do tribunal
            case_number: Número do processo
            config: Configurações opcionais

        Returns:
            Case com detalhes ou None
        """
        logger.info(f"Obtendo detalhes: tribunal={tribunal}, case={case_number}")

        try:
            tribunal_client = self.registry.get_tribunal(tribunal, config)
            case = await tribunal_client.get_case_details(case_number)

            if case:
                logger.info(f"Detalhes obtidos para processo {case_number}")
            else:
                logger.warning(f"Processo {case_number} não encontrado")

            return case

        except Exception as e:
            logger.error(f"Erro ao obter detalhes: {e}")
            raise

    def list_available_tribunals(self) -> list[str]:
        """
        Lista tribunais disponíveis

        Returns:
            Lista de códigos de tribunais
        """
        return self.registry.list_available()

    async def validate_tribunal(self, tribunal: str) -> bool:
        """
        Valida se tribunal está disponível e acessível

        Args:
            tribunal: Código do tribunal

        Returns:
            True se disponível
        """
        try:
            if not self.registry.is_available(tribunal):
                return False

            tribunal_client = self.registry.get_tribunal(tribunal)
            return await tribunal_client.validate_connection()

        except Exception as e:
            logger.error(f"Erro ao validar tribunal {tribunal}: {e}")
            return False
