const fs = require('fs');

console.log('Optimizing index...');
const data = JSON.parse(fs.readFileSync('file_system_index.json', 'utf8'));

// Simplify nodes - only keep essential fields
const optimizedNodes = data.nodes.map(n => ({
    id: n.id,
    n: n.name,      // shortened key
    t: n.type,      // shortened key
    l: n.level,     // shortened key
    s: n.size       // shortened key
}));

// Simplify links
const optimizedLinks = data.links.map(l => ({
    s: l.source,
    t: l.target
}));

const optimized = {
    nodes: optimizedNodes,
    links: optimizedLinks,
    stats: data.stats
};

fs.writeFileSync('file_system_optimized.json', JSON.stringify(optimized));
console.log('Optimized file size:', (fs.statSync('file_system_optimized.json').size / 1024 / 1024).toFixed(2), 'MB');

// Create a smaller sample for faster loading
const sampleNodes = optimizedNodes.slice(0, 10000);
const sampleLinks = optimizedLinks.filter(l => 
    sampleNodes.find(n => n.id === l.s) && sampleNodes.find(n => n.id === l.t)
);

const sample = {
    nodes: sampleNodes,
    links: sampleLinks,
    stats: { ...data.stats, totalNodes: sampleNodes.length, isSample: true }
};

fs.writeFileSync('file_system_sample.json', JSON.stringify(sample));
console.log('Sample file size:', (fs.statSync('file_system_sample.json').size / 1024 / 1024).toFixed(2), 'MB');
console.log('Sample nodes:', sampleNodes.length);
