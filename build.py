#!/usr/bin/env python3
"""
Assembles standalone HTML pages from GHL piece files.
Run from ~/clients/jay-mora/essays-site/
"""
import re, os

PAGES_DIR = os.path.expanduser("~/clients/jay-mora/pages")
OUT_DIR   = os.path.expanduser("~/clients/jay-mora/essays-site")
GA4_ID    = "YOUR_GA4_ID_HERE"  # Jay: replace with your GA4 measurement ID

GA4_SNIPPET = f"""  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA4_ID}");</script>"""

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def strip_ghl_meta(piece2):
    # Remove GHL og:image:alt workaround meta (standalone HTML doesn't need it)
    piece2 = re.sub(r'<!-- og:image:alt fallback.*?-->\s*\n', '', piece2, flags=re.DOTALL)
    piece2 = re.sub(r'<meta property="og:image:alt"[^>]+>\s*\n', '', piece2)
    return piece2

def update_essay_urls(header, slug):
    """Update canonical + og:url + schema URLs to include /essays/ prefix."""
    old = f"https://thejaymora.com/{slug}"
    new = f"https://thejaymora.com/essays/{slug}"
    return header.replace(old, new)

def assemble(title, piece1_path, piece2_path, out_path, slug=None):
    p1 = read(piece1_path)
    p2 = read(piece2_path)

    # Strip HTML comment blocks from pieces
    p1 = re.sub(r'<!--\s*={3,}.*?={3,}\s*-->\s*\n', '', p1, flags=re.DOTALL)
    p2 = re.sub(r'<!--\s*={3,}.*?={3,}\s*-->\s*\n', '', p2, flags=re.DOTALL)

    # Update essay URLs to /essays/ prefix
    if slug:
        p1 = update_essay_urls(p1, slug)

    # Clean Piece 2
    p2 = strip_ghl_meta(p2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
{GA4_SNIPPET}
{p1.strip()}
</head>
<body>
{p2.strip()}
</body>
</html>
"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Built: {out_path.replace(OUT_DIR, '')}")

# ── ESSAYS INDEX ────────────────────────────────────────────────────────────
assemble(
    title     = "Sales Psychology Essays | Jay Mora",
    piece1_path = f"{PAGES_DIR}/ESSAYS-INDEX-PIECE1-HEADER-v4.txt",
    piece2_path = f"{PAGES_DIR}/ESSAYS-INDEX-PIECE2-BODY-v7.txt",
    out_path  = f"{OUT_DIR}/index.html",
)

# ── ESSAY 1: How to Qualify ──────────────────────────────────────────────────
assemble(
    title     = 'How to Qualify Any Prospect in Three Minutes or Less | Jay Mora',
    piece1_path = f"{PAGES_DIR}/ESSAY-WEEK02-PIECE1-HEADER-v6.txt",
    piece2_path = f"{PAGES_DIR}/ESSAY-WEEK02-PIECE2-BODY-v6.txt",
    out_path  = f"{OUT_DIR}/how-to-qualify-any-prospect-in-three-minutes-or-less/index.html",
    slug      = "how-to-qualify-any-prospect-in-three-minutes-or-less",
)

# ── ESSAY 2: Why Coaches Who Care Close Least ────────────────────────────────
assemble(
    title     = "Why the Coaches Who Care Most Close the Least | Jay Mora",
    piece1_path = f"{PAGES_DIR}/ESSAY-WEEK01-PIECE1-HEADER-v2.txt",
    piece2_path = f"{PAGES_DIR}/ESSAY-WEEK01-PIECE2-BODY-v2.txt",
    out_path  = f"{OUT_DIR}/why-the-coaches-who-care-most-close-the-least/index.html",
    slug      = "why-the-coaches-who-care-most-close-the-least",
)

# ── ESSAY 3: Best Discovery Calls ───────────────────────────────────────────
assemble(
    title     = "Your Best Discovery Calls Are the Ones You Lose | Jay Mora",
    piece1_path = f"{PAGES_DIR}/ESSAY-WEEK00-PIECE1-HEADER-v5.txt",
    piece2_path = f"{PAGES_DIR}/ESSAY-WEEK00-PIECE2-BODY-v5.txt",
    out_path  = f"{OUT_DIR}/your-best-discovery-calls-are-the-ones-you-lose/index.html",
    slug      = "your-best-discovery-calls-are-the-ones-you-lose",
)

# ── ESSAY 4: I Need to Think About It ───────────────────────────────────────
assemble(
    title     = 'How to Handle "I Need to Think About It" on a Sales Call | Jay Mora',
    piece1_path = f"{PAGES_DIR}/ESSAY-WEEK03-PIECE1-HEADER-v5.txt",
    piece2_path = f"{PAGES_DIR}/ESSAY-WEEK03-PIECE2-BODY-v6.txt",
    out_path  = f"{OUT_DIR}/i-need-to-think-about-it-sales-objection/index.html",
    slug      = "i-need-to-think-about-it-sales-objection",
)

print("\nDone. All pages assembled.")
