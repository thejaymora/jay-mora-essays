#!/usr/bin/env python3
"""
Essay GHL Pipeline — generates Piece 1 (Header) + Piece 2 (Body) from essay data.

Usage:
    python generate_essay.py <essay_input.py> [--version N]

The input file must define an `essay` dict. See essay-inputs/template.py for format.
Outputs go to ~/clients/jay-mora/pages/:
    ESSAY-{WEEK_TAG}-PIECE1-HEADER-vN.txt  -> GHL Header Tracking Code
    ESSAY-{WEEK_TAG}-PIECE2-BODY-vN.txt    -> GHL Custom Code element (body)
"""

import sys, os, json, importlib.util, argparse
from pathlib import Path

PAGES_DIR = Path.home() / "clients/jay-mora/pages"

# ── Asset URLs (never change unless rebranded) ────────────────────────────────
HEADSHOT_URL      = "https://assets.cdn.filesafe.space/oYYHLxBrKKJKNNDegpIm/media/69d576e784c045c274d95758.png"
NEWSLETTER_LOGO   = "https://assets.cdn.filesafe.space/oYYHLxBrKKJKNNDegpIm/media/69e8690b5e482c379bddc3bb.png"
BLUEPRINT_IMG     = "https://assets.cdn.filesafe.space/oYYHLxBrKKJKNNDegpIm/media/69e92aa9a1636a6c65450ae1.png"
LI_NEWSLETTER_URN = "7450423578321264640"

# ── Social icon SVGs ──────────────────────────────────────────────────────────
_LI_SVG  = '<svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
_YT_SVG  = '<svg viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'
_FB_SVG  = '<svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>'
_WEB_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'


def _social_row(indent="            "):
    lines = [indent + '<div class="jmbp-social-row">']
    socials = [
        ("https://www.linkedin.com/in/thejaymora/", "LinkedIn",  _LI_SVG,  True),
        ("https://www.youtube.com/@thejaymora",      "YouTube",   _YT_SVG,  True),
        ("https://www.facebook.com/itsjaymora/",     "Facebook",  _FB_SVG,  True),
        ("https://www.thejaymora.com",               "Website",   _WEB_SVG, False),
    ]
    for href, label, svg, external in socials:
        ext = ' target="_blank" rel="noopener"' if external else ""
        lines.append(indent + '  <a href="' + href + '"' + ext + ' class="jmbp-social-icon" aria-label="' + label + '">')
        lines.append(indent + '    ' + svg)
        lines.append(indent + '  </a>')
    lines.append(indent + '</div>')
    return "\n".join(lines)


