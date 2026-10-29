"""Real 'receipt' capture: screenshot a source page (study, article) at 2x in the installed Edge and record where
each key phrase sits, so the editor can drop highlighter / marker circles exactly on the words.

  uv run --no-project --with playwright python receipt.py <url> <out.png> "phrase one" "phrase two" ...

Writes <out.png> (full page, 2x) and <out.json>: {"scale": 2, "phrases": {phrase: [[x0,y0,x1,y1], ...one box per line]}}
Phrases are matched case-insensitively with whitespace collapsed; a phrase may wrap across lines (several boxes).
"""
import sys, json
from playwright.sync_api import sync_playwright

JS = r"""
(phrases) => {
  const norm = s => s.toLowerCase();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = []; let n;
  while ((n = walker.nextNode())) {
    const el = n.parentElement;
    if (!el || ['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName)) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    nodes.push(n);
  }
  // one flat string of all visible text with whitespace collapsed, plus a map back to (node, offset)
  let flat = '', map = [], prevSpace = true;
  for (const node of nodes) {
    const t = node.data;
    for (let i = 0; i < t.length; i++) {
      const ch = /\s/.test(t[i]) ? ' ' : t[i];
      if (ch === ' ' && prevSpace) continue;
      flat += ch; map.push([node, i]); prevSpace = ch === ' ';
    }
  }
  const low = norm(flat), out = {};
  for (const p of phrases) {
    const q = norm(p.replace(/\s+/g, ' ').trim());
    const at = low.indexOf(q);
    if (at < 0) { out[p] = null; continue; }
    const [n0, o0] = map[at], [n1, o1] = map[at + q.length - 1];
    const rg = document.createRange(); rg.setStart(n0, o0); rg.setEnd(n1, o1 + 1);
    out[p] = Array.from(rg.getClientRects()).filter(r => r.width > 1)
      .map(r => [r.left + scrollX, r.top + scrollY, r.right + scrollX, r.bottom + scrollY]);
  }
  return out;
}
"""

def main():
    url, out, phrases = sys.argv[1], sys.argv[2], sys.argv[3:]
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        pg = b.new_page(viewport={"width": 1400, "height": 1300}, device_scale_factor=2)
        try:
            pg.goto(url, wait_until="networkidle", timeout=30000)
        except Exception:                      # ad-heavy news sites never go idle: take the page once it has loaded
            pg.wait_for_load_state("domcontentloaded", timeout=60000); pg.wait_for_timeout(5000)
        pg.wait_for_timeout(1500)
        boxes = pg.evaluate(JS, phrases)
        pg.screenshot(path=out, full_page=True)
        b.close()
    S = 2
    res = {"url": url, "scale": S,
           "phrases": {k: (None if v is None else [[round(c * S) for c in r] for r in v]) for k, v in boxes.items()}}
    json.dump(res, open(out.rsplit(".", 1)[0] + ".json", "w", encoding="utf-8"), indent=1)
    for k, v in res["phrases"].items():
        print(("MISSING " if v is None else f"{len(v)} box  ") + k)

if __name__ == "__main__":
    main()
