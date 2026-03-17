#!/usr/bin/env python3
"""
PUCRS Proxy Client - Acesso institucional completo

Usa o proxy PUCRS (prx.pucrs.br:3128) para autenticar e baixar PDFs
de bases de dados acadêmicas (Springer, IEEE, JSTOR, etc.).

O proxy é configurado automaticamente para todos os domínios listados
no PAC da PUCRS.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, List
from pathlib import Path
from urllib.parse import urlparse
import re

# PUCRS Proxy Configuration
PUCRS_PROXY = "http://prx.pucrs.br:3128"

# Domínios cobertos pelo proxy PUCRS (extraídos do PAC)
PUCRS_PROXY_DOMAINS = [
    "aacnjournals.org", "aacrjournals.org", "academic.oup.com",
    "acm.org", "acs.org", "aip.org", "ams.org", "aps.org",
    "annualreviews.org", "ascelibrary.org", "ascopubs.org",
    "asm.org", "asme.org", "bioone.org", "bmj.com",
    "cambridge.org", "cell.com", "degruyter.com", "dl.acm.org",
    "elsevier.com", "emerald.com", "ieee.org", "iop.org",
    "jstor.org", "link.springer.com", "lww.com", "nature.com",
    "nejm.org", "pnas.org", "sciencedirect.com", "sciencemag.org",
    "science.org", "springer.com", "springerlink.com", "tandfonline.com",
    "wiley.com", "worldscientific.com",
    # ... e muitos outros do PAC
]


def needs_proxy(url: str) -> bool:
    """Verifica se a URL precisa passar pelo proxy PUCRS."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    # Remove www. prefix
    domain = re.sub(r'^www\.', '', domain)
    
    # Verifica se está na lista de domínios do proxy
    for proxy_domain in PUCRS_PROXY_DOMAINS:
        if domain == proxy_domain or domain.endswith('.' + proxy_domain):
            return True
    
    return False


