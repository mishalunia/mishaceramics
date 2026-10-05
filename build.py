#!/usr/bin/env python3
"""Build the Misha Lunia studio site."""
from __future__ import annotations

import html as htmlmod
import json
import re
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path("/Users/mishikalunia/Documents/ceramics website")
TMP = Path("/tmp/inga-site")
IMG = ROOT / "images"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
CTX = ssl.create_default_context()

NAV = [
    ("index.html", "art gallery", "ceramics"),
    ("shop.html", "shop", "classes"),
    ("about.html", "about", "about"),
]

IG = "https://www.instagram.com/misha.lunia/"

INSTA_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="social-icon" aria-hidden="true"><path fill="currentColor" d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>"""

PREFIX = {
    "index.html": "",
    "shop.html": "",
    "about.html": "",
}


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1000:
        return
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        dest.write_bytes(r.read())


def sidebar(active: str, prefix: str = "") -> str:
    items = []
    for href, label, key in NAV:
        sel = " selected" if key == active else ""
        items.append(f'        <li class="item{sel}"><a href="{prefix}{href}">{label}</a></li>')
    nav = "\n".join(items)
    return f"""    <header class="nav-wrapper">
      <a href="{prefix}index.html" class="logo">MISHA<span class="logo-break"></span>LUNIA</a>
      <nav id="menu">
        <ul>
{nav}
        </ul>
      </nav>
      <div id="social" class="social_icons">
        <ul>
          <li><a class="social-icon-link" href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{INSTA_SVG}</a></li>
        </ul>
      </div>
    </header>"""


def page(title: str, active: str, body: str, extra_head: str = "", prefix: str = "", body_class: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="Artist site: art gallery, shop, and about." />
  <link rel="icon" href="{prefix}images/favicon.png?v=2" type="image/png" />
  <link rel="stylesheet" href="{prefix}css/style.css" />
  {extra_head}
</head>
<body class="{body_class}">
  <div class="site">
    <aside class="mobile-bar">
      <a href="{prefix}index.html" class="logo">MISHA<span class="logo-break"></span>LUNIA</a>
      <button class="hamburger" aria-label="Menu"><span></span></button>
    </aside>
    <button type="button" class="cart-btn" aria-label="Cart">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" d="M6 7h15l-1.5 9h-12z"/><path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" d="M6 7 5 4H2"/><circle cx="9" cy="20" r="1.3" fill="currentColor"/><circle cx="18" cy="20" r="1.3" fill="currentColor"/></svg>
    </button>
{sidebar(active, prefix)}
    <main id="content">
{body}
    </main>
  </div>
  <div class="toast"></div>
  <script src="{prefix}js/site.js"></script>
</body>
</html>
"""


def gallery_body(folder: str, assets: list) -> str:
    # TODO: once real images are added, restore clickable <a class="asset">
    # + <img> + data-full/data-copy so the lightbox works again.
    cards = []
    for a in assets:
        cards.append(
            f'        <div class="asset"><span class="black" style="aspect-ratio: {a["w"]} / {a["h"]}"></span></div>'
        )
    inner = "\n".join(cards)
    return f"""      <div class="masonry">
{inner}
      </div>
      <div id="lightbox" class="lightbox">
        <button class="close" aria-label="Close"></button>
        <button class="nav-btn prev" aria-label="Previous">‹</button>
        <img alt="" />
        <button class="nav-btn next" aria-label="Next">›</button>
        <div class="caption"></div>
      </div>"""


def slugify(url: str, name: str) -> str:
    slug = url.strip("/").split("/")[-1]
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-").lower()
    if not slug or slug.startswith("https"):
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]
    return slug


