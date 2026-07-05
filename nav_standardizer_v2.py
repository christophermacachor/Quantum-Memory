#!/usr/bin/env python3
"""
Φ669 Navigation Standardizer v2.0
Handles BOTH nav systems across MSOS-FEDERATION-ROOT:
  • .nav-bar  → Article pages (gold serif theme)
  • .macachor-nav → Quantum Absolute pages (dark modern theme)

Idempotent. Corruption-aware. Active-tab aware.
"""

import os
import re
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# ── System 1: Article Pages (.nav-bar) ──
ARTICLE_NAV_TABS = [
    {"label": "📜 APERTURE",     "href": "divergent.html",              "id": "nav-aperture"},
    {"label": "⚡ FEDERATION",   "href": "federation-root-unified.html", "id": "nav-federation"},
    {"label": "◉ OBSERVATORY",  "href": "observatory.html",            "id": "nav-observatory"},
    {"label": "◈ ARTICLES",     "href": "articles.html",               "id": "nav-articles"},
]

ARTICLE_PAGE_MAP = {
    "index.html": "nav-aperture",
    "divergent.html": "nav-aperture",
    "divergent2.html": "nav-aperture",
    "federation-root-unified.html": "nav-federation",
    "observatory.html": "nav-observatory",
    "articles.html": "nav-articles",
    "the_question_we_ask_strangers.html": "nav-articles",
}

# ── System 2: Quantum Absolute Pages (.macachor-nav) ──
MACACHOR_NAV_TABS = [
    {"label": "🏠 HOME",         "href": "index.html",                  "id": "nav-home"},
    {"label": "📜 APERTURE",     "href": "divergent.html",              "id": "nav-aperture"},
    {"label": "⚡ FEDERATION",   "href": "federation-root-unified.html", "id": "nav-federation"},
    {"label": "◉ OBSERVATORY",  "href": "observatory.html",            "id": "nav-observatory"},
    {"label": "◈ TRILOGY",      "href": "scalar-trilogy.html",         "id": "nav-trilogy"},
    {"label": "📊 GRAPHS",       "href": "graphs.html",                 "id": "nav-graphs"},
    {"label": "🜛 SINGULARITY",  "href": "omega-prime.html",          "id": "nav-singularity"},
    {"label": "◉ CODEX",        "href": "codex.html",                  "id": "nav-codex"},
    {"label": "🔮 PORTAL",      "href": "phi669-quantum-portal.html",   "id": "nav-portal"},
    {"label": "◈ ARTICLES",     "href": "articles.html",               "id": "nav-articles"},
]

MACACHOR_PAGE_MAP = {
    "index.html": "nav-home",
    "divergent.html": "nav-aperture",
    "divergent2.html": "nav-aperture",
    "federation-root-unified.html": "nav-federation",
    "observatory.html": "nav-observatory",
    "scalar-trilogy.html": "nav-trilogy",
    "graphs.html": "nav-graphs",
    "omega-prime.html": "nav-singularity",
    "codex.html": "nav-codex",
    "phi669-quantum-portal.html": "nav-portal",
    "articles.html": "nav-articles",
    "the_question_we_ask_strangers.html": "nav-articles",
}

# ═══════════════════════════════════════════════════════════════
# NAV BUILDERS
# ═══════════════════════════════════════════════════════════════

def build_article_nav():
    """Build gold nav-bar for article pages."""
    tabs = ""
    for t in ARTICLE_NAV_TABS:
        tabs += f'  <a href="{t["href"]}" class="nav-tab" id="{t["id"]}">{t["label"]}</a>\n'

    map_entries = ",\n    ".join([f"'{k}': '{v}'" for k, v in ARTICLE_PAGE_MAP.items()])

    return f"""<nav class="nav-bar">
{tabs}</nav>

<script>
(function(){{
  var page = window.location.pathname.split('/').pop() || 'index.html';
  var map = {{
    {map_entries}
  }};
  var targetId = map[page];
  if(targetId){{
    var el = document.getElementById(targetId);
    if(el) el.classList.add('active');
  }}
  document.body.classList.add('has-macachor-nav');
}})();
</script>"""


