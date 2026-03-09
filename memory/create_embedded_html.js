const fs = require('fs');

console.log('Criando HTML com dados embutidos...');

// Read directories
const dirs = fs.readFileSync('fs_index/dirs.txt', 'utf8').split('\n').filter(d => d.trim());
const files = fs.readFileSync('fs_index/files.txt', 'utf8').split('\n').filter(f => f.trim());

console.log(`Dirs: ${dirs.length}, Files: ${files.length}`);

// Build hierarchical structure (sample for visualization)
const nodes = [];
const links = [];
const nodeMap = new Map();

// Add root
nodes.push({ id: '/', n: '/', t: 'd', l: 1 });
nodeMap.set('/', true);

// Sample strategy: include all dirs, sample files
const MAX_FILES = 100000; // Limit files for performance
let fileCount = 0;

// Process all directories
console.log('Processing directories...');
dirs.forEach(d => {
    if (!d || d === '/') return;
    const parts = d.split('/').filter(p => p);
    const name = parts[parts.length - 1];
    const level = parts.length + 1;
    const parentId = parts.length === 1 ? '/' : '/' + parts.slice(0, -1).join('/');
    
    nodes.push({ id: d, n: name.substring(0, 40), t: 'd', l: level });
    nodeMap.set(d, true);
    
    if (nodeMap.has(parentId)) {
        links.push({ s: parentId, t: d });
    }
});

// Sample files (1 in every ~28 files to get ~100k)
const fileStep = Math.ceil(files.length / MAX_FILES);
console.log(`Processing 1 in every ${fileStep} files...`);
files.forEach((f, i) => {
    if (!f || i % fileStep !== 0) return;
    
    const parts = f.split('/').filter(p => p);
    const name = parts[parts.length - 1];
    const level = parts.length + 1;
    const parentId = '/' + parts.slice(0, -1).join('/');
    
    nodes.push({ id: f, n: name.substring(0, 40), t: 'f', l: level });
    
    if (nodeMap.has(parentId)) {
        links.push({ s: parentId, t: f });
    }
    
    fileCount++;
});

console.log(`Total nodes: ${nodes.length}, links: ${links.length}`);

const data = { nodes, links };
const dataStr = JSON.stringify(data);

console.log(`Data size: ${(dataStr.length / 1024 / 1024).toFixed(2)} MB`);

// Create HTML with embedded data
const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File System Explorer - ${nodes.length.toLocaleString()} Nodes</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://unpkg.com/3d-force-graph@1.73.0/dist/3d-force-graph.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { overflow: hidden; background: #000; font-family: -apple-system, sans-serif; }
        #container { width: 100vw; height: 100vh; }
        
        #search-container {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 100;
            width: 500px;
        }
        #search-box {
            width: 100%;
            padding: 14px 20px;
            font-size: 15px;
            border: 2px solid rgba(0,255,136,0.3);
            border-radius: 25px;
            background: rgba(0,0,0,0.9);
            color: #fff;
            outline: none;
        }
        #search-box:focus { border-color: #00ff88; }
        #search-results {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.95);
            border-radius: 15px;
            margin-top: 5px;
            max-height: 300px;
            overflow-y: auto;
            display: none;
        }
        .search-result {
            padding: 10px 15px;
            cursor: pointer;
            color: #fff;
            border-bottom: 1px solid #222;
        }
        .search-result:hover { background: rgba(0,255,136,0.2); }
        .search-name { font-weight: 500; }
        .search-path { font-size: 11px; color: #666; font-family: monospace; }
        
        #stats {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.9);
            padding: 15px 20px;
            border-radius: 15px;
            color: #00ff88;
            font-size: 13px;
            z-index: 100;
        }
        #stats .big { font-size: 28px; font-weight: bold; }
        #stats .row { margin: 5px 0; }
        
        #controls {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 10px;
            z-index: 100;
        }
        #controls button {
            background: rgba(0,0,0,0.9);
            color: #fff;
            border: 1px solid #333;
            padding: 10px 18px;
            border-radius: 10px;
            cursor: pointer;
        }
        #controls button:hover { border-color: #00ff88; }
        
        #node-panel {
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(0,0,0,0.95);
            padding: 20px;
            border-radius: 15px;
            color: #fff;
            min-width: 300px;
            display: none;
            border: 1px solid #00ff88;
        }
        #node-panel.visible { display: block; }
        #node-panel h3 { color: #00ff88; margin-bottom: 5px; }
        #node-panel .path { font-family: monospace; font-size: 11px; color: #888; margin-bottom: 15px; word-break: break-all; }
        #node-panel .btn {
            width: 100%;
            padding: 10px;
            margin-top: 8px;
            background: #00ff88;
            color: #000;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        
        #level-btns {
            position: absolute;
            bottom: 20px;
            right: 20px;
            display: flex;
            gap: 10px;
            z-index: 100;
        }
        #level-btns button {
            background: rgba(0,0,0,0.9);
            color: #00ff88;
            border: 1px solid #00ff88;
            padding: 10px 15px;
            border-radius: 10px;
            cursor: pointer;
        }
        #level-btns button:hover { background: rgba(0,255,136,0.2); }
        
        #loading {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            z-index: 1000;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid #222;
            border-top-color: #00ff88;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        #loading .text { color: #00ff88; font-size: 16px; }
    </style>