# ── CSS (all essay page styles) ───────────────────────────────────────────────
CSS = r"""@import url('https://fonts.googleapis.com/css2?family=League+Spartan:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Playfair+Display:ital,wght@0,400;1,400&display=swap');

.jmbp * { box-sizing: border-box; margin: 0; padding: 0; }

.jmbp {
  background: #050505;
  color: #F5EFE3;
  font-family: 'DM Sans', sans-serif;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

.jmbp-gold { color: #F5C842; }

.jmbp-divider {
  height: 1px;
  background: linear-gradient(90deg, rgba(245,200,66,.12), rgba(245,200,66,.9) 50%, rgba(245,200,66,.12));
}

.jmbp-eyebrow {
  display: inline-block;
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #F5C842;
}

.jmbp-back {
  display: block;
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(245,239,227,.38);
  text-decoration: none;
  margin-bottom: 5px;
  transition: color .2s ease;
}
.jmbp-back:hover { color: #F5C842; }
.jmbp-back::before { content: '\2190  '; }

.jmbp-hero .jmbp-eyebrow {
  display: block;
  margin-bottom: 6px;
  padding-top: 1.5px;
  border-top: 1px solid rgba(245,200,66,.16);
  width: fit-content;
}

.jmbp-hero {
  position: relative;
  overflow: hidden;
  padding: 64px 24px 36px;
}
.jmbp-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 100% 80% at 50% 30%, rgba(245,200,66,.15), rgba(58,43,23,.07) 50%, rgba(5,5,5,0) 75%);
  pointer-events: none;
}
.jmbp-hero-inner {
  position: relative;
  max-width: 1100px;
  margin: 0 auto;
}
.jmbp-hero-title {
  font-family: 'League Spartan', sans-serif;
  font-size: clamp(32px, 4vw, 58px);
  font-weight: 800;
  line-height: 0.97;
  letter-spacing: -0.028em;
  color: #F5EFE3;
  margin: 34px 0 24px;
  max-width: 900px;
}
.jmbp-hero-lede {
  font-family: 'DM Sans', sans-serif;
  font-size: clamp(17px, 2vw, 24px);
  font-weight: 300;
  color: #E4D9C4;
  line-height: 1.55;
  max-width: 760px;
  margin-bottom: 24px;
}
.jmbp-hero-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #9C9387;
}
.jmbp-meta-sep { opacity: .4; }

.jmbp-body {
  max-width: 1240px;
  margin: 0 auto;
  padding: 32px 24px 0;
  display: grid;
  gap: 48px;
  grid-template-columns: 1fr;
}
@media (min-width: 1200px) {
  .jmbp-body {
    grid-template-columns: minmax(0, 860px) 280px;
    gap: 40px;
  }
}

.jmbp-article-card {
  background: #0A0A0A;
  border: 1px solid rgba(245,200,66,.20);
  border-radius: 28px;
  padding: 52px;
  box-shadow: inset 0 1px 0 rgba(245,200,66,.04);
}

.jmbp-article-lede {
  font-family: 'DM Sans', sans-serif;
  font-size: clamp(22px, 2.5vw, 30px);
  font-weight: 300;
  line-height: 1.65;
  color: #F5EFE3;
  margin-bottom: 28px;
}

.jmbp-p {
  font-family: 'DM Sans', sans-serif;
  font-size: 19px;
  font-weight: 300;
  line-height: 1.88;
  color: #E4D9C4;
  margin-bottom: 26px;
}

.jmbp-impact {
  font-family: 'DM Sans', sans-serif;
  font-size: clamp(20px, 2.2vw, 25px);
  font-weight: 400;
  line-height: 1.55;
  color: #FFFFFF;
  margin: 34px 0 30px;
}

.jmbp-beat {
  font-family: 'Playfair Display', serif;
  font-size: clamp(22px, 2.4vw, 28px);
  font-weight: 400;
  font-style: italic;
  line-height: 1.5;
  color: #FFFFFF;
  margin: 34px 0 30px;
}

.jmbp-h2 {
  font-family: 'League Spartan', sans-serif;
  font-size: clamp(26px, 3vw, 38px);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.02em;
  color: #F5EFE3;
  margin: 72px 0 24px;
  padding-top: 48px;
  border-top: 1px solid rgba(245,200,66,.14);
}

.jmbp-pullquote {
  border-left: 3px solid #D4A62A;
  background: linear-gradient(135deg, rgba(58,43,23,.24) 0%, rgba(17,17,17,.94) 65%);
  border-radius: 0 20px 20px 0;
  padding: 30px 32px;
  margin: 56px 0;
}
.jmbp-pullquote p {
  font-family: 'Playfair Display', serif;
  font-size: clamp(24px, 3vw, 38px);
  font-style: italic;
  line-height: 1.28;
  color: #F5C842;
  margin: 0;
}

.jmbp-reflection {
  background: linear-gradient(135deg, rgba(58,43,23,.18) 0%, rgba(10,10,10,1) 70%);
  border: 1px solid rgba(245,200,66,.18);
  border-radius: 20px;
  padding: 28px 32px;
  margin: 52px 0;
}
.jmbp-reflection p {
  font-family: 'DM Sans', sans-serif;
  font-size: clamp(18px, 2vw, 24px);
  font-weight: 300;
  line-height: 1.6;
  color: #F5EFE3;
  margin: 0;
}

.jmbp-byline {
  margin-top: 0;
  padding-top: 32px;
  border-top: none;
  display: flex;
  align-items: center;
  gap: 16px;
}
.jmbp-byline-icon {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 2px solid rgba(245,200,66,.42);
  overflow: hidden;
  flex-shrink: 0;
  background: #111;
}
.jmbp-byline-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.jmbp-byline-name {
  font-family: 'League Spartan', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #F5EFE3;
  letter-spacing: -0.01em;
  line-height: 1.2;
}
.jmbp-byline-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 500;
  color: #F5C842;
  margin-top: 4px;
  letter-spacing: 0.02em;
}
.jmbp-byline-co {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: #9C9387;
  margin-top: 3px;
}

.jmbp-social-row {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}
.jmbp-social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid rgba(245,200,66,.28);
  color: #C9BFAF;
  text-decoration: none;
  transition: border-color .2s ease, color .2s ease;
  flex-shrink: 0;
}
.jmbp-social-icon svg { width: 16px; height: 16px; fill: currentColor; display: block; }
.jmbp-social-icon[aria-label="Website"] svg { fill: none; stroke: currentColor; }
.jmbp-social-icon:hover { border-color: #F5C842; color: #F5C842; }

.jmbp-sidebar { display: none; }
@media (min-width: 1020px) {
  .jmbp-sidebar { display: block; }
}
.jmbp-sidebar-inner {
  position: sticky;
  top: 16px;
  max-height: calc(100vh - 32px);
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
  -ms-overflow-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
  -webkit-mask-image: linear-gradient(to bottom, black calc(100% - 56px), transparent 100%);
  mask-image: linear-gradient(to bottom, black calc(100% - 56px), transparent 100%);
}
.jmbp-sidebar-inner::-webkit-scrollbar { display: none; }
.jmbp-sidebar-card {
  background: #0A0A0A;
  border: 1px solid rgba(245,200,66,.14);
  border-radius: 18px;
  padding: 16px;
}
.jmbp-sidebar-title {
  font-family: 'League Spartan', sans-serif;
  font-size: 18px;
  font-weight: 800;
  line-height: 1.18;
  color: #F5EFE3;
  margin: 6px 0 8px;
}
.jmbp-sidebar-body {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 300;
  line-height: 1.7;
  color: #C9BFAF;
  margin-bottom: 12px;
}
.jmbp-sidebar-btn {
  display: block;
  text-align: center;
  background: #F5C842;
  color: #050505;
  font-family: 'League Spartan', sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  text-decoration: none;
  padding: 9px 16px;
  border-radius: 8px;
  transition: background .15s ease;
}
.jmbp-sidebar-btn:hover { background: #fff; }

.jmbp-sidebar-img {
  display: block;
  width: 100%;
  border-radius: 14px;
  margin-bottom: 10px;
  object-fit: cover;
}

#jmbp-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 0%;
  height: 6px;
  background: #F5C842;
  z-index: 9999;
  pointer-events: none;
  transition: width 0.08s linear, opacity 0.4s ease;
}

chat-widget { display: none !important; }

body, html, :root { background: #050505 !important; }
.bgCover, .bg-fixed { background: #050505 !important; }

@media (max-width: 600px) {
  .jmbp { margin-top: -60px; }
  .jmbp-hero { padding: 24px 18px 36px; }
  .jmbp-body { padding: 24px 18px 48px; gap: 0; }
  .jmbp-article-card { padding: 30px 22px; }
  .jmbp-p { font-size: 17px; }
  .jmbp-impact, .jmbp-beat { font-size: 19px; margin: 28px 0 24px; }
  .jmbp-pullquote { padding: 22px; margin: 44px 0; }
  .jmbp-reflection { padding: 22px; margin: 44px 0; }
  .jmbp-byline-icon { width: 110px; height: 110px; }
}

.jmbp-mobile-cta {
  padding: 0 18px 56px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 680px;
  margin: 0 auto;
}
@media (min-width: 1020px) {
  .jmbp-mobile-cta { display: none; }
}

.jm-slim-nav {
  background: #050505;
  border-bottom: 1px solid rgba(245,200,66,0.15);
  padding: 14px 20px;
  text-align: center;
  margin-top: -40px;
}
.jm-slim-nav__links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
  list-style: none;
  margin: 0;
  padding: 0;
}
.jm-slim-nav__links a {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 400;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(245,239,227,0.55);
  text-decoration: none;
  transition: color 0.2s;
}
.jm-slim-nav__links a:hover { color: #F5EFE3; text-decoration: none; }
@media (max-width: 600px) {
  .jm-slim-nav__links { gap: 20px; }
  .jm-slim-nav__links a { font-size: 11px; }
}

.apply-newsletter { padding: 64px 24px; background: #050505; }
.apply-newsletter-card { max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, rgba(245,200,66,.08) 0%, rgba(14,14,14,1) 40%, rgba(10,10,10,1) 100%); border: 1px solid rgba(245,200,66,.28); border-radius: 28px; padding: 0 10px 44px; text-align: center; overflow: hidden; }
.apply-newsletter-logo { display: block; height: 280px; width: auto; margin: -30px auto -80px; object-fit: contain; }
.apply-newsletter-eyebrow { display: block; font-family: 'DM Sans', sans-serif; font-size: 18px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: #F5EFE3; margin-bottom: 6px; }
.apply-newsletter-sub { font-family: 'DM Sans', sans-serif; font-size: 17px; font-weight: 300; line-height: 1.7; color: #C9BFAF; max-width: 500px; margin: 16px auto 28px; }
.apply-newsletter-btn { display: inline-flex; align-items: center; gap: 8px; background: #F5C842; color: #050505; font-family: 'League Spartan', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; text-decoration: none; padding: 14px 28px; border-radius: 12px; transition: transform .15s ease, background .15s ease; }
.apply-newsletter-btn:hover { background: #fff; transform: translateY(-1px); text-decoration: none; }
@media (max-width: 600px) {
  .apply-newsletter-logo { height: auto; width: 72%; max-width: 240px; margin: -12px auto -44px; }
  .apply-newsletter-card { padding: 0 10px 36px; }
}

.jmor-container { max-width: 880px; margin: 0 auto; }
.jmor-crosslinks { padding: 60px 20px; text-align: center; background: #111111; }
.jmor-crosslinks__label { font-family: 'DM Sans', sans-serif; font-size: 25px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #ffffff; margin-bottom: 28px; display: block; }
.jmor-crosslinks__grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; max-width: 700px; margin: 0 auto; }
.jmor-crosslinks__grid a { font-family: 'DM Sans', sans-serif; font-size: 22px; font-weight: 500; color: #ffffff !important; text-decoration: none; padding: 10px 20px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.05); border-radius: 4px; transition: color 0.2s, border-color 0.2s, background 0.2s; }
.jmor-crosslinks__grid a:hover { color: #F5C842 !important; border-color: #F5C842; text-decoration: none; }
@media (max-width: 600px) {
  .jmor-crosslinks__grid a { font-size: 20px; width: 100%; text-align: center; }
}

.jmor-footer { padding: 80px 20px 64px; text-align: center; background: #050505; }
.jmor-footer__social { display: flex; justify-content: center; gap: 32px; margin-bottom: 52px; flex-wrap: wrap; }
.jmor-footer__social a { text-decoration: none; opacity: 0.7; transition: opacity 0.2s; }
.jmor-footer__social a:hover { opacity: 1; text-decoration: none; }
.jmor-footer__social img { width: 40px; height: 40px; }
.jmor-footer__headshot { width: 150px; height: 150px; border-radius: 50%; border: 3px solid #F5C842; margin: 0 auto 20px; object-fit: cover; display: block; }
.jmor-footer__name { font-family: 'League Spartan', sans-serif; font-size: 28px; font-weight: 700; color: #ffffff; margin-bottom: 12px; }
.jmor-footer__title { font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #F5C842; margin: -6px auto 20px; max-width: 480px; }
.jmor-footer__bio { font-family: 'DM Sans', sans-serif; font-size: 22px; line-height: 1.5; color: rgba(255,255,255,0.7); max-width: 560px; margin: 0 auto 28px; }
.jmor-footer__contact { font-family: 'DM Sans', sans-serif; font-size: 18px; color: rgba(255,255,255,0.5); margin-bottom: 36px; }
.jmor-footer__contact a { color: rgba(255,255,255,0.65) !important; text-decoration: none; }
.jmor-footer__contact a:hover { color: #F5C842 !important; }
.jmor-footer__links { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px 14px; margin-bottom: 40px; }
.jmor-footer__links a { font-family: 'DM Sans', sans-serif; font-size: 15px; font-weight: 500; color: rgba(255,255,255,0.75) !important; text-decoration: none; padding: 8px 18px; border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; background: rgba(255,255,255,0.04); transition: color 0.2s, border-color 0.2s, background 0.2s; }
.jmor-footer__links a:hover { color: #F5C842 !important; border-color: #F5C842; background: rgba(245,200,66,0.06); text-decoration: none; }
.jmor-footer__copy { font-family: 'DM Sans', sans-serif; font-size: 14px; color: rgba(255,255,255,0.3); letter-spacing: 0.05em; }
@media (max-width: 900px) {
  .jmor-footer__social { flex-wrap: nowrap !important; justify-content: space-between !important; gap: 0 !important; padding: 0 4px; }
  .jmor-footer__social img { width: 28px !important; height: 28px !important; }
  .jmor-footer__headshot { width: 120px; height: 120px; }
  .jmor-footer__name { font-size: 20px; }
  .jmor-footer__bio { font-size: 14px; }
  .jmor-footer__links { display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 8px !important; max-width: 340px; margin: 0 auto 32px !important; }
  .jmor-footer__links a { display: block !important; text-align: center !important; border: 1px solid rgba(255,255,255,0.25) !important; border-radius: 4px !important; padding: 10px 4px !important; font-size: 14px !important; color: rgba(255,255,255,0.8) !important; }
}"""