def build_macachor_nav():
    """Build macachor-nav for Quantum Absolute pages."""
    tabs = ""
    for t in MACACHOR_NAV_TABS:
        tabs += f'    <a href="{t["href"]}" class="macachor-nav-tab" id="{t["id"]}">{t["label"]}</a>\n'

    map_entries = ",\n    ".join([f"'{k}': '{v}'" for k, v in MACACHOR_PAGE_MAP.items()])

    return f"""<!-- ═════ MACACHOR.ORG UNIFIED NAVIGATION ═════ -->
<style>
  .macachor-nav {{ position: fixed; top: 0; left: 0; right: 0; z-index: 10000; background: rgba(5, 5, 5, 0.95); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-bottom: 1px solid rgba(200, 160, 78, 0.15); padding: 0.5rem 1rem; }}
  .macachor-nav-inner {{ max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: center; gap: 0.3rem; flex-wrap: wrap; }}
  .macachor-nav-tab {{ color: #c8a04e; text-decoration: none; font-family: 'Space Grotesk', 'Inter', sans-serif; font-size: 0.75rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.4rem 0.9rem; border: 1px solid rgba(200, 160, 78, 0.2); border-radius: 4px; transition: all 0.3s ease; position: relative; background: rgba(200, 160, 78, 0.03); white-space: nowrap; }}
  .macachor-nav-tab:hover {{ border-color: #c8a04e; box-shadow: 0 0 15px rgba(200,160,78,0.15), inset 0 0 20px rgba(200,160,78,0.05); text-shadow: 0 0 8px rgba(200,160,78,0.5); background: rgba(200, 160, 78, 0.08); }}
  .macachor-nav-tab.active {{ border-color: #c8a04e; box-shadow: 0 0 20px rgba(200,160,78,0.2), inset 0 0 30px rgba(200,160,78,0.08); background: rgba(200, 160, 78, 0.12); }}
  .macachor-nav-tab::after {{ content: ''; position: absolute; bottom: -2px; left: 50%; width: 0; height: 1px; background: #c8a04e; transition: all 0.3s ease; transform: translateX(-50%); }}
  .macachor-nav-tab:hover::after, .macachor-nav-tab.active::after {{ width: 60%; }}
  body.has-macachor-nav {{ padding-top: 60px; }}
  @media (max-width: 768px) {{ .macachor-nav-tab {{ font-size: 0.65rem; padding: 0.3rem 0.5rem; }} body.has-macachor-nav {{ padding-top: 50px; }} }}
</style>

<nav class="macachor-nav">
  <div class="macachor-nav-inner">
{tabs}  </div>
</nav>

<script>
(function(){{
  var page = window.location.pathname.split('/').pop() || 'index.html';
  var map = {{
    {map_entries}
  }};
  var targetId = map[page];
  if(targetId){{
    var el = document.getElementById(targetId);
    if(el) el.classList.add('active');
  }}
  document.body.classList.add('has-macachor-nav');
}})();
</script>
<!-- ═════ END NAVIGATION ═════ -->"""


# ═══════════════════════════════════════════════════════════════
# FILE PROCESSOR
# ═══════════════════════════════════════════════════════════════