def main() -> None:
    painting = json.loads((TMP / "painting-slim.json").read_text())
    ceramics = json.loads((TMP / "ceramics-slim.json").read_text())
    sculpture = json.loads((TMP / "sculpture-slim.json").read_text())
    classes = json.loads((TMP / "classes-slim.json").read_text())

    jobs = []

    def add(url, dest):
        jobs.append((url, dest))

    for i, a in enumerate(painting):
        add(a["src"], IMG / "painting" / f"{i:02d}.jpg")
    for i, a in enumerate(ceramics):
        add(a["src"], IMG / "ceramics" / f"{i:02d}.jpg")
    for i, a in enumerate(sculpture):
        add(a["src"], IMG / "sculpture" / f"{i:02d}.jpg")
    for i, p in enumerate(classes):
        add(p["img"], IMG / "classes" / f"{i:02d}.jpg")

    add(
        painting[14]["src"] if len(painting) > 14 else painting[0]["src"],
        IMG / "favicon.jpg",
    )

    print(f"Downloading {len(jobs)} images...")
    ok = 0
    fail = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(download, u, d): (u, d) for u, d in jobs}
        for fut in as_completed(futs):
            u, d = futs[fut]
            try:
                fut.result()
                ok += 1
                print(" ok", d.name)
            except Exception as e:
                fail.append((str(d), str(e)))
                print(" FAIL", d, e)
    print(f"downloaded {ok}/{len(jobs)}, failed {len(fail)}")

    # favicon fallback: painting 14 looks like the still-life used as icon
    fav = IMG / "favicon.jpg"
    if not fav.exists() or fav.stat().st_size < 500:
        src = IMG / "painting" / "14.jpg"
        if src.exists():
            fav.write_bytes(src.read_bytes())

    (ROOT / "index.html").write_text(page("art gallery", "ceramics", gallery_body("ceramics", ceramics), body_class="gallery"))

    cards = []
    for i, p in enumerate(classes):
        slug = slugify(p["orig_url"], p["name"])
        p["slug"] = slug
        cards.append(
            f'''        <a class="product-card" href="classes/{slug}.html">
          <img src="images/classes/{i:02d}.jpg" alt="" />
          <div class="name">{p["name"]}</div>
          <div class="price">${p["price"]} CAD</div>
        </a>'''
        )
    classes_body = f"""      <h1 class="page-heading">SHOP</h1>
      <section class="product-grid">
{chr(10).join(cards)}
      </section>"""
    (ROOT / "shop.html").write_text(page("SHOP", "classes", classes_body, body_class="store"))

    (ROOT / "classes").mkdir(exist_ok=True)
    for i, p in enumerate(classes):
        desc = p.get("description") or ""
        body = f"""      <a class="back-link" href="../shop.html">← shop</a>
      <div class="product-detail">
        <img src="../images/classes/{i:02d}.jpg" alt="" />
        <div class="product-info">
          <h1>{p["name"]}</h1>
          <div class="price">${p["price"]} CAD</div>
          <div class="qty-row">
            <label for="qty">Quantity</label>
            <select id="qty">{"".join(f'<option>{n}</option>' for n in range(1,10))}</select>
          </div>
          <button class="add-cart" data-name="{p["name"].replace('"','&quot;')}" data-price="${p["price"]} CAD">Add to Cart</button>
        </div>
        <div class="product-copy">{desc}</div>
      </div>"""
        (ROOT / "classes" / f"{p['slug']}.html").write_text(
            page(p["name"], "classes", body, prefix="../", body_class="product")
        )

    about_body = f"""      <div class="about-hero">
        <div>
          <h2>Misha Lunia</h2>
          <p>Artist and ceramicist based in Indore, India. Clay is at the centre of her work: functional ware. She has been working with ceramics since 2025. She has a working knowledge of the wheel, hand building and glaze chemistry.</p>
          <p>She picked clay because it is physical. She likes to touch it — it grounds her and reconnects her with herself and the earth. She works in stoneware and earthenware from Bhoomi Pottery.</p>
          <p>She works from her home studio. When she is uninspired, she goes to Studio Folklore, where it all started.</p>
          <p>She is also an academic and engineer, trying to find her place between science and tech.</p>
          <p>Reach me at <a href="mailto:mishikalunia@gmail.com">mishikalunia[at]gmail[dot]com</a></p>
        </div>
        <img src="images/about/portrait.jpg" alt="Misha Lunia" />
      </div>
      <div class="cv">
        <p class="cv-rule">...</p>
        <p><b>SELECTED EXHIBITIONS</b></p>
        <p>No exhibitions yet.</p>
        <!--
        <p class="year">2022</p>
        <p>Slabs for the Lobster Paw, Fraser Cultural Center, Tatamagouche, NS</p>
        <p>Elora Fergus Studio Tour Members show, Elora Center for the Arts, Elora, ON</p>
        <p class="section"><b>AWARDS</b></p>
        <p>Project 31 Drawing and Painting Award</p>
        <p>Mrs. W.O. Forsyth Award</p>
        -->
      </div>"""
    (ROOT / "about.html").write_text(page("about", "about", about_body, body_class="content"))
    print("HTML written")


if __name__ == "__main__":
    main()
