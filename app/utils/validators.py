"""
Utilitários de validação
"""
import re
from typing import Optional


def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF brasileiro

    Args:
        cpf: CPF a ser validado (pode conter pontos e traço)

    Returns:
        True se válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)

    # Verifica tamanho
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcula primeiro dígito verificador
    sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit1 = (sum_digits * 10 % 11) % 10

    if int(cpf[9]) != digit1:
        return False

    # Calcula segundo dígito verificador
    sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit2 = (sum_digits * 10 % 11) % 10

    return int(cpf[10]) == digit2


def clean_cpf(cpf: str) -> str:
    """Remove formatação do CPF, mantendo apenas números"""
    return re.sub(r'\D', '', cpf)


def format_cpf(cpf: str) -> str:
    """Formata CPF no padrão XXX.XXX.XXX-XX"""
    cpf = clean_cpf(cpf)
    if len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def validate_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ brasileiro

    Args:
        cnpj: CNPJ a ser validado

    Returns:
        True se válido, False caso contrário
    """
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    # Primeiro dígito
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_digits = sum(int(cnpj[i]) * weights[i] for i in range(12))
    digit1 = (sum_digits % 11)
    digit1 = 0 if digit1 < 2 else 11 - digit1

    if int(cnpj[12]) != digit1:
        return False

    # Segundo dígito
    weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_digits = sum(int(cnpj[i]) * weights[i] for i in range(13))
    digit2 = (sum_digits % 11)
    digit2 = 0 if digit2 < 2 else 11 - digit2

    return int(cnpj[13]) == digit2


def clean_cnpj(cnpj: str) -> str:
    """Remove formatação do CNPJ"""
    return re.sub(r'\D', '', cnpj)


def validate_case_number(case_number: str, tribunal: Optional[str] = None) -> bool:
    """
    Valida número de processo judicial (padrão CNJ)
    Formato: NNNNNNN-DD.AAAA.J.TR.OOOO

    Args:
        case_number: Número do processo
        tribunal: Código do tribunal (opcional)

    Returns:
        True se válido
    """
    # Remove caracteres não numéricos para validação
    clean = re.sub(r'\D', '', case_number)

    # Deve ter 20 dígitos
    if len(clean) != 20:
        return False

    # Valida formato com regex
    pattern = r'^\d{7}-?\d{2}\.?\d{4}\.?\d\.?\d{2}\.?\d{4}$'
    if not re.match(pattern, case_number):
        return False

    return True


def clean_case_number(case_number: str) -> str:
    """Remove formatação do número do processo"""
    return re.sub(r'\D', '', case_number)


def format_case_number(case_number: str) -> str:
    """
    Formata número do processo no padrão CNJ
    NNNNNNN-DD.AAAA.J.TR.OOOO
    """
    clean = clean_case_number(case_number)
    if len(clean) != 20:
        return case_number

    return (
        f"{clean[0:7]}-{clean[7:9]}.{clean[9:13]}."
        f"{clean[13]}.{clean[14:16]}.{clean[16:20]}"
    )
