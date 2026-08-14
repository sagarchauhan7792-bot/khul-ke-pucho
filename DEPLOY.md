# Khul Ke Pucho — Go-Live Guide (funnel site)

This is the static HTML funnel in `C:\Claude\khulkepucho-site\funnel\`. It's a complete, self-contained site (HTML + inline CSS/JS + local SVG images). All links are relative, so it works on any host or subpath.

---

## A. Pre-launch checklist — fill every TODO

Search the `funnel/` folder for `TODO` and replace:

| What | Where | Notes |
|---|---|---|
| WhatsApp number `919999999999` | `index.html`, `product.html` (+ regenerate), `checkout.html`, all policy pages | Your WhatsApp Business number, country code, no `+` |
| Analytics IDs `TODO_GA4_ID`, `TODO_PIXEL_ID` | `index.html`, `product.html` `<head>` | GA4 Measurement ID + Meta Pixel ID; inert until filled |
| Razorpay key `RAZORPAY_KEY` (blank) | `checkout.html` `<script>` | See section C for real payments |
| AYUSH licence no. | `index.html` footer, product pages | Also add lab-report PDF links on product pages |
| Company legal block | all policy pages footer | Legal entity name, GST no., registered address, support email/phone, grievance officer |
| Doctor names / photos / reg. nos. | `index.html` doctors section; swap `img/doc1–4.svg` | Real headshots strongly recommended |
| Real product photos | `funnel/img/*.svg` | Replace with `.jpg`/`.png` (keep same base filename, or update `<img src>`) |
| Stats numbers | `index.html` stats band | Use real counts only |
| Policy dates + review | all policy pages | **Have a lawyer review** the templates before publishing |

**Site structure (Aug 2026):** multi-page. Shared styles/JS live in `assets/kkp.css` + `assets/kkp.js`. Wing/category pages (`aarogya`, `aanand`, `timing`, `erection-health`, `vitality`, `devices`, `intimate-care`, `couples`) are generated from `category.html`. After editing `category.html`, regenerate them:
```powershell
# from repo root
$root='.'; $src=[IO.File]::ReadAllText("$root\category.html")
$needle="var cat = /*KKP_CAT*/ new URLSearchParams(location.search).get('c') || 'aarogya';"
$pages=@('aarogya','aanand','timing','erection-health','vitality','devices','intimate-care','couples')
$enc=New-Object System.Text.UTF8Encoding($false)
foreach($p in $pages){[IO.File]::WriteAllText("$root\$p.html",$src.Replace($needle,"var cat = '$p';"),$enc)}
```

Journal articles are generated from `article.html` the same way (needle `var art = /*KKP_ART*/...`, pages: why-timing-happens, erection-circulation-story, shilajit-science, arousal-gap, how-couples-start-talking, discreet-buying-guide). Standalone pages: `exercises.html`, `journal.html`, `track-order.html`.

After editing `product.html`, regenerate the 17 product pages:
```powershell
# from repo root
$root='.\funnel'; $src=[IO.File]::ReadAllText("$root\product.html")
$needle="var key = /*KKP_KEY*/ new URLSearchParams(location.search).get('p');"
$map=[ordered]@{urja='shukra.html';shilajit='shilajit.html';oil='paurush-oil.html';kit='complete-care-kit.html';pme='pme-course.html';ed='ed-course.html';yoga='yoga-course.html';consult='consultation.html';yugal='yugal.html';tarang='tarang.html';bindu='bindu.html';bandhan='bandhan.html';snigdha='snigdha.html';sparsh='sparsh.html';jyoti='jyoti.html';milan='milan-kit.html';khulibaat='khuli-baat.html'}
$enc=New-Object System.Text.UTF8Encoding($false)
foreach($k in $map.Keys){[IO.File]::WriteAllText("$root\$($map[$k])",$src.Replace($needle,"var key = '$k';"),$enc)}
```

---

## B. Publish free on GitHub Pages (fastest)

1. Create a GitHub repo (e.g. `khulkepucho-site`).
2. Put the **contents of `funnel/`** at the repo root (so `index.html` is at the top).
3. Push:
   ```bash
   git init
   git add .
   git commit -m "Launch Khul Ke Pucho funnel site"
   git branch -M main
   git remote add origin https://github.com/<you>/khulkepucho-site.git
   git push -u origin main
   ```
4. GitHub → **Settings → Pages** → Source: `main` / root → Save. Live in ~60s at `https://<you>.github.io/khulkepucho-site/`.

### Connect khulkepucho.com
- GitHub Pages → Custom domain → enter `khulkepucho.com` → Save (creates a `CNAME` file).
- At your domain registrar (DNS):
  - `A` records for apex `@` → `185.199.108.153`, `.109.153`, `.110.153`, `.111.153`
  - `CNAME` `www` → `<you>.github.io`
- Tick **Enforce HTTPS** once DNS resolves.

*(Alternatives: Netlify or Vercel — drag-and-drop the `funnel/` folder; both give free HTTPS + custom domain.)*

---

## C. Real payments (checkout.html)

The checkout page has a **fully working COD flow** and a **Razorpay path in test mode**. Razorpay Checkout on a static page is not production-secure on its own — the payment must be created and its signature verified server-side. Two options:

- **Easiest (no backend):** use **Razorpay Payment Pages / Payment Links**, or move selling to the **Shopify theme** in `C:\Claude\khulkepucho-site\` (its README already documents Razorpay + COD). Recommended if you don't want to run a server.
- **Keep this checkout:** add a tiny backend (e.g. a serverless function) that (1) creates a Razorpay order and returns its `order_id`, and (2) verifies `razorpay_signature` on success before you treat the order as paid. Then set `RAZORPAY_KEY` in `checkout.html` and pass the server `order_id` into the `Razorpay(...)` options. Until then, COD is the live-safe option.

---

## D. Also required before ads / payments go live
- Working **policy pages** (done — fill the company/legal TODOs).
- **18+ age gate** (already on the homepage).
- Razorpay KYC (business docs, GST, bank account).
- Meta/Google: send ad traffic to education/consult pages, population-framed creative, no cure claims (see brand guidelines ch. 10).
