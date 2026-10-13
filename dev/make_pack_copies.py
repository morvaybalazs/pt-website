#!/usr/bin/env python3
"""Makes the PDF copies of the coaching terms and the privacy notice for the New client pack.

The pages on this site are the master. A client can be sent a link, or one of these copies as an
attachment. Each copy carries its page's "Last updated" date in its name, and dev/check_site.py
fails when a copy is older than its page. So after changing either page, run:

    python3 dev/make_pack_copies.py

It prints with Google Chrome and installs nothing. The copies go to the New client pack folder in
Google Drive on this Mac, or to the folder given with --out.
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

SITE = pathlib.Path(__file__).resolve().parent.parent
ADDRESS = "https://bmorvay.com/"
COPIES = {"terms.html": "Coaching terms", "privacy.html": "Privacy notice"}
PACK = "Library/CloudStorage/GoogleDrive-*/My Drive/Program Builder Forms/Business/New client pack"
CHROME = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "google-chrome", "chromium"]

STYLE = """
@page { size: A4; margin: 20mm 18mm 22mm;
        @bottom-center { content: "Page " counter(page) " of " counter(pages);
                         font: 9pt Helvetica, Arial, sans-serif; color: #555; } }
body { font: 11pt/1.5 Helvetica, Arial, sans-serif; color: #111; }
h1 { font-size: 22pt; margin: 0 0 4pt; }
h2 { font-size: 14pt; margin: 18pt 0 6pt; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 12pt 0 4pt; break-after: avoid; }
p, li { margin: 0 0 6pt; }
ul, ol { padding-left: 18pt; margin: 0 0 8pt; }
a { color: #111; }
.eyebrow { display: none; }
.lead { color: #444; margin-bottom: 10pt; }
.source { font-size: 9pt; color: #555; border-bottom: 0.5pt solid #999; padding-bottom: 6pt;
          margin-bottom: 14pt; }
.legal-toc { border: 0.5pt solid #bbb; padding: 8pt 12pt 2pt; margin: 10pt 0 14pt; }
.legal-toc p { font-weight: bold; }
.cancel-form { border: 0.75pt dashed #777; padding: 10pt 14pt 4pt; break-inside: avoid; }
"""


def page_date(html):
    """The date a page says it was last updated, as written on the page."""
    found = re.search(r"Last updated (\d{1,2} [A-Z][a-z]+ \d{4})", html)
    return found.group(1) if found else None


def copy_name(label, date):
    return f"{label} (website copy, {date}).pdf"


def pack_folders():
    """The New client pack in Google Drive, where this Mac has one."""
    return sorted(p for p in pathlib.Path.home().glob(PACK) if p.is_dir())


def printable(name):
    """(the page's words as a document that prints cleanly, its date). Nothing is reworded."""
    html = (SITE / name).read_text()
    date = page_date(html)
    main = re.search(r"<main\b[^>]*>(.*?)</main>", html, flags=re.S)
    if not date or not main:
        sys.exit(f"{name}: no 'Last updated' date or no main content, so no copy was made")
    body = re.sub(r'href="(?!https?:|mailto:|tel:|#)([^"]+)"', lambda m: f'href="{ADDRESS}{m.group(1)}"',
                  main.group(1))
    title = COPIES[name]
    source = f"B. Morvay Coaching. A copy of {ADDRESS}{name}, as last updated on {date}."
    return (f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{title}</title>'
            f"<style>{STYLE}</style></head><body><p class=\"source\">{source}</p>{body}</body></html>"), date


def chrome():
    for candidate in CHROME:
        path = candidate if pathlib.Path(candidate).is_file() else shutil.which(candidate)
        if path:
            return path
    sys.exit("Google Chrome was not found, and it does the printing")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=pathlib.Path, help="folder to write to instead of the pack in Drive")
    args = parser.parse_args()
    folders = [args.out] if args.out else pack_folders()
    if not folders:
        sys.exit("The New client pack folder was not found in Google Drive. Use --out FOLDER.")
    browser = chrome()
    with tempfile.TemporaryDirectory() as work:
        work = pathlib.Path(work)
        for name, label in COPIES.items():
            document, date = printable(name)
            source = work / name
            source.write_text(document)
            made = work / copy_name(label, date)
            subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            f"--user-data-dir={work / 'profile'}", f"--print-to-pdf={made}",
                            source.as_uri()], check=True, capture_output=True, timeout=180)
            if not made.is_file() or made.stat().st_size < 1000:
                sys.exit(f"{name}: Chrome did not make a PDF")
            for folder in folders:
                folder.mkdir(parents=True, exist_ok=True)
                # Only this script's own earlier copies of the same page are replaced.
                for old in folder.glob(copy_name(label, "*")):
                    if old.name != made.name:
                        old.unlink()
                shutil.copyfile(made, folder / made.name)
                print(f"made: {folder / made.name}")


if __name__ == "__main__":
    main()
