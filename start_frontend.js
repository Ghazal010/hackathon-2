#!/usr/bin/env node
/**
 * Script to start the frontend server for the Todo App
 */
const { spawn } = require('child_process');
const path = require('path');

function startFrontend() {
  const frontendDir = path.join(__dirname, 'frontend');

  console.log('Starting frontend server on http://localhost:3000');
  console.log('Press Ctrl+C to stop the server');

  const npm = /^win/.test(process.platform) ? 'npm.cmd' : 'npm';
  const child = spawn(npm, ['run', 'dev'], {
    cwd: frontendDir,
    stdio: 'inherit'
  });

  child.on('error', (err) => {
    console.error('Failed to start frontend:', err.message);
  });
}

startFrontend();