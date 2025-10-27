"""
Parser para extrair dados das páginas HTML do TJSP
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup
from loguru import logger

from app.tribunals.base import Case, Party, Movement, CaseStatus


class TJSPParser:
    """Parser para processar HTML do TJSP"""

    async def parse_search_results(self, html: str, tribunal: str) -> List[Case]:
        """
        Extrai lista de processos de uma página de resultados

        Args:
            html: HTML da página de resultados
            tribunal: Código do tribunal

        Returns:
            Lista de objetos Case
        """
        soup = BeautifulSoup(html, 'html.parser')
        cases = []

        try:
            # Procura tabela de resultados (a estrutura pode variar)
            # Esta é uma implementação simplificada que deve ser ajustada
            # de acordo com a estrutura real das páginas do TJSP

            result_rows = soup.find_all('tr', class_='fundocinza1')

            for row in result_rows:
                try:
                    case = self._parse_result_row(row, tribunal)
                    if case:
                        cases.append(case)
                except Exception as e:
                    logger.warning(f"Erro ao processar linha de resultado: {e}")
                    continue

            # Fallback: busca por divs com informações de processo
            if not cases:
                process_divs = soup.find_all('div', class_=['processoLinha', 'numeroProcesso'])
                for div in process_divs:
                    try:
                        case = self._parse_result_div(div, tribunal)
                        if case:
                            cases.append(case)
                    except Exception as e:
                        logger.warning(f"Erro ao processar div de resultado: {e}")
                        continue

        except Exception as e:
            logger.error(f"Erro ao fazer parse dos resultados: {e}")

        return cases

    def _parse_result_row(self, row, tribunal: str) -> Optional[Case]:
        """Extrai dados de uma linha de resultado"""
        try:
            # Busca número do processo
            number_td = row.find('td', class_='numeroProcesso') or row.find('a', href=True)
            if not number_td:
                return None

            case_number = number_td.get_text(strip=True)

            # Busca outras informações disponíveis
            cells = row.find_all('td')

            # Estrutura simplificada
            return Case(
                case_number=case_number,
                tribunal=tribunal,
                status=CaseStatus.ATIVO,
                raw_data={"source": "search_result"}
            )

        except Exception as e:
            logger.error(f"Erro ao processar linha: {e}")
            return None

    def _parse_result_div(self, div, tribunal: str) -> Optional[Case]:
        """Extrai dados de uma div de resultado"""
        try:
            case_number = div.get_text(strip=True)

            return Case(
                case_number=case_number,
                tribunal=tribunal,
                status=CaseStatus.ATIVO,
                raw_data={"source": "search_result"}
            )

        except Exception as e:
            logger.error(f"Erro ao processar div: {e}")
            return None

    async def parse_case_details(self, html: str, case_number: str, tribunal: str) -> Optional[Case]:
        """
        Extrai detalhes completos de um processo

        Args:
            html: HTML da página de detalhes
            case_number: Número do processo
            tribunal: Código do tribunal

        Returns:
            Objeto Case completo
        """
        soup = BeautifulSoup(html, 'html.parser')

        try:
            # Extrai informações básicas
            case_data = {
                "case_number": case_number,
                "tribunal": tribunal,
                "status": CaseStatus.ATIVO
            }

            # Busca área/classe
            area_div = soup.find('div', id='classeProcesso')
            if area_div:
                case_data["subject"] = area_div.get_text(strip=True)

            # Busca comarca/foro
            comarca_div = soup.find('div', id='foroProcesso')
            if comarca_div:
                case_data["court"] = comarca_div.get_text(strip=True)

            # Busca data de distribuição
            distrib_div = soup.find('div', id='dataHoraDistribuicaoProcesso')
            if distrib_div:
                date_str = distrib_div.get_text(strip=True)
                case_data["start_date"] = self._parse_date(date_str)

            # Extrai partes do processo
            parties = self._extract_parties(soup)
            case_data["parties"] = parties

            # Extrai movimentações
            movements = self._extract_movements(soup)
            case_data["movements"] = movements

            # Armazena HTML original
            case_data["raw_data"] = {"html_length": len(html)}

            return Case(**case_data)

        except Exception as e:
            logger.error(f"Erro ao fazer parse dos detalhes do processo: {e}")
            return None

    def _extract_parties(self, soup: BeautifulSoup) -> List[Party]:
        """Extrai informações das partes do processo"""
        parties = []

        try:
            # Busca tabela de partes
            party_table = soup.find('table', id='tablePartesPrincipais') or soup.find('table', class_='secaoFormBody')

            if party_table:
                rows = party_table.find_all('tr')

                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        role = cells[0].get_text(strip=True).replace(':', '')
                        name = cells[1].get_text(strip=True)

                        if name:
                            parties.append(Party(
                                name=name,
                                role=role
                            ))

        except Exception as e:
            logger.warning(f"Erro ao extrair partes: {e}")

        return parties

    def _extract_movements(self, soup: BeautifulSoup) -> List[Movement]:
        """Extrai movimentações do processo"""
        movements = []

        try:
            # Busca tabela de movimentações
            mov_table = soup.find('table', id='tabelaTodasMovimentacoes') or soup.find('tbody', id='tabelaUltimasMovimentacoes')

            if mov_table:
                rows = mov_table.find_all('tr', class_='movimentacaoLinha')

                for row in rows:
                    date_cell = row.find('td', class_='dataMovimentacao')
                    desc_cell = row.find('td', class_='descricaoMovimentacao')

                    if date_cell and desc_cell:
                        date_str = date_cell.get_text(strip=True)
                        description = desc_cell.get_text(strip=True)

                        movement_date = self._parse_date(date_str)

                        if movement_date:
                            movements.append(Movement(
                                date=movement_date,
                                description=description
                            ))

        except Exception as e:
            logger.warning(f"Erro ao extrair movimentações: {e}")

        return movements

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Converte string de data para datetime

        Args:
            date_str: String com data (ex: "15/01/2024")

        Returns:
            Objeto datetime ou None
        """
        try:
            # Remove horários e informações extras
            date_str = date_str.split()[0]

            # Tenta diferentes formatos
            for fmt in ["%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"]:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue

            return None

        except Exception as e:
            logger.warning(f"Erro ao fazer parse de data '{date_str}': {e}")
            return None
