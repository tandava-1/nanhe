# Nanhe — project rules

Read `CONTEXT.md` first, every time. It holds the current state and the log of
decisions; continue from it rather than re-deciding things.

## What this project is

Brand identity, packaging and brand book for **Nanhe** (नन्हे, "little ones"),
a premium, India-first baby skincare and toiletries line. Natural ingredients,
clinically tested. The work is design, not software.

## Folder map

| Path | Holds |
|---|---|
| `docs/product/` | Product line, ingredients, claims and regulatory notes |
| `docs/design/` | Brand guidelines, design decisions, AI render prompts |
| `assets/logo/` | Wordmark, Devanagari lockup, icon — SVG is the source of truth |
| `assets/packaging/` | One SVG render plus front/back label per product |
| `assets/renders/` | AI photo renders |
| `brand-book/` | The shareable brand book page (`index.html`) |

## Rules

- **Branching.** Never commit to `main`. Work on a dated `<topic>-YYYY-MM-DD`
  branch, push it, open a PR. One reviewable slice per PR.
- **Vector first.** Logos, packaging and labels are hand-built SVG. Raster
  exports are derived from them, never edited separately.
- **Claims stay honest.** "Clinically tested", "dermatologist tested",
  "% naturally derived" and similar claims carry a footnote placeholder
  (`[lab data pending]`) until real test reports exist. Never invent study
  numbers, certifications or seals (no fake "ECOCERT", "FDA", etc.).
- **Regulatory placeholders.** Back labels keep India's mandatory fields as
  visible placeholders: MRP, net quantity, batch no., mfg/expiry date,
  manufacturing licence no., manufacturer name and address, customer care.
- **AI renders are labelled.** Anything in `assets/renders/` is AI-generated
  and named or captioned as such. Record the prompt in
  `docs/design/render-prompts.md`.
- **No personal data or secrets** in the repo.
- **Commit trailers.** Every commit ends with:

  ```
  Agent: <tool> (<model>) · <machine>
  Agent-Time: YYYY-MM-DD HH:MM <TZ>
  ```
