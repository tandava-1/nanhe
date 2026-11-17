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
