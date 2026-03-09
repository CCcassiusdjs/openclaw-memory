const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const OUTPUT_FILE = 'file_system_complete.json';

console.log('=== INDEXAÇÃO COMPLETA DO SISTEMA DE ARQUIVOS ===\n');

// Get all files using find
console.log('Coletando todos os arquivos...');
let findOutput;
try {
    findOutput = execSync('find / -type f 2>/dev/null', { 
        maxBuffer: 1024 * 1024 * 1024,
        timeout: 600000 
    }).toString();
} catch (e) {
    findOutput = e.stdout ? e.stdout.toString() : '';
}

console.log('Coletando todos os diretórios...');
let findDirOutput;
try {
    findDirOutput = execSync('find / -type d 2>/dev/null', {
        maxBuffer: 1024 * 1024 * 1024,
        timeout: 300000
    }).toString();
} catch (e) {
    findDirOutput = e.stdout ? e.stdout.toString() : '';
}

// Parse results
const files = findOutput.split('\n').filter(f => f.trim());
const dirs = findDirOutput.split('\n').filter(d => d.trim());

console.log(`Arquivos: ${files.length.toLocaleString()}`);
console.log(`Diretórios: ${dirs.length.toLocaleString()}`);

// Build nodes incrementally
const nodes = [];
const links = [];
const nodeMap = new Map();
let maxDepth = 1;

// Add root
nodes.push({ id: '/', name: '/', type: 'dir', level: 1 });
nodeMap.set('/', 1);

// Process directories
console.log('\nProcessando diretórios...');
dirs.forEach(d => {
    if (!d || d === '/') return;
    const parts = d.split('/').filter(p => p);
    const name = parts[parts.length - 1] || '/';
    const level = parts.length + 1;
    const parentId = parts.length === 1 ? '/' : '/' + parts.slice(0, -1).join('/');
    
    if (level > maxDepth) maxDepth = level;
    
    nodes.push({
        id: d,
        name: name.length > 50 ? name.substring(0, 47) + '...' : name,
        type: 'dir',
        level: level
    });
    nodeMap.set(d, level);
    
    if (nodeMap.has(parentId)) {
        links.push({ source: parentId, target: d });
    }
});

// Process files
console.log('Processando arquivos...');
let processedFiles = 0;
files.forEach(f => {
    if (!f) return;
    const parts = f.split('/').filter(p => p);
    const name = parts[parts.length - 1] || 'file';
    const level = parts.length + 1;
    const parentId = '/' + parts.slice(0, -1).join('/');
    
    if (level > maxDepth) maxDepth = level;
    
    let size = 0;
    try {
        size = fs.statSync(f).size;
    } catch (e) {}
    
    nodes.push({
        id: f,
        name: name.length > 50 ? name.substring(0, 47) + '...' : name,
        type: 'file',
        level: level,
        size: size
    });
    
    if (nodeMap.has(parentId)) {
        links.push({ source: parentId, target: f });
    }
    
    processedFiles++;
    if (processedFiles % 500000 === 0) {
        console.log(`  ${processedFiles.toLocaleString()} arquivos...`);
    }
});

const stats = {
    totalNodes: nodes.length,
    dirs: nodes.filter(n => n.type === 'dir').length,
    files: nodes.filter(n => n.type === 'file').length,
    maxDepth: maxDepth,
    timestamp: new Date().toISOString()
};

console.log('\nSalvando...');
const result = { nodes, links, stats };
fs.writeFileSync(OUTPUT_FILE, JSON.stringify(result));

console.log('\n=== RESULTADO ===');
console.log(`Total de nós: ${stats.totalNodes.toLocaleString()}`);
console.log(`Diretórios: ${stats.dirs.toLocaleString()}`);
console.log(`Arquivos: ${stats.files.toLocaleString()}`);
console.log(`Profundidade máxima: ${stats.maxDepth}`);
console.log(`Tamanho: ${(fs.statSync(OUTPUT_FILE).size / 1024 / 1024).toFixed(2)} MB`);