</head>
<body>
    <div id="container"></div>
    
    <div id="stats">
        <div class="row"><span class="big" id="total">0</span></div>
        <div class="row">nodes loaded</div>
        <div class="row"><span id="dirs">0</span> dirs • <span id="files">0</span> files</div>
    </div>
    
    <div id="search-container">
        <input type="text" id="search-box" placeholder="Search files...">
        <div id="search-results"></div>
    </div>
    
    <div id="controls">
        <button onclick="toggleLabels()">Labels</button>
        <button onclick="resetView()">Reset</button>
    </div>
    
    <div id="node-panel">
        <h3 id="node-name">-</h3>
        <div class="path" id="node-path">-</div>
        <div>Type: <span id="node-type">-</span></div>
        <div>Level: <span id="node-level">-</span></div>
        <button class="btn" onclick="focusNode()">Focus</button>
    </div>
    
    <div id="level-btns">
        <button onclick="loadLevel(1)">Level 1</button>
        <button onclick="loadLevel(3)">Level 3</button>
        <button onclick="loadLevel(5)">Level 5</button>
        <button onclick="loadLevel(10)">Level 10</button>
        <button onclick="loadAll()">ALL</button>
    </div>
    
    <div id="loading">
        <div class="spinner"></div>
        <div class="text">Loading ${nodes.length.toLocaleString()} nodes...</div>
    </div>

    <script>
        const ALL_DATA = ${dataStr};
        
        let Graph = null;
        let currentData = { nodes: [], links: [] };
        let maxLevel = 0;
        let selectedNode = null;
        let showLabels = false;
        
        function getColor(n) {
            if (n.id === '/') return '#00ff88';
            if (n.t === 'd') return '#00ffff';
            return '#ff6600';
        }
        
        function getSize(n) {
            if (n.id === '/') return 25;
            if (n.t === 'd') return 6;
            return 3;
        }
        
        function init() {
            // Start with level 1-3
            loadLevel(3);
        }
        
        function loadLevel(level) {
            maxLevel = level;
            
            currentData.nodes = ALL_DATA.nodes.filter(n => n.l <= level);
            
            const nodeIds = new Set(currentData.nodes.map(n => n.id));
            currentData.links = ALL_DATA.links.filter(l => nodeIds.has(l.s) && nodeIds.has(l.t));
            
            const dirCount = currentData.nodes.filter(n => n.t === 'd').length;
            const fileCount = currentData.nodes.filter(n => n.t === 'f').length;
            
            document.getElementById('total').textContent = currentData.nodes.length.toLocaleString();
            document.getElementById('dirs').textContent = dirCount.toLocaleString();
            document.getElementById('files').textContent = fileCount.toLocaleString();
            document.getElementById('loading').style.display = 'none';
            
            if (!Graph) {
                Graph = ForceGraph3D()(document.getElementById('container'))
                    .graphData(currentData)
                    .nodeId('id')
                    .nodeLabel(n => n.n + '\\n' + n.id)
                    .nodeColor(getColor)
                    .nodeSize(getSize)
                    .nodeOpacity(0.8)
                    .linkColor(() => 'rgba(100,150,200,0.15)')
                    .linkWidth(0.3)
                    .linkOpacity(0.2)
                    .backgroundColor('#000810')
                    .enableNodeDrag(true)
                    .enableNavigationControls(true)
                    .warmupTicks(50)
                    .cooldownTicks(30)
                    .onNodeClick(n => { if (n) selectNode(n); });
                
                Graph.cameraPosition({ x: 0, y: 0, z: 400 });
            } else {
                Graph.graphData(currentData);
            }
        }
        
        function loadAll() {
            loadLevel(24);
        }
        
        function selectNode(n) {
            selectedNode = n;
            document.getElementById('node-panel').classList.add('visible');
            document.getElementById('node-name').textContent = n.n;
            document.getElementById('node-path').textContent = n.id;
            document.getElementById('node-type').textContent = n.t === 'd' ? 'Directory' : 'File';
            document.getElementById('node-level').textContent = n.l;
            focusNode();
        }
        
        function focusNode() {
            if (!selectedNode) return;
            const dist = 100;
            Graph.cameraPosition(
                { x: selectedNode.x + dist, y: selectedNode.y + dist, z: selectedNode.z + dist },
                selectedNode,
                1000
            );
        }
        
        function resetView() {
            Graph.cameraPosition({ x: 0, y: 0, z: 400 }, { x: 0, y: 0, z: 0 }, 1000);
            document.getElementById('node-panel').classList.remove('visible');
        }
        
        function toggleLabels() {
            showLabels = !showLabels;
            Graph.nodeLabel(n => showLabels ? n.n : '');
        }
        
        // Search
        const searchBox = document.getElementById('search-box');
        const searchResults = document.getElementById('search-results');
        
        searchBox.addEventListener('input', e => {
            const q = e.target.value.toLowerCase();
            if (q.length < 2) { searchResults.style.display = 'none'; return; }
            
            const matches = currentData.nodes.filter(n => 
                n.n.toLowerCase().includes(q) || n.id.toLowerCase().includes(q)
            ).slice(0, 20);
            
            if (matches.length) {
                searchResults.innerHTML = matches.map(m => 
                    '<div class="search-result" data-id="' + m.id + '">' +
                    '<div class="search-name">' + m.n + '</div>' +
                    '<div class="search-path">' + m.id + '</div></div>'
                ).join('');
                searchResults.style.display = 'block';
                
                document.querySelectorAll('.search-result').forEach(el => {
                    el.onclick = () => {
                        const n = currentData.nodes.find(x => x.id === el.dataset.id);
                        if (n) selectNode(n);
                        searchResults.style.display = 'none';
                        searchBox.value = '';
                    };
                });
            } else {
                searchResults.innerHTML = '<div class="search-result" style="color:#666">No results</div>';
                searchResults.style.display = 'block';
            }
        });
        
        document.addEventListener('click', e => {
            if (!searchBox.contains(e.target)) searchResults.style.display = 'none';
        });
        
        window.onload = init;
        window.onresize = () => Graph && Graph.width(window.innerWidth).height(window.innerHeight);
    </script>
</body>
</html>`;

fs.writeFileSync('file_tree_complete.html', html);
console.log(`Created file_tree_complete.html (${(fs.statSync('file_tree_complete.html').size / 1024 / 1024).toFixed(2)} MB)`);
