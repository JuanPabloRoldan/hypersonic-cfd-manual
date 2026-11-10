"""Open every built page in headless Chrome and report rendering problems.

Run after `mkdocs build --strict`, from the repository root:

    python scripts/check_render.py            # checks ./site
    python scripts/check_render.py --shots /tmp/shots   # also save full-page PNGs

It fails (exit code 1) if any page has

  * a MathJax error, or an equation that still shows a raw backslash command;
  * a `$...$` or `\\(` left in the visible text (math that was never picked up);
  * an image that didn't load, or a display equation, image or table wider than
    the text column;
  * a course reference ("Track 6", "checkpoint", "lesson") in the visible text.

Needs `pip install playwright` and a Chrome or Chromium binary (set CHROME_PATH
if it isn't /usr/bin/google-chrome). The site loads MathJax and Mermaid from
CDNs. On a machine without internet access, install them locally with
`npm install mathjax@3 mermaid@11` in some directory and point LOCAL_NPM at it;
the script then serves those files in place of the CDN requests.
"""

import argparse
import asyncio
import functools
import http.server
import os
import re
import sys
import threading
from pathlib import Path

from playwright.async_api import async_playwright

CHROME = os.environ.get("CHROME_PATH", "/usr/bin/google-chrome")
LOCAL_NPM = os.environ.get("LOCAL_NPM")

PAGE_JS = r"""
() => {
  const out = {};
  out.merror = document.querySelectorAll('mjx-merror').length;
  out.rawMath = Array.from(document.querySelectorAll('mjx-container'))
    .map(c => c.textContent).filter(t => t.includes('\\')).slice(0, 3);
  const article = document.querySelector('article') || document.body;
  const clone = article.cloneNode(true);
  clone.querySelectorAll('pre, code, mjx-container, script, style').forEach(e => e.remove());
  const text = clone.innerText || '';
  out.dollar = (text.match(/\$[^$\n]{1,80}\$/g) || []).slice(0, 3);
  out.backslash = (text.match(/\\[a-zA-Z]{2,}|\\\(|\\\[/g) || []).slice(0, 3);
  out.course = (text.match(/Track \d[\d.]*|\bcheckpoint\b|\blesson\b/gi) || []).slice(0, 3);
  out.brokenImg = Array.from(article.querySelectorAll('img'))
    .filter(i => !(i.complete && i.naturalWidth > 0)).map(i => i.getAttribute('src'));
  const right = article.getBoundingClientRect().right;
  out.wideMath = Array.from(article.querySelectorAll('mjx-container[display="true"]'))
    .filter(c => { const m = c.querySelector('mjx-math'); return m && m.getBoundingClientRect().right > right + 4; })
    .map(c => c.textContent.slice(0, 40)).slice(0, 3);
  out.wideImg = Array.from(article.querySelectorAll('img, table'))
    .filter(e => e.getBoundingClientRect().right > right + 4 && !e.closest('.md-typeset__scrollwrap')).length;
  out.mermaidTotal = article.querySelectorAll('.mermaid').length;
  out.mathCount = document.querySelectorAll('mjx-container').length;
  out.arith = document.querySelectorAll('.arithmatex').length;
  return out;
}
"""


def serve(directory):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):
            pass

    handler = functools.partial(Quiet, directory=str(directory))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


async def route_cdn(route):
    url = route.request.url
    m = re.match(r"https://(?:cdn\.jsdelivr\.net/npm|unpkg\.com)/(@?[\w.-]+)@[^/]+/(.*)", url)
    if LOCAL_NPM and m:
        f = Path(LOCAL_NPM) / "node_modules" / m.group(1) / m.group(2).split("?")[0]
        if f.is_file():
            ctype = "font/woff" if f.suffix == ".woff" else "application/javascript"
            await route.fulfill(path=str(f), content_type=ctype)
            return
    await route.continue_()


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site", nargs="?", default="site")
    ap.add_argument("--shots", help="directory for full-page screenshots")
    ap.add_argument("--only", help="substring filter on page paths")
    args = ap.parse_args()

    site = Path(args.site).resolve()
    pages = sorted(p.relative_to(site).as_posix() for p in site.rglob("index.html"))
    pages = [p for p in pages if not p.startswith(("assets/", "search/"))]
    if args.only:
        pages = [p for p in pages if args.only in p]
    srv = serve(site)
    base = f"http://127.0.0.1:{srv.server_address[1]}/"

    failures = 0
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        await ctx.route(re.compile(r"https://(cdn\.jsdelivr\.net|unpkg\.com)/.*"), route_cdn)
        for rel in pages:
            page = await ctx.new_page()
            try:
                await page.goto(base + rel.replace("index.html", ""), wait_until="networkidle", timeout=60000)
                await page.wait_for_timeout(1200)
                r = await page.evaluate(PAGE_JS)
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL {rel}: could not load ({exc})")
                failures += 1
                await page.close()
                continue
            problems = []
            if r["merror"]:
                problems.append(f"{r['merror']} MathJax error(s)")
            if r["rawMath"]:
                problems.append(f"raw LaTeX inside math: {r['rawMath']}")
            if r["dollar"]:
                problems.append(f"unrendered $...$: {r['dollar']}")
            if r["backslash"]:
                problems.append(f"backslash command in text: {r['backslash']}")
            if r["wideMath"]:
                problems.append(f"display equation wider than the text column: {r['wideMath']}")
            if r["wideImg"]:
                problems.append(f"{r['wideImg']} image(s) or table(s) wider than the text column")
            if r["brokenImg"]:
                problems.append(f"broken image(s): {r['brokenImg']}")
            if r["course"] and not rel.startswith(("how-to-use", "index.html")):
                problems.append(f"course reference: {r['course']}")
            if r["arith"] and not r["mathCount"]:
                problems.append("math present but MathJax did not run")
            if args.shots:
                Path(args.shots).mkdir(parents=True, exist_ok=True)
                name = rel.replace("/index.html", "").replace("/", "__") or "home"
                await page.screenshot(path=str(Path(args.shots) / f"{name}.png"), full_page=True)
            if problems:
                failures += 1
                print(f"FAIL {rel}")
                for p in problems:
                    print("     ", p)
            await page.close()
        await browser.close()
    srv.shutdown()
    print(f"{len(pages)} pages checked, {failures} with problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
