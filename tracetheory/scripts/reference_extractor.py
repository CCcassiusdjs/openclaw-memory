#!/usr/bin/env python3
"""
ReferenceExtractor - Extrai referências bibliográficas de PDFs acadêmicos

Pipeline híbrido:
1. OpenAlex API (para papers indexados)
2. Regex patterns (para papers antigos)
3. Text analysis (para citações no texto)

Autor: TraceTheory
"""

import re
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Reference:
    """Representa uma referência bibliográfica."""
    authors: List[str]
    year: Optional[int]
    title: Optional[str]
    venue: Optional[str]  # Journal/Conference
    volume: Optional[str]
    pages: Optional[str]
    doi: Optional[str]
    openalex_id: Optional[str]
    source: str  # 'openalex', 'regex', 'text'
    confidence: float  # 0.0-1.0

class ReferenceExtractor:
    """Extrai referências de papers acadêmicos."""
    
    # Padrões regex para referências no texto
    PATTERNS = {
        # "Church (1936)" ou "Church (1936a)"
        'author_year': re.compile(
            r'([A-Z][a-z]+(?:\s+(?:and|&)\s+[A-Z][a-z]+)?)\s*\((\d{4})([a-z])?\)',
            re.MULTILINE
        ),
        # "Church, A. (1936)"
        'author_comma_year': re.compile(
            r'([A-Z][a-z]+),\s*([A-Z]\.(?:\s*[A-Z]\.)*)\s*\((\d{4})\)',
            re.MULTILINE
        ),
        # "Hilbert and Ackermann (1928)"
        'dual_author_year': re.compile(
            r'([A-Z][a-z]+)\s+and\s+([A-Z][a-z]+)\s*\((\d{4})\)',
            re.MULTILINE
        ),
        # "Hilbert & Bernays (1934)"
        'dual_author_amp': re.compile(
            r'([A-Z][a-z]+)\s*&\s*([A-Z][a-z]+)\s*\((\d{4})\)',
            re.MULTILINE
        ),
        # "(Berlin, 1934)" - local + ano
        'location_year': re.compile(
            r'\(([A-Z][a-z]+(?:,\s*[A-Z][a-z]+)*),\s*(\d{4})\)',
            re.MULTILINE
        ),
        # Títulos de trabalhos em itálico ou aspas
        'title_quotes': re.compile(
            r'["""]([^"""]+)["""]',
            re.MULTILINE
        ),
    }
    
    # Autores conhecidos da área de computabilidade/lógica (1930s)
    KNOWN_AUTHORS = {
        'Church': 'Alonzo Church',
        'Turing': 'Alan M. Turing',
        'Gödel': 'Kurt Gödel',
        'Godel': 'Kurt Gödel',
        'Hilbert': 'David Hilbert',
        'Kleene': 'Stephen C. Kleene',
        'Ackermann': 'Wilhelm Ackermann',
        'Peano': 'Giuseppe Peano',
        'Russell': 'Bertrand Russell',
        'Whitehead': 'Alfred N. Whitehead',
        'Post': 'Emil Post',
        'Bernays': 'Paul Bernays',
        'Rosser': 'J. Barkley Rosser',
    }
    
    # Trabalhos conhecidos da época
    KNOWN_WORKS = {
        ('Church', 1936): {
            'title': 'An Unsolvable Problem of Elementary Number Theory',
            'venue': 'American Journal of Mathematics'
        },
        ('Church', 1936, 'b'): {
            'title': 'A Note on the Entscheidungsproblem',
            'venue': 'Journal of Symbolic Logic'
        },
        ('Turing', 1936): {
            'title': 'On Computable Numbers, with an Application to the Entscheidungsproblem',
            'venue': 'Proceedings of the London Mathematical Society'
        },
        ('Gödel', 1931): {
            'title': 'On Formally Undecidable Propositions of Principia Mathematica',
            'venue': 'Monatshefte für Mathematik und Physik'
        },
        ('Hilbert', 1928): {
            'title': 'Grundzüge der theoretischen Logik',
            'venue': 'Springer'
        },
        ('Hilbert', 1934): {
            'title': 'Grundlagen der Mathematik',
            'venue': 'Springer'
        },
        ('Kleene', 1936): {
            'title': 'General Recursive Functions of Natural Numbers',
            'venue': 'Mathematische Annalen'
        },
    }
    
    def __init__(self, openalex_email: str = "cassiojonesdhein@gmail.com"):
        self.openalex_email = openalex_email
        self.openalex_base = "https://api.openalex.org"
        
    def extract_from_openalex(self, openalex_id: str) -> List[Reference]:
        """Extrai referências via OpenAlex API."""
        refs = []
        
        try:
            # Buscar referências citadas pelo paper
            url = f"{self.openalex_base}/works/{openalex_id}"
            params = {
                'mailto': self.openalex_email,
                'select': 'referenced_works'
            }
            
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            referenced_works = data.get('referenced_works', [])
            
            # Buscar detalhes de cada referência
            for work_id in referenced_works[:50]:  # Limite de 50 para evitar timeout
                try:
                    work_url = f"{self.openalex_base}/works/{work_id}"
                    work_resp = requests.get(work_url, params={'mailto': self.openalex_email}, timeout=10)
                    work_resp.raise_for_status()
                    work_data = work_resp.json()
                    
                    # Extrair ano
                    year = work_data.get('publication_year')
                    
                    # Extrair autores
                    authors = []
                    for authorship in work_data.get('authorships', [])[:5]:
                        author = authorship.get('author', {})
                        name = author.get('display_name', '')
                        if name:
                            authors.append(name)
                    
                    # Extrair título
                    title = work_data.get('title', '')
                    
                    # Extrair venue
                    venue = work_data.get('primary_location', {})
                    if venue:
                        source = venue.get('source', {})
                        venue_name = source.get('display_name', '') if source else ''
                    else:
                        venue_name = ''
                    
                    refs.append(Reference(
                        authors=authors,
                        year=year,
                        title=title,
                        venue=venue_name if 'venue_name' in dir() else None,
                        volume=None,
                        pages=None,
                        doi=work_data.get('doi'),
                        openalex_id=work_id,
                        source='openalex',
                        confidence=0.9
                    ))
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Erro OpenAlex: {e}")
            
        return refs
    
    def extract_from_text(self, text: str) -> List[Reference]:
        """Extrai referências do texto usando regex e análise."""
        refs = []
        found_refs = set()  # Para evitar duplicatas
        
        # Padrão 1: "Author (Year)"
        for match in self.PATTERNS['author_year'].finditer(text):
            author_lastname = match.group(1)
            year = int(match.group(2))
            suffix = match.group(3) or ''
            
            # Normalizar nome do autor
            full_name = self.KNOWN_AUTHORS.get(author_lastname, author_lastname)
            
            # Criar chave única
            ref_key = (author_lastname, year, suffix)
            if ref_key not in found_refs:
                found_refs.add(ref_key)
                
                # Verificar se é um trabalho conhecido
                known_key = (author_lastname, year) if not suffix else (author_lastname, year, suffix)
                known_work = self.KNOWN_WORKS.get(known_key, {})
                
                refs.append(Reference(
                    authors=[full_name],
                    year=year,
                    title=known_work.get('title'),
                    venue=known_work.get('venue'),
                    volume=None,
                    pages=None,
                    doi=None,
                    openalex_id=None,
                    source='regex',
                    confidence=0.7 if known_work else 0.5
                ))
        
        # Padrão 2: "Author1 and Author2 (Year)"
        for match in self.PATTERNS['dual_author_year'].finditer(text):
            author1 = match.group(1)
            author2 = match.group(2)
            year = int(match.group(3))
            
            full_name1 = self.KNOWN_AUTHORS.get(author1, author1)
            full_name2 = self.KNOWN_AUTHORS.get(author2, author2)
            
            ref_key = (author1, author2, year)
            if ref_key not in found_refs:
                found_refs.add(ref_key)
                
                # Verificar trabalho conhecido
                known_work = self.KNOWN_WORKS.get((author1, year), {})
                
                refs.append(Reference(
                    authors=[full_name1, full_name2],
                    year=year,
                    title=known_work.get('title'),
                    venue=known_work.get('venue'),
                    volume=None,
                    pages=None,
                    doi=None,
                    openalex_id=None,
                    source='regex',
                    confidence=0.6
                ))
        
        # Padrão 3: "(Location, Year)" - pode ser citação de local
        for match in self.PATTERNS['location_year'].finditer(text):
            location = match.group(1)
            year = int(match.group(2))
            
            # Verificar se é um local de publicação conhecido
            if location in ['Berlin', 'London', 'Cambridge', 'Oxford', 'Princeton', 'Paris']:
                # Pode ser uma referência a um livro publicado nesse local
                # Ex: "(Berlin, 1934)" -> Hilbert & Bernays
                pass  # Por enquanto, ignorar
        
        return refs
    
    def merge_references(self, openalex_refs: List[Reference], text_refs: List[Reference]) -> List[Reference]:
        """Mescla referências de diferentes fontes, removendo duplicatas."""
        merged = {}
        
        # Adicionar referências do OpenAlex (maior confiança)
        for ref in openalex_refs:
            key = (tuple(ref.authors), ref.year)
            merged[key] = ref
        
        # Adicionar referências do texto (complementar)
        for ref in text_refs:
            key = (tuple(ref.authors), ref.year)
            if key not in merged:
                merged[key] = ref
            else:
                # Se já existe, atualizar confiança
                existing = merged[key]
                existing.confidence = max(existing.confidence, ref.confidence)
                if ref.title and not existing.title:
                    existing.title = ref.title
                    existing.confidence = min(existing.confidence + 0.1, 1.0)
        
        return sorted(merged.values(), key=lambda r: r.year or 0, reverse=True)
    
    def resolve_openalex_id(self, ref: Reference) -> Optional[str]:
        """Tenta resolver o OpenAlex ID para uma referência."""
        try:
            # Buscar por autor + ano
            query = f"{ref.authors[0]} {ref.year}"
            if ref.title:
                query += f" {ref.title[:50]}"
            
            url = f"{self.openalex_base}/works"
            params = {
                'mailto': self.openalex_email,
                'search': query,
                'per_page': 5
            }
            
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            results = data.get('results', [])
            if results:
                # Retornar o ID do primeiro resultado
                return results[0].get('id')
                
        except Exception:
            pass
            
        return None
    
    def to_json(self, refs: List[Reference]) -> str:
        """Converte referências para JSON."""
        return json.dumps([
            {
                'authors': r.authors,
                'year': r.year,
                'title': r.title,
                'venue': r.venue,
                'doi': r.doi,
                'openalex_id': r.openalex_id,
                'source': r.source,
                'confidence': r.confidence
            }
            for r in refs
        ], indent=2, ensure_ascii=False)
    
    def to_bibtex(self, refs: List[Reference]) -> str:
        """Converte referências para formato BibTeX."""
        bibtex_entries = []
        
        for i, ref in enumerate(refs):
            # Gerar chave
            first_author_last = ref.authors[0].split()[-1] if ref.authors else 'Unknown'
            key = f"{first_author_last}{ref.year or 'XXXX'}"
            
            entry = f"@article{{{key},\n"
            entry += f"  author = {{{' and '.join(ref.authors)}}},\n"
            if ref.year:
                entry += f"  year = {{{ref.year}}},\n"
            if ref.title:
                entry += f"  title = {{{ref.title}}},\n"
            if ref.venue:
                entry += f"  journal = {{{ref.venue}}},\n"
            if ref.doi:
                entry += f"  doi = {{{ref.doi}}},\n"
            entry += "}\n"
            
            bibtex_entries.append(entry)
        
        return "\n".join(bibtex_entries)


