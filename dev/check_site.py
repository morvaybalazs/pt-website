#!/usr/bin/env python3
"""Checks the website against dev/SERVICE.md and the fixes from the September 2026 review.

Run it before you publish:   python3 dev/check_site.py

It does not need anything installed. It fails loudly if a stale promise comes back, if a page
loses its header, footer or main content, if a link or picture points at a file that is not
there, or if a colour drops below the contrast the guidelines ask for.
"""
import json
import pathlib
import re
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent
PAGES = sorted(p for p in SITE.glob("*.html") if not p.name.startswith("google"))
NOINDEX = {"privacy.html", "terms.html", "thanks.html", "404.html"}
problems = []
notes = []


def fail(page, message):
    problems.append(f"{page}: {message}")


def text_of(html):
    """Visible text only: no tags, scripts, styles or attributes."""
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", body)


# 1. Promises that must not come back (dev/SERVICE.md)
BANNED = [
    (r"\bno contracts\b", "says 'no contracts'; the service has an agreement, say 'no minimum term'"),
    (r"most popular", "'Most Popular' claim has no sales evidence behind it"),
    (r"25\s*-\s*39%|up to 39%", "the 25-39% muscle claim; the studies measured lean mass"),
    (r"updated weekly", "'updated weekly' programming is not what is delivered"),
    (r"weekly or fortnightly", "check-ins are after week 1, then every two weeks"),
    (r"meal planning|I provide meal plans|meal plans included", "no meal plans are provided"),
    (r"myfitnesspal connected", "there is no MyFitnessPal integration"),
    (r"quick daytime replies|within a few hours", "reply times are one working day (enquiries) and two (clients)"),
    (r"no sales pitch", "the call does discuss a paid service"),
    (r"core specialism", "unsupported specialist claim"),
    (r"06:00|21:00", "seven-day opening hours are not real"),
    (r"book (a )?free consultation|book consultation", "the form sends a request, so say 'request'"),
]
# 2. Code-level defects the review found
CODE_BANNED = [
    (r"body\s*{[^}]*transform\s*:", "body transform breaks the fixed header (W01)"),
    (r"images\.pexels\.com|fonts\.googleapis\.com|fonts\.gstatic\.com",
     "loads files from another company; keep fonts and pictures on this site"),
    (r"google\.com/maps/embed", "the embedded map loads Google on every visit; link to the map instead"),
    (r"onclick=", "inline onclick; behaviour belongs in site.js"),
    (r"document\.write", "document.write blocks the page; use [data-year] in site.js"),
    (r"history\.back\(\)", "a 'Back' link that guesses; name the destination"),
    (r'target="_blank"', "internal links should open in the same tab"),
]
PRICES_OK = {"200", "100", "60", "50"}
EQUIPMENT_PRICES = {"150", "400", "800"}  # the home gym budgets
PRICE_FREE = {"home-gym-guide.html"}      # equipment prices live here

# 3. Facts that must be stated (page, regex, what it is)
REQUIRED = [
    ("index.html", r"£200", "the coaching price"),
    ("index.html", r"after your first week, then every two weeks", "the check-in rhythm"),
    ("index.html", r"within two working days", "the reply time for clients"),
    ("index.html", r"within one working day", "the reply time for enquiries"),
    ("index.html", r"No minimum term|no minimum term", "the cancellation wording"),
    ("index.html", r"free pilot", "the testimonials must say they are free pilot clients"),
    ("index.html", r"prescriber stays in charge", "the GLP-1 safety line"),
    ("faq.html", r"18 and over|aged 18 or over", "coaching is for adults"),
    ("faq.html", r"after your first week, then every two weeks", "the check-in rhythm"),
    ("terms.html", r"death or personal injury caused by negligence", "the liability wording the law requires"),
    ("terms.html", r"after your first week, then every two weeks", "the check-in rhythm"),
    ("privacy.html", r"Anthropic", "the AI assistant must be disclosed"),
    ("privacy.html", r"Article 9\(2\)\(a\)", "the lawful basis for health information"),
    ("blog-glp1.html", r"lean mass is not the same as muscle|Lean mass is not the same as muscle", "the lean mass correction"),
]

