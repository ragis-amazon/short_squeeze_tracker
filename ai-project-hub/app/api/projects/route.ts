import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    const projects: any[] = [];
    
    // Read markdown docs
    const docsDir = path.join(process.cwd(), 'docs');
    if (fs.existsSync(docsDir)) {
      const docFiles = fs.readdirSync(docsDir).filter(file => file.endsWith('.md'));
      docFiles.forEach(file => {
        const filePath = path.join(docsDir, file);
        const stats = fs.statSync(filePath);
        projects.push({
          id: `doc-${file}`,
          title: file.replace('.md', '').replace(/-/g, ' '),
          type: 'doc',
          path: filePath,
          lastModified: stats.mtime.toISOString(),
        });
      });
    }

    // Read code prototypes
    const prototypesDir = path.join(process.cwd(), 'prototypes');
    if (fs.existsSync(prototypesDir)) {
      const prototypeDirs = fs.readdirSync(prototypesDir, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory())
        .map(dirent => dirent.name);
      
      prototypeDirs.forEach(dir => {
        const dirPath = path.join(prototypesDir, dir);
        const stats = fs.statSync(dirPath);
        // Look for main file (prefer index.js, index.ts, main.js, main.ts, or first .js/.ts file)
        const files = fs.readdirSync(dirPath);
        const mainFile = files.find(f => f === 'index.js' || f === 'index.ts' || f === 'main.js' || f === 'main.ts') 
          || files.find(f => f.endsWith('.js') || f.endsWith('.ts') || f.endsWith('.py'));
        
        if (mainFile) {
          projects.push({
            id: `prototype-${dir}`,
            title: dir.replace(/-/g, ' '),
            type: 'prototype',
            path: path.join(dirPath, mainFile),
            lastModified: stats.mtime.toISOString(),
          });
        }
      });
    }

    // Sort by last modified
    projects.sort((a, b) => new Date(b.lastModified).getTime() - new Date(a.lastModified).getTime());

    return NextResponse.json(projects);
  } catch (error) {
    console.error('Error reading projects:', error);
    return NextResponse.json({ error: 'Failed to load projects' }, { status: 500 });
  }
}

