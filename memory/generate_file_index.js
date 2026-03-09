const fs = require('fs');
const path = require('path');

// Configurações
const MAX_FILES = 50000; // Limite para performance
const MAX_DEPTH = 12; // Profundidade máxima
const OUTPUT_FILE = 'file_system_index.json';

let fileCount = 0;
let dirCount = 0;
const nodes = [];
const links = [];

// Extensões que indicam dependências
const CODE_EXTENSIONS = ['.js', '.ts', '.py', '.jsx', '.tsx', '.mjs', '.cjs', '.sh', '.bash', '.json'];
const DEPENDENCY_PATTERNS = {
    '.js': [/require\s*\(\s*['"]([^'"]+)['"]\s*\)/g, /import\s+.*from\s+['"]([^'"]+)['"]/g],
    '.ts': [/import\s+.*from\s+['"]([^'"]+)['"]/g, /require\s*\(\s*['"]([^'"]+)['"]\s*\)/g],
    '.py': [/^import\s+(\S+)/gm, /^from\s+(\S+)\s+import/gm],
    '.mjs': [/import\s+.*from\s+['"]([^'"]+)['"]/g],
    '.cjs': [/require\s*\(\s*['"]([^'"]+)['"]\s*\)/g],
};

function shouldScan(dirPath) {
    const skipDirs = ['node_modules', '.git', '__pycache__', 'venv', '.venv', 'env', '.env', 
                      'dist', 'build', '.cache', '.npm', '.config', 'cache', 'tmp'];
    const baseName = path.basename(dirPath);
    return !skipDirs.includes(baseName) && !baseName.startsWith('.');
}

function getDependencies(filePath, content) {
    const ext = path.extname(filePath);
    const deps = [];
    
    if (!DEPENDENCY_PATTERNS[ext]) return deps;
    
    const patterns = DEPENDENCY_PATTERNS[ext];
    patterns.forEach(pattern => {
        let match;
        const regex = new RegExp(pattern.source, pattern.flags);
        while ((match = regex.exec(content)) !== null) {
            if (match[1] && !match[1].startsWith('.') === false) {
                // Resolver caminhos relativos seria complexo, vamos só capturar
                deps.push(match[1]);
            }
        }
    });
    
    return [...new Set(deps)].slice(0, 20); // Limitar dependências
}

function scanDirectory(dirPath, depth = 1, parentId = null) {
    if (fileCount >= MAX_FILES || depth > MAX_DEPTH) return;
    
    try {
        const entries = fs.readdirSync(dirPath, { withFileTypes: true });
        
        for (const entry of entries) {
            if (fileCount >= MAX_FILES) break;
            
            const fullPath = path.join(dirPath, entry.name);
            const isDir = entry.isDirectory();
            const isFile = entry.isFile();
            
            if (!isDir && !isFile) continue;
            
            const node = {
                id: fullPath,
                name: entry.name,
                type: isDir ? 'dir' : 'file',
                level: depth,
                deps: [],
                size: 0
            };
            
            // Adicionar ao grafo
            nodes.push(node);
            if (isDir) dirCount++; else fileCount++;
            
            // Link com pai
            if (parentId) {
                links.push({ source: parentId, target: fullPath });
            }
            
            if (isDir && shouldScan(fullPath)) {
                scanDirectory(fullPath, depth + 1, fullPath);
            } else if (isFile && CODE_EXTENSIONS.includes(path.extname(fullPath))) {
                // Extrair dependências de arquivos de código
                try {
                    const content = fs.readFileSync(fullPath, 'utf8').slice(0, 10000);
                    node.deps = getDependencies(fullPath, content);
                } catch (e) {}
            }
            
            // Tentar obter tamanho
            try {
                if (isFile) {
                    node.size = fs.statSync(fullPath).size;
                }
            } catch (e) {}
        }
    } catch (e) {
        // Ignorar erros de permissão
    }
}

console.log('Starting file system index...');
console.time('Scan');

// Escanear a partir da raiz
try {
    scanDirectory('/', 1, null);
} catch (e) {
    console.log('Root scan failed, trying home...');
}

// Se não escaneou muito, tentar home
if (nodes.length < 1000) {
    console.log('Scanning home directory...');
    const homePath = process.env.HOME || '/home/csilva';
    scanDirectory(homePath, 1, null);
}

console.timeEnd('Scan');

const result = {
    nodes: nodes,
    links: links,
    stats: {
        totalNodes: nodes.length,
        dirs: nodes.filter(n => n.type === 'dir').length,
        files: nodes.filter(n => n.type === 'file').length,
        timestamp: new Date().toISOString()
    }
};

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(result, null, 2));
console.log(`\nIndex created: ${OUTPUT_FILE}`);
console.log(`Nodes: ${nodes.length} (${dirCount} dirs, ${fileCount} files)`);
console.log(`Links: ${links.length}`);