# ── Static JS ─────────────────────────────────────────────────────────────────

def _js_title_force(title):
    escaped = title.replace("\\", "\\\\").replace("'", "\\'")
    return ("<script>(function(){function o(){var t='" + escaped + "';"
            "if(document.title!==t)document.title=t;}if(document.readyState==='loading'){"
            "document.addEventListener('DOMContentLoaded',o);}else{o();}"
            "window.addEventListener('load',o);setTimeout(o,300);setTimeout(o,1000);}})();</script>")


JS_DARK_SCROLL = """<script>
(function(){
  function forceDark(){
    var els=document.querySelectorAll('.bgCover,.bg-fixed');
    for(var i=0;i<els.length;i++){
      els[i].style.setProperty('background','#050505','important');
      els[i].style.setProperty('background-color','#050505','important');
    }
    document.documentElement.style.setProperty('background-color','#050505','important');
    document.body.style.setProperty('background-color','#050505','important');
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',forceDark);
  } else {
    forceDark();
  }
  window.addEventListener('load',forceDark);
  setTimeout(forceDark,200);
  setTimeout(forceDark,800);
})();
(function(){
  var depthsFired={};
  function pct(){
    var d=document.documentElement;
    var s=d.scrollTop||document.body.scrollTop;
    var t=d.scrollHeight-d.clientHeight;
    return t>0?Math.round(s/t*100):0;
  }
  window.addEventListener('scroll',function(){
    var depth=pct();
    [25,50,75].forEach(function(m){
      if(depth>=m&&!depthsFired[m]){
        depthsFired[m]=true;
        if(typeof gtag==='function'){
          gtag('event','scroll_depth',{percent_scrolled:m,page_path:window.location.pathname});
        }
      }
    });
  },{passive:true});
  document.addEventListener('click',function(e){
    var link=e.target.closest('a');
    if(!link)return;
    var href=link.getAttribute('href')||'';
    var text=link.textContent.trim().toLowerCase();
    if(href.includes('/apply')||href.includes('/calculator')||text==='apply'||text.includes('diagnostic')||text.includes('revenue leak')||text.includes('calculator')){
      if(typeof gtag==='function'){
        gtag('event','essay_cta_clicked',{page_path:window.location.pathname,link_text:link.textContent.trim()});
      }
    }
  });
})();
</script>"""

