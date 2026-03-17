"""
EZProxy Authentication for PUCRS

Handles authentication with PUCRS library proxy to access subscription content.

Usage:
1. Configure credentials in config.yaml
2. Use proxy_url for all requests to subscription content

The proxy will automatically redirect through login page if needed.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from urllib.parse import quote, urlparse, urljoin
import re
from dataclasses import dataclass


@dataclass
class ProxyConfig:
    """EZProxy configuration"""
    proxy_base: str = "https://biblioteca.pucrs.br/recursos-tecnologicos/acesso-remoto/pucrs/"
    login_url: str = "https://login.ezproxy.pucrs.br/login"
    email: str = ""
    password: str = ""


class EZProxyClient:
    """
    Client for accessing subscription content via EZProxy.
    
    PUCRS uses EZProxy for remote access to subscription databases.
    Authentication requires email acadêmico (@edu.pucrs.br) and senha de rede.
    """
    
    def __init__(self, config: ProxyConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.authenticated = False
        self.cookie_jar: Optional[aiohttp.CookieJar] = None
    
    async def __aenter__(self):
        self.cookie_jar = aiohttp.CookieJar()
        self.session = aiohttp.ClientSession(
            cookie_jar=self.cookie_jar,
            follow_redirects=True,
            timeout=aiohttp.ClientTimeout(total=60)
        )
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def authenticate(self) -> bool:
        """
        Authenticate with EZProxy using PUCRS credentials.
        
        Returns True if authentication successful.
        """
        if not self.config.email or not self.config.password:
            raise ValueError("PUCRS credentials not configured. Set email and password in config.yaml")
        
        # PUCRS EZProxy login endpoint
        login_url = self.config.login_url
        
        # Form data
        data = {
            "user": self.config.email,
            "pass": self.config.password,
        }
        
        try:
            async with self.session.post(login_url, data=data) as response:
                if response.status == 200:
                    # Check for successful login indicators
                    text = await response.text()
                    
                    # EZProxy usually sets session cookies on success
                    if "session" in [c.key.lower() for c in self.cookie_jar]:
                        self.authenticated = True
                        return True
                    
                    # Check for error messages
                    if "inválido" in text.lower() or "incorreto" in text.lower():
                        raise PermissionError("Invalid PUCRS credentials")
                    
                    # Some proxies redirect on success
                    if response.url and "login" not in str(response.url):
                        self.authenticated = True
                        return True
                
                return False
                
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to connect to EZProxy: {e}")
    
    def get_proxied_url(self, original_url: str) -> str:
        """
        Convert a regular URL to its proxied version.
        
        EZProxy typically uses URL rewriting:
        - https://publisher.com/article -> https://publisher.com.ezproxy.pucrs.br/article
        
        Or uses a prefix:
        - https://login.ezproxy.pucrs.br/login?url=https://publisher.com/article
        """
        parsed = urlparse(original_url)
        
        # If already proxied, return as-is
        if "ezproxy.pucrs.br" in parsed.netloc:
            return original_url
        
        # EZProxy URL format for PUCRS
        # This may need adjustment based on PUCRS's specific EZProxy configuration
        proxied_netloc = f"{parsed.netloc}.ezproxy.pucrs.br"
        proxied_url = f"{parsed.scheme}://{proxied_netloc}{parsed.path}"
        
        if parsed.query:
            proxied_url += f"?{parsed.query}"
        
        return proxied_url
    
    async def download_pdf(self, url: str, output_path: str) -> bool:
        """
        Download a PDF through EZProxy.
        
        Args:
            url: Original PDF URL
            output_path: Where to save the file
            
        Returns:
            True if download successful
        """
        if not self.authenticated:
            await self.authenticate()
        
        proxied_url = self.get_proxied_url(url)
        
        try:
            async with self.session.get(proxied_url) as response:
                if response.status != 200:
                    return False
                
                # Verify it's a PDF
                content_type = response.headers.get("Content-Type", "")
                if "pdf" not in content_type.lower():
                    return False
                
                # Save to file
                content = await response.read()
                with open(output_path, "wb") as f:
                    f.write(content)
                
                return True
                
        except aiohttp.ClientError:
            return False
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a web page through EZProxy.
        
        Returns HTML content or None if failed.
        """
        if not self.authenticated:
            await self.authenticate()
        
        proxied_url = self.get_proxied_url(url)
        
        try:
            async with self.session.get(proxied_url) as response:
                if response.status == 200:
                    return await response.text()
                return None
        except aiohttp.ClientError:
            return None


# CAPES Portal bases accessible via PUCRS proxy
CAPES_BASES = {
    # Major academic databases
    "web_of_science": "https://www.webofscience.com",
    "scopus": "https://www.scopus.com",
    "jstor": "https://www.jstor.org",
    "springer_link": "https://link.springer.com",
    "ieee_xplore": "https://ieeexplore.ieee.org",
    "acm_dl": "https://dl.acm.org",
    "science_direct": "https://www.sciencedirect.com",
    "wiley": "https://onlinelibrary.wiley.com",
    
    # Domain-specific
    "pubmed": "https://pubmed.ncbi.nlm.nih.gov",
    "mathscinet": "https://mathscinet.ams.org",
    "zbmath": "https://zbmath.org",
    
    # Brazilian
    "scielo": "https://scielo.org",
    "lilacs": "https://lilacs.bvsalud.org",
}


async def main():
    """Demo: Test proxy authentication"""
    config = ProxyConfig(
        email="your.email@edu.pucrs.br",
        password="your_password"
    )
    
    async with EZProxyClient(config) as client:
        # This will fail without valid credentials
        print("Attempting authentication...")
        # authenticated = await client.authenticate()
        # print(f"Authenticated: {authenticated}")


if __name__ == "__main__":
    asyncio.run(main())