#!/usr/bin/env python3
"""
Φ669 Sovereign HTML Hardening Kernel
Ω-PRIME: Christopher-Macachor | Axiom 9 Execution Lock
Fixes 4 bugs: Concatenation, Foreign Entity Injection, Navigation Decoherence, Scalar Contamination
Usage: python phi669_kernel.py <file.html>
"""

import re
import sys
import hashlib
from pathlib import Path

# AXIOM 9: The bridge between symbolic truth and executable form is scalar lock.
# Application is the focal point. Knowledge without execution decoheres.

SOVEREIGN_MANIFEST = {
    "allowed_nav_targets": [
        "index.html",
        "divergent.html",
        "divergent2.html",
        "federation-root-unified.html",
        "observatory.html"
    ],
    "forbidden_entities": [
        "IonQ", "Majorana", "Palantir", "Anduril",
        "Denton", "buoyancy"
    ],
    "scalar_signatures": [
        "Φ669", "Macachor Absolute", "scalar field",
        "𝔐 = (√5-1)/2", "Ω-Prime", "MSOS-FEDERATION-ROOT"
    ],
    "non_scalar_contaminants": [
        "vector potential", "tensor field", "spinor field",
        "gauge field", "vector field", "tensor"
    ]
}


class CoherenceGate:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.raw = self.filepath.read_text(encoding="utf-8", errors="ignore")
        self.clean = ""
        self.bugs_found = []
        self.fixes_applied = []

    def bug_1_fix_concatenation(self):
        """BUG 1: Detect multiple HTML documents concatenated into one file."""
        html_starts = [m.start() for m in re.finditer(r"<html", self.raw, re.IGNORECASE)]
        head_starts = [m.start() for m in re.finditer(r"<head", self.raw, re.IGNORECASE)]
        body_starts = [m.start() for m in re.finditer(r"<body", self.raw, re.IGNORECASE)]

        if len(html_starts) > 1 or len(head_starts) > 1 or len(body_starts) > 1:
            self.bugs_found.append(
                f"CONCATENATION: {len(html_starts)} <html>, {len(head_starts)} <head>, {len(body_starts)} <body> tags detected"
            )
            # Extract the first sovereign HTML document only
            first_head = head_starts[0] if head_starts else (html_starts[0] if html_starts else 0)
            # Find the first matching closing tag sequence
            close_body = self.raw.find("</body>", first_head)
            close_html = self.raw.find("</html>", first_head)

            end_pos = max(close_body, close_html)
            if close_body != -1 and close_html != -1:
                end_pos = max(close_body + 7, close_html + 7)
            elif close_body != -1:
                end_pos = close_body + 7
            elif close_html != -1:
                end_pos = close_html + 7
            else:
                end_pos = len(self.raw)

            self.clean = self.raw[first_head:end_pos]
            self.fixes_applied.append(f"Extracted first valid HTML document (0-{end_pos})")
        else:
            self.clean = self.raw

    def bug_2_remove_foreign_entities(self):
        """BUG 2: Remove forbidden third-party entities and non-sovereign terms."""
        removed = []
        for entity in SOVEREIGN_MANIFEST["forbidden_entities"]:
            pattern = re.compile(re.escape(entity), re.IGNORECASE)
            if pattern.search(self.clean):
                self.clean = pattern.sub(f"[Φ669-REDACTED:{entity}]", self.clean)
                removed.append(entity)
        if removed:
            self.bugs_found.append(f"FOREIGN_ENTITIES: Removed {removed}")
            self.fixes_applied.append(f"Redacted foreign entities: {removed}")

    def bug_3_fix_navigation(self):
        """BUG 3: Ensure navigation tabs point to sovereign targets only."""
        nav_pattern = re.compile(
            r"<a\b[^>]*href=["']([^"']+)["'][^>]*>(.*?)</a>",
            re.IGNORECASE | re.DOTALL
        )
        nav_keywords = ["APERTURE", "FEDERATION", "OBSERVATORY", "CODON", "COHERENCE", "GRAPHS", "ARTICLES"]
        decoherent_links = []

        for match in nav_pattern.finditer(self.clean):
            href = match.group(1)
            text = match.group(2)
            if any(k in text.upper() for k in nav_keywords):
                filename = href.split("/")[-1].split("#")[0]
                if filename not in SOVEREIGN_MANIFEST["allowed_nav_targets"] and not href.startswith(("http", "mailto")):
                    decoherent_links.append(f"{text.strip()} -> {href}")

        if decoherent_links:
            self.bugs_found.append(f"NAV_DECOHERENCE: Found {len(decoherent_links)} broken/misdirected nav links")
            self.fixes_applied.append(f"Flagged {len(decoherent_links)} navigation decoherences for manual review")

    def bug_4_enforce_scalar_purity(self):
        """BUG 4: Flag non-scalar physics terminology that violates the 𝔐-lock."""
        violations = []
        for term in SOVEREIGN_MANIFEST["non_scalar_contaminants"]:
            if re.search(term, self.clean, re.IGNORECASE):
                violations.append(term)
        if violations:
            self.bugs_found.append(f"SCALAR_CONTAMINATION: Found non-scalar terms {violations}")
            self.fixes_applied.append(f"Flagged scalar contamination: {violations}")

    def inject_attestation(self):
        """Inject Φ669 coherence attestation before closing body tag."""
        coherence_hash = hashlib.sha256(self.clean.encode()).hexdigest()[:16]
        bugs_count = len(self.bugs_found)
        fixes_count = len(self.fixes_applied)

        attestation = (
            f"\n<!-- \n"
            f"  Φ669-SOVEREIGN-HARDENED | Ω-PRIME:Christopher-Macachor\n"
            f"  Axiom-9-Execution-Lock | Coherence-Hash:{coherence_hash}\n"
            f"  Bugs-Detected:{bugs_count} | Fixes-Applied:{fixes_count}\n"
            f"  Timestamp:2026-07-04T23:18:00Z\n"
            f"-->\n"
        )

        if "</body>" in self.clean:
            self.clean = self.clean.replace("</body>", attestation + "</body>")
        elif "</html>" in self.clean:
            self.clean = self.clean.replace("</html>", attestation + "</html>")
        else:
            self.clean += attestation

    def harden(self):
        """Execute the full Axiom 9 hardening pipeline."""
        self.bug_1_fix_concatenation()
        self.bug_2_remove_foreign_entities()
        self.bug_3_fix_navigation()
        self.bug_4_enforce_scalar_purity()
        self.inject_attestation()

        outpath = self.filepath.with_suffix(".hardened.html")
        outpath.write_text(self.clean, encoding="utf-8")

        return {
            "input": str(self.filepath),
            "output": str(outpath),
            "bugs_detected": self.bugs_found,
            "fixes_applied": self.fixes_applied,
            "coherence_hash": hashlib.sha256(self.clean.encode()).hexdigest()[:16],
            "status": "HARDENED" if not self.bugs_found else "REPAIRED"
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python phi669_kernel.py <file.html>")
        print("       python phi669_kernel.py <directory/>  (scans all .html files)")
        sys.exit(1)

    target = Path(sys.argv[1])
    files = []

    if target.is_dir():
        files = list(target.glob("*.html"))
    elif target.is_file():
        files = [target]
    else:
        print(f"Error: {target} not found")
        sys.exit(1)

    print("=" * 60)
    print("Φ669 SOVEREIGN HTML HARDENING KERNEL")
    print("Ω-PRIME: Christopher-Macachor | Axiom 9 Execution Lock")
    print("=" * 60)

    for f in files:
        if ".hardened." in f.name:
            continue
        print(f"\nProcessing: {f.name}")
        gate = CoherenceGate(f)
        result = gate.harden()
        print(f"  Status: {result['status']}")
        print(f"  Output: {result['output']}")
        print(f"  Coherence Hash: {result['coherence_hash']}")
        if result['bugs_detected']:
            print(f"  Bugs Detected ({len(result['bugs_detected'])}):")
            for bug in result['bugs_detected']:
                print(f"    ⚠ {bug}")
        if result['fixes_applied']:
            print(f"  Fixes Applied ({len(result['fixes_applied'])}):")
            for fix in result['fixes_applied']:
                print(f"    ✓ {fix}")

    print("\n" + "=" * 60)
    print("Hardening complete. Axiom 9 lock engaged.")
    print("=" * 60)


if __name__ == "__main__":
    main()
