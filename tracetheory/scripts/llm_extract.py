#!/usr/bin/env python3
"""Extrai referências usando análise de padrões do texto."""

import re
import json
from pathlib import Path
from typing import List, Dict

def extract_references_from_text(text: str) -> List[Dict]:
    """Extrai referências bibliográficas do texto."""
    refs = []
    seen = set()
    
    # Padrão 1: Footnotes com "Author, "Title"..."
    # Ex: 'f Alonzo Church, " An unsolvable problem...", American Journal...'
    footnote_pattern = re.compile(
        r'^[fX•]\s+([A-Z][a-zéö]+(?:\s+[A-Z][a-z]+)*),\s*["""]([^"""]+)["""]',
        re.MULTILINE
    )
    
    for match in footnote_pattern.finditer(text):
        author = match.group(1).strip()
        title = match.group(2).strip().strip('"').strip('"').strip()
        
        key = (author, title[:30] if title else '')
        if key not in seen:
            seen.add(key)
            
            # Buscar ano e journal no contexto
            context_start = match.start()
            context = text[context_start:context_start+200]
            
            year_match = re.search(r'\((\d{4})\)', context)
            year = int(year_match.group(1)) if year_match else None
            
            refs.append({
                'authors': [author],
                'year': year,
                'title': title,
                'venue': None,
                'context': context[:100].replace('\n', ' ')
            })
    
    # Padrão 2: Menções no texto "Author (Year)"
    author_year_pattern = re.compile(
        r'([A-Z][a-z]+(?:\s+(?:and|&)\s+[A-Z][a-z]+)?)\s*\((\d{4})([a-z])?\)'
    )
    
    for match in author_year_pattern.finditer(text):
        author = match.group(1).strip()
        year = int(match.group(2))
        suffix = match.group(3) or ''
        
        key = (author, year, suffix)
        if key not in seen:
            seen.add(key)
            
            # Verificar contexto para título
            context_start = max(0, match.start() - 50)
            context_end = min(len(text), match.end() + 100)
            context = text[context_start:context_end]
            
            refs.append({
                'authors': [author],
                'year': year,
                'title': None,
                'venue': None,
                'context': context.replace('\n', ' ')
            })
    
    # Padrão 3: Referências a trabalhos conhecidos
    known_refs = [
        {
            'pattern': r'Hilbert\s+and\s+Bernays',
            'authors': ['David Hilbert', 'Paul Bernays'],
            'year': 1934,
            'title': 'Grundlagen der Mathematik',
            'venue': 'Springer'
        },
        {
            'pattern': r'Hilbert\s+and\s+Ackermann|Grundzüge\s+der\s+Theoretischen\s+Logik',
            'authors': ['David Hilbert', 'Wilhelm Ackermann'],
            'year': 1928,
            'title': 'Grundzüge der Theoretischen Logik',
            'venue': 'Springer'
        },
        {
            'pattern': r'Gödel|Godel.*1931|formal\s+unentscheidbare',
            'authors': ['Kurt Gödel'],
            'year': 1931,
            'title': 'Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme, I',
            'venue': 'Monatshefte Math. Phys.'
        },
        {
            'pattern': r'Kleene.*1935|Kleene.*positive\s+integers',
            'authors': ['Stephen C. Kleene'],
            'year': 1935,
            'title': 'A theory of positive integers in formal logic',
            'venue': 'American Journal of Math.'
        },
        {
            'pattern': r'Principia\s+Mathematica',
            'authors': ['Alfred N. Whitehead', 'Bertrand Russell'],
            'year': 1910,
            'title': 'Principia Mathematica',
            'venue': 'Cambridge'
        },
        {
            'pattern': r'Church.*unsolvable|Alonzo\s+Church',
            'authors': ['Alonzo Church'],
            'year': 1936,
            'title': 'An Unsolvable Problem of Elementary Number Theory',
            'venue': 'American Journal of Mathematics'
        },
        {
            'pattern': r'Church.*Entscheidungsproblem|Note\s+on\s+the\s+Entscheidungsproblem',
            'authors': ['Alonzo Church'],
            'year': 1936,
            'title': 'A Note on the Entscheidungsproblem',
            'venue': 'J. of Symbolic Logic'
        }
    ]
    
    for known in known_refs:
        if re.search(known['pattern'], text, re.IGNORECASE):
            key = (tuple(known['authors']), known['year'])
            if key not in seen:
                seen.add(key)
                refs.append({
                    'authors': known['authors'],
                    'year': known['year'],
                    'title': known['title'],
                    'venue': known['venue'],
                    'context': f"Pattern: {known['pattern']}"
                })
    
    # Ordenar por ano
    refs.sort(key=lambda r: r['year'] or 0)
    
    return refs

# Executar
text_path = Path("output/turing_1936_text.txt")
text = text_path.read_text()

refs = extract_references_from_text(text)

print("══════════════════════════════════════════════════════════════════════════")
print("REFERÊNCIAS EXTRAÍDAS DO TURING 1936")
print("══════════════════════════════════════════════════════════════════════════")

for i, ref in enumerate(refs, 1):
    print(f"\n{i}. {', '.join(ref['authors'])} ({ref['year'] or 's.d.'})")
    if ref['title']:
        print(f'   "{ref["title"]}"')
    if ref['venue']:
        print(f"   {ref['venue']}")

print("\n" + "═" * 78)
print(f"Total: {len(refs)} referências")

# Salvar JSON
output = {
    'paper': 'Turing 1936 - On Computable Numbers',
    'total_refs': len(refs),
    'references': refs
}

Path("output/turing_references_complete.json").write_text(
    json.dumps(output, indent=2, ensure_ascii=False)
)
print(f"\n✅ Salvo em: output/turing_references_complete.json")
