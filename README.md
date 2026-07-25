# Khul Ke Pucho — "Aarogya" Shopify Theme

Custom Online Store 2.0 theme implementing Brand Guidelines v2 (`C:\Claude\Khul-Ke-Pucho-Brand-Guidelines-v2.pdf`).
Kumkum maroon `#5E1F30` · Kanchan gold `#C9962E` · Manuscript ivory `#F7EFDF` · Tiro Devanagari Sanskrit + EB Garamond + Mukta.

## 1. Create the store (if you don't have one)

1. Go to shopify.com → Start free trial → store name e.g. `khulkepucho`.
2. Pick the **Basic** plan when the trial ends (₹/month — needed for a live checkout).

## 2. Upload the theme

1. Zip this folder's contents (or use the ready `khulkepucho-theme.zip` next to this folder — the zip must contain `layout/`, `sections/`, `templates/`, etc. at its root).
2. Shopify admin → **Online Store → Themes → Add theme → Upload zip file**.
3. Click **Customize** to open the theme editor, then **Publish** when ready.

## 3. Add the 7 products

Create these in **Products** (Admin → Products → Add product):

| Product | Price | Type | Physical? |
|---|---|---|---|
| Super Urja | ₹3,938 | Vitality formulation | Yes |
| Shilajit | ₹2,400 | Classical rasayana | Yes |
| Paurush Oil (30ml) | ₹960 | External application | Yes |
| Private Doctor Consultation | ₹99 | Consultation | No — untick "This is a physical product" |
| PME Course | your price | Course | No |
| ED Course | your price | Course | No |
| Yoga for Vitality Course | your price | Course | No |

- Create a collection **"All formulations"** (the 3 physical products) and assign it to the homepage **Featured products** section in the customizer.
- For consult/course products: after purchase, send the booking/access link via the order confirmation email (Settings → Notifications → Order confirmation) or a WhatsApp flow.

## 4. Payments — Razorpay + COD

1. **Razorpay:** Admin → Settings → Payments → choose **Razorpay Secure** (Payments app for India) → connect your Razorpay account (KYC needed). This enables UPI, cards, netbanking, wallets.
2. **COD:** Settings → Payments → **Manual payment methods → Cash on Delivery** → activate. In the instructions field write: *"Pay in cash when your plain parcel arrives. No product name appears outside."*

## 5. Theme settings to fill (Customize → Theme settings)

- **Trust & compliance → AYUSH license number** — the footer and trust strip show a TODO until this is set.
- **Trust & compliance → WhatsApp number** — powers the floating WhatsApp button.
- **Brand colors** — pre-set to Brand Guidelines v2; don't change without checking the contrast table (Guidelines ch. 6).

## 6. Pages & navigation

Create pages (Admin → Online Store → Pages) and assign templates:
- **About Us** → template `page.about`
- **Consultation** → template `page.consult`
- **Courses** → template `page.courses`
- **Contact** → template `page.contact`

Menus (Online Store → Navigation): `main-menu` → Home, Shop (All formulations collection), Consultation, Courses, Blog, About. `footer` → Contact, Privacy Policy, Terms, Refund Policy, Shipping Policy (generate policies in Settings → Policies).

## 7. Replace the placeholders (marked TODO throughout)

- Product photos → upload on each product (placeholder art disappears automatically).
- Doctor photos, names, qualifications, registration numbers → homepage/consult page **Doctor panel** section blocks.
- Lab report PDFs → upload in Content → Files, then paste the URL into each product page's **Lab report PDF link** section setting.
- Stats band numbers → real counts only (brand rule: this audience distrusts rounded numbers).
- Testimonials → real service-experience quotes, no medical-outcome claims (Drugs & Magic Remedies Act).

## 8. Domain

Settings → Domains → Connect existing domain → `khulkepucho.com` (update DNS at your registrar: CNAME `www` → `shops.myshopify.com`, A record `@` → Shopify's IP as instructed on that screen).

## Compliance notes (do not skip)

- Never publish copy claiming to **cure** impotence/PE — "supports", "helps improve", "doctor-guided plan" only.
- Keep the medical disclaimer setting filled; it renders on product pages, articles and the footer.
- Meta ads: send traffic to education/consult pages, never directly to restricted product pages; population-framing only (see Guidelines ch. 10).

## Theme structure

```
layout/theme.liquid          — head, fonts, header/footer hooks, WhatsApp float
config/settings_schema.json  — brand colors, AYUSH license, WhatsApp, disclaimer
templates/*.json             — page compositions (OS 2.0 JSON templates)
sections/*.liquid            — 20 sections incl. hero-shloka, trust-strip, doctor-panel,
                               consult-cta, course-cards, ingredient-story, shloka-divider,
                               journey-steps, stats-band, testimonials, faq, newsletter
snippets/*.liquid            — product-card, price, trust-badges, placeholder-image
assets/theme.css, theme.js   — tokens from Guidelines ch. 11; JS kept tiny for T2/T3 data budgets
```
