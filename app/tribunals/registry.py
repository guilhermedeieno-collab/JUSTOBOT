"""
Registry Pattern para gerenciar tribunais disponíveis
"""
from typing import Dict, Type, Optional
from app.tribunals.base import BaseTribunal
from loguru import logger


class TribunalRegistry:
    """
    Registro centralizado de todos os tribunais disponíveis.

    Implementa o padrão Registry para gerenciar instâncias de tribunais.
    """

    _tribunals: Dict[str, Type[BaseTribunal]] = {}
    _instances: Dict[str, BaseTribunal] = {}

    @classmethod
    def register(cls, tribunal_code: str):
        """
        Decorator para registrar um novo tribunal

        Uso:
            @TribunalRegistry.register("TJSP")
            class TJSPClient(BaseTribunal):
                ...
        """
        def wrapper(tribunal_class: Type[BaseTribunal]):
            cls._tribunals[tribunal_code.upper()] = tribunal_class
            logger.info(f"Tribunal registrado: {tribunal_code.upper()}")
            return tribunal_class
        return wrapper

    @classmethod
    def get_tribunal(cls, tribunal_code: str, config: Optional[dict] = None) -> BaseTribunal:
        """
        Obtém instância de um tribunal

        Args:
            tribunal_code: Código do tribunal (ex: 'TJSP')
            config: Configurações opcionais

        Returns:
            Instância do tribunal

        Raises:
            ValueError: Se o tribunal não estiver registrado
        """
        tribunal_code = tribunal_code.upper()

        # Retorna instância em cache se existir e não houver config personalizada
        if config is None and tribunal_code in cls._instances:
            return cls._instances[tribunal_code]

        if tribunal_code not in cls._tribunals:
            available = ", ".join(cls._tribunals.keys())
            raise ValueError(
                f"Tribunal '{tribunal_code}' não encontrado. "
                f"Tribunais disponíveis: {available}"
            )

        # Cria nova instância
        tribunal_class = cls._tribunals[tribunal_code]
        instance = tribunal_class(config=config)

        # Armazena em cache se não houver config personalizada
        if config is None:
            cls._instances[tribunal_code] = instance

        return instance

    @classmethod
    def list_available(cls) -> list[str]:
        """Lista todos os tribunais disponíveis"""
        return list(cls._tribunals.keys())

    @classmethod
    def is_available(cls, tribunal_code: str) -> bool:
        """Verifica se um tribunal está disponível"""
        return tribunal_code.upper() in cls._tribunals

    @classmethod
    def clear_cache(cls):
        """Limpa cache de instâncias"""
        cls._instances.clear()
        logger.info("Cache de tribunais limpo")