JS_SIDEBAR_PROGRESS = """  <!-- Sidebar fade: remove mask when scrolled to bottom -->
  <script>
  (function(){
    var inner = document.querySelector('.jmbp-sidebar-inner');
    if (!inner) return;
    var FADE = 'linear-gradient(to bottom, black calc(100% - 56px), transparent 100%)';
    function updateMask(){
      var atBottom = inner.scrollTop + inner.clientHeight >= inner.scrollHeight - 12;
      inner.style.webkitMaskImage = atBottom ? 'none' : FADE;
      inner.style.maskImage = atBottom ? 'none' : FADE;
    }
    inner.addEventListener('scroll', updateMask, { passive: true });
    updateMask();
  })();
  </script>

  <!-- Reading Progress Bar Script -->
  <script>
  (function(){
    var bar = document.getElementById('jmbp-progress');
    if(!bar) return;
    function updateBar(){
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
      var docHeight = Math.max(
        document.body.scrollHeight, document.documentElement.scrollHeight,
        document.body.offsetHeight, document.documentElement.offsetHeight
      ) - window.innerHeight;
      var pct = docHeight > 0 ? Math.min(scrollTop / docHeight * 100, 100) : 0;
      bar.style.width = pct + '%';
      bar.style.opacity = pct >= 99.5 ? '0' : '1';
    }
    window.addEventListener('scroll', updateBar, { passive: true });
    document.addEventListener('scroll', updateBar, { passive: true });
    updateBar();
  })();
  </script>"""

GOLD_RULE = '<div style="width:880px;max-width:calc(100% - 40px);height:3px;background:#F5C842;margin:0 auto;" role="presentation"></div>'


# ── Static HTML blocks ────────────────────────────────────────────────────────

def _sidebar_cards():
    return (
        "        <!-- Card 1: Identity + Social -->\n"
        '        <div class="jmbp-sidebar-card">\n'
        '          <span class="jmbp-eyebrow">Jay Mora</span>\n'
        '          <h4 class="jmbp-sidebar-title">High-Ticket Sales Psychologist for Coaches</h4>\n'
        '          <p class="jmbp-sidebar-body">I work with established coaches who lose high-ticket deals. Not because of their offer. Because of what happens inside them the moment money enters the conversation.</p>\n'
        + _social_row("          ") + "\n"
        "        </div>\n\n"
        "        <!-- Card 2: Calculator -->\n"
        '        <div class="jmbp-sidebar-card">\n'
        '          <span class="jmbp-eyebrow">Free Tool</span>\n'
        '          <h4 class="jmbp-sidebar-title">See what the mishandled objections have cost you.</h4>\n'
        '          <p class="jmbp-sidebar-body">60 seconds. Your close rate, your call volume, your average deal size. It shows you the number.</p>\n'
        '          <a href="https://thejaymora.com/calculator" class="jmbp-sidebar-btn">Run the Calculator</a>\n'
        "        </div>\n\n"
        "        <!-- Card 3: LinkedIn Newsletter -->\n"
        '        <div class="jmbp-sidebar-card">\n'
        '          <span class="jmbp-eyebrow">Newsletter</span>\n'
        '          <h4 class="jmbp-sidebar-title">The Decision Leader</h4>\n'
        '          <p class="jmbp-sidebar-body">Weekly insights on sales psychology, identity, and the exact moments revenue is won or lost. Delivered on LinkedIn.</p>\n'
        '          <a href="https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=' + LI_NEWSLETTER_URN + '" target="_blank" rel="noopener" class="jmbp-sidebar-btn">Subscribe on LinkedIn</a>\n'
        "        </div>\n\n"
        "        <!-- Card 4: 3-Minute Qualification Blueprint -->\n"
        '        <div class="jmbp-sidebar-card">\n'
        '          <img src="' + BLUEPRINT_IMG + '" alt="The 3-Minute Qualification Blueprint" class="jmbp-sidebar-img" loading="lazy">\n'
        '          <span class="jmbp-eyebrow">Free Download</span>\n'
        '          <h4 class="jmbp-sidebar-title">The 3-Minute Qualification Blueprint</h4>\n'
        '          <p class="jmbp-sidebar-body">The exact framework. Free when you run the calculator.</p>\n'
        '          <a href="https://thejaymora.com/calculator" class="jmbp-sidebar-btn">Get the Blueprint</a>\n'
        "        </div>"
    )


def _mobile_cta_cards():
    return (
        '    <div class="jmbp-sidebar-card">\n'
        '      <span class="jmbp-eyebrow">Jay Mora</span>\n'
        '      <h4 class="jmbp-sidebar-title">High-Ticket Sales Psychologist for Coaches</h4>\n'
        '      <p class="jmbp-sidebar-body">I work with established coaches who lose high-ticket deals. Not because of their offer. Because of what happens inside them the moment money enters the conversation.</p>\n'
        + _social_row("      ") + "\n"
        "    </div>\n\n"
        '    <div class="jmbp-sidebar-card">\n'
        '      <span class="jmbp-eyebrow">Free Tool</span>\n'
        '      <h4 class="jmbp-sidebar-title">See what the mishandled objections have cost you.</h4>\n'
        '      <p class="jmbp-sidebar-body">60 seconds. Your close rate, your call volume, your average deal size. It shows you the number.</p>\n'
        '      <a href="https://thejaymora.com/calculator" class="jmbp-sidebar-btn">Run the Calculator</a>\n'
        "    </div>\n\n"
        '    <div class="jmbp-sidebar-card">\n'
        '      <span class="jmbp-eyebrow">Newsletter</span>\n'
        '      <h4 class="jmbp-sidebar-title">The Decision Leader</h4>\n'
        '      <p class="jmbp-sidebar-body">Weekly insights on sales psychology, identity, and the exact moments revenue is won or lost. Delivered on LinkedIn.</p>\n'
        '      <a href="https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=' + LI_NEWSLETTER_URN + '" target="_blank" rel="noopener" class="jmbp-sidebar-btn">Subscribe on LinkedIn</a>\n'
        "    </div>\n\n"
        '    <div class="jmbp-sidebar-card">\n'
        '      <img src="' + BLUEPRINT_IMG + '" alt="The 3-Minute Qualification Blueprint" class="jmbp-sidebar-img" loading="lazy">\n'
        '      <span class="jmbp-eyebrow">Free Download</span>\n'
        '      <h4 class="jmbp-sidebar-title">The 3-Minute Qualification Blueprint</h4>\n'
        '      <p class="jmbp-sidebar-body">The exact framework. Free when you run the calculator.</p>\n'
        '      <a href="https://thejaymora.com/calculator" class="jmbp-sidebar-btn">Get the Blueprint</a>\n'
        "    </div>"
    )


