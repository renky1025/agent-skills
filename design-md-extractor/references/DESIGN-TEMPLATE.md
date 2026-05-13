---
name: Brand Name
description: One-line brand description (e.g., "A premium AI-native design tool")
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface: "#FFFFFF"
  error: "#D32F2F"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  h2:
    fontFamily: Public Sans
    fontSize: 36px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: -0.015em
  h3:
    fontFamily: Public Sans
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Public Sans
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-lg:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.08em
  label-md:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.08em
  label-sm:
    fontFamily: Space Grotesk
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.06em
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 64px
  gutter: 24px
  margin: 32px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 12px 20px
    typography: "{typography.label-lg}"
  button-primary-hover:
    backgroundColor: "#A33A28"
  button-primary-active:
    backgroundColor: "#8C2F20"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: 12px 20px
    typography: "{typography.label-lg}"
    border: "1px solid {colors.secondary}"
  button-secondary-hover:
    backgroundColor: "rgba(108,114,120,0.08)"
  input-default:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 12px 16px
    typography: "{typography.body-md}"
    border: "1px solid {colors.secondary}"
  input-focused:
    border: "2px solid {colors.tertiary}"
  card-default:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
    padding: 24px
---

## Overview

Architectural Minimalism meets Journalistic Gravitas. The interface evokes a premium matte finish — a high-end broadsheet or contemporary gallery. The dominant background is a warm limestone surface that provides a tactile, inviting foundation. Deep ink typography in Public Sans conveys institutional trustworthiness, while the single Boston Clay accent commands attention for every interaction. Space Grotesk labels introduce a precise, technical counterpoint — like a watchmaker's engraving on a leather-bound journal. The result is a system that feels both established and intimate, built for long-form reading and deliberate action.

## Colors

The palette is rooted in high-contrast neutrals and a single, evocative accent color.

