#!/usr/bin/env python3
"""
FLUXO Server - Servidor Flask para a Memória Temporal

Serve a visualização e API para o FLUXO.
"""

import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Importar engine FLUXO
from fluxo_engine import Fluxo, WORKSPACE

app = Flask(__name__)
CORS(app)

# Instância global do FLUXO
fluxo = Fluxo()

@app.route('/')
def index():
    """Serve a visualização do FLUXO."""
    return send_from_directory(WORKSPACE, 'fluxo_visual.html')

@app.route('/api/fluxo')
def get_fluxo():
    """Retorna dados para visualização."""
    return jsonify(fluxo.get_visualization_data())

@app.route('/api/fluxo/recall', methods=['POST'])
def api_recall():
    """API de recall."""
    data = request.json
    query = data.get('query', '')
    n = data.get('n', 5)
    
    results = fluxo.recall(query, n)
    
    return jsonify({
        'query': query,
        'results': [
            {
                'stream_id': r[0],
                'stream': fluxo.streams[r[0]].pattern if r[0] in fluxo.streams else r[0],
                'strength': r[1]
            }
            for r in results
        ]
    })

@app.route('/api/fluxo/imagine', methods=['POST'])
def api_imagine():
    """API de imagine."""
    data = request.json
    seed = data.get('seed', '')
    n = data.get('n', 3)
    
    results = fluxo.imagine(seed, n)
    
    return jsonify({
        'seed': seed,
        'imagined': results
    })

@app.route('/api/fluxo/predict', methods=['POST'])
def api_predict():
    """API de predict."""
    data = request.json
    context = data.get('context', '')
    
    result = fluxo.predict(context)
    
    return jsonify(result)

@app.route('/api/fluxo/learn', methods=['POST'])
def api_learn():
    """API de learn."""
    data = request.json
    pattern = data.get('pattern', '')
    context = data.get('context', {})
    
    stream_id = fluxo.learn(pattern, context)
    fluxo.save()
    
    return jsonify({
        'success': True,
        'stream_id': stream_id,
        'pattern': pattern
    })

@app.route('/api/fluxo/flow', methods=['POST'])
def api_flow():
    """API de flow."""
    data = request.json
    from_stream = data.get('from', '')
    to_stream = data.get('to', '')
    
    fluxo.flow(from_stream, to_stream)
    fluxo.save()
    
    return jsonify({
        'success': True,
        'current': fluxo.current.stream_id
    })

@app.route('/api/fluxo/settle', methods=['POST'])
def api_settle():
    """API de settle."""
    fluxo.settle()
    fluxo.save()
    
    return jsonify({
        'success': True,
        'streams': len(fluxo.streams)
    })

@app.route('/api/fluxo/rebuild', methods=['POST'])
def api_rebuild():
    """Reconstrói o FLUXO a partir das memórias."""
    fluxo.build_from_memories()
    
    return jsonify({
        'success': True,
        'streams': len(fluxo.streams),
        'confluences': sum(len(s.confluences) for s in fluxo.streams.values()),
        'eddies': len(fluxo.eddies)
    })

@app.route('/api/fluxo/depth/<float:depth>', methods=['GET'])
def api_get_by_depth(depth):
    """Retorna streams em uma profundidade específica."""
    streams = [
        {
            'id': k,
            'pattern': v.pattern,
            'depth': v.depth,
            'flow': v.flow,
            'category': v.category
        }
        for k, v in fluxo.streams.items()
        if abs(v.depth - depth) < 0.2
    ]
    
    return jsonify({
        'depth': depth,
        'streams': streams
    })

@app.route('/api/fluxo/stats')
def api_stats():
    """Estatísticas do FLUXO."""
    # Distribuição por profundidade
    depth_dist = {}
    for stream in fluxo.streams.values():
        depth_bucket = round(stream.depth, 1)
        depth_dist[depth_bucket] = depth_dist.get(depth_bucket, 0) + 1
    
    # Distribuição por categoria
    cat_dist = {}
    for stream in fluxo.streams.values():
        cat_dist[stream.category] = cat_dist.get(stream.category, 0) + 1
    
    # Flux médio
    avg_flow = sum(s.flow for s in fluxo.streams.values()) / max(1, len(fluxo.streams))
    
    return jsonify({
        'total_streams': len(fluxo.streams),
        'total_confluences': sum(len(s.confluences) for s in fluxo.streams.values()),
        'total_eddies': len(fluxo.eddies),
        'depth_distribution': depth_dist,
        'category_distribution': cat_dist,
        'average_flow': avg_flow,
        'current_stream': fluxo.current.stream_id,
        'current_history': fluxo.current.history[-5:]
    })

if __name__ == '__main__':
    print("=" * 70)
    print("FLUXO - Memória Temporal")
    print("=" * 70)
    print()
    print("Uma arquitetura de memória baseada na neurociência real:")
    print("- Streams (correntes) em vez de nodos")
    print("- Confluences em vez de arestas")
    print("- Depths em vez de camadas")
    print("- Current (correnteza) em vez de cursor")
    print()
    print("O FLUXO representa memória como PROCESSO TEMPORAL,")
    print("não como armazenamento estático.")
    print()
    
    # Carregar estado existente ou construir a partir das memórias
    if os.path.exists(fluxo.FLUXO_STATE if hasattr(fluxo, 'FLUXO_STATE') else 
                       os.path.join(WORKSPACE, 'FLUXO_STATE.json')):
        print("Carregando estado existente...")
        fluxo.load()
    else:
        print("Construindo FLUXO a partir das memórias...")
        fluxo.build_from_memories()
    
    print(f"Streams: {len(fluxo.streams)}")
    print(f"Confluences: {sum(len(s.confluences) for s in fluxo.streams.values())}")
    print(f"Eddies: {len(fluxo.eddies)}")
    print()
    print("Abra: http://localhost:5003")
    print()
    
    app.run(host='0.0.0.0', port=5003, debug=True)