def main():
    """Demo do ReferenceExtractor."""
    import sys
    
    print("══════════════════════════════════════════════════════════════════════════")
    print("                    REFERENCE EXTRACTOR - DEMO")
    print("══════════════════════════════════════════════════════════════════════════")
    
    extractor = ReferenceExtractor()
    
    # Teste com Turing 1936
    print("\n📖 Testando com Turing 1936...")
    
    # 1. OpenAlex
    print("\n1. Buscando referências no OpenAlex...")
    openalex_refs = extractor.extract_from_openalex('W2126160338')
    print(f"   Encontradas: {len(openalex_refs)} referências")
    
    # 2. Regex no texto
    print("\n2. Extraindo do texto com regex...")
    text_path = Path("/home/csilva/.openclaw/workspace/tracetheory/output/turing_1936_text.txt")
    if text_path.exists():
        text = text_path.read_text()
        text_refs = extractor.extract_from_text(text)
        print(f"   Encontradas: {len(text_refs)} referências")
    else:
        print("   Arquivo de texto não encontrado")
        text_refs = []
    
    # 3. Mesclar
    print("\n3. Mesclando referências...")
    merged = extractor.merge_references(openalex_refs, text_refs)
    
    print("\n" + "═" * 78)
    print("REFERÊNCIAS EXTRAÍDAS:")
    print("═" * 78)
    
    for i, ref in enumerate(merged, 1):
        print(f"\n{i}. {', '.join(ref.authors)} ({ref.year or 's.d.'})")
        if ref.title:
            print(f"   \"{ref.title}\"")
        if ref.venue:
            print(f"   {ref.venue}")
        print(f"   Fonte: {ref.source} (confiança: {ref.confidence:.1%})")
    
    # Salvar resultados
    output_dir = Path("/home/csilva/.openclaw/workspace/tracetheory/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    json_path = output_dir / "turing_references.json"
    json_path.write_text(extractor.to_json(merged))
    print(f"\n✅ JSON salvo em: {json_path}")
    
    # BibTeX
    bibtex_path = output_dir / "turing_references.bib"
    bibtex_path.write_text(extractor.to_bibtex(merged))
    print(f"✅ BibTeX salvo em: {bibtex_path}")
    
    print("\n" + "═" * 78)
    print(f"Total: {len(merged)} referências únicas")
    print("═" * 78)


if __name__ == '__main__':
    main()