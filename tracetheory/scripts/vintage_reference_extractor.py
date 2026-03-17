#!/usr/bin/env python3
"""
VintageReferenceExtractor - Extrator especializado para papers acadêmicos antigos (1900-1950)

Analisa padrões específicos de citações em papers da época:
1. Footnotes marcadas com f, X, •, *
2. Referências inline no formato "Author (Year)"
3. Menções a trabalhos clássicos sem citação formal
4. Referências a journals com volume/página

Autor: TraceTheory
Data: 2026-03-16
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime

@dataclass
class Reference:
    """Representa uma referência bibliográfica."""
    authors: List[str]
    year: Optional[int]
    title: Optional[str] = None
    venue: Optional[str] = None
    volume: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    openalex_id: Optional[str] = None
    source: str = "text"  # 'footnote', 'inline', 'mentioned', 'openalex'
    confidence: float = 0.5
    context: Optional[str] = None
    raw_text: Optional[str] = None

@dataclass
class FootnoteReference:
    """Referência encontrada em footnote."""
    marker: str  # 'f', 'X', '•', '*'
    authors: List[str]
    title: Optional[str]
    journal: Optional[str]
    year: Optional[int]
    volume: Optional[str]
    pages: Optional[str]
    raw_text: str

class VintageReferenceExtractor:
    """
    Extrator de referências para papers antigos (1900-1950).
    
    Características:
    - Detecta footnotes com marcadores especiais
    - Extrai referências inline no formato "Author (Year)"
    - Identifica menções a trabalhos clássicos
    - Parsing de formato de journal antigo
    """
    
    # Autores conhecidos da época (1900-1950) - computabilidade/lógica/fundamentos
    KNOWN_AUTHORS = {
        # Lógica e Fundamentos
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
        'Bernays': 'Paul Bernays',
        'Post': 'Emil Post',
        'Rosser': 'J. Barkley Rosser',
        'Skolem': 'Thoralf Skolem',
        'Herbrand': 'Jacques Herbrand',
        'Tarski': 'Alfred Tarski',
        'Von Neumann': 'John von Neumann',
        'von Neumann': 'John von Neumann',
        'Zermelo': 'Ernst Zermelo',
        'Fraenkel': 'Abraham Fraenkel',
        'Cantor': 'Georg Cantor',
        'Frege': 'Gottlob Frege',
        'Brouwer': 'L.E.J. Brouwer',
        'Heyting': 'Arend Heyting',
        'Gentzen': 'Gerhard Gentzen',
        
        # Matemáticos mencionados
        'Hobson': 'E.W. Hobson',
        'Bessel': 'Friedrich Bessel',
        'Dedekind': 'Richard Dedekind',
    }
    
    # Trabalhos clássicos conhecidos
    KNOWN_WORKS = [
        # Computabilidade e Lógica
        {
            'authors': ['Alonzo Church'],
            'year': 1936,
            'title': 'An Unsolvable Problem of Elementary Number Theory',
            'venue': 'American Journal of Mathematics',
            'volume': '58',
            'pages': '345-363',
            'keywords': ['Church', 'unsolvable', 'elementary number theory', 'lambda']
        },
        {
            'authors': ['Alonzo Church'],
            'year': 1936,
            'title': 'A Note on the Entscheidungsproblem',
            'venue': 'Journal of Symbolic Logic',
            'volume': '1',
            'pages': '40-41',
            'keywords': ['Church', 'Entscheidungsproblem', 'note']
        },
        {
            'authors': ['Kurt Gödel'],
            'year': 1931,
            'title': 'Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I',
            'venue': 'Monatshefte für Mathematik und Physik',
            'volume': '38',
            'pages': '173-198',
            'keywords': ['Gödel', 'Godel', 'unentscheidbare', 'formal', 'Sätze']
        },
        {
            'authors': ['David Hilbert', 'Wilhelm Ackermann'],
            'year': 1928,
            'title': 'Grundzüge der Theoretischen Logik',
            'venue': 'Springer',
            'keywords': ['Hilbert', 'Ackermann', 'Grundzüge', 'Logik']
        },
        {
            'authors': ['David Hilbert', 'Paul Bernays'],
            'year': 1934,
            'title': 'Grundlagen der Mathematik',
            'venue': 'Springer',
            'keywords': ['Hilbert', 'Bernays', 'Grundlagen', 'Mathematik']
        },
        {
            'authors': ['Stephen C. Kleene'],
            'year': 1935,
            'title': 'A Theory of Positive Integers in Formal Logic',
            'venue': 'American Journal of Mathematics',
            'volume': '57',
            'pages': '153-173, 219-244',
            'keywords': ['Kleene', 'positive integers', 'formal logic']
        },
        {
            'authors': ['Stephen C. Kleene'],
            'year': 1936,
            'title': 'General Recursive Functions of Natural Numbers',
            'venue': 'Mathematische Annalen',
            'keywords': ['Kleene', 'recursive', 'natural numbers']
        },
        {
            'authors': ['Alfred N. Whitehead', 'Bertrand Russell'],
            'year': 1910,
            'year_end': 1913,
            'title': 'Principia Mathematica',
            'venue': 'Cambridge University Press',
            'keywords': ['Principia Mathematica', 'Whitehead', 'Russell']
        },
        {
            'authors': ['Emil Post'],
            'year': 1936,
            'title': 'Finite Combinatory Processes - Formulation I',
            'venue': 'Journal of Symbolic Logic',
            'keywords': ['Post', 'combinatory', 'formulation']
        },
        {
            'authors': ['Alan M. Turing'],
            'year': 1936,
            'title': 'On Computable Numbers, with an Application to the Entscheidungsproblem',
            'venue': 'Proceedings of the London Mathematical Society',
            'volume': '42',
            'pages': '230-265',
            'keywords': ['Turing', 'computable', 'Entscheidungsproblem']
        },
        {
            'authors': ['Alan M. Turing'],
            'year': 1937,
            'title': 'On Computable Numbers, with an Application to the Entscheidungsproblem. A Correction',
            'venue': 'Proceedings of the London Mathematical Society',
            'volume': '43',
            'pages': '544-546',
            'keywords': ['Turing', 'correction', 'computable']
        },
    ]
    
    # Padrões de journal antigos
    JOURNAL_PATTERNS = [
        # American Journal of Math., 58 (1936), 345-363
        r'(?:American\s+)?J(?:ournal)?\.?\s*(?:of\s+)?Math\.?,?\s*(\d+),?\s*\((\d{4})\),?\s*(\d+[-–]\d+|\d+)',
        # J. of Symbolic Logic, 1 (1936), 40-41
        r'J\.?\s*(?:of\s+)?Symbolic\s+Logic,?\s*(\d+),?\s*\((\d{4})\),?\s*(\d+[-–]\d+|\d+)',
        # Monatshefte Math. Phys., 38 (1931), 173-198
        r'Monatshefte?\s*(?:Math\.?\s*Phys\.?|für\s+Mathematik\s+und\s+Physik),?\s*(\d+),?\s*\((\d{4})\),?\s*(\d+[-–]\d+|\d+)',
        # Proc. London Math. Soc.
        r'(?:Proc(?:eedings)?\.?\s+)?London\s+Math(?:ematical)?\.?\s+Soc(?:iety)?\.?,?\s*(\d+),?\s*\((\d{4})\),?\s*(\d+[-–]\d+|\d+)',
    ]

    def __init__(self):
        self.references: List[Reference] = []
        self.footnotes: List[FootnoteReference] = []
        self._seen_refs: set = set()
        
    def _normalize_author(self, author: str) -> str:
        """Normaliza nome do autor para forma canônica."""
        # Remover espaços extras
        author = ' '.join(author.split())
        
        # Verificar se é um autor conhecido
        for key, full_name in self.KNOWN_AUTHORS.items():
            if key.lower() in author.lower():
                return full_name
        
        return author
    
    def _get_known_work(self, text: str) -> Optional[Dict]:
        """Verifica se o texto menciona um trabalho conhecido."""
        text_lower = text.lower()
        
        for work in self.KNOWN_WORKS:
            for keyword in work['keywords']:
                if keyword.lower() in text_lower:
                    # Verificar se é realmente esse trabalho
                    if 'authors' in work:
                        author_match = any(
                            self._normalize_author(a.split()[0]).lower() in text_lower
                            for a in work['authors']
                        )
                        if author_match:
                            return work
                    elif work['keywords'][0].lower() in text_lower:
                        return work
        
        return None
    
    def extract_footnotes(self, text: str) -> List[FootnoteReference]:
        """
        Extrai referências de footnotes.
        
        Padrões detectados:
        - f Author, "Title", Journal, vol (year), pages
        - X Author, "Title", Journal, vol (year), pages
        - • Author, Title (Location, year)
        """
        footnotes = []
        
        # Padrão 1: f/X/• seguido de citação completa
        footnote_pattern = re.compile(
            r'^([fX•*])\s+([A-Z][a-zéö]+(?:\s+[A-Z]\.(?:\s+[A-Z]\.)*)?(?:\s+[A-Z][a-z]+)?)'
            r'[,\s]+["""]?([^"""]+?)["""]?'
            r'(?:,?\s*([A-Z][^,\d]+?))?'
            r'(?:,?\s*(\d+))?\s*\((\d{4})\)?'
            r'(?:,?\s*(\d+[-–]\d+|\d+))?',
            re.MULTILINE
        )
        
        for match in footnote_pattern.finditer(text):
            marker = match.group(1)
            author = self._normalize_author(match.group(2))
            title = match.group(3).strip().strip('"').strip('"') if match.group(3) else None
            journal = match.group(4).strip() if match.group(4) else None
            volume = match.group(5) if match.group(5) else None
            year = int(match.group(6)) if match.group(6) else None
            pages = match.group(7) if match.group(7) else None
            
            footnotes.append(FootnoteReference(
                marker=marker,
                authors=[author],
                title=title,
                journal=journal,
                year=year,
                volume=volume,
                pages=pages,
                raw_text=match.group(0)
            ))
        
        # Padrão 2: Referências quebradas em múltiplas linhas
        # Ex: "f Godel, " Über formal unentscheidbare..." seguido de mais texto
        broken_footnote_pattern = re.compile(
            r'^([fX•])\s+([A-Z][a-zéö]+)[,，]\s*["""]([^"""]+)',
            re.MULTILINE
        )
        
        for match in broken_footnote_pattern.finditer(text):
            marker = match.group(1)
            author = self._normalize_author(match.group(2))
            title = match.group(3).strip()
            
            # Verificar se já foi capturado
            key = (tuple([author]), title[:30] if title else '')
            if key not in [(tuple(f.authors), f.title[:30] if f.title else '') for f in footnotes]:
                footnotes.append(FootnoteReference(
                    marker=marker,
                    authors=[author],
                    title=title,
                    journal=None,
                    year=None,
                    volume=None,
                    pages=None,
                    raw_text=match.group(0)
                ))
        
        self.footnotes = footnotes
        return footnotes
    
    def extract_inline_citations(self, text: str) -> List[Reference]:
        """
        Extrai citações inline no formato "Author (Year)" ou "Author (Year, p. X)".
        """
        refs = []
        
        # Padrão: "Author (Year)" ou "Author (Yeara)" para múltiplos trabalhos
        inline_pattern = re.compile(
            r'([A-Z][a-zéö]+(?:\s+(?:and|&|und)\s+[A-Z][a-z]+)?)\s*\((\d{4})([a-z])?\)',
            re.MULTILINE
        )
        
        for match in inline_pattern.finditer(text):
            author = self._normalize_author(match.group(1))
            year = int(match.group(2))
            suffix = match.group(3) or ''
            
            key = (author, year, suffix)
            if key not in self._seen_refs:
                self._seen_refs.add(key)
                
                # Contexto
                context_start = max(0, match.start() - 50)
                context_end = min(len(text), match.end() + 100)
                context = text[context_start:context_end].replace('\n', ' ')
                
                refs.append(Reference(
                    authors=[author],
                    year=year,
                    source='inline',
                    confidence=0.7,
                    context=context
                ))
        
        return refs
    
    def extract_mentioned_works(self, text: str) -> List[Reference]:
        """
        Extrai trabalhos mencionados no texto sem citação formal.
        
        Ex: "Hilbertian Entscheidungsproblem" → Hilbert
        Ex: "Principia Mathematica" → Whitehead & Russell
        """
        refs = []
        text_lower = text.lower()
        
        # Buscar menções de trabalhos conhecidos
        for work in self.KNOWN_WORKS:
            for keyword in work['keywords']:
                if keyword.lower() in text_lower:
                    # Verificar se o autor também é mencionado
                    author_mentioned = any(
                        a.split()[0].lower() in text_lower
                        for a in work['authors']
                    )
                    
                    key = (tuple(work['authors']), work['year'])
                    if key not in self._seen_refs and author_mentioned:
                        self._seen_refs.add(key)
                        
                        # Encontrar contexto
                        idx = text_lower.find(keyword.lower())
                        context_start = max(0, idx - 100)
                        context_end = min(len(text), idx + 200)
                        context = text[context_start:context_end].replace('\n', ' ')
                        
                        refs.append(Reference(
                            authors=work['authors'],
                            year=work['year'],
                            title=work.get('title'),
                            venue=work.get('venue'),
                            volume=work.get('volume'),
                            pages=work.get('pages'),
                            source='mentioned',
                            confidence=0.8 if author_mentioned else 0.5,
                            context=context
                        ))
                        break
        
        return refs
    
    def extract_journal_references(self, text: str) -> List[Reference]:
        """
        Extrai referências no formato de journal antigo.
        
        Ex: "American Journal of Math., 58 (1936), 345-363"
        """
        refs = []
        
        for pattern in self.JOURNAL_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                volume = match.group(1)
                year = int(match.group(2))
                pages = match.group(3)
                
                # Contexto para identificar autor/título
                context_start = max(0, match.start() - 200)
                context = text[context_start:match.start()]
                
                # Tentar extrair autor do contexto
                author_match = re.search(r'([A-Z][a-zéö]+(?:\s+[A-Z][a-z]+)?)', context)
                author = self._normalize_author(author_match.group(1)) if author_match else None
                
                if author:
                    key = (author, year)
                    if key not in self._seen_refs:
                        self._seen_refs.add(key)
                        refs.append(Reference(
                            authors=[author],
                            year=year,
                            volume=volume,
                            pages=pages,
                            source='journal_format',
                            confidence=0.6,
                            context=context[-100:] + match.group(0)
                        ))
        
        return refs
    
    def extract_all(self, text: str) -> List[Reference]:
        """Extrai todas as referências do texto."""
        all_refs = []
        
        # 1. Footnotes
        footnotes = self.extract_footnotes(text)
        for fn in footnotes:
            key = (tuple(fn.authors), fn.year) if fn.year else (tuple(fn.authors), 0)
            if key not in self._seen_refs:
                self._seen_refs.add(key)
                all_refs.append(Reference(
                    authors=fn.authors,
                    year=fn.year,
                    title=fn.title,
                    venue=fn.journal,
                    volume=fn.volume,
                    pages=fn.pages,
                    source='footnote',
                    confidence=0.9,
                    raw_text=fn.raw_text
                ))
        
        # 2. Inline citations
        all_refs.extend(self.extract_inline_citations(text))
        
        # 3. Mentioned works
        all_refs.extend(self.extract_mentioned_works(text))
        
        # 4. Journal format
        all_refs.extend(self.extract_journal_references(text))
        
        # Ordenar por ano
        all_refs.sort(key=lambda r: r.year or 0)
        
        self.references = all_refs
        return all_refs
    
    def merge_with_openalex(self, openalex_refs: List[Reference]) -> List[Reference]:
        """Mescla referências extraídas com referências do OpenAlex."""
        merged = {}
        
        # Adicionar referências do OpenAlex (maior confiança)
        for ref in openalex_refs:
            key = (tuple(ref.authors), ref.year)
            if key not in merged:
                merged[key] = ref
        
        # Adicionar/complementar com referências extraídas
        for ref in self.references:
            key = (tuple(ref.authors), ref.year)
            if key not in merged:
                merged[key] = ref
            else:
                # Complementar informações faltantes
                existing = merged[key]
                if ref.title and not existing.title:
                    existing.title = ref.title
                if ref.venue and not existing.venue:
                    existing.venue = ref.venue
                if ref.context and not existing.context:
                    existing.context = ref.context
        
        return sorted(merged.values(), key=lambda r: r.year or 0)
    
    def to_json(self) -> str:
        """Converte referências para JSON."""
        return json.dumps(
            [asdict(r) for r in self.references],
            indent=2,
            ensure_ascii=False
        )
    
    def to_bibtex(self) -> str:
        """Converte referências para formato BibTeX."""
        entries = []
        
        for ref in self.references:
            # Gerar chave
            first_author = ref.authors[0].split()[-1] if ref.authors else 'Unknown'
            year_str = str(ref.year) if ref.year else 'XXXX'
            key = f"{first_author}{year_str}"
            
            entry = f"@article{{{key},\n"
            entry += f"  author = {{{' and '.join(ref.authors)}}},\n"
            if ref.year:
                entry += f"  year = {{{ref.year}}},\n"
            if ref.title:
                entry += f"  title = {{{ref.title}}},\n"
            if ref.venue:
                entry += f"  journal = {{{ref.venue}}},\n"
            if ref.volume:
                entry += f"  volume = {{{ref.volume}}},\n"
            if ref.pages:
                entry += f"  pages = {{{ref.pages}}},\n"
            entry += "}\n"
            
            entries.append(entry)
        
        return "\n".join(entries)
    
    def print_summary(self):
        """Imprime resumo das referências extraídas."""
        print("═" * 78)
        print(f"REFERÊNCIAS EXTRAÍDAS: {len(self.references)}")
        print("═" * 78)
        
        # Agrupar por fonte
        by_source = {}
        for ref in self.references:
            source = ref.source
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(ref)
        
        for source, refs in by_source.items():
            print(f"\n📚 {source.upper()} ({len(refs)} referências)")
            print("-" * 40)
            
            for i, ref in enumerate(refs, 1):
                print(f"\n{i}. {', '.join(ref.authors)} ({ref.year or 's.d.'})")
                if ref.title:
                    print(f'   "{ref.title}"')
                if ref.venue:
                    print(f"   {ref.venue}")
                if ref.volume and ref.pages:
                    print(f"   Vol. {ref.volume}, pp. {ref.pages}")
                print(f"   Confiança: {ref.confidence:.0%}")


