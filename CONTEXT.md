# Nanhe — context

## Current state

**What it is.** Brand identity, packaging and brand book for Nanhe (नन्हे,
"little ones"): a premium, India-first baby skincare and toiletries line.
Natural ingredients, clinically tested. Price band around Mamaearth / The Moms
Co., or slightly above.

**Folder map.** See the table in `AGENTS.md`.

**Done.**
- Name chosen: Nanhe (over Kopal, Mridu, Sprig).
- Project skeleton created and pushed.
- Brand foundations (PR on `brand-foundations-2026-11-17`): wordmark and mark
  SVGs in `assets/logo/`, brand book edition 1 in `brand-book/index.html`
  (published privately at https://claude.ai/artifact/SUywwYqP1KskvkSx4AqhVo),
  decisions in `docs/design/brand-foundations.md`. Approved by founder.
- Packaging (same branch / PR 1): `docs/product/products.json` is the single
  source for the line; `scripts/build_packaging.py` renders
  `assets/packaging/*.svg` (9 packs + `lineup.svg`),
  `docs/product/product-line.md`, and the generated block between
  `<!-- BEGIN:packaging -->` / `<!-- END:packaging -->` in the brand book
  (line-up, product pages, front + back label). Brand book is now edition 2.
  To change a product, edit the JSON and re-run the script; never hand-edit
  the generated block.
- Little friends (direction A) is the approved look: nine baby animal
  characters on labels, wipes lid and line-up arches. `STYLE` in the script
  defaults to it. Brand book is edition 3. Exploration page kept at
  `docs/design/explorations/baby-directions.html`.
- Photography: 8 AI concept renders in `assets/renders/` (Figma file
  https://www.figma.com/design/tLnDO6jOWOoKlgg7wpCIbg). Three product shots
  have the real label composited by `scripts/composite_renders.py`. Prompts
  in `docs/design/render-prompts.md`. Brand book is edition 4 with a
  photography section; `brand-book/renders` is a symlink to
  `../assets/renders` so the page works locally and when published.
- Range extension (branch `product-line-extension-2026-11-17`, stacked on PR 1):
  19 products in five categories. New: Bath & Toiletries (butter #F5DA8C) —
  head-to-toe wash, shampoo, bubble bath, first toothpaste (1000 ppm
  fluoride), finger toothbrush, grooming kit; Diapering (lavender #CFC3E8) —
  taped diapers NB, diaper pants M, hand & face wipes, Water Wipes (moved from
  Hygiene), value 3-pack. Eight new characters (Udu, Sheru, Mendu, Magru,
  Mainu, Gendu, Pandu, Nevu). New pack shapes, diaper prints, a two-row
  line-up, and two more AI renders (diapers composited, bath lifestyle).
  Brand book is edition 5.

**Agreed direction.**
- Look: modern botanical. Soft matte packs tinted by hero ingredient; rounded
  lowercase wordmark with a leaf-shaped letterform; Devanagari secondary
  lockup; fine-line ingredient illustrations; verification-seal style
  "clinically tested" badge.
- Colour: cream base, deep moss ink; category colours — apricot (Moisturise),
  sage (Care & Protect), sky (Everyday Hygiene).
- Type: soft serif for headlines, clean sans for labels (Google Fonts).

**Product line (9).**
- Moisturise: Daily Lotion (oat + shea, 200 ml pump); Massage Oil (coconut,
  almond, ashwagandha, 100 ml); Rich Cream (ceramides + oat, 100 g jar).
- Care & Protect: Diaper Rash Cream (zinc + calendula, 50 g tube); All-Purpose
  Balm (ghee + beeswax, 25 g tin); Mineral Sunscreen SPF 50, 6 months+ (50 g
  tube).
- Everyday Hygiene: Water Wipes (99% water, 72s); Talc-Free Powder (corn starch
  + neem, 100 g); Bottle & Accessory Wash (soapnut, 300 ml foam pump).
- Bath category deliberately left out of the first line.

**In scope.** Logo system, colour, type, icons, 9 packaging renders with
front/back labels, AI photo renders, brand book page, e-com and shelf mockups.

**Out of scope.** Print-ready dielines, formulations, regulatory sign-off,
trademark clearance.

**Next steps (build in slices, pause after each).**
1. Brand foundations: logo system, colour, type, claim icons.
2. Packaging line-up: 9 SVG renders + label layouts.
3. AI photo renders (plain-label packs; real vector logo composited or used as
   mood/lifestyle only).
4. Brand book page + mockups; publish.

**Open questions.**
- Trademark search (Class 3) and domain availability for "Nanhe".
- Real clinical test data to replace claim placeholders.

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