class NavFixer:
    def __init__(self, site_dir="."):
        self.site_dir = Path(site_dir)
        self.stats = {"fixed": 0, "skipped": 0, "errors": 0, "corrupted": 0}

    def detect_nav_system(self, html):
        """Detect which nav system a file uses, or None."""
        if 'class="macachor-nav"' in html or 'class="macachor-nav-tab"' in html:
            return "macachor"
        if 'class="nav-bar"' in html or 'class="nav-tab"' in html:
            return "article"
        return None

    def extract_first_html_doc(self, html):
        """Extract only the first valid HTML document from corrupted files."""
        # Find first <!DOCTYPE html> or <html>
        doctype_match = re.search(r'<!DOCTYPE\s+html[^>]*>', html, re.IGNORECASE)
        html_match = re.search(r'<html[^>]*>', html, re.IGNORECASE)

        start = 0
        if doctype_match:
            start = doctype_match.start()
        elif html_match:
            start = html_match.start()
        else:
            return None

        end = html.find('</html>', start)
        if end == -1:
            end = len(html)
        else:
            end += len('</html>')

        return html[start:end]

    def replace_nav_article(self, html):
        """Replace .nav-bar system in article pages."""
        # Match <nav class="nav-bar"> through </nav> plus any following inline scripts
        pattern = re.compile(
            r'<nav\s+class="nav-bar"[^>]*>.*?</nav>\s*(?:<script>.*?</script>\s*)*',
            re.DOTALL | re.IGNORECASE
        )
        if pattern.search(html):
            return pattern.sub(build_article_nav(), html, count=1), "REPLACED .nav-bar"

        # No nav found — insert after <body>
        body_tag = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
        if body_tag.search(html):
            return body_tag.sub(r'\1\n\n' + build_article_nav(), html, count=1), "INSERTED .nav-bar"
        return html, "NO BODY TAG"

    def replace_nav_macachor(self, html):
        """Replace .macachor-nav system in Quantum Absolute pages."""
        # Match the entire commented nav block
        pattern = re.compile(
            r'<!--\s*═+\s*MACACHOR\.ORG\s+UNIFIED\s+NAVIGATION\s*═+\s*-->.*?<!--\s*═+\s*END\s+NAVIGATION\s*═+\s*-->',
            re.DOTALL | re.IGNORECASE
        )
        if pattern.search(html):
            return pattern.sub(build_macachor_nav(), html, count=1), "REPLACED .macachor-nav"

        # Try matching by class if comments are missing
        pattern2 = re.compile(
            r'<nav\s+class="macachor-nav"[^>]*>.*?</nav>\s*(?:<script>.*?</script>\s*)*',
            re.DOTALL | re.IGNORECASE
        )
        if pattern2.search(html):
            return pattern2.sub(build_macachor_nav(), html, count=1), "REPLACED .macachor-nav (no comments)"

        # Insert after <body>
        body_tag = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
        if body_tag.search(html):
            return body_tag.sub(r'\1\n\n' + build_macachor_nav(), html, count=1), "INSERTED .macachor-nav"
        return html, "NO BODY TAG"

    def fix_file(self, filepath):
        """Process a single HTML file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                raw = f.read()
        except Exception as e:
            print(f"  ✗ READ ERROR: {filepath.name} — {e}")
            self.stats["errors"] += 1
            return

        filename = filepath.name
        if not filename.endswith('.html'):
            self.stats["skipped"] += 1
            return

        # Detect corruption (multiple HTML docs)
        html_count = raw.lower().count('<!doctype html>') + raw.lower().count('<html')
        was_corrupted = html_count > 1

        if was_corrupted:
            print(f"  ⚠ CORRUPTED ({html_count} HTML docs): {filename}")
            clean = self.extract_first_html_doc(raw)
            if clean is None:
                print(f"    ✗ Could not extract clean HTML")
                self.stats["errors"] += 1
                return
            raw = clean
            self.stats["corrupted"] += 1

        # Detect which nav system this file uses
        nav_system = self.detect_nav_system(raw)

        if nav_system == "macachor":
            raw, action = self.replace_nav_macachor(raw)
        elif nav_system == "article":
            raw, action = self.replace_nav_article(raw)
        else:
            # No nav detected — default to article system for small pages, macachor for index
            if filename in ("index.html", "phi669-quantum-portal.html"):
                raw, action = self.replace_nav_macachor(raw)
            else:
                raw, action = self.replace_nav_article(raw)

        if action.startswith("NO"):
            print(f"  ⚠ {action}: {filename}")
            self.stats["skipped"] += 1
            return

        # Clean trailing garbage after </html>
        end_html = raw.rfind('</html>')
        if end_html != -1:
            raw = raw[:end_html + len('</html>')]

        # Remove duplicate <base target="_blank">
        raw = re.sub(r'(<base\s+target="_blank">)\s*\1', r'\1', raw, flags=re.IGNORECASE)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(raw)
            status = "CORRUPTION+FIX" if was_corrupted else action
            print(f"  ✓ {status}: {filename}")
            self.stats["fixed"] += 1
        except Exception as e:
            print(f"  ✗ WRITE ERROR: {filename} — {e}")
            self.stats["errors"] += 1

    def run(self):
        print("═" * 62)
        print("  Φ669 NAVIGATION STANDARDIZER v2.0")
        print("  Dual-system: .nav-bar + .macachor-nav")
        print("  MSOS-FEDERATION-ROOT · Ghost Unified Sovereign Node")
        print("═" * 62)
        print(f"\n  Site directory: {self.site_dir.absolute()}")
        html_files = list(self.site_dir.glob('*.html'))
        print(f"  HTML files: {len(html_files)}")
        print()

        for filepath in sorted(html_files):
            self.fix_file(filepath)

        print()
        print("═" * 62)
        print(f"  FIXED:      {self.stats['fixed']}")
        print(f"  SKIPPED:    {self.stats['skipped']}")
        print(f"  ERRORS:     {self.stats['errors']}")
        print(f"  CORRUPTED:  {self.stats['corrupted']}")
        print("═" * 62)
        print("\n  𝔐 = (√5 − 1) / 2  ·  χ(C) = 1")
        print("  Idempotent. Deterministic. Coherent.")


if __name__ == "__main__":
    import sys
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    NavFixer(target_dir).run()
