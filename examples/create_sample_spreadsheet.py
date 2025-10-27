"""
Script para criar planilhas de exemplo
"""
import pandas as pd


def create_cpf_spreadsheet():
    """Cria planilha de exemplo com CPFs"""
    data = {
        'cpf': [
            '12345678900',
            '98765432100',
            '11122233344',
            '55566677788',
            '99988877766'
        ]
    }

    df = pd.DataFrame(data)
    df.to_excel('exemplo_cpf.xlsx', index=False)
    print("✓ Criada: exemplo_cpf.xlsx")


def create_name_spreadsheet():
    """Cria planilha de exemplo com nomes"""
    data = {
        'nome': [
            'João da Silva',
            'Maria Santos',
            'Pedro Oliveira',
            'Ana Costa',
            'Carlos Souza'
        ]
    }

    df = pd.DataFrame(data)
    df.to_excel('exemplo_nomes.xlsx', index=False)
    print("✓ Criada: exemplo_nomes.xlsx")


def create_case_number_spreadsheet():
    """Cria planilha de exemplo com números de processo"""
    data = {
        'processo': [
            '1000001-01.2024.8.26.0100',
            '1000002-02.2024.8.26.0200',
            '1000003-03.2024.8.26.0300',
            '1000004-04.2024.8.26.0400',
            '1000005-05.2024.8.26.0500'
        ]
    }

    df = pd.DataFrame(data)
    df.to_excel('exemplo_processos.xlsx', index=False)
    print("✓ Criada: exemplo_processos.xlsx")


def create_mixed_spreadsheet():
    """Cria planilha com múltiplas colunas"""
    data = {
        'cpf': ['12345678900', '98765432100', '11122233344'],
        'nome': ['João da Silva', 'Maria Santos', 'Pedro Oliveira'],
        'observacao': ['Cliente 1', 'Cliente 2', 'Cliente 3']
    }

    df = pd.DataFrame(data)
    df.to_excel('exemplo_completo.xlsx', index=False)
    print("✓ Criada: exemplo_completo.xlsx")


def create_csv_example():
    """Cria exemplo em CSV"""
    data = {
        'cpf': ['12345678900', '98765432100', '11122233344']
    }

    df = pd.DataFrame(data)
    df.to_csv('exemplo_cpf.csv', index=False)
    print("✓ Criada: exemplo_cpf.csv")


if __name__ == "__main__":
    print("Criando planilhas de exemplo...\n")

    create_cpf_spreadsheet()
    create_name_spreadsheet()
    create_case_number_spreadsheet()
    create_mixed_spreadsheet()
    create_csv_example()

    print("\nPlanilhas criadas com sucesso!")
    print("\nUso:")
    print("  1. Acesse http://localhost:8000/docs")
    print("  2. Vá em POST /api/v1/bulk/upload")
    print("  3. Faça upload de uma das planilhas")
    print("  4. Selecione o tribunal (TJSP) e tipo de busca")
    print("  5. Acompanhe o progresso via /api/v1/bulk/status/{job_id}")