def _byline_html():
    return (
        "\n      <!-- Byline -->\n"
        '      <div class="jmbp-byline">\n'
        '        <div class="jmbp-byline-icon">\n'
        '          <img src="' + HEADSHOT_URL + '" alt="Jay Mora">\n'
        "        </div>\n"
        "        <div>\n"
        '          <div class="jmbp-byline-name">Jay Mora</div>\n'
        '          <div class="jmbp-byline-title">High-Ticket Sales Psychologist for Coaches</div>\n'
        '          <div class="jmbp-byline-co">Mora Signature Consulting</div>\n'
        + _social_row("          ") + "\n"
        "        </div>\n"
        "      </div>\n"
    )


def _newsletter_section():
    return (
        '<section class="apply-newsletter" aria-label="LinkedIn Newsletter">\n'
        '  <div class="apply-newsletter-card">\n'
        '    <img src="' + NEWSLETTER_LOGO + '" alt="The Decision Leader Newsletter" class="apply-newsletter-logo" loading="lazy">\n'
        '    <span class="apply-newsletter-eyebrow">Newsletter</span>\n'
        '    <p class="apply-newsletter-sub">Weekly insights on sales psychology, identity, and the exact moments revenue is won or lost. Delivered every week on LinkedIn.</p>\n'
        '    <a href="https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=' + LI_NEWSLETTER_URN + '" target="_blank" rel="noopener" class="apply-newsletter-btn">Subscribe on LinkedIn &#8594;</a>\n'
        "  </div>\n"
        "</section>"
    )


def _blueprint_section():
    return (
        '<section style="padding:64px 24px;background:#050505;">\n'
        '  <div style="max-width:600px;margin:0 auto;background:linear-gradient(135deg,rgba(245,200,66,.07) 0%,rgba(14,14,14,1) 40%,rgba(10,10,10,1) 100%);border:1px solid rgba(245,200,66,.22);border-radius:28px;padding:40px 36px 36px;text-align:center;">\n'
        '    <img src="' + BLUEPRINT_IMG + '" alt="The 3-Minute Qualification Blueprint" style="width:260px;max-width:90%;height:auto;display:block;margin:0 auto 24px;" loading="lazy">\n'
        '    <span style="display:block;font-family:\'DM Sans\',sans-serif;font-size:14px;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;color:#F5C842;margin-bottom:10px;">Free Resource</span>\n'
        '    <h3 style="font-family:\'League Spartan\',sans-serif;font-size:26px;font-weight:800;color:#F5EFE3;line-height:1.1;letter-spacing:-0.015em;margin:0 0 14px;">The 3-Minute Qualification Blueprint</h3>\n'
        '    <p style="font-family:\'DM Sans\',sans-serif;font-size:16px;font-weight:300;line-height:1.7;color:#C9BFAF;max-width:460px;margin:0 auto 24px;">The exact five gates Jay Mora uses to qualify any prospect before minute three. Stop giving strategy to people who were never going to buy.</p>\n'
        '    <ul style="list-style:none;padding:0;margin:0 auto 28px;max-width:420px;text-align:left;">\n'
        '      <li style="font-family:\'DM Sans\',sans-serif;font-size:16px;color:rgba(245,239,227,0.75);padding:8px 0;border-bottom:1px solid rgba(245,200,66,.12);display:flex;align-items:flex-start;gap:10px;"><span style="color:#F5C842;font-weight:700;flex-shrink:0;">&#10003;</span><span>The Five-Gate Filter&#8482;: qualify or fire the prospect in under three minutes</span></li>\n'
        '      <li style="font-family:\'DM Sans\',sans-serif;font-size:16px;color:rgba(245,239,227,0.75);padding:8px 0;border-bottom:1px solid rgba(245,200,66,.12);display:flex;align-items:flex-start;gap:10px;"><span style="color:#F5C842;font-weight:700;flex-shrink:0;">&#10003;</span><span>Gates 1&ndash;5: pain, money, authority, timeline, and character</span></li>\n'
        '      <li style="font-family:\'DM Sans\',sans-serif;font-size:16px;color:rgba(245,239,227,0.75);padding:8px 0;border-bottom:1px solid rgba(245,200,66,.12);display:flex;align-items:flex-start;gap:10px;"><span style="color:#F5C842;font-weight:700;flex-shrink:0;">&#10003;</span><span>Blueprint A: The Unscripted Brain Picker Call framework</span></li>\n'
        '      <li style="font-family:\'DM Sans\',sans-serif;font-size:16px;color:rgba(245,239,227,0.75);padding:8px 0;border-bottom:1px solid rgba(245,200,66,.12);display:flex;align-items:flex-start;gap:10px;"><span style="color:#F5C842;font-weight:700;flex-shrink:0;">&#10003;</span><span>Blueprint B: The Booked Discovery Call structure</span></li>\n'
        '      <li style="font-family:\'DM Sans\',sans-serif;font-size:16px;color:rgba(245,239,227,0.75);padding:8px 0;display:flex;align-items:flex-start;gap:10px;"><span style="color:#F5C842;font-weight:700;flex-shrink:0;">&#10003;</span><span>The exact language to close or fire at each decision point</span></li>\n'
        "    </ul>\n"
        '    <a href="https://thejaymora.com/calculator" style="display:inline-flex;align-items:center;gap:8px;background:#F5C842;color:#050505;font-family:\'League Spartan\',sans-serif;font-size:16px;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;text-decoration:none;padding:14px 28px;border-radius:12px;">Get the Blueprint &#8594;</a>\n'
        '    <p style="font-family:\'DM Sans\',sans-serif;font-size:13px;font-weight:300;color:rgba(245,239,227,0.6);margin-top:14px;line-height:1.5;">Run the Revenue Leak Calculator first. The blueprint is waiting on the other side.</p>\n'
        "  </div>\n"
        "</section>"
    )


