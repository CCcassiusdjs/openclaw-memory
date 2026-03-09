const fs = require('fs');
const path = require('path');

const OUTPUT_FILE = 'file_system_index.json';
const MAX_NODES = 100000;
const MAX_DEPTH = 24;

const nodes = [];
const links = [];
const nodeMap = new Map();

// Skip directories for performance
const SKIP_DIRS = new Set([
    'node_modules', '.git', '__pycache__', 'venv', '.venv', 'env', '.env',
    'dist', 'build', '.cache', '.npm', '.config', 'cache', 'tmp', 'tmp',
    '.cargo', '.rustup', '.gradle', '.m2', '.android', '.thumbnails',
    'Trash', '.Trash', '.local', '.mozilla', '.cache'
]);

const SKIP_PREFIX = new Set(['.', '..']);

let fileCount = 0;
let dirCount = 0;

function shouldSkip(name) {
    return SKIP_PREFIX.has(name) || name.startsWith('.') || SKIP_DIRS.has(name);
}

function formatSize(bytes) {
    if (!bytes || bytes === 0) return 0;
    return bytes;
}

function scanDirectory(dirPath, depth = 1, parentId = null) {
    if (nodes.length >= MAX_NODES || depth > MAX_DEPTH) return;
    
    try {
        const entries = fs.readdirSync(dirPath, { withFileTypes: true });
        
        for (const entry of entries) {
            if (nodes.length >= MAX_NODES) break;
            if (shouldSkip(entry.name)) continue;
            
            const fullPath = path.join(dirPath, entry.name);
            const isDir = entry.isDirectory();
            const isFile = entry.isFile();
            
            if (!isDir && !isFile) continue;
            
            // Limit path length for display
            const displayName = entry.name.length > 40 ? entry.name.substring(0, 37) + '...' : entry.name;
            
            const node = {
                id: fullPath,
                name: displayName,
                type: isDir ? 'dir' : 'file',
                level: depth,
                size: 0,
                deps: []
            };
            
            // Get file size
            if (isFile) {
                try {
                    node.size = fs.statSync(fullPath).size;
                } catch (e) {}
            }
            
            nodes.push(node);
            nodeMap.set(fullPath, node);
            
            if (isDir) {
                dirCount++;
            } else {
                fileCount++;
            }
            
            // Create link to parent
            if (parentId) {
                links.push({ source: parentId, target: fullPath });
            }
            
            // Recurse into directories
            if (isDir && depth < MAX_DEPTH) {
                scanDirectory(fullPath, depth + 1, fullPath);
            }
        }
    } catch (e) {
        // Permission denied, etc. - skip
    }
}

console.log('Starting full file system index (24 levels)...');
console.time('Index Time');

// Start from root
console.log('Scanning root level...');
scanDirectory('/', 1, null);

// Also scan home in more detail
const homePath = process.env.HOME || '/home/csilva';
console.log('Scanning home directory:', homePath);

console.timeEnd('Index Time');

const result = {
    nodes: nodes,
    links: links,
    stats: {
        totalNodes: nodes.length,
        dirs: dirCount,
        files: fileCount,
        maxDepth: Math.max(...nodes.map(n => n.level)),
        timestamp: new Date().toISOString()
    }
};

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(result));
console.log(`\nIndex created: ${OUTPUT_FILE}`);
console.log(`Total nodes: ${nodes.length.toLocaleString()}`);
console.log(`Directories: ${dirCount.toLocaleString()}`);
console.log(`Files: ${fileCount.toLocaleString()}`);
console.log(`Max depth: ${result.stats.maxDepth}`);
console.log(`File size: ${(fs.statSync(OUTPUT_FILE).size / 1024 / 1024).toFixed(2)} MB`);
