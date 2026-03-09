const fs = require('fs');
const { execSync } = require('child_process');

const OUTPUT_DIR = './fs_index';
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

console.log('=== INDEXAÇÃO COMPLETA (STREAMING) ===\n');

// Get all paths
console.log('Coletando caminhos...');
const files = execSync('find / -type f 2>/dev/null', { maxBuffer: 1024*1024*1024, timeout: 600000 }).toString().split('\n').filter(f => f.trim());
const dirs = execSync('find / -type d 2>/dev/null', { maxBuffer: 1024*1024*1024, timeout: 300000 }).toString().split('\n').filter(d => d.trim());

console.log(`Total: ${files.length.toLocaleString()} arquivos, ${dirs.length.toLocaleString()} diretórios`);

// Write metadata
const metadata = {
    totalFiles: files.length,
    totalDirs: dirs.length,
    maxDepth: 24,
    timestamp: new Date().toISOString()
};
fs.writeFileSync(`${OUTPUT_DIR}/metadata.json`, JSON.stringify(metadata));

// Write directories as JSONL (one per line)
console.log('Salvando diretórios...');
const dirsStream = fs.createWriteStream(`${OUTPUT_DIR}/dirs.jsonl`);
dirs.forEach(d => {
    if (!d) return;
    const parts = d.split('/').filter(p => p);
    const name = parts[parts.length - 1] || '/';
    const level = parts.length + 1;
    const parentId = parts.length === 1 ? '/' : '/' + parts.slice(0, -1).join('/');
    dirsStream.write(JSON.stringify({ id: d, n: name, t: 'd', l: level, p: parentId }) + '\n');
});
dirsStream.end();

// Write files as JSONL
console.log('Salvando arquivos...');
const filesStream = fs.createWriteStream(`${OUTPUT_DIR}/files.jsonl`);
let count = 0;
files.forEach(f => {
    if (!f) return;
    const parts = f.split('/').filter(p => p);
    const name = parts[parts.length - 1] || 'file';
    const level = parts.length + 1;
    const parentId = '/' + parts.slice(0, -1).join('/');
    let size = 0;
    try { size = fs.statSync(f).size; } catch (e) {}
    filesStream.write(JSON.stringify({ id: f, n: name, t: 'f', l: level, s: size, p: parentId }) + '\n');
    count++;
    if (count % 500000 === 0) console.log(`  ${count.toLocaleString()}...`);
});
filesStream.end();

console.log('\n=== CONCLUÍDO ===');
console.log(`Metadata: ${OUTPUT_DIR}/metadata.json`);
console.log(`Dirs: ${OUTPUT_DIR}/dirs.jsonl`);
console.log(`Files: ${OUTPUT_DIR}/files.jsonl`);
