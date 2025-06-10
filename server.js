const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const LANGUAGE_EXT = {
  python: '.py',
  javascript: '.js',
  ruby: '.rb',
  php: '.php',
  perl: '.pl',
  c: '.c',
  cpp: '.cpp',
  java: '.java'
};

function runCode(lang, code) {
  const ext = LANGUAGE_EXT[lang];
  if (!ext) {
    return `Unsupported language: ${lang}`;
  }
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'code-'));
  const file = path.join(dir, 'prog' + ext);
  fs.writeFileSync(file, code);
  const result = spawnSync('python3', ['run_code.py', file], { encoding: 'utf8' });
  return result.stdout + result.stderr;
}

function handleRequest(req, res) {
  if (req.method === 'POST' && req.url === '/run') {
    let body = '';
    req.on('data', chunk => (body += chunk));
    req.on('end', () => {
      const params = new URLSearchParams(body);
      const lang = params.get('language');
      const code = params.get('code') || '';
      const output = runCode(lang, code);
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end(output);
    });
  } else {
    const options = Object.keys(LANGUAGE_EXT)
      .map(l => `<option value="${l}">${l}</option>`) 
      .join('\n');
    const page = `<!doctype html>
<title>Code Runner</title>
<form method="post" action="/run">
<select name="language">
${options}
</select><br>
<textarea name="code" rows="10" cols="40"></textarea><br>
<input type="submit" value="Run">
</form>`;
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(page);
  }
}

if (require.main === module) {
  const port = parseInt(process.env.PORT || '8000', 10);
  http.createServer(handleRequest).listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
} else {
  module.exports = { runCode, handleRequest };
}
