# Eurofiora design system

Context file for building shop.eurofiora.it, app.eurofiora.it and admin.eurofiora.it. Read this before writing any template, CSS or UI code. If a choice is not covered here, pick the quieter option.

## 1. Where this comes from

The reference is a premium florist storefront (downloaded locally as a study copy). We take its **qualities**, never its material:

What we take: lots of white space, photography doing the selling, one serif voice for headlines against a plain sans for everything else, flat surfaces with no decoration, a short homepage with clear sections, product cards that are just a square photo, a name and a price, and a product page where the photo is large and the buying panel is calm.

What we never take: their HTML, CSS, JavaScript, images, product names, copy, logo, or their exact font pairing (Instrument Serif with DM Sans) and colour values. Eurofiora has its own identity below. The study copy stays on the local PC and never goes into the repo.

## 2. Identity in one line

A Milan florist with Italian restraint: editorial, quiet, confident. It should feel like a good printed catalogue, not an app template.

## 3. Colour

Exact values only. Do not lighten, darken, add opacity variants, or invent in between shades. If a shade is missing from this table, it is not allowed.

| Token | Hex | Use |
|---|---|---|
| `--paper` | `#FFFFFF` | Page background |
| `--stone` | `#F4F1EC` | Secondary surfaces: footer, info bands, photo backdrops, input fill on hover |
| `--ink` | `#171614` | Text, primary buttons, icons |
| `--ink-soft` | `#6B665F` | Secondary text, captions, meta |
| `--line` | `#E3DED6` | Every border and divider, always 1px |
| `--leaf` | `#1E4A38` | The only accent: selected states (size, date), focus ring, small labels like "Consegna oggi" |
| `--alert` | `#A8321F` | Errors, sold out, cutoff passed. Never decorative |

Rules: no gradients, no shadows, no coloured backgrounds behind sections except `--stone`. Text on photos only when the photo has a calm area; never add a dark overlay to force contrast. Green is used sparingly, roughly one green element per screen.

## 4. Typography

Both families are on Google Fonts. Load only the weights listed.

| Role | Family | Weights | Notes |
|---|---|---|---|
| Display | Bodoni Moda | 400, 400 italic | Headlines, product names, prices on the product page. Italian heritage, high contrast. Never bold, never uppercase |
| Text and UI | Hanken Grotesk | 400, 500 | Body, navigation, buttons, forms, everything else |
| Data | IBM Plex Mono | 400 | Only in app and admin: order numbers, quantities, timestamps |

Scale (desktop / mobile):

| Token | Size | Line height | Family |
|---|---|---|---|
| `--t-hero` | 76px / 44px | 1.02 | Bodoni Moda |
| `--t-h1` | 48px / 34px | 1.08 | Bodoni Moda |
| `--t-h2` | 32px / 26px | 1.15 | Bodoni Moda |
| `--t-h3` | 21px / 19px | 1.25 | Bodoni Moda |
| `--t-body` | 16px | 1.6 | Hanken Grotesk |
| `--t-small` | 14px | 1.5 | Hanken Grotesk |
| `--t-label` | 12px, letter spacing 0.08em, uppercase | 1.4 | Hanken Grotesk 500 |

Headlines use sentence case. Italic Bodoni is allowed for one or two words inside a headline for emphasis, nowhere else. Body text never exceeds 64 characters per line.

## 5. Space and layout

Spacing scale, nothing outside it: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 px.

Page container: max width 1440px, side padding 20px mobile, 48px desktop. Sections are separated by 96px on desktop and 64px on mobile, not by borders or background changes.

Product grid: 2 columns mobile, 3 tablet, 4 desktop. Column gap 24px, row gap 48px.

Corners: 0 radius everywhere. Inputs, buttons, images, drawers: all square.

## 6. Photography (this decides whether it looks premium)

Every product photo: square 1:1, one arrangement centred, shot against a plain warm light backdrop matching `--stone`, soft daylight from one side, the same camera height and framing across the whole catalogue. No props, no text on images, no lifestyle clutter in the grid.

Lifestyle and atmosphere photos (hero, about, events) can be wider and more natural, but use few of them: one hero, at most two others on the homepage.

For the demo, use Eurofiora's own product photos. Until those exist, use plain `--stone` squares with the product name set small in the centre. Never stock photos with watermarks, never AI flower images, never images from the reference site.

## 7. Components: shop

**Announcement bar.** One line, 36px tall, `--ink` background, white `--t-small` text, centred. Used for the delivery cutoff, for example "Consegna in giornata a Milano per ordini entro le 14:00". No close button, no rotation.

**Header.** White, 72px tall, hairline bottom border. Wordmark "Eurofiora" centred in Bodoni Moda 28px. Navigation left in Hanken Grotesk 15px: Fiori, Piante, Occasioni, Regali. Right side as words, not icon soup: Cerca, Account, Carrello (2). Sticky on scroll.

**Hero.** One static full width image, height about 82vh, capped at 820px. Headline in `--t-hero` bottom left over a calm part of the photo, one short line of body text, one button. No carousel, no autoplay, no video.

**Category row.** Three or four tall tiles (4:5), photo above, `--t-h3` name below. Whole tile is the link. No arrows, no "Scopri di più" text.

