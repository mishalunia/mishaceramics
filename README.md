# Misha Lunia

Artist site for ceramics and a small shop.

Live at [mishalunia.com/mishaceramics](https://mishalunia.com/mishaceramics/): art gallery, shop (cups and mugs) and about.

Instagram: [mishaaceramics](https://www.instagram.com/mishaaceramics/)  

## How the site is built

GitHub Pages builds the site with Jekyll on every push. There is no build step to run yourself.

- `_layouts/default.html`: the page frame (head, sidebar, nav, cart button, scripts). Every page uses it.
- `_includes/header.html`: the sidebar and nav. Change the nav here once and every page updates.
- `_layouts/work.html`: the artwork page template.
- `_work/`: one short file per artwork.
- `index.html`, `shop.html`, `about.html`, `classes/`: the other pages; each holds only its own content.

CSS and JS links get a fresh `?v=` number on every build, so browsers always pick up changes.

## Add an artwork

1. Put the main photo in `images/gallery/`, for example `bowl.jpg`.
2. Put any process photos in `images/work/bowl/`.
3. Create `_work/bowl.md`:

```markdown
---
title: Bowl
order: 6
image: bowl.jpg
alt: "Short description of the main photo"
process:
  - src: bowl/process-01.jpg
    alt: "Short description of this photo"
---
A sentence or two about the piece.
```

It appears in the art gallery at position `order` (smallest first) and gets its own page at `/work/bowl`. Leave out `process:` if there are no process photos. To reorder the gallery, change the `order` numbers.

## Run locally

With Docker running, build the site exactly as GitHub Pages does:

```bash
docker run --rm -v "$PWD":/src -w /src -e GITHUB_WORKSPACE=/src -e INPUT_SOURCE=. -e INPUT_DESTINATION=./_site -e INPUT_FUTURE=false -e INPUT_VERBOSE=false -e INPUT_BUILD_REVISION=local -e INPUT_TOKEN= ghcr.io/actions/jekyll-build-pages:v1.0.13
```

The built site is in `_site/` (not committed). Serve it under `/mishaceramics/` to match the live address.

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
| 15.5px | ← shop / ← art gallery |
| 16px | About section headings, shop card prices |
| 18px | Cart panel title, name in the mobile header |
| 20px | Product page price |
| 22px | Shop product names, work page titles (Vessels, Teapot) |
| 24px | Product page title (Cups/Mugs) |
| 26px | Shop heading |
| 30px | Name in the desktop sidebar |

Default weight is 400. About CV years use 600. Line height for body copy is 1.5.

Page background is `#fffff8`. Link hover is `#b5522a`.