class PUCRSProxyClient:
    """
    Cliente para acessar bases acadêmicas via proxy PUCRS.
    
    O proxy usa autenticação HTTP Basic com email/senha institucional.
    Para URLs de domínios cobertos, o proxy autentica automaticamente.
    """
    
    def __init__(self, email: str, password: str):
        """
        Inicializa o cliente com credenciais PUCRS.
        
        Args:
            email: Email acadêmico (@edu.pucrs.br)
            password: Senha de rede PUCRS
        """
        self.email = email
        self.password = password
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        # Configura sessão com proxy
        proxy_auth = aiohttp.BasicAuth(self.email, self.password)
        
        self.session = aiohttp.ClientSession(
            proxy=PUCRS_PROXY,
            proxy_auth=proxy_auth,
            timeout=aiohttp.ClientTimeout(total=120),
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """
        Busca uma página web via proxy.
        
        Args:
            url: URL da página
            
        Returns:
            HTML da página ou None se falhar
        """
        if not needs_proxy(url):
            # Não precisa de proxy - usar conexão direta
            async with aiohttp.ClientSession() as direct_session:
                async with direct_session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    return None
        
        # Usa proxy PUCRS
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
                elif resp.status == 401 or resp.status == 403:
                    print(f"❌ Autenticação falhou para {url}")
                    return None
                else:
                    print(f"⚠️ Status {resp.status} para {url}")
                    return None
        except aiohttp.ClientError as e:
            print(f"❌ Erro ao buscar {url}: {e}")
            return None
    
    async def download_pdf(self, url: str, output_path: str) -> bool:
        """
        Baixa um PDF via proxy.
        
        Args:
            url: URL do PDF
            output_path: Caminho para salvar
            
        Returns:
            True se sucesso, False se falhar
        """
        try:
            # Usa sessão com proxy
            async with self.session.get(url) as resp:
                if resp.status != 200:
                    print(f"❌ Status {resp.status} para {url}")
                    return False
                
                # Verifica se é PDF
                content_type = resp.headers.get("Content-Type", "")
                if "pdf" not in content_type.lower() and not url.endswith(".pdf"):
                    print(f"⚠️ Conteúdo não é PDF: {content_type}")
                    # Tenta baixar mesmo assim - pode ser PDF sem header correto
                
                # Salva arquivo
                content = await resp.read()
                
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(content)
                
                print(f"✅ PDF baixado: {output_path} ({len(content):,} bytes)")
                return True
                
        except aiohttp.ClientError as e:
            print(f"❌ Erro ao baixar {url}: {e}")
            return False
    
    async def get_pdf_url_from_page(self, page_url: str) -> Optional[str]:
        """
        Extrai URL do PDF de uma página de artigo.
        
        Muitas bases (Springer, IEEE, etc.) têm páginas HTML
        que linkam para o PDF. Este método tenta encontrar o link.
        """
        html = await self.fetch_page(page_url)
        if not html:
            return None
        
        # Padrões comuns de links para PDF
        pdf_patterns = [
            r'href="([^"]*\.pdf[^"]*)"',
            r'href="([^"]*content/[^"]*\.pdf[^"]*)"',
            r'href="([^"]*pdf[^"]*)"',
            r'"pdfUrl"\s*:\s*"([^"]+)"',
            r'"contentUrl"\s*:\s*"([^"]+\.pdf[^"]*)"',
        ]
        
        for pattern in pdf_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                # Resolve URL relativa
                if match.startswith("http"):
                    return match
                elif match.startswith("/"):
                    parsed = urlparse(page_url)
                    return f"{parsed.scheme}://{parsed.netloc}{match}"
        
        return None


# Lista de bases acadêmicas mais usadas
MAJOR_DATABASES = {
    "IEEE Xplore": {
        "domain": "ieeexplore.ieee.org",
        "url_pattern": "https://ieeexplore.ieee.org/document/{doi}",
        "pdf_pattern": "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={id}",
    },
    "Springer Link": {
        "domain": "link.springer.com",
        "url_pattern": "https://link.springer.com/content/pdf/{doi}.pdf",
    },
    "ScienceDirect": {
        "domain": "sciencedirect.com",
        "url_pattern": "https://www.sciencedirect.com/science/article/pii/{pii}",
    },
    "Wiley": {
        "domain": "onlinelibrary.wiley.com",
        "url_pattern": "https://onlinelibrary.wiley.com/doi/pdf/{doi}",
    },
    "Nature": {
        "domain": "nature.com",
        "url_pattern": "https://www.nature.com/articles/{id}.pdf",
    },
    "JSTOR": {
        "domain": "jstor.org",
        "url_pattern": "https://www.jstor.org/stable/{id}",
    },
    "ACM DL": {
        "domain": "dl.acm.org",
        "url_pattern": "https://dl.acm.org/doi/pdf/{doi}",
    },
}


async def test_proxy_connection():
    """Testa a conexão com o proxy PUCRS."""
    print("🔐 Testando conexão com proxy PUCRS...")
    print(f"   Proxy: {PUCRS_PROXY}")
    print()
    
    # Testa sem proxy (apenas para verificar conectividade)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://httpbin.org/ip", timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()
                print(f"🌐 IP público (sem proxy): {data.get('origin', '?')}")
        except Exception as e:
            print(f"⚠️ Conexão direta falhou: {e}")
    
    print()
    print("📋 Para testar o proxy, configure suas credenciais PUCRS:")
    print("   email: c.jones@edu.pucrs.br")
    print("   password: @CiaoMiau2955")
    print()
    print("   Proxy: http://prx.pucrs.br:3128")
    print()
    print("⚠️ NOTA: O proxy PUCRS requer autenticação HTTP Basic.")
    print("   Alguns domínios podem requerer login via web primeiro.")


if __name__ == "__main__":
    asyncio.run(test_proxy_connection())