CROSSLINKS_SECTION = (
    '<section style="background:#050505;padding:0;" aria-label="Explore More">\n'
    '  <nav class="jmor-crosslinks" style="max-width:880px;margin:0 auto;background:#111111;" aria-label="Related pages">\n'
    '    <div class="jmor-container">\n'
    '      <span class="jmor-crosslinks__label">Explore More</span>\n'
    '      <div class="jmor-crosslinks__grid">\n'
    '        <a href="https://thejaymora.com/calculator" style="color:#F5C842 !important;">Revenue Leak Calculator</a>\n'
    '        <a href="https://thejaymora.com/services">How the Work Is Done</a>\n'
    '        <a href="https://thejaymora.com/essays">Essays</a>\n'
    '        <a href="https://thejaymora.com/faq">Frequently Asked Questions</a>\n'
    '        <a href="https://thejaymora.com/apply">Apply</a>\n'
    "      </div>\n"
    "    </div>\n"
    "  </nav>\n"
    "</section>"
)


def _footer_html():
    return (
        '<footer class="jmor-footer" role="contentinfo">\n'
        '  <div class="jmor-container">\n\n'
        '    <nav class="jmor-footer__social" aria-label="Social media links">\n'
        '      <a href="https://www.linkedin.com/in/thejaymora" target="_blank" rel="noopener noreferrer" aria-label="Jay Mora on LinkedIn">\n'
        '        <img src="https://stcdn.leadconnectorhq.com/funnel/icons/light-gray/linkedin-light-gray.svg" alt="LinkedIn" width="40" height="40">\n'
        "      </a>\n"
        '      <a href="https://www.youtube.com/@thejaymora" target="_blank" rel="noopener noreferrer" aria-label="Jay Mora on YouTube">\n'
        '        <img src="https://stcdn.leadconnectorhq.com/funnel/icons/light-gray/youtube-light-gray.svg" alt="YouTube" width="40" height="40">\n'
        "      </a>\n"
        '      <a href="https://www.facebook.com/itsjaymora/" target="_blank" rel="noopener noreferrer" aria-label="Jay Mora on Facebook">\n'
        '        <img src="https://stcdn.leadconnectorhq.com/funnel/icons/light-gray/facebook-light-gray.svg" alt="Facebook" width="40" height="40">\n'
        "      </a>\n"
        '      <a href="https://x.com/thejaymora" target="_blank" rel="noopener noreferrer" aria-label="Jay Mora on X">\n'
        '        <img src="https://stcdn.leadconnectorhq.com/funnel/icons/light-gray/x-light-gray.svg" alt="X (Twitter)" width="40" height="40">\n'
        "      </a>\n"
        "    </nav>\n\n"
        '    <img\n'
        '      class="jmor-footer__headshot"\n'
        '      src="' + HEADSHOT_URL + '"\n'
        '      alt="Jay Mora, founder of Mora Signature Consulting and creator of the Elevator of Sales&#8482;"\n'
        '      width="150" height="150" loading="lazy">\n'
        '    <p class="jmor-footer__name">Jay Mora</p>\n'
        '    <p class="jmor-footer__title">High-Ticket Sales Psychologist for Coaches</p>\n'
        '    <p class="jmor-footer__bio">I fix the psychology that causes proven experts to under-earn in the sales conversation.<br>Decision Architecture&#8482;, not scripts.</p>\n\n'
        '    <p class="jmor-footer__contact">\n'
        '      <a href="mailto:jay@thejaymora.com" aria-label="Email Jay Mora">jay@thejaymora.com</a>\n'
        "      &nbsp;&nbsp;|&nbsp;&nbsp;\n"
        '      <a href="https://thejaymora.com" aria-label="Jay Mora website">www.thejaymora.com</a>\n'
        "    </p>\n\n"
        '    <div class="jmor-footer__links">\n'
        '      <a href="https://thejaymora.com/#about">About</a>\n'
        '      <a href="https://thejaymora.com/services">The Work</a>\n'
        '      <a href="https://thejaymora.com/faq">FAQ</a>\n'
        '      <a href="https://thejaymora.com/calculator">Calculator</a>\n'
        '      <a href="https://thejaymora.com/essays">Essays</a>\n'
        '      <a href="https://thejaymora.com/apply" style="color:#F5C842 !important;font-weight:700;">Apply</a>\n'
        "    </div>\n\n"
        '    <p class="jmor-footer__copy">&copy; 2026 Jay Mora &nbsp;|&nbsp; Mora Signature Consulting. All rights reserved.</p>\n'
        "  </div>\n"
        "</footer>"
    )


# ── Article body renderer ─────────────────────────────────────────────────────

def render_body_sections(sections):
    """Convert list of (type, content) tuples to article HTML.

    Types:
        comment     HTML comment: <!-- content -->
        lede        Large opening paragraph (.jmbp-article-lede)
        p           Body paragraph (.jmbp-p)
        h2          Section heading (.jmbp-h2)
        impact      White emphasis line (.jmbp-impact)
        beat        Italic prose beat (.jmbp-beat)
        pullquote   Gold pull quote block (.jmbp-pullquote)
        reflection  Dialog/quote box (.jmbp-reflection)
        byline      Author byline — content ignored, pass None

    All content strings are treated as raw HTML (use HTML entities for
    typographic chars: &ldquo; &rsquo; &hellip; &trade; etc.)
    """
    parts = []
    for section_type, content in sections:
        if section_type == "comment":
            parts.append("\n      <!-- " + str(content) + " -->\n")
        elif section_type == "lede":
            parts.append('\n      <p class="jmbp-article-lede">' + content + "</p>\n")
        elif section_type == "p":
            parts.append('\n      <p class="jmbp-p">' + content + "</p>\n")
        elif section_type == "h2":
            parts.append('\n      <h2 class="jmbp-h2">' + content + "</h2>\n")
        elif section_type == "impact":
            parts.append('\n      <p class="jmbp-impact">' + content + "</p>\n")
        elif section_type == "beat":
            parts.append('\n      <p class="jmbp-beat">' + content + "</p>\n")
        elif section_type == "pullquote":
            parts.append('\n      <div class="jmbp-pullquote">\n        <p>' + content + "</p>\n      </div>\n")
        elif section_type == "reflection":
            parts.append('\n      <div class="jmbp-reflection">\n        <p>' + content + "</p>\n      </div>\n")
        elif section_type == "byline":
            parts.append(_byline_html())
        else:
            raise ValueError("Unknown section type: " + section_type)
    return "".join(parts)


