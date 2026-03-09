const fs = require('fs');

console.log('Dividindo dados por nível...');

const dirs = fs.readFileSync('fs_index/dirs.txt', 'utf8').split('\n').filter(d => d.trim());
const files = fs.readFileSync('fs_index/files.txt', 'utf8').split('\n').filter(f => f.trim());

console.log(`Total: ${dirs.length} dirs, ${files.length} files`);

// Group by level
const byLevel = {};
const nodeMap = new Map();

// Add root
byLevel[1] = [{ id: '/', n: '/', t: 'd', l: 1 }];
nodeMap.set('/', 1);

// Process directories
console.log('Processando diretórios...');
dirs.forEach(d => {
    if (!d || d === '/') return;
    const parts = d.split('/').filter(p => p);
    const level = parts.length + 1;
    const name = parts[parts.length - 1].substring(0, 50);
    const parentId = parts.length === 1 ? '/' : '/' + parts.slice(0, -1).join('/');
    
    if (!byLevel[level]) byLevel[level] = [];
    byLevel[level].push({ id: d, n: name, t: 'd', l: level, p: parentId });
    nodeMap.set(d, level);
});

// Sample files (1/10 for levels <= 10, 1/100 for higher)
console.log('Processando arquivos...');
const fileSampleRate = 0.05; // 5% of files
files.forEach((f, i) => {
    if (!f || Math.random() > fileSampleRate) return;
    
    const parts = f.split('/').filter(p => p);
    const level = parts.length + 1;
    const name = parts[parts.length - 1].substring(0, 50);
    const parentId = '/' + parts.slice(0, -1).join('/');
    
    if (!byLevel[level]) byLevel[level] = [];
    byLevel[level].push({ id: f, n: name, t: 'f', l: level, p: parentId });
});

// Write each level to separate file
console.log('Salvando arquivos por nível...');
for (let level = 1; level <= 24; level++) {
    if (byLevel[level] && byLevel[level].length > 0) {
        fs.writeFileSync(`fs_index/level_${level}.json`, JSON.stringify(byLevel[level]));
        console.log(`Level ${level}: ${byLevel[level].length} nodes`);
    }
}

// Create index file
const index = {
    levels: Object.keys(byLevel).map(Number).sort((a,b) => a-b),
    counts: {},
    totalNodes: Object.values(byLevel).reduce((sum, arr) => sum + arr.length, 0)
};
for (let l in byLevel) {
    index.counts[l] = byLevel[l].length;
}
fs.writeFileSync('fs_index/index.json', JSON.stringify(index));

console.log(`\nTotal nodes: ${index.totalNodes.toLocaleString()}`);
console.log('Done!');
