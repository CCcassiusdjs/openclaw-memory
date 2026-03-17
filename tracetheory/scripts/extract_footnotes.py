#!/usr/bin/env python3
"""Extrai referências de footnotes do Turing 1936."""

import re
from pathlib import Path

# Texto extraído do PDF
text_path = Path("output/turing_1936_text.txt")
text = text_path.read_text()

# Padrões de footnotes
patterns = [
    # "f Author, "Title", Journal, vol (year), pages."
    re.compile(r'^[fX•] ([A-Z][a-zéö]+(?:\s+[A-Z][a-z]+)*),\s*["""]([^"""]+)["""]', re.MULTILINE),
    # Journal com ano
    re.compile(r'(?:Journal|Monatsheft|American|Proc\.|Math\.)[^,\d]*(\d+)\s*\((\d{4})\)[,\s]*(\d+[-–]\d+)?'),
    # "Hilbert and Bernays, Grundlagen..."
    re.compile(r'([A-Z][a-z]+)\s+and\s+([A-Z][a-z]+),\s+([A-Z][a-zA-Zäöü]+(?:\s+[A-Za-zäöü]+)*)'),
]

print("══════════════════════════════════════════════════════════════════════════")
print("EXTRAÇÃO DE REFERÊNCIAS DO TURING 1936 (Footnotes)")
print("══════════════════════════════════════════════════════════════════════════")

refs = []

# Buscar footnotes que começam com 'f' ou 'X'
lines = text.split('\n')
for i, line in enumerate(lines):
    line = line.strip()
    
    # Footnote markers
    if line.startswith(('f ', 'X ', '•')):
        # Limpar marker
        content = line[2:].strip()
        
        # Verificar se é uma referência
        if '"' in content or '"' in content:
            # Extrair autor
            author_match = re.match(r'^([A-Z][a-zéö]+(?:\s+[A-Z][a-z]+)*)', content)
            if author_match:
                author = author_match.group(1)
                
                # Extrair título
                title_match = re.search(r'["""]([^"""]+)["""]', content)
                title = title_match.group(1) if title_match else None
                
                # Extrair ano
                year_match = re.search(r'\((\d{4})\)', content)
                year = int(year_match.group(1)) if year_match else None
                
                # Extrair journal
                journal_match = re.search(r'\]\s*([^,\d]+(?:Journal|Monatsheft|Logic|Math)[^,\d]*)', content)
                journal = journal_match.group(1).strip() if journal_match else None
                
                refs.append({
                    'author': author,
                    'title': title,
                    'year': year,
                    'journal': journal,
                    'raw': content
                })

# Buscar menções no texto
mentions = []

# Hilbert and Bernays
if 'Hilbert and Bernays' in text or 'Hilbert & Bernays' in text:
    mentions.append({
        'authors': ['David Hilbert', 'Paul Bernays'],
        'year': 1934,
        'title': 'Grundlagen der Mathematik',
        'source': 'text'
    })

# Hilbert and Ackermann
if 'Hilbert and Ackermann' in text or 'Hilbertian Entscheidungsproblem' in text:
    mentions.append({
        'authors': ['David Hilbert', 'Wilhelm Ackermann'],
        'year': 1928,
        'title': 'Grundzüge der Theoretischen Logik',
        'source': 'text'
    })

# Gödel
if 'Gödel' in text or 'Godel' in text:
    mentions.append({
        'authors': ['Kurt Gödel'],
        'year': 1931,
        'title': 'Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme, I',
        'source': 'text'
    })

# Kleene
if 'Kleene' in text:
    mentions.append({
        'authors': ['Stephen C. Kleene'],
        'year': 1935,
        'title': 'A theory of positive integers in formal logic',
        'journal': 'American Journal of Math.',
        'source': 'text'
    })

# Church (já temos do OpenAlex)
if 'Church' in text:
    # Verificar se já foi encontrado
    pass

# Whitehead & Russell
if 'Principia Mathematica' in text:
    mentions.append({
        'authors': ['Alfred N. Whitehead', 'Bertrand Russell'],
        'year': 1910,
        'title': 'Principia Mathematica',
        'source': 'text'
    })

print("\n📚 REFERÊNCIAS EM FOOTNOTES:")
print("=" * 78)
for i, ref in enumerate(refs, 1):
    print(f"\n{i}. {ref['author']}")
    if ref['title']:
        print(f'   "{ref["title"]}"')
    if ref['journal']:
        print(f"   {ref['journal']}")
    if ref['year']:
        print(f"   Ano: {ref['year']}")

print("\n\n📚 REFERÊNCIAS MENCIIONADAS NO TEXTO:")
print("=" * 78)
for i, ref in enumerate(mentions, 1):
    print(f"\n{i}. {', '.join(ref['authors'])} ({ref['year']})")
    if ref['title']:
        print(f'   "{ref["title"]}"')
    if 'journal' in ref:
        print(f"   {ref['journal']}")

# Salvar
import json
output = {
    'footnotes': refs,
    'mentions': mentions
}

Path('output/turing_footnotes.json').write_text(json.dumps(output, indent=2, ensure_ascii=False))
print("\n\n✅ Salvo em: output/turing_footnotes.json")