def main():
    """Demo do VintageReferenceExtractor."""
    import sys
    
    print("═" * 78)
    print("VINTAGE REFERENCE EXTRACTOR - Especializado para Papers 1900-1950")
    print("═" * 78)
    
    # Carregar texto do Turing 1936
    text_path = Path("/home/csilva/.openclaw/workspace/tracetheory/output/turing_1936_text.txt")
    
    if not text_path.exists():
        print(f"❌ Arquivo não encontrado: {text_path}")
        return 1
    
    text = text_path.read_text()
    
    # Extrair referências
    extractor = VintageReferenceExtractor()
    refs = extractor.extract_all(text)
    
    # Imprimir resumo
    extractor.print_summary()
    
    # Salvar resultados
    output_dir = Path("/home/csilva/.openclaw/workspace/tracetheory/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    json_path = output_dir / "vintage_references.json"
    json_path.write_text(extractor.to_json())
    print(f"\n✅ JSON salvo em: {json_path}")
    
    # BibTeX
    bibtex_path = output_dir / "vintage_references.bib"
    bibtex_path.write_text(extractor.to_bibtex())
    print(f"✅ BibTeX salvo em: {bibtex_path}")
    
    # Mostrar footnotes detectados
    print("\n" + "═" * 78)
    print("FOOTNOTES DETECTADOS:")
    print("═" * 78)
    
    for i, fn in enumerate(extractor.footnotes, 1):
        print(f"\n{i}. Marker: '{fn.marker}'")
        print(f"   Author: {', '.join(fn.authors)}")
        if fn.title:
            print(f"   Title: {fn.title[:60]}...")
        if fn.journal:
            print(f"   Journal: {fn.journal}")
        if fn.year:
            print(f"   Year: {fn.year}")
    
    print("\n" + "═" * 78)
    print(f"TOTAL: {len(refs)} referências únicas extraídas")
    print("═" * 78)
    
    return 0


if __name__ == '__main__':
    exit(main())