# ── Schema generators ─────────────────────────────────────────────────────────

def _article_schema(e):
    keywords = ", ".join(e["article_tags"])
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": e["ghl_title"],
        "description": e["meta_description"],
        "image": e["og_image_url"],
        "url": "https://thejaymora.com/" + e["slug"],
        "datePublished": e["publish_date_iso"],
        "dateModified": e["publish_date_iso"],
        "articleSection": e["pillar"],
        "keywords": keywords,
        "wordCount": e["word_count"],
        "author": {
            "@type": "Person",
            "name": "Jay Mora",
            "url": "https://thejaymora.com",
            "jobTitle": "High-Ticket Sales Psychologist for Coaches",
            "sameAs": [
                "https://www.linkedin.com/in/thejaymora",
                "https://www.youtube.com/@thejaymora",
                "https://twitter.com/thejaymora",
            ],
        },
        "publisher": {
            "@type": "Organization",
            "name": "Mora Signature Consulting",
            "url": "https://thejaymora.com",
            "logo": {
                "@type": "ImageObject",
                "url": HEADSHOT_URL,
            },
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": "https://thejaymora.com/" + e["slug"],
        },
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + "\n</script>"


def _faq_schema(faqs):
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["a"]},
            }
            for faq in faqs
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + "\n</script>"


def _breadcrumb_schema(e):
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",   "item": "https://thejaymora.com"},
            {"@type": "ListItem", "position": 2, "name": "Essays", "item": "https://thejaymora.com/essays"},
            {
                "@type": "ListItem",
                "position": 3,
                "name": e.get("breadcrumb_title", e["ghl_title"]),
                "item": "https://thejaymora.com/" + e["slug"],
            },
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + "\n</script>"


# ── Piece generators ──────────────────────────────────────────────────────────

def generate_piece1(e, version):
    slug         = e["slug"]
    url          = "https://thejaymora.com/" + slug
    ghl_title    = e["ghl_title"]
    og_title_esc = ghl_title.replace('"', "&quot;")
    meta_desc    = e["meta_description"]
    og_desc      = e.get("og_description", meta_desc)
    og_image     = e["og_image_url"]
    og_image_alt = e["og_image_alt"]
    pub_iso      = e["publish_date_iso"]
    pillar       = e["pillar"]
    edition      = e.get("edition", "")
    pub_display  = e["publish_date_display"]
    ghl_meta     = e.get("ghl_meta_description", meta_desc)
    display_title= e.get("display_title", ghl_title)

    tags_html = "\n".join(
        '<meta property="article:tag" content="' + t + '">' for t in e["article_tags"]
    )

    comment = (
        "<!-- ============================================================\n"
        "     EDITION " + str(edition) + " | ESSAY POST | GHL READY v" + str(version) + "\n"
        "     Title: " + display_title + "\n"
        "     URL Slug: /" + slug + "\n"
        "     Pillar: " + pillar + "\n"
        "     Publish Date: " + pub_display + "\n"
        "     GHL Page Title: " + ghl_title + "\n"
        "     GHL Meta Description (155 chars max, no apostrophes): " + ghl_meta + "\n"
        "     DEPLOY: Piece 1 -> GHL Header Tracking Code (Settings gear -> Tracking Code -> Header tab)\n"
        "             Piece 2 -> GHL Custom Code element (page builder body)\n"
        "     ============================================================ -->"
    )

    return (
        comment + "\n\n"
        "<!-- Title tag -- GHL does not inject one; this is required for SEO -->\n"
        "<title>" + ghl_title + "</title>\n\n"
        "<!-- SEO: Full Meta Stack -->\n"
        '<link rel="canonical" href="' + url + '">\n'
        '<meta name="description" content="' + meta_desc + '">\n'
        '<meta name="robots" content="index, follow">\n'
        '<meta name="author" content="Jay Mora">\n\n'
        "<!-- Open Graph -->\n"
        '<meta property="og:type" content="article">\n'
        '<meta property="og:site_name" content="Jay Mora">\n'
        '<meta property="og:locale" content="en_US">\n'
        '<meta property="og:url" content="' + url + '">\n'
        '<meta property="og:title" content="' + og_title_esc + '">\n'
        '<meta property="og:description" content="' + og_desc + '">\n'
        '<meta property="og:image" content="' + og_image + '">\n'
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
        '<meta property="og:image:alt" content="' + og_image_alt + '">\n'
        '<meta property="article:published_time" content="' + pub_iso + '">\n'
        '<meta property="article:modified_time" content="' + pub_iso + '">\n'
        '<meta property="article:author" content="https://thejaymora.com">\n'
        '<meta property="article:section" content="' + pillar + '">\n'
        + tags_html + "\n\n"
        "<!-- Twitter Card -->\n"
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:site" content="@thejaymora">\n'
        '<meta name="twitter:creator" content="@thejaymora">\n'
        '<meta name="twitter:title" content="' + og_title_esc + '">\n'
        '<meta name="twitter:description" content="' + meta_desc + '">\n'
        '<meta name="twitter:image" content="' + og_image + '">\n'
        '<meta name="twitter:image:alt" content="' + og_image_alt + '">\n\n'
        "<!-- iOS status bar -- keep dark regardless of progress bar color -->\n"
        '<meta name="theme-color" content="#050505">\n\n'
        "<style>\n" + CSS + "\n</style>\n\n"
        + _js_title_force(ghl_title) + "\n"
        + JS_DARK_SCROLL + "\n\n"
        + _article_schema(e) + "\n\n"
        + _faq_schema(e["faqs"]) + "\n\n"
        + _breadcrumb_schema(e) + "\n"
    )