**Product card.** Square photo, then 12px gap, product name in Hanken Grotesk 15px, price under it in `--ink-soft`. On hover the photo swaps to a second angle if one exists, otherwise nothing happens. No badges except a small `--t-label` "Esaurito" or "Consegna oggi". No quick add buttons, no ratings, no heart icons.

**Price format.** Italian: `€ 65,00`. Variable price: `da € 65,00`.

**Product page.** Desktop: photos stacked on the left (60% width), buying panel sticky on the right (40%). Mobile: swipeable photos, then the panel. The panel, in this order:

1. Product name in `--t-h1`
2. Price in Bodoni Moda 24px
3. Two or three lines of description
4. Size as a row of square text buttons (Piccolo, Medio, Grande). Selected state: `--ink` 1px border plus `--leaf` text
5. Vase option as the same button style
6. Delivery block (see section 8)
7. Card message, textarea, 200 character limit with a live counter
8. Add to cart button, full width
9. Accordions with hairline dividers: Cura dei fiori, Consegna, Sostituzioni

**Buttons.** 48px tall, square, Hanken Grotesk 500 15px sentence case. Primary: `--ink` fill, white text, hover becomes `--leaf` fill. Secondary: 1px `--ink` border, transparent. Text links: underlined 1px with 3px offset.

**Forms.** Labels above fields in `--t-small`. Fields 48px tall, 1px `--line` border, focus border `--leaf`. Errors in `--alert` under the field, in words, never just a red border.

**Cart.** Drawer from the right, 420px wide, full screen on mobile. Each line: small square photo, name, size, delivery date, quantity stepper, price. Totals and the checkout button pinned to the bottom.

**Checkout.** One page, three numbered blocks: Destinatario, Consegna, Pagamento. Order summary on the right on desktop, collapsible at the top on mobile. Test payments only in the demo.

**FAQ.** Accordion list with hairline dividers, question in `--t-h3`, answer in body text. No icons except a plain plus that turns to a minus.

**Footer.** `--stone` background. Four short text columns, newsletter field, P.IVA and legal links at the bottom in `--t-small`.

## 8. Delivery: the smart part, designed to feel simple

**Postcode check** on the product page: one field, "Inserisci il CAP". The answer appears in one line under it: "Consegniamo a 20121 oggi" or "Prima consegna disponibile: giovedì 9". Never a modal.

**Date picker.** A horizontal row of the next seven days as square buttons (day name above, number below). Unavailable days are `--ink-soft` with a strike. Today shows the cutoff in words: "Ordina entro 2 h 15 min".

**Time slots.** Three text buttons: Mattina 9:00 a 13:00, Pomeriggio 14:00 a 18:00, Sera 18:00 a 20:00. Full slots disappear rather than showing disabled.

**Tracking page** for the customer: order status as a vertical list of plain text steps with times, a simple map only once the order is out for delivery, and the estimated arrival as one large line in Bodoni Moda.

## 9. App (vendors) and admin

Same colours and fonts, different density. These are tools, not a catalogue:

No hero type. Page titles in `--t-h2`. Tables are the main element: 44px rows, hairline dividers only between rows, numbers right aligned in IBM Plex Mono, status as small `--t-label` text in the relevant colour, never coloured pills. Left sidebar navigation, 232px wide, plain text links, current page marked with a 2px `--ink` bar on the left. Metrics in admin are plain numbers in Bodoni Moda 32px with a `--t-small` label underneath, not cards with icons.

## 10. Motion

Only three things move: drawers slide in (200ms), accordions open (180ms), images fade in on load (300ms). Ease out. Nothing animates on scroll, no parallax, no marquees, no hover lifts.

## 11. Words

Customer facing text is in Italian, written plainly and warmly, short sentences. Buttons say exactly what happens: "Aggiungi al carrello", "Scegli la data", "Paga ora". Admin and vendor portals can be Italian or English, but consistent within a screen.

## 12. Never do this

These are the tells that make a site look generated. Check every screen against this list before shipping.

Rounded corners, drop shadows, gradients, glass or blur effects, indigo or purple anywhere, emoji used as icons, icon grids with three "feature" boxes, stock illustration, tinted variants of the palette colours, every section on a different background colour, centred text in long paragraphs, more than one accent colour on a screen, carousels on the homepage, badges on every product, star ratings in the grid, "Scopri di più" links on everything, decorative dividers, heavy bold headlines, uppercase headlines, testimonial sliders, floating chat bubbles, cookie banners that cover half the screen.

## 13. CSS starting point

```css
:root {
  --paper: #FFFFFF;
  --stone: #F4F1EC;
  --ink: #171614;
  --ink-soft: #6B665F;
  --line: #E3DED6;
  --leaf: #1E4A38;
  --alert: #A8321F;

  --font-display: "Bodoni Moda", "Didot", "Bodoni 72", Georgia, serif;
  --font-text: "Hanken Grotesk", "Helvetica Neue", Arial, sans-serif;
  --font-data: "IBM Plex Mono", ui-monospace, Menlo, monospace;

  --container: 1440px;
  --pad: 20px;
  --section: 64px;
}
@media (min-width: 900px) {
  :root { --pad: 48px; --section: 96px; }
}
* { border-radius: 0; box-shadow: none; }
body { background: var(--paper); color: var(--ink); font: 400 16px/1.6 var(--font-text); }
```
