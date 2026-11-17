# Brand foundations

The brand book page (`brand-book/index.html`) is the visual reference. This file
records the decisions behind it so later work stays consistent.

## Logo

- **Wordmark** (`assets/logo/nanhe-wordmark.svg`): lowercase "nanhe" drawn as a
  single rounded monoline. Stroke 14 on a 60-unit x-height, round caps. Round
  letters (a, e) sit 2 units tighter than straight-to-straight pairs for even
  optical spacing.
- **Signature leaf**: a new leaf sprouts from the top of the h. It is always New
  Leaf green (#5E8E4E), or pale sage (#BFD6B0) when reversed on moss. Never
  recoloured per category.
- **Mark** (`assets/logo/nanhe-mark.svg`): a seedling n, with a leaf growing
  from the crown of the arch. Used for app icon, avatars, caps, the clinical
  seal and the wipes lid. An earlier version put the leaf on top of the left
  stem; it read as an "h", so the leaf moved to the arch.
- **Bilingual lockup**: wordmark above नन्हे set in Baloo 2 SemiBold.
- **Clear space**: the height of the n on all sides.
- **Minimum size**: wordmark 18 mm / 64 px wide; mark 5 mm / 20 px.
- **Open item**: the Devanagari lockup uses live type. Before print, outline it
  in a design tool so it doesn't depend on the font being installed.

## Colour

| Token | Hex | Use |
|---|---|---|
| Milk | #FBF7F0 | Pack body, page ground (~70%) |
| Moss | #1F3A2B | All type, logo (~10%) |
| New leaf | #5E8E4E | Logo leaf only |
| Marigold | #EFA43A | Clinical seal only |
| Apricot / wash / deep | #F6BE9A / #FCE9DC / #B4592C | Moisturise |
| Neem sage / wash / deep | #BFD6B0 / #E7F0E0 / #43703C | Care & Protect |
| Monsoon sky / wash / deep | #BFDCEC / #E4F0F7 / #2F6689 | Everyday Hygiene |

Packs are matte milk-white. The category colour goes on the cap and the label
band (~18% of a layout). The deep shades are only for small category text.
Print colour matching (Pantone or CMYK proofs) is out of scope for now.

## Type

- **Display**: Fraunces, `SOFT` axis 100. Weight 500 for product names, 400 italic
  for the tagline.
- **Text**: Figtree. 400 body, 600 emphasis, 700 small caps (+16% tracking).
- **Devanagari**: Baloo 2 SemiBold. Hindi sits beside English at about 55% of its size.

## Claims

- Front-of-pack claims always carry an asterisk, and the back explains each one.
- Seal: "Clinically tested · on infant skin*" ring in Marigold, with the mark
  at the centre and the age range below it.
- Icon set (24 px grid, 1.6 stroke): dermatologically tested, % naturally
  derived (ISO 16128), pH 5.5, no added fragrance, hypoallergenic (HRIPT),
  recyclable pack.
- "Made without" list: parabens, SLS/SLES, mineral oil, synthetic fragrance,
  talc, phthalates, artificial dyes.
- Never say: "chemical-free", "100% safe", "doctor recommended" without a named
  study, or any seal or certification Nanhe doesn't hold.
- All figures (97% naturally derived, sample sizes) are placeholders until lab
  reports are in.

## Voice

Like a calm paediatric nurse: warm, plain and specific. Talk to parents as
capable adults who are short on sleep. Address all caregivers ("parents,
grandparents and anyone on night duty"), not only mothers.

## Tagline

"Made gentle. Tested gentle." This puts the two brand promises, natural
formulation and clinical testing, side by side.

## Little friends (direction A, chosen 2026-11-17)

Each product has a baby Indian animal, and each animal has a reason for being
on that product. The full comparison with the nursery-motif direction is in
`docs/design/explorations/baby-directions.html`.

| Product | Character | Animal | Why |
|---|---|---|---|
| Daily Lotion | Haathi | Elephant calf | Gentle giant with famously soft skin |
| Massage Oil | Gilu | Palm squirrel | Lives in the coconut trees the oil comes from |
| Rich Cream | Bhalu | Himalayan bear cub | Cold, dry winter cheeks |
| Diaper Rash Cream | Kachhu | Tortoise | Its shell is a barrier, like the cream |
| All-Purpose Balm | Kaantu | Indian hedgehog | Small, tough, handy |
| Mineral Sunscreen | Moru | Peacock chick | Loves the sun |
| Talc-Free Powder | Khargu | Hare | Powder-puff tail |
| Bottle Wash | Batku | Duckling | Water and bubbles |
| Water Wipes | Susu | Ganges river dolphin | Local name along the Ganga; pure water |

- **Drawing rules:** head and shoulders, facing forward (Susu swims side-on).
  Moss outline at a constant weight, filled with the category colour and wash.
  Dot eyes with a white glint, blush on the cheeks.
- **Where they appear:** front labels (in place of the ingredient drawing),
  the wipes lid, the tops of the line-up arches, gift boxes, social media and
  the website.
- **What they never do:** speak, hold products, sit inside the clinical seal,
  replace the wordmark, or appear in claims or safety text.
- **Status:** concept art drawn in `scripts/build_packaging.py`. An
  illustrator redraws the set before print.