def generate_piece2(e, version):
    og_image_alt  = e["og_image_alt"]
    pillar        = e["pillar"]
    pub_date      = e["publish_date_display"]
    read_time     = e.get("read_time", "10 min read")
    hero_h1       = e["hero_h1"]
    hero_lede     = e["hero_lede"]
    article_html  = render_body_sections(e["body_sections"])

    return (
        "<!-- og:image:alt fallback -- GHL body injection -->\n"
        '<meta property="og:image:alt" content="' + og_image_alt + '">\n\n'
        '<div class="jmbp">\n\n'
        "  <!-- Reading Progress Bar -->\n"
        '  <div id="jmbp-progress"></div>\n\n'
        "  <!-- Slim Nav -->\n"
        '  <nav class="jm-slim-nav" role="navigation" aria-label="Site navigation">\n'
        '    <ul class="jm-slim-nav__links">\n'
        '      <li><a href="https://thejaymora.com">Jay Mora</a></li>\n'
        '      <li><a href="https://thejaymora.com/services">The Work</a></li>\n'
        '      <li><a href="https://thejaymora.com/calculator">Calculator</a></li>\n'
        '      <li><a href="https://thejaymora.com/faq">FAQ</a></li>\n'
        '      <li><a href="https://thejaymora.com/essays">Essays</a></li>\n'
        '      <li><a href="https://thejaymora.com/apply">Apply</a></li>\n'
        "    </ul>\n"
        "  </nav>\n\n"
        '  <div class="jmbp-divider"></div>\n\n'
        "  <!-- Post Hero -->\n"
        '  <header class="jmbp-hero">\n'
        '    <div class="jmbp-hero-inner">\n'
        '      <a href="/essays" class="jmbp-back">All Posts</a>\n'
        '      <span class="jmbp-eyebrow">' + pillar + "</span>\n"
        '      <h1 class="jmbp-hero-title">' + hero_h1 + "</h1>\n"
        '      <p class="jmbp-hero-lede">' + hero_lede + "</p>\n"
        '      <div class="jmbp-hero-meta">\n'
        "        <span>Jay Mora</span>\n"
        '        <span class="jmbp-meta-sep">|</span>\n'
        "        <span>" + pub_date + "</span>\n"
        '        <span class="jmbp-meta-sep">|</span>\n'
        "        <span>" + read_time + "</span>\n"
        "      </div>\n"
        "    </div>\n"
        "  </header>\n\n"
        "  <!-- Body: article + sidebar -->\n"
        '  <div class="jmbp-body">\n\n'
        "    <!-- Article -->\n"
        '    <article class="jmbp-article-card">\n'
        + article_html +
        "    </article>\n\n"
        "    <!-- Sidebar -->\n"
        '    <aside class="jmbp-sidebar">\n'
        '      <div class="jmbp-sidebar-inner">\n\n'
        + _sidebar_cards() + "\n\n"
        "      </div>\n"
        "    </aside>\n\n"
        "  </div>\n\n"
        "  <!-- Mobile CTAs -- hidden on desktop where sidebar shows -->\n"
        '  <div class="jmbp-mobile-cta">\n\n'
        + _mobile_cta_cards() + "\n\n"
        "  </div>\n\n"
        + JS_SIDEBAR_PROGRESS + "\n\n"
        "</div>\n\n\n"
        "<!-- ============================================================\n"
        "     READ ALL ESSAYS\n"
        "     ============================================================ -->\n"
        "<style>\n"
        ".jmor-read-all { text-align:center; padding:48px 20px; background:#050505; }\n"
        ".jmor-read-all a { display:inline-flex; align-items:center; gap:10px; font-family:'DM Sans',sans-serif; font-size:13px; font-weight:500; letter-spacing:0.16em; text-transform:uppercase; color:rgba(245,239,227,.85); text-decoration:none; border:1px solid rgba(245,200,66,.50); padding:13px 32px; border-radius:100px; transition:color .2s, border-color .2s; }\n"
        ".jmor-read-all a:hover { color:#F5C842 !important; border-color:#F5C842; text-decoration:none; }\n"
        "</style>\n"
        '<div class="jmor-read-all">\n'
        '  <a href="https://thejaymora.com/essays">&larr; Read All Essays</a>\n'
        "</div>\n\n\n"
        "<!-- ============================================================\n"
        "     GOLD RULE\n"
        "     ============================================================ -->\n"
        + GOLD_RULE + "\n\n\n"
        "<!-- ============================================================\n"
        "     LINKEDIN NEWSLETTER\n"
        "     ============================================================ -->\n"
        + _newsletter_section() + "\n\n\n"
        "<!-- ============================================================\n"
        "     GOLD RULE\n"
        "     ============================================================ -->\n"
        + GOLD_RULE + "\n\n\n"
        "<!-- ============================================================\n"
        "     3-MINUTE QUALIFICATION BLUEPRINT\n"
        "     ============================================================ -->\n"
        + _blueprint_section() + "\n\n\n"
        "<!-- ============================================================\n"
        "     GOLD RULE\n"
        "     ============================================================ -->\n"
        + GOLD_RULE + "\n\n\n"
        "<!-- ============================================================\n"
        "     EXPLORE MORE CROSSLINKS\n"
        "     ============================================================ -->\n"
        + CROSSLINKS_SECTION + "\n\n\n"
        "<!-- ============================================================\n"
        "     GOLD RULE\n"
        "     ============================================================ -->\n"
        + GOLD_RULE + "\n\n\n"
        "<!-- ============================================================\n"
        "     FOOTER\n"
        "     ============================================================ -->\n"
        + _footer_html() + "\n"
    )


# ── Loader & main ─────────────────────────────────────────────────────────────

def load_essay(input_path):
    spec = importlib.util.spec_from_file_location("essay_input", input_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.essay


def main():
    parser = argparse.ArgumentParser(description="Generate GHL essay deploy files from essay data.")
    parser.add_argument("input",           help="Path to essay input .py file")
    parser.add_argument("--version", "-v", type=int, default=1, help="Output version number (default: 1)")
    args = parser.parse_args()

    e = load_essay(os.path.expanduser(args.input))
    v = args.version

    week_tag = e.get("week_tag", "WEEK{:02d}".format(e.get("edition", 0)))

    p1_name = "ESSAY-{}-PIECE1-HEADER-v{}.txt".format(week_tag, v)
    p2_name = "ESSAY-{}-PIECE2-BODY-v{}.txt".format(week_tag, v)
    p1_path = PAGES_DIR / p1_name
    p2_path = PAGES_DIR / p2_name

    p1_path.write_text(generate_piece1(e, v), encoding="utf-8")
    p2_path.write_text(generate_piece2(e, v), encoding="utf-8")

    print("  Piece 1: {}".format(p1_path))
    print("  Piece 2: {}".format(p2_path))
    print("\nDone. Deploy to GHL:")
    print("  Piece 1 -> Settings gear -> Tracking Code -> Header tab")
    print("  Piece 2 -> Custom Code element (page builder body)")


if __name__ == "__main__":
    main()
