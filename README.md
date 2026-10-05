# Misha Lunia

Artist site for ceramics and a small shop.

**Pages**

- [Art gallery](index.html)
- [Shop](shop.html) — cups and mugs
- [About](about.html)

Instagram: [misha.lunia](https://www.instagram.com/misha.lunia/)  

## Run locally

From this folder:

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

## Add a gallery photo

Put the file in `images/gallery/` (jpg, png, or webp). Name it after the piece, like `bowl.png`. Then run:

```bash
python3 build-gallery.py
```

That adds it to the art gallery and creates `work/bowl.html` if it does not exist yet. You can edit that page for the write-up and extra photos. If you push a new image without running the script, GitHub will build the page for you.

## Fonts and sizes

Loaded from Google Fonts in `css/style.css` ([Zen Kaku Gothic Antique + Zen Kaku Gothic New](https://fontpair.co/playground/zen-kaku-gothic-antique-zen-kaku-gothic-new?color=FFCD70&icons=1)):

- **Zen Kaku Gothic Antique** — name, headings, product names
- **Zen Kaku Gothic New** — body text, nav, prices, buttons (weights 400, 500, 700)

Fallbacks: Avenir Next, Avenir, Helvetica, Arial, sans-serif.

The name is stacked on desktop (MISHA / LUNIA) and one line on mobile.

| Size | Where |
| --- | --- |
| 12px | Gallery “coming soon” labels |
| 13px | Shop “out of stock”, cart empty text, toast |
| 14px | Body copy, nav links, Add to Cart |
| 15px | ← shop / ← art gallery |
| 16px | About section headings, shop card prices |
| 18px | Cart panel title, name in the mobile header |
| 20px | Product page price |
| 22px | Shop product names, work page titles (Vessels, Teapot) |
| 24px | Product page title (Cups/Mugs) |
| 26px | Shop heading |
| 30px | Name in the desktop sidebar |

Default weight is 400. About CV years use 600. Line height for body copy is 1.5.

Page background is `#fffff8`. Link hover is `#b5522a`.