for page in PAGES:
    html = page.read_text()
    name = page.name
    visible = text_of(html)

    for pattern, why in BANNED:
        if re.search(pattern, visible, re.I):
            fail(name, f"stale promise: {why}")
    for pattern, why in CODE_BANNED:
        if re.search(pattern, html, re.I):
            fail(name, f"defect: {why}")

    # Prices must be ones we actually charge
    if name not in PRICE_FREE:
        for amount in re.findall(r"£\s?([\d,]+)", visible):
            if amount.replace(",", "") not in PRICES_OK | EQUIPMENT_PRICES:
                fail(name, f"price £{amount} is not one of the real prices")

    # Page structure
    if '<main id="main"' not in html:
        fail(name, "no <main id=\"main\"> for the skip link to land on")
    if 'class="skip-link" href="#main"' not in html:
        fail(name, "no skip link")
    if "<title>" not in html:
        fail(name, "no title")
    if 'name="description"' not in html:
        fail(name, "no meta description")
    if name not in NOINDEX and 'rel="canonical"' not in html:
        fail(name, "no canonical link")
    if 'class="site-header"' not in html or 'class="site-footer' not in html:
        fail(name, "missing the shared header or footer")
    for must in ["privacy.html", "terms.html", "faq.html", "library.html"]:
        if must not in html:
            fail(name, f"footer or header link to {must} is missing")
    if "#consultation" not in html:
        fail(name, "no route to the consultation form")
    if 'href="index.html#how-it-works"' not in html and name != "index.html":
        fail(name, "header is missing the How it works link")

    # A table that scrolls sideways must be reachable with a keyboard
    for hit in re.findall(r'<div class="table-wrap"(?! tabindex="0")', html):
        fail(name, "a table that scrolls sideways needs tabindex=\"0\" so a keyboard can reach it")

    # Duplicate ids
    ids = re.findall(r'\sid="([^"]+)"', html)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        fail(name, f"duplicate id(s): {', '.join(sorted(dupes))}")

    # Pictures need alt text and a size, so the page does not jump while loading
    for tag in re.findall(r"<img\b[^>]*>", html):
        if "alt=" not in tag:
            fail(name, f"picture without alt text: {tag[:70]}")
        if "width=" not in tag or "height=" not in tag:
            fail(name, f"picture without width and height: {tag[:70]}")

    # Local links and files must exist
    for target in re.findall(r'(?:href|src)="([^"]+)"', html):
        if target.startswith(("http://", "https://", "mailto:", "tel:", "sms:", "data:", "//", "#")):
            continue
        target = target.split("#")[0].split("?")[0]
        if not target:
            continue
        if not (SITE / target).exists():
            fail(name, f"link or file that is not there: {target}")

    # Structured data must be valid JSON
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            fail(name, f"structured data is not valid JSON: {exc}")

    # Dashes used as punctuation (the testimonial is quoted word for word, so it is allowed)
    for hit in re.findall(r"[a-z,\)] - [a-zA-Z0-9(]", visible):
        if "hotel gyms" in visible and name == "index.html":
            continue
        fail(name, f"dash used as punctuation near '{hit}'")

for page_name, pattern, what in REQUIRED:
    page = SITE / page_name
    if not page.exists():
        fail(page_name, "page is missing")
    elif not re.search(pattern, page.read_text(), re.I):
        fail(page_name, f"does not state {what}")

# 4. Colour contrast of the shared tokens (WCAG 2.1 AA)
css = (SITE / "styles.css").read_text()
tokens = dict(re.findall(r"--([\w-]+):(#[0-9a-fA-F]{6})", css))


def luminance(hex_colour):
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


for fg, bg, least, label in [
    ("ink", "white", 4.5, "body text on white"),
    ("mid", "white", 4.5, "secondary text on white"),
    ("mid", "surface", 4.5, "secondary text on grey"),
    ("muted", "white", 4.5, "quiet text on white"),
    ("muted", "surface", 4.5, "quiet text on grey"),
    ("accent-dim", "white", 4.5, "gold links on white"),
    ("accent-dim", "surface", 4.5, "gold links on grey"),
    ("on-accent", "accent", 4.5, "text on a gold button"),
    ("accent", "black", 4.5, "gold text on black"),
]:
    if fg in tokens and bg in tokens:
        got = ratio(tokens[fg], tokens[bg])
        if got < least:
            fail("styles.css", f"{label} is {got:.2f}:1, needs {least}:1")

print("Checked %d pages." % len(PAGES))
for note in notes:
    print("  note:", note)
if problems:
    print("\n%d problem(s):" % len(problems))
    for problem in problems:
        print("  -", problem)
    sys.exit(1)
print("All checks passed.")
