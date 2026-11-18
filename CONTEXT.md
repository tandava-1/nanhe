# Nanhe — context

## Current state

**What it is.** Brand identity, packaging, brand book and a clickable website
prototype for Nanhe (नन्हे, "little ones"): a premium, India-first baby
skincare, toiletries and diapering line. Natural ingredients, clinically
tested. Price band around Mamaearth / The Moms Co., or slightly above.

**Folder map.** See the table in `AGENTS.md`.

**Done.**
- Name, brand foundations, logo (`assets/logo/`), colour, type, claims and
  voice. Brand book in `brand-book/index.html`, now edition 5 (published at
  https://claude.ai/artifact/SUywwYqP1KskvkSx4AqhVo).
- Product line: 19 products in five categories, defined once in
  `docs/product/products.json`. `scripts/build_packaging.py` renders the packs
  (`assets/packaging/`), the line-up, `docs/product/product-line.md`, the brand
  book's packaging block and, since 2026-11-18, one SVG per little friend in
  `assets/characters/` plus `characters.json`.
- Categories: Moisturise (apricot), Care & Protect (sage), Everyday Hygiene
  (sky), Bath & Toiletries (butter), Diapering (lavender). All wipes are in
  Diapering. Ages are full ranges (mostly 0–36 months).
- Little friends: 17 Indian baby animals, one per product (Magru is on both
  first-teeth products; Susu on both water-wipes packs). Concept art; an
  illustrator redraws before print.
- Photography: 10 AI concept renders in `assets/renders/` (Figma file
  https://www.figma.com/design/tLnDO6jOWOoKlgg7wpCIbg), real labels
  composited on the product shots by `scripts/composite_renders.py`.
- Website prototype, slice 1 (branch `website-2026-11-18`): Astro static site
  in `site/` with Home, Shop (five shelves, one-line filters for routine and
  baby's age, sort) and all 19 product pages (gallery, sample reviews with
  "babies like yours" filters, claims with `[lab data pending]`, subscribe
  option, pincode check, cart kept in the browser). Other links go to
  placeholder pages that say which slice builds them. Architecture in
  `docs/engineering/website.md`. Wireframes and branded mock-ups that led here
  are on the canvas https://claude.ai/artifact/EUdWmFgK1wvQR6mj2GSBPV.

**Open PRs (stacked).** PR 1 brand foundations → PR 2 range extension
(`product-line-extension-2026-11-17`) → website slice 1 (`website-2026-11-18`,
based on PR 2's branch). Merge in that order.

**In progress / next.**
1. Deploy slice 1 to Vercel (needs the founder's Vercel login or the repo
   imported in the Vercel dashboard with Root Directory `site`).
2. Website slice 2: cart, checkout (demo, no payments), baby profile, write a
   review, compare.
3. Website slice 3: parent guides, kits & gifts, Ask (assistant demo +
   experts), search.

**Open questions.**
- Trademark search (Class 3) and domain for "Nanhe".
- Real clinical test data to replace claim placeholders.
- Real prices (the website shows sample prices).
- A diaper size for 5–7 kg (gap between Newborn and Medium).
- Customer care hours: the pack says Mon–Sat 10am–6pm; the website's Ask page
  promises experts anytime.
- Returns policy for opened products.

## Log

### 2026-11-17 18:23 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Created the project skeleton: AGENTS.md, CLAUDE.md, README.md,
CONTEXT.md, `docs/product`, `docs/design`, `assets/{logo,packaging,renders}`,
`brand-book/`. Private repo `tandava-1/nanhe`.
**Decided:** Name is Nanhe. Positioning premium, India-first. Range is
Moisturise, Care & Protect and Everyday Hygiene (no Bath). Deliverable is a
brand book plus AI photo renders. Layout adapts the standard one: no
`docs/engineering/` (design project, not software) and `assets/` +
`brand-book/` in place of `src/`. Claims like "clinically tested" carry
placeholders until real lab data exists.
**Next:** Build brand foundations on a dated branch and show for feedback.

### 2026-11-17 18:40 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Added `assets/logo/nanhe-wordmark.svg`, `assets/logo/nanhe-mark.svg`,
`brand-book/index.html` (edition 1: cover, story, logo, colour, type, label
anatomy, claims and icons, voice) and `docs/design/brand-foundations.md`.
Published the brand book as a private artifact.
**Decided:** Monoline rounded wordmark with a leaf sprouting from the h. Mark
is a seedling n with the leaf on the arch crown (the first try, with the leaf
on the stem, read as "h"). Tagline "Made gentle. Tested gentle." Brand book is
light-theme only because it shows print colours. Claim figures (97%, study
details) are placeholders. Devanagari lockup is live type for now and needs
outlining before print.
**Next:** Founder feedback on foundations, then packaging line-up (9 SVG
renders + front/back labels) on this same branch if the PR is still open.

### 2026-11-17 19:10 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Added `docs/product/products.json`, `scripts/build_packaging.py`,
`assets/packaging/` (9 pack SVGs + `lineup.svg`), `docs/product/product-line.md`,
and the generated packaging block in `brand-book/index.html` (line-up, product
pages, flat front label, full back label for Daily Lotion). Republished the
brand book as edition 2.
**Decided:** Packs are generated from one JSON file so names, sizes and claims
stay consistent across renders, brand book and docs. Pack formats: 200 ml
pump (lotion), clear 100 ml bottle showing the oil, 100 g jar, 50 g
stand-on-cap tubes (rash cream, sunscreen), 25 g tin (balm), sifter shaker
(powder), 300 ml foam pump (bottle wash), 72-wipe soft pack with rigid lid.
Footnotes: `*` = clinical testing, `**` = % naturally derived (ISO 16128).
Sunscreen is labelled 6+ months, and massage oil carries a nut-allergy warning.
Formulas (INCI) are indicative only. Back label covers Legal Metrology and
Cosmetics Rules 2020 fields as placeholders. Only Daily Lotion has a full
back label; the others follow the same template.
**Next:** Founder review of packaging, then AI photo renders (step 3).

### 2026-11-17 20:05 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Founder asked for more "baby-like" visuals and wanted to compare
animal characters against nursery motifs. Added style switches to
`scripts/build_packaging.py` (`STYLE["chars"]`, `STYLE["motif"]`, both off by
default so the approved edition-2 output is unchanged), nine character
drawings, three category pattern tiles, rainbow-arch line-up decorations, and
a generated comparison page `docs/design/explorations/baby-directions.html`
(published at https://claude.ai/artifact/LE7WAksDssKTU9pTRA5YNe).
**Decided:** Scope is packs and page graphics only; logo, colour and type
stay. Characters: Haathi (elephant calf, Daily Lotion), Gilu (palm squirrel,
Massage Oil), Bhalu (bear cub, Rich Cream), Kachhu (tortoise, Diaper Rash
Cream), Kaantu (hedgehog, Balm), Moru (peacock chick, Sunscreen), Khargu
(hare, Powder), Batku (duckling, Bottle Wash), Susu (Ganges river dolphin,
Wipes). Recommended direction A; B is pleasant but generic in the category.
Character drawings are concept art and need an illustrator before print.
**Next:** Founder picks A, B or a middle path; then flip the switch for the
brand book and standalone pack files, then AI photo renders.

### 2026-11-17 20:20 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Made direction A the default (`STYLE["chars"] = True`), regenerated
pack SVGs, line-up and brand book. Added a "Little friends" section to the
brand book (character sheet and drawing rules) and recorded the characters in
`docs/design/brand-foundations.md`. Brand book is now edition 3.
**Decided:** Founder chose A, Little friends. Direction B (nursery motifs)
stays available in the script but is unused.
**Next:** AI photo renders (step 3), then final brand book assembly and
mockups.

### 2026-11-17 20:55 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Generated 8 AI renders in a new Figma file "Nanhe — Photo
Renders" (founder approved the Figma AI credit spend), saved as JPEG in
`assets/renders/`. Added `scripts/composite_renders.py`, which overlays the
real labels on the lotion, rash cream and wipes shots. Added a photography
section to the brand book (edition 4), `docs/design/render-prompts.md`, and a
`brand-book/renders` symlink. Wipes label now keeps the water-drop drawing
because Susu is on the lid.
**Decided:** Packs were generated with blank labels and the real labels
composited on top, because AI garbles text. No baby faces in any photography,
only hands, backs and feet. All photos are labelled as AI concepts, and a
real shoot is needed before launch.
**Next:** Founder review of edition 4. Open items: illustrator to redraw the
characters, outline the Devanagari lockup, real lab data for the claims,
trademark check for "Nanhe", real photo shoot, and merging PR 1.

### 2026-11-17 22:25 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Extended the line to toiletries, diapers and wipes on a new
branch `product-line-extension-2026-11-17`. Ten new products in
`docs/product/products.json`, two new categories, eight new characters, seven
new pack shapes (flip-cap, tall bottle, small tube, carton, pouch, diaper bag,
value bundle), flat diaper prints, a two-row line-up, the brand book's colour
section and cover updated, and a new diaper-prints section. Generated two
Figma renders (founder approved the credits) and composited the real bag
artwork onto the diaper shot.
**Decided:** One SKU each for taped diapers (NB) and pants (M), as the
founder asked, with a different animal per diaper size. Toothpaste uses
1000 ppm fluoride with a rice-grain dose, per current paediatric dental
guidance (founder agreed). All wipes sit under Diapering. Very wide line-up
groups get a rounded-top panel instead of a semicircle.
**Next:** Founder review of edition 5. Merge PR 1, then this PR. Same open
items as before, plus diaper and toothpaste formulation partners.

### 2026-11-17 22:40 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Replaced Gendu (rhino calf) on the Newborn taped diapers with
Chitku, a chital fawn, in `scripts/build_packaging.py`. Regenerated the packs,
the diaper print, the line-up, the brand book and the composited diaper
photo. Removed the unused rhino drawing.
**Decided:** Founder asked to change the newborn animal and chose the chital
fawn. Its white spots carry into the all-over diaper print.
**Next:** Founder review; merge PR 1, then PR 2.

### 2026-11-18 00:10 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Replaced open-ended ages ("0+ months") with full ranges on every
pack, product page, label sample and composited photo: most products 0–36
months, sunscreen and hand & face wipes 6–36, bubble bath 12–36, finger
toothbrush 4–24, toothpaste first tooth to 3 years. Diapers keep their weight
ranges; bottle wash has no age because it's for feeding gear. Shortened the
toothpaste footer to "1000 PPM FLUORIDE" so it doesn't collide with the
quantity.
**Decided:** Founder wanted ranges instead of "+". Chose ranges per product
with an upper limit, not stage bands or narrow per-stage products, because
narrow ranges would wrongly tell parents to stop using a product early.
**Next:** Founder review; merge PR 1, then PR 2.

### 2026-11-18 05:45 IST — Claude Code (Opus 5.5) · Shivank’s MacBook Air
**Changed:** Started the website. Wireframes (low-fi, then Nanhe-branded
mobile and desktop) were iterated with the founder on the canvas
https://claude.ai/artifact/EUdWmFgK1wvQR6mj2GSBPV. Built slice 1 on branch
`website-2026-11-18`: Astro static site in `site/` (Home, Shop, 19 product
pages, placeholder pages), `docs/engineering/website.md`, `AGENTS.md` and
`README.md` updated for the website. `scripts/build_packaging.py` now also
writes `assets/characters/` (17 SVGs + `characters.json`).
**Decided:** Founder chose a clickable prototype (no real payments), hosted
on Vercel, with Home, Shop and product pages fully branded and the other
screens built in later slices. The site lives in this repo so products and
artwork have one source: it reads `products.json` and `assets/` at build time.
Astro over a Python generator (about 12 page types share header, footer and
cards) and over Next.js (no server needs yet). Prices, ratings and reviews are
labelled samples; the site carries a prototype banner, `noindex` and a
`robots.txt` that blocks crawlers. Review signals are the founder's priority:
every product page has "babies like yours" filters by age and skin type, and
critical reviews are one tap away. Shop filters stay on one line (founder
feedback from the wireframes). Branched from PR 2's branch because the site
needs the 19-product data; expect the routine CONTEXT.md conflict on merge.
**Next:** Founder logs in to Vercel (or imports the repo with Root Directory
`site`) so slice 1 can deploy; founder sends edits; then slice 2.
