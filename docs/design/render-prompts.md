# AI render prompts

All images in `assets/renders/` are AI-generated concepts. They were made on
2026-11-17 with Figma's image generator (model `gpt-image-2.5-flare`) in the
Figma file "Nanhe — Photo Renders"
(https://www.figma.com/design/tLnDO6jOWOoKlgg7wpCIbg). The originals came out
as PNG and are stored here as JPEG at quality 90.

## Rules used for every prompt

- Packs are described by shape and colour only, with **blank labels and no
  text**. Image models scramble lettering.
- No baby faces. Show hands, backs and feet only.
- Soft daylight, milk-white surfaces, and the three category pastels.

## Images

| File | Figma node | Prompt summary |
|---|---|---|
| `ai-01-hero-range.jpg` | 1:2 | The nine packs in three groups in front of apricot, sage and sky arches, with oat sprigs and calendula, morning light |
| `ai-02-maalish.jpg` | 2:2 | Adult hands with a gold bangle massaging a baby's back on a cream towel, oil bottle and brass bowl beside, face not visible |
| `ai-03-changing-kit.jpg` | 2:3 | Top-down flat lay on sage linen: tube, tin, wipes pack, muslin cloth, baby sock, calendula petals |
| `ai-04-bath-shelf.jpg` | 2:4 | Lotion pump and powder shaker on a bathroom shelf, hooded towel, rubber duck, baby's foot over the tub |
| `ai-05-ingredients.jpg` | 2:5 | Halved coconut, oats, calendula, neem, almonds, shea butter and ghee on a milk-white surface |
| `ai-06-lotion-plain.jpg` | 2:6 | One pump bottle, straight-on and centred, blank front, apricot backdrop, oats at its base |
| `ai-07-rash-cream-plain.jpg` | 2:7 | One tube standing on its sage cap, straight-on, blank front, sage backdrop, calendula at its base |
| `ai-08-wipes-plain.jpg` | 2:8 | Wipes pack from directly above, blank, sky blue lid, sky backdrop, water droplets |

## Composites

`ai-06/07/08-*-labelled.jpg` are made by `scripts/composite_renders.py`. It lays
the real vector label and character from `scripts/build_packaging.py` onto the
plain shots, using a multiply blend so the photo's lighting shows through. The
placement of each label, in image pixels, is recorded in that script. If a base
photo is regenerated, re-measure the placement.

## Before launch

These are concepts. Commission a real shoot with production packs, following
the photography rules in the brand book.

## Added 2026-11-17 (range extension)

| File | Figma node | Prompt summary |
|---|---|---|
| `ai-09-diapers-plain.jpg` | 3:2 | Two blank pillow-shaped diaper bags with handle cut-outs, straight-on, lavender backdrop, muslin and a knitted bootie |
| `ai-10-bath-shampoo.jpg` | 3:3 | An adult pours water from a brass lota over a baby's foamy hair, seen from behind, with blank butter-cap shampoo and wash bottles on the tub edge |

`ai-09-diapers-labelled.jpg` has the real bag artwork (Chitku NB, Pandu M) composited
by `scripts/composite_renders.py`.