- **Primary (#1A1C1E):** A deep ink used for headlines and core text to provide maximum readability and a sense of permanence.
- **Secondary (#6C7278):** A sophisticated slate used primarily for utilitarian elements like borders, captions, and metadata.
- **Tertiary (#B8422E):** "Boston Clay" — the sole driver for interaction, used exclusively for primary actions and critical highlights.
- **Neutral (#F7F5F2):** A warm limestone that serves as the foundation for all pages, providing a softer, more organic feel than pure white.
- **Surface (#FFFFFF):** Pure white for cards and elevated containers, creating clear visual separation from the warm page background.
- **Error (#D32F2F):** Reserved exclusively for destructive actions and validation messages.

### Design Tokens

The `colors` section in the YAML front matter defines all color tokens. See front matter for complete values.

## Typography

The typography strategy leverages two distinct typefaces: **Public Sans** for narrative content and **Space Grotesk** for technical data and labels.

- **Headlines (h1-h3):** Set in Public Sans Semi-Bold (weight 600) to establish an institutional and trustworthy voice. Letter spacing tightens at larger sizes for editorial polish.
- **Body (body-lg, body-md, body-sm):** Public Sans Regular at sizes ranging from 14-18px ensures contemporary professionalism and long-form readability. Consistent 1.6 line-height across all body sizes maintains a comfortable reading rhythm.
- **Labels (label-lg, label-md, label-sm):** Space Grotesk Medium is used for all technical data, timestamps, metadata, and button text. Its geometric construction evokes the precision of a digital instrument. Labels are strictly uppercase with generous letter spacing (0.06em-0.08em).

### Design Tokens

See front matter `typography` section for complete token definitions with exact values.

## Layout

The layout follows a **Fluid Grid** model for mobile devices and a **Fixed-Max-Width Grid** for desktop (max 1200px content area). Navigation is sticky with a transparent-to-solid background transition on scroll.

An 8px spacing scale (with a 4px half-step) maintains consistent rhythm. Components are grouped using a containment principle: related items live in cards with generous internal padding (24px), emphasizing the brand's approachable nature. Section spacing (64px) provides clear visual breathing room between content blocks.

The layout uses a 24px gutter between columns and 32px outer margin on desktop viewports, collapsing to 16px margins on mobile.

## Elevation & Depth

The design achieves visual hierarchy through **Tonal Layering** rather than heavy shadows. The foundation sits on the warm Neutral (#F7F5F2) surface, while content areas rise onto pure white cards. This creates a subtle but clear distinction without relying on drop shadows.

When elevation is needed for interactive states, shadows use the secondary color (#6C7278) at low opacity, creating a sophisticated diffusion rather than harsh drops. Modals and dialogs use a scrim based on Primary (#1A1C1E) at 40% opacity.

## Shapes

The shape language is defined by **Architectural Sharpness with Gentle Softening**. All interactive elements use a minimal 4px corner radius, providing just enough softness to feel modern while maintaining a rigid, engineered aesthetic.

- Cards and containers: 12px radius for a contained, friendly feel
- Buttons and inputs: 4px (sm) for precision
- Pills and tags: 9999px (full) for maximum roundness
- Notification badges: 9999px (full)

Inconsistent corner treatments between adjacent elements are avoided — all edges within a component family share the same radius.

### Design Tokens

See front matter `rounded` section for complete values.

## Components

### Primary Button
**Role:** Primary call to action

```yaml
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"  # #B8422E
    textColor: "{colors.neutral}"         # #F7F5F2
    rounded: "{rounded.sm}"               # 4px
    padding: 12px 20px
    typography: "{typography.label-lg}"   # Space Grotesk 14px/500/1/0.08em
  button-primary-hover:
    backgroundColor: "#A33A28"            # Darker clay
  button-primary-active:
    backgroundColor: "#8C2F20"            # Deepest clay
```

Used once per view for the single most important action. Never use multiple primary buttons on the same screen.

### Secondary Button
**Role:** Alternative actions, dismiss

```yaml
components:
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"         # #1A1C1E
    rounded: "{rounded.sm}"               # 4px
    padding: 12px 20px
    border: "1px solid {colors.secondary}"
    typography: "{typography.label-lg}"
  button-secondary-hover:
    backgroundColor: "rgba(108,114,120,0.08)"
```

Used for secondary actions alongside a primary button, or standalone for non-critical paths.

### Input Field
**Role:** Text and data entry

```yaml
components:
  input-default:
    backgroundColor: "{colors.neutral}"   # #F7F5F2
    textColor: "{colors.primary}"         # #1A1C1E
    rounded: "{rounded.md}"               # 8px
    padding: 12px 16px
    border: "1px solid {colors.secondary}"
    typography: "{typography.body-md}"    # Public Sans 16px/400/1.6
  input-focused:
    border: "2px solid {colors.tertiary}" # #B8422E
```

Includes descriptive label above using `{typography.label-md}` and helper text below. Error state sets border to `{colors.error}` (#D32F2F).

### Card
**Role:** Content containers

```yaml
components:
  card-default:
    backgroundColor: "{colors.surface}"   # #FFFFFF
    rounded: "{rounded.lg}"               # 12px
    padding: 24px
```

Cards group related content on the Neutral (#F7F5F2) background. Internal spacing uses `{spacing.md}` (16px) between elements within the card.

## Do's and Don'ts

### Do
- Use `{colors.primary}` (#1A1C1E) for all headlines and body text to maintain maximum readability
- Apply `{colors.tertiary}` (#B8422E) exclusively for the single most important action per screen
- Use `{typography.label-lg}` (Space Grotesk 14px uppercase) for all button labels to ensure consistency
- Maintain `{rounded.sm}` (4px) for all interactive elements to preserve the architectural aesthetic
- Use `{colors.neutral}` (#F7F5F2) as the primary page background and `{colors.surface}` (#FFFFFF) for cards
- Keep 1.6 line-height on `{typography.body-md}` for comfortable long-form reading
- Use `{spacing.section}` (64px) between major content sections for clear visual hierarchy
- Apply `{colors.error}` (#D32F2F) only to destructive actions and validation errors

### Don't
- Don't use `{colors.tertiary}` (#B8422E) for non-interactive elements — it's reserved exclusively for actions
- Don't mix `{rounded.sm}` (4px) and `{rounded.lg}` (12px) within the same component group
- Don't use Public Sans for labels and metadata — that's the role of Space Grotesk
- Don't place text directly on `{colors.neutral}` (#F7F5F2) without a card container — use `{colors.surface}` instead
- Don't use more than two font weights on a single screen (400 + 600 for Public Sans, 500 for Space Grotesk labels)
- Don't exceed 1200px content width — the grid is designed for fixed-max-width at desktop
- Don't use `{colors.secondary}` (#6C7278) for primary body text — it fails WCAG AA contrast on `{colors.neutral}`
- Don't add decorative drop shadows — prefer tonal layering for elevation
