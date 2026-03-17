#!/usr/bin/env python3
"""
Teste de conexão com proxy PUCRS.

Verifica se as credenciais funcionam e se é possível
baixar PDFs de bases acadêmicas.
"""

import asyncio
import aiohttp
from pathlib import Path
import sys

# Credenciais PUCRS
PUCRS_EMAIL = "c.jones@edu.pucrs.br"
PUCRS_PASSWORD = "@CiaoMiau2955"

# Proxy
PUCRS_PROXY = "http://prx.pucrs.br:3128"


async def test_basic_connectivity():
    """Testa conectividade básica."""
    print("=== Teste de Conectividade ===\n")
    
    # Teste sem proxy
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://httpbin.org/ip", timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"✅ Conexão direta funciona")
                    print(f"   IP público: {data.get('origin', '?')}\n")
                else:
                    print(f"⚠️ Status {resp.status} na conexão direta\n")
        except Exception as e:
            print(f"❌ Erro na conexão direta: {e}\n")


async def test_proxy_auth():
    """Testa autenticação no proxy."""
    print("=== Teste de Autenticação Proxy ===\n")
    
    proxy_auth = aiohttp.BasicAuth(PUCRS_EMAIL, PUCRS_PASSWORD)
    
    connector = aiohttp.TCPConnector(ssl=False)
    
    async with aiohttp.ClientSession(
        proxy=PUCRS_PROXY,
        proxy_auth=proxy_auth,
        connector=connector,
        timeout=aiohttp.ClientTimeout(total=30),
        headers={"User-Agent": "Mozilla/5.0"}
    ) as session:
        
        # Tenta acessar uma base acadêmica via proxy
        test_urls = [
            ("IEEE Xplore", "https://ieeexplore.ieee.org"),
            ("Springer", "https://link.springer.com"),
            ("JSTOR", "https://www.jstor.org"),
        ]
        
        for name, url in test_urls:
            print(f"Testando {name}...")
            try:
                async with session.get(url) as resp:
                    print(f"   Status: {resp.status}")
                    if resp.status == 200:
                        content = await resp.text()
                        print(f"   ✅ Sucesso! {len(content):,} bytes recebidos")
                    elif resp.status in [401, 403]:
                        print(f"   ❌ Falha na autenticação")
                    elif resp.status == 407:
                        print(f"   ❌ Proxy requer autenticação")
                    else:
                        print(f"   ⚠️ Status inesperado")
            except aiohttp.ClientError as e:
                print(f"   ❌ Erro: {e}")
            except Exception as e:
                print(f"   ❌ Erro inesperado: {e}")
            print()


async def test_pdf_download():
    """Tenta baixar um PDF público via proxy."""
    print("=== Teste de Download de PDF ===\n")
    
    proxy_auth = aiohttp.BasicAuth(PUCRS_EMAIL, PUCRS_PASSWORD)
    
    # PDF público de teste
    test_pdf = "https://arxiv.org/pdf/2301.00001.pdf"  # Paper público
    
    print(f"Tentando baixar: {test_pdf}")
    print("⚠️ Nota: arXiv é público, não requer proxy\n")
    
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=60)
    ) as session:
        try:
            async with session.get(test_pdf) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    print(f"✅ Download OK: {len(content):,} bytes")
                    
                    # Salva teste
                    output_path = Path("/tmp/test_pdf.pdf")
                    with open(output_path, "wb") as f:
                        f.write(content)
                    print(f"   Salvo em: {output_path}")
                else:
                    print(f"❌ Status: {resp.status}")
        except Exception as e:
            print(f"❌ Erro: {e}")


async def test_springer_article():
    """Testa acessar artigo do Springer via proxy."""
    print("\n=== Teste de Acesso Springer ===\n")
    
    proxy_auth = aiohttp.BasicAuth(PUCRS_EMAIL, PUCRS_PASSWORD)
    
    # Artigo de teste (pode não estar disponível)
    test_url = "https://link.springer.com/article/10.1007/s00354-020-00115-5"
    
    print(f"Tentando acessar: {test_url}\n")
    
    async with aiohttp.ClientSession(
        proxy=PUCRS_PROXY,
        proxy_auth=proxy_auth,
        timeout=aiohttp.ClientTimeout(total=30),
        headers={"User-Agent": "Mozilla/5.0"}
    ) as session:
        try:
            async with session.get(test_url) as resp:
                print(f"Status: {resp.status}")
                if resp.status == 200:
                    html = await resp.text()
                    print(f"✅ Página carregada: {len(html):,} bytes")
                    
                    # Verifica se há link para PDF
                    if ".pdf" in html.lower():
                        print("   📄 Link para PDF encontrado")
                    else:
                        print("   ⚠️ Nenhum link para PDF visível")
                        
                elif resp.status == 401:
                    print("❌ Autenticação necessária")
                elif resp.status == 403:
                    print("❌ Acesso negado")
                elif resp.status == 407:
                    print("❌ Proxy requer autenticação")
                else:
                    print(f"⚠️ Status: {resp.status}")
                    
        except aiohttp.ClientError as e:
            print(f"❌ Erro: {e}")


async def main():
    print("=" * 60)
    print("PUCRS Proxy Test")
    print("=" * 60)
    print()
    print(f"Proxy: {PUCRS_PROXY}")
    print(f"Email: {PUCRS_EMAIL}")
    print(f"Senha: {'*' * len(PUCRS_PASSWORD)}")
    print()
    
    await test_basic_connectivity()
    await test_proxy_auth()
    await test_pdf_download()
    await test_springer_article()
    
    print("\n" + "=" * 60)
    print("Testes concluídos!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())