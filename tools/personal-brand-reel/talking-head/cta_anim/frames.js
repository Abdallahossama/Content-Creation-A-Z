// Render an animated HTML (window.render(t)) to a transparent PNG sequence via headless Edge + CDP.
// usage: node frames.js call_a.html outDir seconds [W H]
const { spawn } = require('child_process'); const fs = require('fs'); const path = require('path');
const [, , html, outDir, secs, W = 1080, H = 720] = process.argv;
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', PORT = 9333 + Math.floor(Math.random() * 500);
const prof = path.resolve(__dirname, 'edge_prof_' + PORT);
fs.mkdirSync(outDir, { recursive: true });
const ed = spawn(EDGE, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', `--remote-debugging-port=${PORT}`, `--user-data-dir=${prof}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let tgt;
  for (let i = 0; i < 60 && !tgt; i++) { try { tgt = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find(x => x.type === 'page'); } catch { } if (!tgt) await sleep(250); }
  const ws = new WebSocket(tgt.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pend = {}; const ev = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend[d.id]) { pend[d.id](d); delete pend[d.id]; } else ev.push(d.method); };
  const cmd = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
  await cmd('Page.enable');
  await cmd('Emulation.setDeviceMetricsOverride', { width: +W, height: +H, deviceScaleFactor: 1, mobile: false });
  await cmd('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
  await cmd('Page.navigate', { url: 'file:///' + path.resolve(html).replace(/\\/g, '/') });
  for (let i = 0; i < 40 && !ev.includes('Page.loadEventFired'); i++) await sleep(100);
  await cmd('Runtime.evaluate', { expression: 'document.fonts.ready.then(()=>1)', awaitPromise: true }); await sleep(300);
  const N = Math.round(+secs * 30);
  for (let f = 0; f < N; f++) {
    await cmd('Runtime.evaluate', { expression: `render(${(f / 30).toFixed(4)})` });
    const r = await cmd('Page.captureScreenshot', { format: 'png', fromSurface: true });
    fs.writeFileSync(path.join(outDir, `f${String(f).padStart(4, '0')}.png`), Buffer.from(r.result.data, 'base64'));
  }
  ws.close(); ed.kill(); await sleep(500); try { fs.rmSync(prof, { recursive: true, force: true }); } catch { }
  console.log('frames', N, outDir);
})().catch(e => { console.error(e); ed.kill(); process.exit(1); });
