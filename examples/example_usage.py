"""
Exemplo de uso da API JUSTOBOT
"""
import asyncio
import httpx
import time


BASE_URL = "http://localhost:8000/api/v1"


async def example_search_by_cpf():
    """Exemplo de busca por CPF"""
    print("\n=== Busca por CPF ===")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/cases/search",
            json={
                "tribunal": "TJSP",
                "search_type": "cpf",
                "query": "12345678900"
            }
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Encontrados: {result['total_found']} processos")
            for case in result['cases']:
                print(f"  - Processo: {case['case_number']}")
                print(f"    Status: {case['status']}")
                print(f"    Tribunal: {case['tribunal']}")
        else:
            print(f"Erro: {response.status_code}")
            print(response.text)


async def example_search_by_name():
    """Exemplo de busca por nome"""
    print("\n=== Busca por Nome ===")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/cases/search",
            json={
                "tribunal": "TJSP",
                "search_type": "name",
                "query": "João da Silva"
            }
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Encontrados: {result['total_found']} processos")
        else:
            print(f"Erro: {response.status_code}")


async def example_case_details():
    """Exemplo de busca de detalhes"""
    print("\n=== Detalhes do Processo ===")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/cases/details",
            json={
                "tribunal": "TJSP",
                "case_number": "1000001-01.2024.8.26.0100"
            }
        )

        if response.status_code == 200:
            case = response.json()
            print(f"Processo: {case['case_number']}")
            print(f"Status: {case['status']}")
            print(f"Comarca: {case.get('court', 'N/A')}")
            print(f"Partes: {len(case['parties'])}")
            print(f"Movimentações: {len(case['movements'])}")
        else:
            print(f"Erro: {response.status_code}")


async def example_bulk_upload():
    """Exemplo de upload em lote"""
    print("\n=== Upload em Lote ===")

    # Criar arquivo de exemplo
    import pandas as pd
    df = pd.DataFrame({
        'cpf': ['12345678900', '98765432100', '11122233344']
    })
    df.to_excel('/tmp/exemplo.xlsx', index=False)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Upload
        with open('/tmp/exemplo.xlsx', 'rb') as f:
            response = await client.post(
                f"{BASE_URL}/bulk/upload",
                files={"file": f},
                data={
                    "tribunal": "TJSP",
                    "search_type": "cpf"
                }
            )

        if response.status_code == 201:
            result = response.json()
            job_id = result['job_id']
            print(f"Job criado: {job_id}")
            print(f"Mensagem: {result['message']}")

            # Monitorar progresso
            while True:
                await asyncio.sleep(2)

                status_response = await client.get(
                    f"{BASE_URL}/bulk/status/{job_id}"
                )

                if status_response.status_code == 200:
                    status = status_response.json()
                    print(f"Progresso: {status['progress_percentage']:.1f}% "
                          f"({status['processed_items']}/{status['total_items']})")

                    if status['status'] in ['completed', 'partial', 'failed']:
                        print(f"\nStatus final: {status['status']}")
                        print(f"Sucesso: {status['successful_items']}")
                        print(f"Falhas: {status['failed_items']}")
                        break
                else:
                    print("Erro ao verificar status")
                    break

            # Download dos resultados
            if status['status'] in ['completed', 'partial']:
                download_response = await client.get(
                    f"{BASE_URL}/bulk/download/{job_id}"
                )

                if download_response.status_code == 200:
                    with open(f'/tmp/resultados_{job_id}.xlsx', 'wb') as f:
                        f.write(download_response.content)
                    print(f"\nResultados salvos em: /tmp/resultados_{job_id}.xlsx")
        else:
            print(f"Erro no upload: {response.status_code}")
            print(response.text)


async def example_list_tribunals():
    """Exemplo de listagem de tribunais"""
    print("\n=== Tribunais Disponíveis ===")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/cases/tribunals")

        if response.status_code == 200:
            result = response.json()
            print(f"Total: {len(result['tribunals'])} tribunais")
            for tribunal in result['tribunals']:
                status = "✓" if tribunal['available'] else "✗"
                print(f"  {status} {tribunal['code']}: {tribunal['name']}")
        else:
            print(f"Erro: {response.status_code}")


async def main():
    """Executa todos os exemplos"""
    print("JUSTOBOT - Exemplos de Uso")
    print("=" * 50)

    try:
        # Verificar se API está online
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✓ API está online\n")
            else:
                print("✗ API não está respondendo")
                return
    except Exception as e:
        print(f"✗ Erro ao conectar: {e}")
        print("\nCertifique-se de que a API está rodando:")
        print("  uvicorn app.main:app --reload")
        return

    # Executar exemplos
    await example_list_tribunals()
    await example_search_by_cpf()
    await example_search_by_name()
    await example_case_details()

    # Bulk (comentado por padrão pois é mais demorado)
    # await example_bulk_upload()

    print("\n" + "=" * 50)
    print("Exemplos concluídos!")


if __name__ == "__main__":
    asyncio.run(main())
