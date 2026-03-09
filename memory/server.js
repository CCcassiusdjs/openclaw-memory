#!/usr/bin/env node
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8765;
const BASE_DIR = __dirname;

const MIME_TYPES = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.txt': 'text/plain',
    '.css': 'text/css'
};

const server = http.createServer((req, res) => {
    let filePath = req.url === '/' ? '/file_tree_spherical.html' : req.url;
    filePath = BASE_DIR + filePath;
    
    const ext = path.extname(filePath);
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';
    
    // Handle large files with streaming
    if (filePath.endsWith('.txt') || filePath.endsWith('.jsonl')) {
        const stat = fs.statSync(filePath);
        res.writeHead(200, {
            'Content-Type': 'text/plain',
            'Content-Length': stat.size
        });
        fs.createReadStream(filePath).pipe(res);
        return;
    }
    
    fs.readFile(filePath, (err, content) => {
        if (err) {
            res.writeHead(404);
            res.end('Not found');
            return;
        }
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content);
    });
});

server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log(`Open http://localhost:${PORT}/file_tree_spherical.html`);
});