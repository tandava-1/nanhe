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
| `site/src/data/guides.ts` | **Sample** parent-guide copy (6 guides, quick answers, doctor list), pending the paediatrician's review. Website only. |
| `site/src/pages/` | `index` (Home), `shop/`, `search`, `products/[slug]` (19), `cart`, `checkout` (demo), `profile`, `write-review`, `compare`, `guides/` + `guides/[slug]` (6), `kits`, `ask`, and `[page]` (placeholders: track, returns, how-we-test, ingredients, review-policy). |
| `site/src/scripts/` | `data.ts` (reads CatalogData, shared helpers), `cart.ts` (cart, totals, coupon, gift), `baby.ts` (baby profile). |
| `site/src/components/` | Header, Footer, Wordmark, ProductCard, AskBand, Icon, CatalogData (puts a small product/kit catalogue in the page as JSON for the browser scripts). |

**Product cards.** Every product card on the site is `ProductCard` inside a
`.pgrid` (in `global.css`), so cards are the same size everywhere: two equal
columns on phones, a fixed 254 px column from 720 px up. Inside the card the
image is a fixed square and each text line has a fixed number of lines.
Product-specific safety notes show as a badge on the image (short text in
`WARN_SHORT` in `catalog.ts`); the full caution is on the product page. Keep
new listings on `.pgrid` + `ProductCard` rather than building another card.

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

Everything a visitor does is kept in their own browser (`localStorage`):

| Key | Holds | Written by |
|---|---|---|
| `nanhe-cart` | `[{id, kind: product\|kit\|box, slug, qty, subscribe, every, items}]` | product pages, Shop, kits, compare, cart |
| `nanhe-coupon` | the applied coupon code (`NANHE10`) | cart; cleared on order |
| `nanhe-gift` | `{on, note, hidePrices}` | cart; cleared on order |
| `nanhe-profile` | `{babies: [{name, born, month, skin, concerns, climate}], active}` | profile page |
| `nanhe-baby` | `{ageBand, skin}` for the active baby, read for "babies like yours" | profile page |
| `nanhe-my-reviews` | reviews the visitor wrote, shown back on that product page | write-review |

Prices and rules (free delivery over ₹499, ₹49 delivery, ₹30 COD fee, 10% off
subscriptions, kit and build-your-own-box discounts, the sample coupon) live in
`RULES` and `KITS` in `catalog.ts`; the browser scripts read them from
CatalogData, so the cart, checkout and kits page always agree.

- **Checkout** is a demo: the OTP is shown on screen, the pincode fills in a
  sample city, COD is off for subscriptions, and placing the order only clears
  the cart. Nothing is sent.
- **Ask** is scripted keyword matching, labelled "prototype". Safety words
  (breathing, fever with rash, swallowed, burns, falls and similar) always get
  "call your doctor or 112" first. Expert chat, phone and paediatrician
  booking are demos with `[to be decided]` hours, numbers and prices.
- **Shop filters**, **guide filters** and **"babies like yours"** run in the
  browser over pre-rendered content; "babies like yours" is a stable sample
  figure, not real data.

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

Live at **https://nanhe-xi.vercel.app** (Vercel project `nanhe`).

Today it deploys from this Mac, building locally because the build reads
`../docs` and `../assets` from outside `site/`:

```
cd site
vercel build --prod --yes
vercel deploy --prebuilt --prod --yes
```

Node is pinned to 24.x in `site/package.json` (`engines`), because Vercel
doesn't accept the Mac's Node 26 yet. `site/.vercel/` and `site/.env*` are
git-ignored; `vercel link` writes a token into `.env.local`.

To deploy on every push instead, connect the GitHub repo in the Vercel
dashboard (Project → Settings → Git) and set Root Directory to `site`, keeping
"Include files outside the root directory" on. Every PR then gets its own
preview link.

## Slices

1. Home, Shop, 19 product pages, search, placeholders for everything else. Built.
2. Cart, checkout (demo), baby profile, write a review, compare. Built.
3. Parent guides (hub + 6 articles), kits & gifts with build-your-own box, Ask
   (assistant demo + experts). Built.

Still placeholders: order tracking, returns, how we test, ingredients
glossary, review policy.
