"""
Testes para validadores
"""
import pytest
from app.utils.validators import (
    validate_cpf,
    clean_cpf,
    format_cpf,
    validate_cnpj,
    validate_case_number,
    format_case_number
)


class TestCPFValidation:
    """Testes de validação de CPF"""

    def test_valid_cpf(self):
        """Testa CPF válido"""
        # CPF válido conhecido
        assert validate_cpf("11144477735") is True

    def test_valid_cpf_with_formatting(self):
        """Testa CPF válido com formatação"""
        assert validate_cpf("111.444.777-35") is True

    def test_invalid_cpf_all_same_digits(self):
        """Testa CPF inválido (todos dígitos iguais)"""
        assert validate_cpf("11111111111") is False

    def test_invalid_cpf_wrong_length(self):
        """Testa CPF com tamanho incorreto"""
        assert validate_cpf("123456789") is False

    def test_clean_cpf(self):
        """Testa limpeza de formatação"""
        assert clean_cpf("111.444.777-35") == "11144477735"

    def test_format_cpf(self):
        """Testa formatação de CPF"""
        assert format_cpf("11144477735") == "111.444.777-35"


class TestCNPJValidation:
    """Testes de validação de CNPJ"""

    def test_valid_cnpj(self):
        """Testa CNPJ válido"""
        assert validate_cnpj("11222333000181") is True

    def test_invalid_cnpj_all_same_digits(self):
        """Testa CNPJ inválido"""
        assert validate_cnpj("11111111111111") is False


class TestCaseNumberValidation:
    """Testes de validação de número de processo"""

    def test_valid_case_number(self):
        """Testa número de processo válido"""
        assert validate_case_number("1000001-01.2024.8.26.0100") is True

    def test_valid_case_number_no_formatting(self):
        """Testa número sem formatação"""
        assert validate_case_number("10000010120248260100") is True

    def test_invalid_case_number_wrong_length(self):
        """Testa número com tamanho incorreto"""
        assert validate_case_number("123456") is False

    def test_format_case_number(self):
        """Testa formatação de número"""
        result = format_case_number("10000010120248260100")
        assert result == "1000001-01.2024.8.26.0100"
