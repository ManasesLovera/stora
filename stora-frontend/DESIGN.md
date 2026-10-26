# Stora Frontend Design

Decisions about the visual design of the Stora frontend. Read this before building or
restyling any UI. Reference mockups live in
[`docs/design-samples/`](docs/design-samples/) and open directly in a browser.

## Current decision

**Use the Ledger style for the whole product** (merchant/client interface and, for now,
tenant storefronts). One design system, one set of tokens.

Decided on 2026-10-25.

## Style directions evaluated

| Direction | Status | Notes |
| --- | --- | --- |
| **Ledger** | **Adopted** | Precise, quiet, tool-like. Used everywhere for now. |
| **Atelier** | Kept for later | Planned as one selectable storefront theme. See feedback below. |
| **Mercado** | Rejected | Too playful and loud for a serious business product. Not kept. |

Reference files:

- [`docs/design-samples/ledger.html`](docs/design-samples/ledger.html): admin dashboard
  (sidebar, KPI cards, chart, appointments, orders table, dark mode).
- [`docs/design-samples/atelier.html`](docs/design-samples/atelier.html): editorial
  storefront (hero, product grid, story section, footer).

## Ledger design system

### Typography

| Role | Font | Notes |
| --- | --- | --- |
| UI and body | **Geist** (400, 500, 600) | 14px base, line-height 1.5 |
| Numbers, IDs, prices | **Geist Mono** (400, 500) | Use `font-variant-numeric: tabular-nums` so columns align |

Headings use Geist 600 with slight negative tracking (`-0.02em`). Page title is 22px.

### Color tokens

Define as CSS custom properties on `:root`, and override them under
`@media (prefers-color-scheme: dark)`.

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `--bg` | `#f7f7f5` | `#101113` | Page background |
| `--surface` | `#ffffff` | `#17181b` | Cards, sidebar |
| `--sunken` | `#f0f0ed` | `#1d1f23` | Hover, table headers, inputs |
| `--ink` | `#17181a` | `#ececea` | Primary text |
| `--muted` | `#6b6e73` | `#8c9096` | Secondary text |
| `--line` | `#e4e4e0` | `#2a2c31` | 1px borders and dividers |
| `--accent` | `#0b6b4f` | `#3ecf9b` | Primary actions, active nav, positive trends |
| `--accent-soft` | `#dff1e9` | `#143528` | Active nav background, "paid" chips |
| `--accent-ink` | `#ffffff` | `#07140f` | Text on `--accent` |
| `--warn` / `--warn-soft` | `#b45309` / `#fdeccd` | `#f5b25a` / `#3a2a10` | Pending |
| `--bad` / `--bad-soft` | `#b42318` / `#fde3e0` | `#ff8a80` / `#3d1a17` | Errors, refunds, negative trends |
| `--info` / `--info-soft` | `#1d4ed8` / `#e0e8fd` | `#8fb0ff` / `#172647` | Shipped, informational |

### Shape and spacing

- Corner radius: 10px for cards, 8px for buttons and inputs, 99px for chips.
- Borders are 1px `--line`. No heavy shadows.
- Layout: 232px sidebar, main content max width 1180px, 14px gap between cards.
- Collapse the sidebar and stack columns below 960px.

### Components shown in the sample

Sidebar with tenant switcher and plan usage meter, KPI card, line chart, appointment list,
data table with status chips, primary and secondary buttons.

### Principles

- One accent color. Status colors are only for status.
- Numbers always use the mono font.
- Keep focus rings visible (`2px solid var(--accent)`) and respect
  `prefers-reduced-motion`.
- No gradients, glassmorphism, or emoji as icons. Use inline SVG with a 1.6px stroke.

## Atelier (future storefront theme)

Editorial and warm. Intended as one of several selectable storefront styles.

- Fonts: **Fraunces** (display serif) and **Instrument Sans** (body). The user likes this
  font family.
- Palette: bone `#f4efe6`, paper `#fbf8f2`, ink `#1c1a17`, clay `#b94a2c`, moss `#4a5a3c`,
  sand `#e3d3b8`.

> [!warning]
> **Feedback on the hero headline.** The headline "Objects made to be used, slowly." is
> almost right but hard to read. In the sample it uses Fraunces weight 300, optical size
> 144, tight tracking (`-0.03em`), and a light italic accent word. When this theme is built,
> use a heavier weight (400 to 500), a lower optical size, looser tracking, and avoid
> italicizing a word in the headline. Re-check at mobile sizes.

## Roadmap: multiple and custom themes

Not built yet. Planned direction:

- Tenants can choose from several storefront design styles (Atelier first).
- Tenants can configure their own style and bring their own (fonts, palette, logo).
- Store the selected preset and overrides in `Tenant.settings` (JSON).
- To make this possible, **all components must read colors, fonts, and radii from CSS
  custom properties**, never hardcoded values. A theme is then just a set of token values.

Until this ships, every tenant uses Ledger.
