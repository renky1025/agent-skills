---
name: design-md-extractor
description: >
  Extract a visual design system from any website URL and generate a DESIGN.md
  that strictly follows the google-labs-code/design.md specification format.
  Use this skill for: "create a DESIGN.md for [url]", "extract design system from [url]",
  "generate design tokens for [url]", "analyze [brand]'s visual style",
  "make a DESIGN.md for [website]", "帮我分析 [url] 的设计系统", "为 [网站] 生成 DESIGN.md".
  Covers: DESIGN.md with YAML front matter (colors, typography, rounded, spacing, components)
  and markdown sections (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes,
  Components, Do's and Don'ts). Output must pass `npx @google/design.md lint`.
---

# Design MD Extractor

Extract a visual design system from any website URL and generate a DESIGN.md conforming to the [google-labs-code/design.md](https://github.com/google-labs-code/design.md) specification.

## Do's

- **Follow the spec exactly.** The output must have valid YAML front matter (color hex values, typography objects with complete properties) and correct section order. Every generated file should pass `npx @google/design.md lint`.
- **Include fontFeature and fontVariation** when observed in the source site's `@font-face` or computed styles. These are part of the Typography token spec.
- **Use token references in components.** Component properties like `backgroundColor` must use `{colors.primary}` syntax, not hardcoded hex values, per the spec.
- **Document every observed component state.** Hover, focus, active, selected, pressed — each state maps to a separate component entry (e.g., `button-primary`, `button-primary-hover`).
- **Capture full CSS for shadows.** Write `0 4px 6px rgba(0,0,0,0.1)` not "subtle shadow". Downstream consumers need parseable box-shadow values.
- **Verify colors against screenshots.** CSS inspection can miss overlay effects and gradient blends. Cross-check with visual evidence.
- **Provide open-source font substitutes.** Proprietary fonts need documented alternatives (Inter, DM Sans, etc.).
- **Write brand voice as design critique.** The Overview section should read like a designer describing visual personality, not a feature list.
- **Name tokens by role** (primary, secondary, surface, ink) not by appearance — unless the descriptive name is the brand's own convention.

## Don'ts

- **Don't invent placeholder values.** If a token category is missing, skip it. Fabricated values break the design system.
- **Don't mix tokens from multiple themes.** If a site has light and dark modes, ask the user which to document. Never blend both into one DESIGN.md.
- **Don't use generic Do's/Don'ts.** Every rule must reference a specific token or property. "Use good contrast" is useless; "Reserve `{colors.tertiary}` for primary actions only" is actionable.
- **Don't omit lineHeight or letterSpacing.** Typography tokens without these are incomplete per the spec.
- **Don't flatten layered shadows.** Multiple box-shadow layers must be preserved as-is with commas.
- **Don't skip the Overview.** It's the design rationale that guides future decisions. Without it, the document is just a token dump.
- **Don't use duplicate section headings.** The spec errors on duplicate `##` headings (e.g., two `## Colors` sections).
- **Don't use unknown YAML keys at the top level.** Only `version`, `name`, `description`, `colors`, `typography`, `rounded`, `spacing`, and `components` are valid in front matter.

## Trigger Behavior

| Input | Output |
|-------|--------|
| `DESIGN.md for [url]` | `DESIGN.md` — full design system document |
| `extract design tokens from [url]` | `DESIGN.md` with tokens only + summary |
| `analyze [url]'s visual style` | `DESIGN.md` + inline analysis |

Natural language triggers: "create a DESIGN.md for linear.app", "extract the design system from stripe.com", "analyze github's visual identity", "帮我分析 https://example.com 的设计", "为 [url] 生成 DESIGN.md"

## Output

```
DESIGN.md   — Design system document conforming to google-labs-code/design.md spec
```

Generated in the current working directory, named after the brand: `themes/{brand-slug}/DESIGN.md`

## Reference

Read the spec before generating: [google-labs-code/design.md spec](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md)

Also available to validate: `npx @google/design.md lint DESIGN.md`

## Workflow

### Step 1 — Gather Visual Data

Access the URL. Screenshot hero, nav, CTAs, cards, typography sections, footer. Inspect DevTools for CSS variables, `@font-face`, computed styles, `box-shadow`, `border-radius`, `spacing`.

**Why:** Screenshots capture decorative elements (gradients, glows, illustrations) that CSS inspection alone misses.

### Step 2 — Extract Design Tokens

Map observed values into the YAML front matter schema:

```yaml
version: alpha
name: {Brand Name}
description: {One-line brand identity description}
colors:
  primary: "{hex}"
  secondary: "{hex}"
  tertiary: "{hex}"
  neutral: "{hex}"
  surface: "{hex}"
  error: "{hex}"
typography:
  h1:
    fontFamily: "{name}"
    fontSize: {n}px
    fontWeight: {n}
    lineHeight: {n}
    letterSpacing: "{n}px"
  body-md:
    fontFamily: "{name}"
    fontSize: {n}px
    fontWeight: {n}
    lineHeight: {n}
  label-caps:
    fontFamily: "{name}"
    fontSize: {n}px
    fontWeight: {n}
    lineHeight: {n}
    letterSpacing: "{n}px"
rounded:
  sm: {n}px
  md: {n}px
  lg: {n}px
  full: 9999px
spacing:
  xs: {n}px
  sm: {n}px
  md: {n}px
  lg: {n}px
  xl: {n}px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{hex}"
    rounded: "{rounded.sm}"
    padding: {n}px
```

**Colors** — Identify 4-8 core colors. At minimum: primary, secondary, tertiary, neutral, surface. Use the [Recommended Token Names](#recommended-token-names-non-normative) from the spec.

**Typography** — Extract every distinct type style. Map to semantic names: h1, h2, h3, body-lg, body-md, body-sm, label-lg, label-md, label-sm, caption. Record: fontFamily, fontSize, fontWeight, lineHeight, letterSpacing.

Check `font-feature-settings` for OpenType features: cv01-99, ss01-20, tnum, dlig, etc.

**Spacing** — Detect base unit: multiples of 4 → base=4px. Multiples of 5 → base=5px. Map to semantic scale: xs, sm, md, lg, xl.

**Radius** — Detect all distinct radius values. Map to: sm, md, lg, full.

**Shadows** — Full CSS syntax only. Capture as part of component tokens.

### Step 3 — Document Components

For each distinct component, document:

```yaml
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.tertiary-container}"
```

Common components: buttons (primary/secondary/ghost), inputs (default/focused/error), cards, navigation, links, tooltips, chips.

Valid component properties per spec: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`.

### Step 4 — Write Section Prose

Write each `##` section in spec order:

1. **Overview** — 3-8 sentence design critique: dominant surface → typeface personality → accent color behavior → depth approach → signature element.
2. **Colors** — Describe each palette's role. Reference the YAML token names.
3. **Typography** — Describe font personalities, pairings, and size roles.
4. **Layout** — Grid system, max-width, spacing philosophy, responsive behavior.
5. **Elevation & Depth** — Shadow system, surface levels, or alternative hierarchy methods.
6. **Shapes** — Border radius philosophy, corner treatment per element type.
7. **Components** — Describe each component's role and styling rules.
8. **Do's and Don'ts** — 5-8 each, every rule referencing a specific token.

### Step 5 — Validate

Run `npx @google/design.md lint DESIGN.md` to check structural correctness.

Fix any errors (broken refs, duplicate sections, invalid tokens) before finishing.

## Format Rules

### YAML Front Matter Structure

```yaml
---
version: alpha
name: Brand Name
description: Optional one-line description
colors:
  token-name: "#HEX"
typography:
  token-name:
    fontFamily: Font Name
    fontSize: Npx
    fontWeight: N
    lineHeight: N
    letterSpacing: Npx
    fontFeature: "cv01, tnum"       # optional
    fontVariation: "..."            # optional
rounded:
  scale-level: Npx
spacing:
  scale-level: Npx
components:
  component-name:
    property: value or "{ref}"
---
```

### Section Order (Must Follow)

1. `## Overview` (alias: Brand & Style)
2. `## Colors`
3. `## Typography`
4. `## Layout` (alias: Layout & Spacing)
5. `## Elevation & Depth` (alias: Elevation)
6. `## Shapes`
7. `## Components`
8. `## Do's and Don'ts`

### Component Property Tokens (Spec-Defined)

- `backgroundColor`: Color
- `textColor`: Color
- `typography`: Typography reference
- `rounded`: Dimension
- `padding`: Dimension
- `size`: Dimension
- `height`: Dimension
- `width`: Dimension

## Edge Cases

- **SPA / client-rendered:** Use view-source + network tab for CSS files
- **Compressed CSS:** Use DevTools computed styles panel
- **Multi-theme (light/dark):** Ask user which theme to document. If both are distinct, offer separate files
- **Auth-gated pages:** Focus on public marketing pages only
- **Missing token categories:** Skip sections rather than invent values
- **Unknown section headings:** Preserve them per spec; do not error
- **Duplicate section headings:** Error; reject and fix before output
