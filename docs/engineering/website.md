# Website — architecture

A clickable prototype of the Nanhe store: real, responsive pages built from the
brand's own data and artwork. It is not a working shop. No payments, accounts,
orders or servers.

## Pieces

| Path | Holds |
|---|---|
| `site/` | The Astro project. `npm run build` writes plain static HTML to `site/dist/`. |
| `site/scripts/sync-assets.mjs` | Copies `assets/{logo,packaging,characters,renders}` into `site/public/brand/` before every build. That folder is generated and git-ignored. |
| `site/src/data/catalog.ts` | Joins `docs/product/products.json` (product facts), `assets/characters/characters.json` (little friends), and the website-only sample data below. Every page reads products from here. |
| `site/src/data/shop.json` | **Sample** prices, ratings, review counts, routines and which render to show. Website only. |
| `site/src/data/reviews.json` | **Sample** reviews and questions. Website only. Never ship as real reviews. |
| `site/src/pages/` | `index` (Home), `shop/`, `products/[slug]` (one page per product, 19 in all), `[page]` (placeholder pages for later slices). |
| `site/src/components/` | Header, Footer, Wordmark, ProductCard, AskBand, Icon. |
| `site/src/scripts/cart.ts` | The cart, kept in the visitor's browser (`localStorage`). |

## How data flows

```
docs/product/products.json ─┐
assets/characters/*.json ───┼─> site/src/data/catalog.ts ─> pages at build time ─> static HTML
site/src/data/{shop,reviews}.json ─┘

assets/{logo,packaging,characters,renders} ─(sync-assets)─> site/public/brand/ ─> <img src="/brand/...">
```

Change a product in `products.json`, re-run `python3 scripts/build_packaging.py`
(packs, characters, brand book), then rebuild the site. The website never has
its own copy of a product name, size, age or ingredient list.

## In the browser

Small scripts only, no framework:

- **Cart** — `localStorage` key `nanhe-cart`: `[{slug, qty, subscribe}]`.
- **Baby profile** — `localStorage` key `nanhe-baby`: `{ageBand, skin}` (written by the profile page in slice 2; read by product pages now).
- **Shop filters** — routine, baby's age and sort, all client-side over pre-rendered cards.
- **"Babies like yours"** — a sample figure derived from the sample rating and fixed share tables, so it is stable but not real.

Nothing a visitor types leaves their browser. There is no analytics or tracking.

## Prototype safeguards

- A banner on every page says prices, ratings and reviews are samples.
- `robots.txt` disallows everything and every page has `noindex, nofollow`.
- Claims keep their footnotes and `[lab data pending]` placeholders, as on the packs.
- Renders are captioned "AI concept photo".

## Run it

```
cd site
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in site/dist/
```

## Deploy

Vercel, Root Directory `site`, framework Astro, build command `npm run build`.
The build reads `../docs` and `../assets`, so "Include files outside the root
directory" must stay on (Vercel's default).

## Slices

1. Home, Shop, 19 product pages, placeholders for everything else. (this PR)
2. Cart, checkout (demo), baby profile, write a review, compare.
3. Parent guides, kits & gifts, Ask, search.
