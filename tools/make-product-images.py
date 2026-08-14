# -*- coding: utf-8 -*-
"""
Khul Ke Pucho — product image generator.
Emits studio-style SVG product renders into ../img/ using the Brand Guidelines v2 palette.
Re-run after edits:  python tools/make-product-images.py
"""
import os, io

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img')

# ---- brand palette -------------------------------------------------------
KUMKUM, KUMKUM_D = '#5E1F30', '#4A1826'
KANCHAN, GOLD_L = '#C9962E', '#DDB967'
IVORY, SURFACE, CHIP = '#F7EFDF', '#FFFDF8', '#EFE3CC'
VANA, TAMRA, TAMRA_D, GULAB = '#2F5D46', '#B4694E', '#8C4E38', '#E8B4B8'
INK, MUTED = '#241419', '#7A5C46'

SERIF = 'Georgia,\'Times New Roman\',serif'
SANS = 'Verdana,Geneva,sans-serif'

# ---- shared studio scaffolding -------------------------------------------
STUDIO_DEFS = f'''
  <radialGradient id="studio" cx=".5" cy=".42" r=".78">
    <stop offset="0" stop-color="{SURFACE}"/><stop offset=".55" stop-color="{IVORY}"/><stop offset="1" stop-color="#E9DCC2"/>
  </radialGradient>
  <radialGradient id="spot" cx=".5" cy=".45" r=".5">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".85"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vig" cx=".5" cy=".5" r=".72">
    <stop offset=".6" stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}" stop-opacity=".13"/>
  </radialGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{INK}" stop-opacity=".07"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/>
  </linearGradient>
  <filter id="soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="26"/></filter>
  <filter id="soft2" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11"/></filter>
  <filter id="soft3" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="glowf" x="-90%" y="-90%" width="280%" height="280%"><feGaussianBlur stdDeviation="34"/></filter>
  <linearGradient id="specV" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".55"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
'''

def backdrop(rings=True, tint=None):
    t = ''
    if tint:
        t = f'<circle cx="500" cy="452" r="330" fill="{tint}" opacity=".10" filter="url(#glowf)"/>'
    r = ''
    if rings:
        r = (f'<circle cx="500" cy="452" r="318" fill="none" stroke="{KANCHAN}" stroke-width="1.6" opacity=".32"/>'
             f'<circle cx="500" cy="452" r="352" fill="none" stroke="{KANCHAN}" stroke-width="1" opacity=".16"/>')
    return (f'<rect width="1000" height="1000" fill="url(#studio)"/>'
            f'<ellipse cx="500" cy="440" rx="430" ry="400" fill="url(#spot)"/>{t}{r}'
            f'<rect x="0" y="812" width="1000" height="188" fill="url(#floor)"/>')

def shadow(cx=500, cy=838, rx=210, ry=30, op=.24):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{INK}" opacity="{op}" filter="url(#soft)"/>'

def wordmark(y=946, color=MUTED, op=.55):
    return (f'<text x="500" y="{y}" text-anchor="middle" font-family="{SERIF}" font-size="19" '
            f'letter-spacing="5" fill="{color}" opacity="{op}">KHUL KE PUCHO</text>')

def eyebrow(text, color=KANCHAN, y=92):
    return (f'<text x="500" y="{y}" text-anchor="middle" font-family="{SANS}" font-size="15" '
            f'letter-spacing="7" fill="{color}" opacity=".9">{text}</text>')

def svg(name, body, defs=''):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img">\n'
           f'<defs>{STUDIO_DEFS}{defs}</defs>\n{body}\n'
           f'<rect width="1000" height="1000" fill="url(#vig)"/>\n</svg>\n')
    with io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(doc)
    return name

# ---- reusable material pieces --------------------------------------------
def glass_body(x, y, w, h, rx, grad, hi_op=.30):
    """bottle/jar body with specular highlight + rim light"""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{grad})"/>'
            f'<rect x="{x+w*0.08}" y="{y+h*0.05}" width="{w*0.13}" height="{h*0.85}" rx="{w*0.065}" fill="#FFFFFF" opacity="{hi_op}" filter="url(#soft3)"/>'
            f'<rect x="{x+w*0.87}" y="{y+h*0.08}" width="{w*0.05}" height="{h*0.8}" rx="{w*0.025}" fill="#FFFFFF" opacity=".16" filter="url(#soft3)"/>')

def label_plate(x, y, w, h, rx=16):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{IVORY}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{KANCHAN}" stroke-width="2" opacity=".75"/>'
            f'<rect x="{x+9}" y="{y+9}" width="{w-18}" height="{h-18}" rx="{max(4,rx-8)}" fill="none" stroke="{KANCHAN}" stroke-width="1" opacity=".45"/>')

def lotus(cx, cy, s=1.0, color=KANCHAN, sw=4):
    """small lotus/diya brand mark"""
    return (f'<g transform="translate({cx},{cy}) scale({s})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round">'
            f'<path d="M0 16 C-14 16 -26 6 -31 -8 C-19 -5 -9 0 0 10 C9 0 19 -5 31 -8 C26 6 14 16 0 16 Z"/>'
            f'<path d="M0 10 C-5 -3 -5 -17 0 -28 C5 -17 5 -3 0 10 Z"/>'
            f'<circle cx="0" cy="-36" r="3.4" fill="{color}" stroke="none"/></g>')

def capsule(cx, cy, rot, w=96, h=38, top=GOLD_L, bot=KUMKUM):
    r = h/2
    return (f'<g transform="translate({cx},{cy}) rotate({rot})">'
            f'<rect x="{-w/2}" y="{-r}" width="{w/2}" height="{h}" rx="{r}" fill="{top}"/>'
            f'<rect x="0" y="{-r}" width="{w/2}" height="{h}" rx="{r}" fill="{bot}"/>'
            f'<rect x="{-w/2+6}" y="{-r+6}" width="{w-12}" height="7" rx="3.5" fill="#FFFFFF" opacity=".28"/></g>')

def booklet(accent, title_sk, title_en, sub, motif):
    """course product: a printed workbook standing up"""
    return f'''
  {shadow(500, 846, 205, 27, .22)}
  <!-- back sheets -->
  <rect x="316" y="238" width="372" height="516" rx="12" fill="#E4D6BC"/>
  <rect x="308" y="230" width="372" height="516" rx="12" fill="#EFE3CC"/>
  <!-- cover -->
  <rect x="298" y="222" width="380" height="524" rx="13" fill="url(#cover)"/>
  <rect x="298" y="222" width="22" height="524" rx="6" fill="{INK}" opacity=".22"/>
  <rect x="330" y="222" width="14" height="524" fill="#FFFFFF" opacity=".07"/>
  <rect x="356" y="286" width="266" height="396" rx="10" fill="none" stroke="{GOLD_L}" stroke-width="1.6" opacity=".55"/>
  {motif}
  <text x="490" y="556" text-anchor="middle" font-family="{SERIF}" font-size="27" fill="{GOLD_L}" opacity=".95">{title_sk}</text>
  <text x="490" y="614" text-anchor="middle" font-family="{SERIF}" font-size="42" font-weight="bold" letter-spacing="2" fill="{IVORY}">{title_en}</text>
  <rect x="425" y="634" width="130" height="2" fill="{accent}"/>
  <text x="490" y="668" text-anchor="middle" font-family="{SANS}" font-size="15" letter-spacing="3" fill="#E2CDB2">{sub}</text>
  {wordmark()}
'''

# =========================================================================
# AAROGYA — wellness
# =========================================================================
def p_shukra():
    defs = f'''
  <linearGradient id="jar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#7A3247"/><stop offset=".18" stop-color="#6F2A3E"/><stop offset=".52" stop-color="{KUMKUM}"/><stop offset=".85" stop-color="#3F1420"/><stop offset="1" stop-color="#572030"/>
  </linearGradient>
  <linearGradient id="cap" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#E7CB8B"/><stop offset=".3" stop-color="{GOLD_L}"/><stop offset=".62" stop-color="{KANCHAN}"/><stop offset="1" stop-color="#8E6819"/>
  </linearGradient>'''
    body = f'''
  {backdrop(tint=KUMKUM)}
  {eyebrow('AAROGYA · VITALITY')}
  {shadow(500, 836, 215, 30)}
  <!-- capsules -->
  {capsule(266, 806, -14)}
  {capsule(742, 812, 11)}
  {capsule(690, 780, -33, 84, 34)}
  <!-- cap -->
  <rect x="326" y="196" width="348" height="86" rx="18" fill="url(#cap)"/>
  <rect x="326" y="196" width="348" height="16" rx="8" fill="#FFFFFF" opacity=".28"/>
  <rect x="326" y="264" width="348" height="9" fill="#6F5114" opacity=".5"/>
  <g stroke="#8E6819" stroke-width="2" opacity=".35">
    {''.join(f'<line x1="{x}" y1="204" x2="{x}" y2="264"/>' for x in range(342, 674, 16))}
  </g>
  <!-- neck + body -->
  <rect x="352" y="272" width="296" height="26" fill="#3F1420"/>
  {glass_body(310, 288, 380, 496, 40, 'jar')}
  <!-- label -->
  {label_plate(346, 372, 308, 330)}
  {lotus(500, 452, 1.05)}
  <text x="500" y="522" text-anchor="middle" font-family="{SERIF}" font-size="24" fill="{MUTED}">शुक्र</text>
  <text x="500" y="576" text-anchor="middle" font-family="{SERIF}" font-size="46" font-weight="bold" letter-spacing="3" fill="{KUMKUM}">SHUKRA</text>
  <rect x="418" y="596" width="164" height="2.4" fill="{KANCHAN}"/>
  <text x="500" y="630" text-anchor="middle" font-family="{SANS}" font-size="15" letter-spacing="4" fill="{MUTED}">VITALITY FORMULATION</text>
  <text x="500" y="662" text-anchor="middle" font-family="{SANS}" font-size="14.5" fill="{MUTED}">60 capsules · 60-day course</text>
  <!-- base seal -->
  <rect x="310" y="716" width="380" height="52" fill="{KUMKUM_D}"/>
  <text x="500" y="750" text-anchor="middle" font-family="{SERIF}" font-size="19" fill="{GOLD_L}">आरोग्यं मूलमुत्तमम्</text>
  {wordmark()}
'''
    return svg('shukra.svg', body, defs), svg('urja.svg', body, defs)

def p_shilajit():
    defs = f'''
  <linearGradient id="jar2" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#4B3A2A"/><stop offset=".2" stop-color="#3A2C20"/><stop offset=".55" stop-color="#2A2018"/><stop offset=".88" stop-color="#1C150F"/><stop offset="1" stop-color="#3A2C20"/>
  </linearGradient>
  <linearGradient id="lid" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#E7CB8B"/><stop offset=".35" stop-color="{GOLD_L}"/><stop offset=".7" stop-color="{KANCHAN}"/><stop offset="1" stop-color="#8E6819"/>
  </linearGradient>
  <radialGradient id="resin" cx=".38" cy=".3" r=".8">
    <stop offset="0" stop-color="#6B5033"/><stop offset=".6" stop-color="#33251A"/><stop offset="1" stop-color="#15100B"/>
  </radialGradient>'''
    body = f'''
  {backdrop(tint='#3A2C20')}
  {eyebrow('AAROGYA · CLASSICAL RASAYANA')}
  {shadow(500, 812, 230, 30)}
  <!-- spatula -->
  <g transform="translate(742,690) rotate(-24)">
    <rect x="-12" y="-190" width="24" height="250" rx="12" fill="{GOLD_L}"/>
    <rect x="-7" y="-180" width="6" height="220" rx="3" fill="#FFFFFF" opacity=".3"/>
    <ellipse cx="0" cy="70" rx="30" ry="22" fill="{KANCHAN}"/>
    <ellipse cx="0" cy="66" rx="22" ry="14" fill="url(#resin)"/>
  </g>
  <!-- lid -->
  <rect x="330" y="292" width="340" height="74" rx="16" fill="url(#lid)"/>
  <rect x="330" y="292" width="340" height="14" rx="7" fill="#FFFFFF" opacity=".3"/>
  <rect x="330" y="350" width="340" height="8" fill="#6F5114" opacity=".45"/>
  <!-- squat jar -->
  {glass_body(342, 356, 316, 372, 34, 'jar2', .18)}
  <ellipse cx="500" cy="404" rx="140" ry="26" fill="url(#resin)"/>
  <ellipse cx="470" cy="396" rx="42" ry="12" fill="#8A6A44" opacity=".35" filter="url(#soft3)"/>
  <!-- label -->
  {label_plate(372, 452, 256, 232)}
  <text x="500" y="502" text-anchor="middle" font-family="{SERIF}" font-size="26" fill="{MUTED}">शिलाजतु</text>
  <text x="500" y="552" text-anchor="middle" font-family="{SERIF}" font-size="42" font-weight="bold" letter-spacing="2" fill="{KUMKUM}">SHILAJIT</text>
  <rect x="420" y="570" width="160" height="2.4" fill="{KANCHAN}"/>
  <text x="500" y="604" text-anchor="middle" font-family="{SANS}" font-size="14.5" letter-spacing="3" fill="{MUTED}">PURE HIMALAYAN RESIN</text>
  <text x="500" y="634" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{VANA}">40% fulvic acid · 20g</text>
  <text x="500" y="662" text-anchor="middle" font-family="{SANS}" font-size="12.5" letter-spacing="2" fill="{MUTED}">SHODHANA-PURIFIED · LAB TESTED</text>
  {wordmark()}
'''
    return svg('shilajit.svg', body, defs)

def p_oil():
    defs = f'''
  <linearGradient id="amber" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#C98A3C"/><stop offset=".2" stop-color="#A96C24"/><stop offset=".55" stop-color="#8A5417"/><stop offset=".88" stop-color="#5E3810"/><stop offset="1" stop-color="#8A5417"/>
  </linearGradient>
  <linearGradient id="drop" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{GOLD_L}"/><stop offset="1" stop-color="#B07C1E"/>
  </linearGradient>'''
    body = f'''
  {backdrop(tint='#A96C24')}
  {eyebrow('AAROGYA · EXTERNAL APPLICATION')}
  {shadow(500, 826, 175, 26)}
  <!-- dropper cap -->
  <rect x="424" y="180" width="152" height="104" rx="16" fill="url(#lidg)"/>
  <rect x="424" y="180" width="152" height="15" rx="7" fill="#FFFFFF" opacity=".32"/>
  <g stroke="#6F5114" stroke-width="2" opacity=".3">
    {''.join(f'<line x1="{x}" y1="190" x2="{x}" y2="274"/>' for x in range(436, 570, 12))}
  </g>
  <rect x="444" y="284" width="112" height="26" fill="#5E3810"/>
  <!-- bottle -->
  {glass_body(392, 306, 216, 452, 30, 'amber')}
  <!-- glass dropper inside (hint) -->
  <rect x="486" y="330" width="28" height="330" rx="14" fill="#FFFFFF" opacity=".12"/>
  <!-- label -->
  {label_plate(414, 396, 172, 300, 12)}
  {lotus(500, 452, .7)}
  <text x="500" y="512" text-anchor="middle" font-family="{SERIF}" font-size="19" fill="{MUTED}">पौरुष</text>
  <text x="500" y="556" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="bold" letter-spacing="1" fill="{KUMKUM}">PAURUSH</text>
  <text x="500" y="586" text-anchor="middle" font-family="{SERIF}" font-size="24" letter-spacing="4" fill="{KUMKUM}">OIL</text>
  <rect x="446" y="602" width="108" height="2" fill="{KANCHAN}"/>
  <text x="500" y="632" text-anchor="middle" font-family="{SANS}" font-size="12.5" letter-spacing="2" fill="{MUTED}">ABHYANGA TAILA</text>
  <text x="500" y="660" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{MUTED}">30 ml</text>
  <!-- oil drop -->
  <path d="M742 700 C742 700 706 748 706 772 a36 36 0 0 0 72 0 C778 748 742 700 742 700 Z" fill="url(#drop)" opacity=".92"/>
  <ellipse cx="730" cy="762" rx="9" ry="13" fill="#FFFFFF" opacity=".45"/>
  {wordmark()}
'''
    defs += f'<linearGradient id="lidg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E7CB8B"/><stop offset=".4" stop-color="{GOLD_L}"/><stop offset=".75" stop-color="{KANCHAN}"/><stop offset="1" stop-color="#8E6819"/></linearGradient>'
    return svg('oil.svg', body, defs)

def p_kit():
    defs = f'''
  <linearGradient id="kbox" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#6F2A3E"/><stop offset=".5" stop-color="{KUMKUM}"/><stop offset="1" stop-color="#3F1420"/>
  </linearGradient>
  <linearGradient id="kjar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#7A3247"/><stop offset=".5" stop-color="{KUMKUM}"/><stop offset="1" stop-color="#3F1420"/>
  </linearGradient>
  <linearGradient id="kamb" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#B87A2E"/><stop offset=".5" stop-color="#8A5417"/><stop offset="1" stop-color="#5E3810"/>
  </linearGradient>
  <linearGradient id="kdark" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#4B3A2A"/><stop offset=".5" stop-color="#2A2018"/><stop offset="1" stop-color="#1C150F"/>
  </linearGradient>'''
    body = f'''
  {backdrop(tint=KUMKUM)}
  {eyebrow('AAROGYA · 60-DAY COMPLETE PLAN')}
  {shadow(500, 828, 300, 32)}
  <!-- keepsake box behind -->
  <rect x="236" y="330" width="528" height="452" rx="20" fill="url(#kbox)"/>
  <rect x="236" y="330" width="528" height="26" rx="12" fill="#FFFFFF" opacity=".10"/>
  <rect x="266" y="366" width="468" height="380" rx="12" fill="none" stroke="{GOLD_L}" stroke-width="1.6" opacity=".5"/>
  <text x="500" y="716" text-anchor="middle" font-family="{SANS}" font-size="14" letter-spacing="5" fill="{GOLD_L}" opacity=".85">COMPLETE CARE KIT</text>
  <!-- jar (left) -->
  <rect x="286" y="410" width="184" height="46" rx="12" fill="{KANCHAN}"/>
  <rect x="296" y="452" width="164" height="252" rx="22" fill="url(#kjar)"/>
  <rect x="306" y="464" width="16" height="226" rx="8" fill="#FFFFFF" opacity=".22"/>
  <rect x="316" y="510" width="124" height="150" rx="8" fill="{IVORY}"/>
  <text x="378" y="576" text-anchor="middle" font-family="{SERIF}" font-size="21" font-weight="bold" fill="{KUMKUM}">SHUKRA</text>
  <text x="378" y="604" text-anchor="middle" font-family="{SANS}" font-size="11" letter-spacing="2" fill="{MUTED}">60 CAPS</text>
  <!-- shilajit jar (centre, short) -->
  <rect x="452" y="500" width="130" height="38" rx="10" fill="{KANCHAN}"/>
  <rect x="458" y="534" width="118" height="170" rx="18" fill="url(#kdark)"/>
  <rect x="466" y="546" width="12" height="146" rx="6" fill="#FFFFFF" opacity=".16"/>
  <rect x="472" y="580" width="90" height="94" rx="7" fill="{IVORY}"/>
  <text x="517" y="622" text-anchor="middle" font-family="{SERIF}" font-size="15" font-weight="bold" fill="{KUMKUM}">SHILAJIT</text>
  <text x="517" y="644" text-anchor="middle" font-family="{SANS}" font-size="10" letter-spacing="1" fill="{MUTED}">20g</text>
  <!-- oil bottle (right) -->
  <rect x="596" y="452" width="96" height="56" rx="12" fill="{KANCHAN}"/>
  <rect x="602" y="504" width="84" height="200" rx="16" fill="url(#kamb)"/>
  <rect x="610" y="516" width="11" height="176" rx="5" fill="#FFFFFF" opacity=".24"/>
  <rect x="614" y="556" width="60" height="104" rx="6" fill="{IVORY}"/>
  <text x="644" y="596" text-anchor="middle" font-family="{SERIF}" font-size="12.5" font-weight="bold" fill="{KUMKUM}">PAURUSH</text>
  <text x="644" y="616" text-anchor="middle" font-family="{SANS}" font-size="9.5" fill="{MUTED}">30ml</text>
  <!-- consult card -->
  <g transform="translate(500,772) rotate(-3)">
    <rect x="-186" y="-34" width="372" height="68" rx="12" fill="{IVORY}" stroke="{KANCHAN}" stroke-width="1.6"/>
    <text x="0" y="-4" text-anchor="middle" font-family="{SERIF}" font-size="20" font-weight="bold" fill="{KUMKUM}">+ Private Doctor Consultation</text>
    <text x="0" y="20" text-anchor="middle" font-family="{SANS}" font-size="12" letter-spacing="2" fill="{MUTED}">INCLUDED · PHONE OR VIDEO</text>
  </g>
  {wordmark()}
'''
    return svg('kit.svg', body, defs)

def p_pme():
    defs = f'<linearGradient id="cover" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6F2A3E"/><stop offset=".55" stop-color="{KUMKUM}"/><stop offset="1" stop-color="#38111D"/></linearGradient>'
    # motif: 6-week progress grid
    cells = ''
    for i in range(12):
        cx = 392 + (i % 4) * 68
        cy = 330 + (i // 4) * 58
        filled = i < 7
        cells += (f'<rect x="{cx}" y="{cy}" width="48" height="40" rx="8" fill="{GOLD_L if filled else "#FFFFFF"}" opacity="{".92" if filled else ".16"}"/>')
        if filled:
            cells += f'<path d="M{cx+15} {cy+21} l7 8 12 -15" fill="none" stroke="{KUMKUM}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
    motif = f'<text x="490" y="308" text-anchor="middle" font-family="{SANS}" font-size="12.5" letter-spacing="4" fill="{GOLD_L}" opacity=".8">WEEKLY PRACTICE TRACKER</text>{cells}'
    body = f'{backdrop(tint=KUMKUM)}{eyebrow("AAROGYA · STRUCTURED COURSE")}{booklet(GOLD_L, "विराम अभ्यास", "PME COURSE", "TIMING · TECHNIQUE · TRACKING", motif)}'
    return svg('pme.svg', body, defs)

def p_ed():
    defs = f'<linearGradient id="cover" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A6B52"/><stop offset=".55" stop-color="{VANA}"/><stop offset="1" stop-color="#1C3A2B"/></linearGradient>'
    # motif: four-cause diagram
    labels = [('SLEEP', 0), ('SUGAR', 1), ('BP', 2), ('STRESS', 3)]
    icons = ''
    for name, i in labels:
        cx = 392 + i * 68 + 24
        icons += (f'<circle cx="{cx}" cy="344" r="24" fill="#FFFFFF" opacity=".14"/>'
                  f'<circle cx="{cx}" cy="344" r="24" fill="none" stroke="{GOLD_L}" stroke-width="1.6" opacity=".7"/>'
                  f'<text x="{cx}" y="392" text-anchor="middle" font-family="{SANS}" font-size="9.5" letter-spacing="1" fill="#CFE3D6">{name}</text>')
    wave = (f'<path d="M368 442 C404 412 424 472 460 442 C496 412 516 472 552 442 C588 412 600 458 618 442" '
            f'fill="none" stroke="{GOLD_L}" stroke-width="4" stroke-linecap="round" opacity=".9"/>')
    motif = (f'<text x="490" y="308" text-anchor="middle" font-family="{SANS}" font-size="12.5" letter-spacing="4" '
             f'fill="{GOLD_L}" opacity=".8">THE FOUR CAUSES</text>{icons}{wave}'
             f'<text x="490" y="484" text-anchor="middle" font-family="{SANS}" font-size="11" letter-spacing="2" fill="#CFE3D6" opacity=".85">CIRCULATION FIRST</text>')
    body = f'{backdrop(tint=VANA)}{eyebrow("AAROGYA · STRUCTURED COURSE", VANA)}{booklet(GOLD_L, "बल पुनर्स्थापन", "ED COURSE", "CAUSE-FIRST · WEEK BY WEEK", motif)}'
    return svg('ed.svg', body, defs)

def p_yoga():
    defs = f'<linearGradient id="cover" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C9A24A"/><stop offset=".5" stop-color="{KANCHAN}"/><stop offset="1" stop-color="#8E6819"/></linearGradient>'
    figure = (f'<g fill="none" stroke="{KUMKUM_D}" stroke-width="7" stroke-linecap="round" opacity=".85">'
              f'<circle cx="490" cy="322" r="21" fill="{KUMKUM_D}" stroke="none"/>'
              f'<path d="M490 346 L490 412"/><path d="M490 366 L440 396 M490 366 L540 396"/>'
              f'<path d="M490 412 C452 412 428 442 440 462 L540 462 C552 442 528 412 490 412 Z" fill="{KUMKUM_D}" stroke="none" opacity=".9"/></g>'
              f'<ellipse cx="490" cy="472" rx="118" ry="14" fill="{KUMKUM_D}" opacity=".25"/>')
    motif = (f'<text x="490" y="292" text-anchor="middle" font-family="{SANS}" font-size="12.5" letter-spacing="4" fill="{KUMKUM_D}" opacity=".75">PADMASANA</text>{figure}')
    body = f'''{backdrop(tint=KANCHAN)}{eyebrow("AAROGYA · STRUCTURED COURSE")}
  {shadow(500, 846, 205, 27, .22)}
  <rect x="316" y="238" width="372" height="516" rx="12" fill="#E4D6BC"/>
  <rect x="308" y="230" width="372" height="516" rx="12" fill="#EFE3CC"/>
  <rect x="298" y="222" width="380" height="524" rx="13" fill="url(#cover)"/>
  <rect x="298" y="222" width="22" height="524" rx="6" fill="{INK}" opacity=".18"/>
  <rect x="330" y="222" width="14" height="524" fill="#FFFFFF" opacity=".12"/>
  <rect x="356" y="270" width="266" height="412" rx="10" fill="none" stroke="{KUMKUM_D}" stroke-width="1.6" opacity=".45"/>
  {motif}
  <text x="490" y="556" text-anchor="middle" font-family="{SERIF}" font-size="26" fill="{KUMKUM_D}" opacity=".9">योग साधना</text>
  <text x="490" y="612" text-anchor="middle" font-family="{SERIF}" font-size="38" font-weight="bold" letter-spacing="1" fill="{KUMKUM_D}">YOGA FOR</text>
  <text x="490" y="652" text-anchor="middle" font-family="{SERIF}" font-size="38" font-weight="bold" letter-spacing="3" fill="{KUMKUM_D}">VITALITY</text>
  <rect x="425" y="670" width="130" height="2" fill="{KUMKUM_D}" opacity=".6"/>
  <text x="490" y="700" text-anchor="middle" font-family="{SANS}" font-size="13" letter-spacing="3" fill="{KUMKUM_D}" opacity=".8">ASANA · PRANAYAMA · SLEEP</text>
  {wordmark()}
'''
    return svg('yoga.svg', body, defs)

def p_consult():
    defs = f'''
  <linearGradient id="phone" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#3A2233"/><stop offset=".5" stop-color="{KUMKUM_D}"/><stop offset="1" stop-color="#1A0D14"/>
  </linearGradient>
  <linearGradient id="screen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{SURFACE}"/><stop offset="1" stop-color="{CHIP}"/>
  </linearGradient>'''
    body = f'''
  {backdrop(tint=GULAB)}
  {eyebrow('AAROGYA · PRIVATE CONSULTATION')}
  {shadow(500, 830, 180, 26)}
  <!-- prescription card behind -->
  <g transform="translate(672,556) rotate(9)">
    <rect x="-130" y="-176" width="260" height="352" rx="12" fill="{IVORY}" stroke="{KANCHAN}" stroke-width="1.5"/>
    <text x="0" y="-138" text-anchor="middle" font-family="{SERIF}" font-size="17" fill="{KUMKUM}">आपकी योजना</text>
    <rect x="-96" y="-120" width="192" height="2" fill="{KANCHAN}" opacity=".6"/>
    {''.join(f'<rect x="-96" y="{-98 + i*30}" width="{w}" height="9" rx="4.5" fill="{MUTED}" opacity=".3"/>' for i, w in enumerate([192, 160, 178, 130, 186, 148, 168]))}
  </g>
  <!-- phone -->
  <rect x="326" y="176" width="348" height="620" rx="46" fill="url(#phone)"/>
  <rect x="342" y="192" width="316" height="588" rx="34" fill="url(#screen)"/>
  <rect x="452" y="204" width="96" height="14" rx="7" fill="{KUMKUM_D}" opacity=".5"/>
  <!-- doctor avatar -->
  <circle cx="500" cy="316" r="66" fill="{CHIP}"/>
  <circle cx="500" cy="316" r="66" fill="none" stroke="{KANCHAN}" stroke-width="2.5"/>
  <circle cx="500" cy="296" r="24" fill="{KUMKUM}" opacity=".8"/>
  <path d="M456 366 C462 336 480 324 500 324 C520 324 538 336 544 366 Z" fill="{KUMKUM}" opacity=".8"/>
  <circle cx="546" cy="356" r="15" fill="{VANA}"/>
  <path d="M540 356 l4 5 8 -9" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="500" y="424" text-anchor="middle" font-family="{SERIF}" font-size="24" font-weight="bold" fill="{KUMKUM}">Registered doctor</text>
  <text x="500" y="452" text-anchor="middle" font-family="{SANS}" font-size="13" letter-spacing="2" fill="{MUTED}">BAMS · MD (AYURVEDA)</text>
  <!-- call chips -->
  <rect x="376" y="486" width="248" height="54" rx="27" fill="{VANA}"/>
  <text x="500" y="520" text-anchor="middle" font-family="{SANS}" font-size="15" letter-spacing="2" fill="#FFFFFF">PHONE OR VIDEO</text>
  <rect x="376" y="556" width="248" height="54" rx="27" fill="none" stroke="{KANCHAN}" stroke-width="2"/>
  <text x="500" y="590" text-anchor="middle" font-family="{SANS}" font-size="15" letter-spacing="2" fill="{KUMKUM}">100% PRIVATE</text>
  <!-- price -->
  <text x="500" y="678" text-anchor="middle" font-family="{SERIF}" font-size="62" font-weight="bold" fill="{KUMKUM}">₹99</text>
  <text x="500" y="712" text-anchor="middle" font-family="{SANS}" font-size="12.5" letter-spacing="3" fill="{MUTED}">FIRST CONSULTATION</text>
  <text x="500" y="750" text-anchor="middle" font-family="{SERIF}" font-size="16" fill="{MUTED}" opacity=".8">plan in writing within 24 hours</text>
  {wordmark()}
'''
    return svg('consult.svg', body, defs)

# =========================================================================
# AANAND — tasteful, abstract, ad-policy-safe
# =========================================================================
def aan_defs(extra=''):
    return f'''
  <linearGradient id="sil" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#D89377"/><stop offset=".22" stop-color="#C97F5E"/><stop offset=".58" stop-color="{TAMRA}"/><stop offset=".88" stop-color="#7A422E"/><stop offset="1" stop-color="#A15C42"/>
  </linearGradient>
  <linearGradient id="blush" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#F4CDD0"/><stop offset=".3" stop-color="{GULAB}"/><stop offset=".72" stop-color="#D99AA0"/><stop offset="1" stop-color="#B9787E"/>
  </linearGradient>
  <radialGradient id="softhead" cx=".38" cy=".3" r=".78">
    <stop offset="0" stop-color="#FBE3E0"/><stop offset=".55" stop-color="{GULAB}"/><stop offset="1" stop-color="#C98A90"/>
  </radialGradient>{extra}'''

def p_tarang():
    body = f'''
  {backdrop(tint=TAMRA)}
  {eyebrow('AANAND · PERSONAL WAND', TAMRA)}
  {shadow(500, 828, 120, 24)}
  <!-- handle -->
  <rect x="446" y="352" width="108" height="452" rx="54" fill="url(#sil)"/>
  <rect x="466" y="372" width="20" height="404" rx="10" fill="#FFFFFF" opacity=".26" filter="url(#soft3)"/>
  <rect x="530" y="384" width="9" height="380" rx="4.5" fill="#FFFFFF" opacity=".14"/>
  <!-- flexible neck -->
  <rect x="464" y="300" width="72" height="80" rx="36" fill="#9A5238"/>
  <!-- head -->
  <ellipse cx="500" cy="268" rx="104" ry="96" fill="url(#softhead)"/>
  <ellipse cx="466" cy="234" rx="34" ry="26" fill="#FFFFFF" opacity=".45" filter="url(#soft3)"/>
  <ellipse cx="500" cy="268" rx="104" ry="96" fill="none" stroke="#B9787E" stroke-width="2.5" opacity=".5"/>
  <!-- control -->
  <circle cx="500" cy="726" r="26" fill="{GOLD_L}"/>
  <circle cx="500" cy="726" r="26" fill="none" stroke="#8E6819" stroke-width="1.6" opacity=".6"/>
  <circle cx="500" cy="726" r="9" fill="{TAMRA_D}" opacity=".55"/>
  <!-- spec chips -->
  <g font-family="{SANS}" font-size="12.5" letter-spacing="2" fill="{MUTED}" text-anchor="middle">
    <text x="500" y="886">MEDICAL-GRADE SILICONE · WHISPER-QUIET · USB</text>
  </g>
  {wordmark(936, MUTED, .5)}
'''
    return svg('tarang.svg', body, aan_defs())

def p_bindu():
    body = f'''
  {backdrop(tint=TAMRA)}
  {eyebrow('AANAND · COMPACT MASSAGER', TAMRA)}
  {shadow(500, 800, 92, 20)}
  <!-- bullet body -->
  <path d="M500 250 C566 250 596 320 596 424 L596 700 a96 96 0 0 1 -192 0 L404 424 C404 320 434 250 500 250 Z" fill="url(#sil)"/>
  <path d="M446 300 C452 268 470 252 486 250 L486 736 C462 730 446 712 442 690 Z" fill="#FFFFFF" opacity=".24" filter="url(#soft3)"/>
  <path d="M574 330 L574 690" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity=".15"/>
  <!-- tip highlight -->
  <ellipse cx="500" cy="292" rx="58" ry="34" fill="#FFFFFF" opacity=".22" filter="url(#soft3)"/>
  <!-- base ring + button -->
  <rect x="428" y="686" width="144" height="18" rx="9" fill="{GOLD_L}" opacity=".9"/>
  <circle cx="500" cy="746" r="24" fill="{GOLD_L}"/>
  <circle cx="500" cy="746" r="8" fill="{TAMRA_D}" opacity=".5"/>
  <g font-family="{SANS}" font-size="12.5" letter-spacing="2" fill="{MUTED}" text-anchor="middle">
    <text x="500" y="880">PALM-SIZED · TRAVEL-FRIENDLY · SPLASH-PROOF</text>
  </g>
  {wordmark(930, MUTED, .5)}
'''
    return svg('bindu.svg', body, aan_defs())

def p_bandhan():
    body = f'''
  {backdrop(tint=GULAB)}
  {eyebrow('AANAND · COUPLES RING', TAMRA)}
  {shadow(500, 742, 150, 24)}
  <!-- soft ring -->
  <ellipse cx="500" cy="470" rx="196" ry="188" fill="none" stroke="url(#sil)" stroke-width="88"/>
  <ellipse cx="500" cy="470" rx="196" ry="188" fill="none" stroke="#FFFFFF" stroke-width="14" opacity=".16" transform="translate(-14,-16)"/>
  <ellipse cx="380" cy="366" rx="44" ry="26" fill="#FFFFFF" opacity=".32" filter="url(#soft3)" transform="rotate(-38 380 366)"/>
  <!-- motor bump -->
  <ellipse cx="500" cy="286" rx="86" ry="60" fill="url(#blush)"/>
  <ellipse cx="500" cy="286" rx="86" ry="60" fill="none" stroke="#B9787E" stroke-width="2" opacity=".5"/>
  <ellipse cx="474" cy="268" rx="26" ry="16" fill="#FFFFFF" opacity=".42" filter="url(#soft3)"/>
  <circle cx="500" cy="286" r="17" fill="{GOLD_L}"/>
  <g font-family="{SANS}" font-size="12.5" letter-spacing="2" fill="{MUTED}" text-anchor="middle">
    <text x="500" y="828">SOFT · STRETCHY · BODY-SAFE SILICONE</text>
  </g>
  {wordmark(884, MUTED, .5)}
'''
    return svg('bandhan.svg', body, aan_defs())

def p_yugal():
    body = f'''
  {backdrop(tint=TAMRA)}
  {eyebrow('AANAND · DUAL COUPLES MASSAGER', TAMRA)}
  {shadow(500, 800, 175, 26)}
  <!-- U-form body -->
  <path d="M370 700 C300 620 300 470 372 396 C420 346 470 340 500 372 C530 340 580 346 628 396 C700 470 700 620 630 700"
        fill="none" stroke="url(#sil)" stroke-width="96" stroke-linecap="round"/>
  <path d="M392 668 C336 600 340 486 396 428" fill="none" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round" opacity=".22"/>
  <!-- tips -->
  <ellipse cx="370" cy="700" rx="52" ry="46" fill="url(#softhead)"/>
  <ellipse cx="630" cy="700" rx="52" ry="46" fill="url(#softhead)"/>
  <ellipse cx="356" cy="688" rx="17" ry="12" fill="#FFFFFF" opacity=".42"/>
  <!-- centre control -->
  <circle cx="500" cy="404" r="34" fill="{GOLD_L}"/>
  <circle cx="500" cy="404" r="34" fill="none" stroke="#8E6819" stroke-width="1.6" opacity=".55"/>
  <circle cx="500" cy="404" r="12" fill="{TAMRA_D}" opacity=".5"/>
  <g font-family="{SANS}" font-size="12.5" letter-spacing="2" fill="{MUTED}" text-anchor="middle">
    <text x="500" y="878">FLEXIBLE · 10 MODES · WATERPROOF · FOR TWO</text>
  </g>
  {wordmark(930, MUTED, .5)}
'''
    return svg('yugal.svg', body, aan_defs())

def p_snigdha():
    defs = aan_defs(f'''
  <linearGradient id="frost" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FDF3F3"/><stop offset=".22" stop-color="#F7E4E5"/><stop offset=".6" stop-color="#EFD2D5"/><stop offset=".9" stop-color="#D9B2B6"/><stop offset="1" stop-color="#F2DEE0"/>
  </linearGradient>''')
    body = f'''
  {backdrop(tint=GULAB)}
  {eyebrow('AANAND · INTIMATE CARE', TAMRA)}
  {shadow(500, 826, 150, 24)}
  <!-- pump -->
  <rect x="452" y="150" width="96" height="30" rx="12" fill="{TAMRA_D}"/>
  <rect x="470" y="180" width="60" height="52" rx="14" fill="{TAMRA}"/>
  <rect x="486" y="232" width="28" height="42" fill="{TAMRA_D}"/>
  <rect x="440" y="266" width="120" height="34" rx="12" fill="{TAMRA}"/>
  <rect x="440" y="266" width="120" height="9" rx="4.5" fill="#FFFFFF" opacity=".26"/>
  <!-- bottle -->
  {glass_body(376, 296, 248, 470, 34, 'frost', .5)}
  {label_plate(404, 386, 192, 312, 14)}
  <g fill="none" stroke="{TAMRA}" stroke-width="4" stroke-linecap="round" opacity=".9">
    <path d="M500 470 C482 448 468 430 468 412 a32 32 0 0 1 64 0 C532 430 518 448 500 470 Z"/>
  </g>
  <text x="500" y="524" text-anchor="middle" font-family="{SERIF}" font-size="21" fill="{MUTED}">स्निग्धा</text>
  <text x="500" y="572" text-anchor="middle" font-family="{SERIF}" font-size="33" font-weight="bold" letter-spacing="1" fill="{KUMKUM}">SNIGDHA</text>
  <rect x="440" y="590" width="120" height="2" fill="{TAMRA}"/>
  <text x="500" y="620" text-anchor="middle" font-family="{SANS}" font-size="12" letter-spacing="2" fill="{MUTED}">WATER-BASED GEL</text>
  <text x="500" y="646" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{VANA}">pH-balanced · condom-safe</text>
  <text x="500" y="672" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}">100 ml</text>
  <g font-family="{SANS}" font-size="12" letter-spacing="2" fill="{MUTED}" text-anchor="middle">
    <text x="500" y="884">NO PARABENS · NO GLYCERIN · DERMATOLOGICALLY TESTED</text>
  </g>
  {wordmark(936, MUTED, .5)}
'''
    return svg('snigdha.svg', body, defs)

def p_sparsh():
    defs = aan_defs(f'''
  <linearGradient id="oilb" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#E8B98A"/><stop offset=".22" stop-color="#D69C63"/><stop offset=".6" stop-color="#B87A46"/><stop offset=".9" stop-color="#8A5730"/><stop offset="1" stop-color="#C08A57"/>
  </linearGradient>
  <linearGradient id="wood" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#B9895C"/><stop offset=".45" stop-color="#96693F"/><stop offset="1" stop-color="#6D4A2B"/>
  </linearGradient>''')
    body = f'''
  {backdrop(tint=TAMRA)}
  {eyebrow('AANAND · SENSUAL MASSAGE OIL', TAMRA)}
  {shadow(500, 826, 158, 25)}
  <!-- wooden cap -->
  <rect x="428" y="186" width="144" height="92" rx="14" fill="url(#wood)"/>
  <rect x="428" y="186" width="144" height="13" rx="6" fill="#FFFFFF" opacity=".2"/>
  <g stroke="#6D4A2B" stroke-width="1.5" opacity=".35">
    {''.join(f'<line x1="{x}" y1="196" x2="{x}" y2="270"/>' for x in range(440, 566, 14))}
  </g>
  <rect x="452" y="278" width="96" height="26" fill="#8A5730"/>
  <!-- bottle -->
  {glass_body(384, 300, 232, 466, 30, 'oilb')}
  {label_plate(412, 394, 176, 306, 12)}
  <g fill="none" stroke="{TAMRA}" stroke-width="3.6" stroke-linecap="round" opacity=".9">
    <path d="M500 462 C482 448 470 428 476 410 C490 418 496 430 500 444 C504 430 510 418 524 410 C530 428 518 448 500 462 Z"/>
  </g>
  <text x="500" y="518" text-anchor="middle" font-family="{SERIF}" font-size="20" fill="{MUTED}">स्पर्श</text>
  <text x="500" y="564" text-anchor="middle" font-family="{SERIF}" font-size="32" font-weight="bold" letter-spacing="1" fill="{KUMKUM}">SPARSH</text>
  <rect x="446" y="582" width="108" height="2" fill="{TAMRA}"/>
  <text x="500" y="612" text-anchor="middle" font-family="{SANS}" font-size="11.5" letter-spacing="2" fill="{MUTED}">MASSAGE OIL</text>
  <text x="500" y="638" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{MUTED}">almond · classical herbs</text>
  <text x="500" y="666" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}">100 ml</text>
  <g font-family="{SANS}" font-size="12" letter-spacing="2" fill="{MUTED}" text-anchor="middle">
    <text x="500" y="884">WARMING · SLOW · FOR SHARED RITUAL</text>
  </g>
  {wordmark(936, MUTED, .5)}
'''
    return svg('sparsh.svg', body, defs)

def p_jyoti():
    defs = aan_defs(f'''
  <linearGradient id="tin" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#E2C79A"/><stop offset=".2" stop-color="#CBAA76"/><stop offset=".55" stop-color="#A8834F"/><stop offset=".85" stop-color="#7C5E36"/><stop offset="1" stop-color="#BE9C68"/>
  </linearGradient>
  <radialGradient id="flame" cx=".5" cy=".7" r=".7">
    <stop offset="0" stop-color="#FFF6D8"/><stop offset=".45" stop-color="{GOLD_L}"/><stop offset="1" stop-color="#E08A20" stop-opacity=".2"/>
  </radialGradient>
  <radialGradient id="wax" cx=".4" cy=".3" r=".8">
    <stop offset="0" stop-color="#FBEEDC"/><stop offset="1" stop-color="#E8D2AE"/>
  </radialGradient>''')
    body = f'''
  {backdrop(tint=GOLD_L)}
  {eyebrow('AANAND · MASSAGE CANDLE', TAMRA)}
  <!-- ambient glow -->
  <circle cx="500" cy="380" r="180" fill="{GOLD_L}" opacity=".30" filter="url(#glowf)"/>
  {shadow(500, 790, 175, 26)}
  <!-- flame -->
  <ellipse cx="500" cy="330" rx="34" ry="62" fill="url(#flame)" opacity=".9"/>
  <path d="M500 268 C520 306 528 330 520 352 C512 372 488 372 480 352 C472 330 480 306 500 268 Z" fill="{GOLD_L}"/>
  <path d="M500 300 C510 326 512 342 506 354 C500 366 490 362 488 350 C486 336 492 320 500 300 Z" fill="#FFF6D8"/>
  <rect x="496" y="386" width="8" height="34" rx="4" fill="#5A4527"/>
  <!-- wax surface -->
  <ellipse cx="500" cy="430" rx="176" ry="42" fill="url(#wax)"/>
  <ellipse cx="500" cy="430" rx="176" ry="42" fill="none" stroke="#C9A97A" stroke-width="2" opacity=".6"/>
  <ellipse cx="500" cy="432" rx="60" ry="16" fill="#E6C88F" opacity=".7"/>
  <!-- tin -->
  <path d="M324 430 L324 700 a176 60 0 0 0 352 0 L676 430" fill="url(#tin)"/>
  <rect x="344" y="452" width="26" height="234" rx="13" fill="#FFFFFF" opacity=".22" filter="url(#soft3)"/>
  <path d="M324 430 a176 42 0 0 0 352 0" fill="none" stroke="#7C5E36" stroke-width="3" opacity=".4"/>
  {label_plate(392, 508, 216, 158, 12)}
  <text x="500" y="552" text-anchor="middle" font-family="{SERIF}" font-size="20" fill="{MUTED}">ज्योति</text>
  <text x="500" y="598" text-anchor="middle" font-family="{SERIF}" font-size="34" font-weight="bold" letter-spacing="2" fill="{KUMKUM}">JYOTI</text>
  <rect x="446" y="614" width="108" height="2" fill="{TAMRA}"/>
  <text x="500" y="640" text-anchor="middle" font-family="{SANS}" font-size="11" letter-spacing="1.5" fill="{MUTED}">SOY MASSAGE CANDLE</text>
  <text x="500" y="660" text-anchor="middle" font-family="{SANS}" font-size="11" letter-spacing="1.5" fill="{MUTED}">120 g</text>
  <g font-family="{SANS}" font-size="12" letter-spacing="2" fill="{MUTED}" text-anchor="middle">
    <text x="500" y="864">MELTS INTO A WARM MASSAGE OIL</text>
  </g>
  {wordmark(918, MUTED, .5)}
'''
    return svg('jyoti.svg', body, defs)

def p_milan():
    defs = aan_defs(f'''
  <linearGradient id="boxo" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#A85636"/><stop offset=".5" stop-color="{TAMRA_D}"/><stop offset="1" stop-color="#5A2F20"/>
  </linearGradient>
  <linearGradient id="boxi" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#F6E2DC"/><stop offset="1" stop-color="#E8C9C2"/>
  </linearGradient>''')
    body = f'''
  {backdrop(tint=TAMRA)}
  {eyebrow('AANAND · COUPLES STARTER BOX', TAMRA)}
  {shadow(500, 812, 275, 30)}
  <!-- lid, leaning behind -->
  <g transform="translate(742,392) rotate(11)">
    <rect x="-150" y="-186" width="300" height="330" rx="16" fill="url(#boxo)"/>
    <rect x="-150" y="-186" width="300" height="18" rx="9" fill="#FFFFFF" opacity=".12"/>
    <rect x="-118" y="-152" width="236" height="262" rx="10" fill="none" stroke="{GULAB}" stroke-width="1.6" opacity=".7"/>
    <text x="0" y="-40" text-anchor="middle" font-family="{SERIF}" font-size="34" fill="{GULAB}">मिलन</text>
    <text x="0" y="10" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="bold" letter-spacing="3" fill="#F6E2DC">MILAN</text>
    <text x="0" y="44" text-anchor="middle" font-family="{SANS}" font-size="11.5" letter-spacing="3" fill="{GULAB}">COUPLES KIT</text>
  </g>
  <!-- open base box -->
  <path d="M212 500 L788 500 L744 780 L256 780 Z" fill="url(#boxo)"/>
  <rect x="212" y="470" width="576" height="46" rx="10" fill="#C4704E"/>
  <path d="M240 516 L760 516 L724 756 L276 756 Z" fill="url(#boxi)"/>
  <!-- contents nested in compartments -->
  <g>
    <!-- bullet -->
    <path d="M352 566 C376 566 388 592 388 630 L388 704 a36 36 0 0 1 -72 0 L316 630 C316 592 328 566 352 566 Z" fill="url(#sil)"/>
    <path d="M330 586 C334 574 342 568 348 566 L348 726 C338 722 330 714 328 702 Z" fill="#FFFFFF" opacity=".22"/>
    <!-- ring -->
    <ellipse cx="470" cy="656" rx="62" ry="58" fill="none" stroke="url(#sil)" stroke-width="30"/>
    <ellipse cx="470" cy="612" rx="26" ry="18" fill="url(#blush)"/>
    <!-- gel bottle -->
    <rect x="546" y="596" width="70" height="126" rx="16" fill="#F7E4E5"/>
    <rect x="556" y="608" width="9" height="100" rx="4.5" fill="#FFFFFF" opacity=".7"/>
    <rect x="562" y="566" width="38" height="34" rx="10" fill="{TAMRA}"/>
    <rect x="556" y="636" width="50" height="52" rx="6" fill="{IVORY}"/>
    <text x="581" y="668" text-anchor="middle" font-family="{SERIF}" font-size="12" font-weight="bold" fill="{KUMKUM}">SNIGDHA</text>
    <!-- cards -->
    <g transform="translate(672,660) rotate(-8)">
      <rect x="-46" y="-64" width="92" height="128" rx="9" fill="{KUMKUM}"/>
      <rect x="-38" y="-56" width="76" height="112" rx="6" fill="none" stroke="{GOLD_L}" stroke-width="1.4" opacity=".8"/>
      <text x="0" y="8" text-anchor="middle" font-family="{SERIF}" font-size="15" fill="{GOLD_L}">खुली</text>
      <text x="0" y="30" text-anchor="middle" font-family="{SERIF}" font-size="15" fill="{GOLD_L}">बात</text>
    </g>
  </g>
  <g font-family="{SANS}" font-size="12.5" letter-spacing="2" fill="{MUTED}" text-anchor="middle">
    <text x="500" y="882">BINDU · BANDHAN · SNIGDHA · KHULI BAAT — IN A KEEPSAKE BOX</text>
  </g>
  {wordmark(934, MUTED, .5)}
'''
    return svg('milan-kit.svg', body, defs)

def p_khulibaat():
    defs = f'''
  <linearGradient id="cardb" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#6F2A3E"/><stop offset=".55" stop-color="{KUMKUM}"/><stop offset="1" stop-color="#38111D"/>
  </linearGradient>'''
    fan = ''
    for i, ang in enumerate([-26, -13, 0, 13, 26]):
        dx = ang * 5.6
        fan += (f'<g transform="translate({500+dx},520) rotate({ang})">'
                f'<rect x="-104" y="-152" width="208" height="304" rx="16" fill="{IVORY}" stroke="{KANCHAN}" stroke-width="1.6"/>'
                f'<rect x="-88" y="-136" width="176" height="272" rx="10" fill="none" stroke="{KANCHAN}" stroke-width="1" opacity=".45"/>'
                f'<text x="0" y="-84" text-anchor="middle" font-family="{SANS}" font-size="10.5" letter-spacing="3" fill="{MUTED}">LEVEL {i+1}</text>'
                f'<text x="0" y="6" text-anchor="middle" font-family="{SERIF}" font-size="62" fill="{KANCHAN}" opacity=".5">?</text>'
                + ''.join(f'<rect x="-64" y="{40 + j*22}" width="{w}" height="8" rx="4" fill="{MUTED}" opacity=".26"/>' for j, w in enumerate([128, 104, 116]))
                + '</g>')
    body = f'''
  {backdrop(tint=KUMKUM)}
  {eyebrow('AANAND · INTIMACY CARD GAME')}
  {shadow(500, 806, 250, 28)}
  {fan}
  <!-- deck box in front -->
  <g transform="translate(500,724)">
    <rect x="-172" y="-92" width="344" height="184" rx="16" fill="url(#cardb)"/>
    <rect x="-172" y="-92" width="344" height="16" rx="8" fill="#FFFFFF" opacity=".12"/>
    <rect x="-146" y="-66" width="292" height="132" rx="10" fill="none" stroke="{GOLD_L}" stroke-width="1.5" opacity=".6"/>
    <text x="0" y="-14" text-anchor="middle" font-family="{SERIF}" font-size="36" fill="{GOLD_L}">खुली बात</text>
    <text x="0" y="26" text-anchor="middle" font-family="{SERIF}" font-size="27" font-weight="bold" letter-spacing="3" fill="{IVORY}">KHULI BAAT</text>
    <text x="0" y="56" text-anchor="middle" font-family="{SANS}" font-size="11.5" letter-spacing="3" fill="{GULAB}">100 CARDS FOR COUPLES</text>
  </g>
  {wordmark(908, MUTED, .5)}
'''
    return svg('khuli-baat.svg', body, defs)

# =========================================================================
# PDP detail thumbnails (t-*.svg) — same studio system, simpler subjects
# =========================================================================
def thumb(name, subject, caption, tint=KANCHAN, defs=''):
    body = f'''
  {backdrop(rings=False, tint=tint)}
  {subject}
  <text x="500" y="906" text-anchor="middle" font-family="{SANS}" font-size="30" letter-spacing="4" fill="{MUTED}">{caption}</text>
'''
    return svg(name, body, defs)

def thumbs():
    made = []
    # herb / botanical source
    leaf = ''.join(
        f'<g transform="translate(500,470) rotate({a})"><path d="M0 -30 C58 -96 122 -84 158 -34 C112 26 44 22 0 -30 Z" '
        f'fill="{VANA}" opacity="{op}"/><path d="M6 -28 C58 -60 106 -56 140 -34" fill="none" stroke="#EAF3EC" '
        f'stroke-width="3" opacity=".4"/></g>'
        for a, op in [(-52, .95), (8, .8), (64, .65), (128, .5), (196, .75), (256, .6)])
    made.append(thumb('t-herb.svg', f'{leaf}<circle cx="500" cy="470" r="34" fill="{GOLD_L}"/>'
                                    f'<circle cx="500" cy="470" r="34" fill="none" stroke="#8E6819" stroke-width="2" opacity=".5"/>',
                      'BOTANICAL SOURCE', VANA))
    # lab report
    lab = f'''
  {shadow(500, 792, 190, 24, .18)}
  <rect x="322" y="212" width="356" height="470" rx="14" fill="{IVORY}" stroke="{KANCHAN}" stroke-width="2"/>
  <text x="500" y="282" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="bold" fill="{KUMKUM}">LAB REPORT</text>
  <rect x="382" y="302" width="236" height="2" fill="{KANCHAN}"/>
  {''.join(f'<rect x="368" y="{334 + i*40}" width="{w}" height="11" rx="5.5" fill="{MUTED}" opacity=".28"/>' for i, w in enumerate([264, 210, 244, 176, 252, 198]))}
  <circle cx="500" cy="600" r="52" fill="none" stroke="{VANA}" stroke-width="5"/>
  <path d="M474 600 l18 20 34 -42" fill="none" stroke="{VANA}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- flask -->
  <g transform="translate(700,660)">
    <path d="M-16 -110 L-16 -34 L-56 46 a26 26 0 0 0 22 40 L34 86 a26 26 0 0 0 22 -40 L16 -34 L16 -110 Z" fill="#FFFFFF" opacity=".8" stroke="{KANCHAN}" stroke-width="3"/>
    <path d="M-44 30 L44 30 a26 26 0 0 1 -10 56 L-34 86 a26 26 0 0 1 -10 -56 Z" fill="{VANA}" opacity=".6"/>
  </g>'''
    made.append(thumb('t-lab.svg', lab, 'BATCH LAB-TESTED'))
    # dosage
    dose = f'''
  {shadow(500, 720, 190, 24, .18)}
  <circle cx="500" cy="440" r="190" fill="{SURFACE}" stroke="{KANCHAN}" stroke-width="3"/>
  <circle cx="500" cy="440" r="150" fill="none" stroke="{KANCHAN}" stroke-width="1.5" opacity=".4"/>
  {capsule(440, 400, -18)}{capsule(560, 470, 12)}
  <text x="500" y="600" text-anchor="middle" font-family="{SERIF}" font-size="34" font-weight="bold" fill="{KUMKUM}">2 capsules</text>
  <text x="500" y="644" text-anchor="middle" font-family="{SANS}" font-size="22" letter-spacing="2" fill="{MUTED}">twice daily · after meals</text>'''
    made.append(thumb('t-dose.svg', dose, 'HOW TO TAKE'))
    # plain parcel
    parcel = f'''
  {shadow(500, 750, 210, 26, .2)}
  <path d="M258 356 L500 268 L742 356 L742 700 L500 788 L258 700 Z" fill="#C9A87E"/>
  <path d="M500 268 L742 356 L500 444 L258 356 Z" fill="#D8BA92"/>
  <path d="M500 444 L742 356 L742 700 L500 788 Z" fill="#B0906A"/>
  <path d="M500 444 L500 788" stroke="#8E7250" stroke-width="3" opacity=".5"/>
  <rect x="470" y="300" width="60" height="480" fill="{IVORY}" opacity=".55" transform="skewY(-20) translate(0,96)"/>
  <rect x="352" y="512" width="150" height="86" rx="6" fill="{IVORY}" opacity=".9" transform="skewY(20) translate(0,-88)"/>
  <text x="500" y="640" text-anchor="middle" font-family="{SANS}" font-size="24" letter-spacing="2" fill="{KUMKUM}" opacity=".75">no product name</text>'''
    made.append(thumb('t-parcel.svg', parcel, 'PLAIN PARCEL', TAMRA))
    # material (aanand)
    mat = f'''
  {shadow(500, 736, 170, 24, .18)}
  <circle cx="500" cy="446" r="178" fill="url(#softhead)"/>
  <circle cx="500" cy="446" r="178" fill="none" stroke="#B9787E" stroke-width="3" opacity=".5"/>
  <ellipse cx="440" cy="386" rx="52" ry="34" fill="#FFFFFF" opacity=".45" filter="url(#soft3)"/>
  <text x="500" y="438" text-anchor="middle" font-family="{SERIF}" font-size="40" font-weight="bold" fill="{KUMKUM}">100%</text>
  <text x="500" y="486" text-anchor="middle" font-family="{SANS}" font-size="22" letter-spacing="2" fill="{KUMKUM}">body-safe</text>
  <text x="500" y="662" text-anchor="middle" font-family="{SANS}" font-size="24" fill="{MUTED}">phthalate- &amp; BPA-free</text>'''
    made.append(thumb('t-material.svg', mat, 'MEDICAL-GRADE SILICONE', TAMRA, aan_defs()))
    # charging
    chg = f'''
  {shadow(500, 740, 170, 24, .18)}
  <rect x="336" y="352" width="328" height="188" rx="34" fill="none" stroke="{TAMRA}" stroke-width="12"/>
  <rect x="672" y="418" width="26" height="56" rx="10" fill="{TAMRA}"/>
  <rect x="362" y="378" width="180" height="136" rx="18" fill="{VANA}"/>
  <path d="M534 372 L470 462 L516 462 L482 546 L560 442 L512 442 Z" fill="{GOLD_L}" stroke="{IVORY}" stroke-width="4" stroke-linejoin="round"/>
  <text x="500" y="646" text-anchor="middle" font-family="{SANS}" font-size="24" fill="{MUTED}">USB-C · up to 2 hours</text>'''
    made.append(thumb('t-charge.svg', chg, 'RECHARGEABLE', TAMRA))
    # cleaning
    clean = f'''
  {shadow(500, 744, 170, 24, .18)}
  <path d="M500 262 C500 262 372 404 372 486 a128 128 0 0 0 256 0 C628 404 500 262 500 262 Z" fill="#A9CFE0" opacity=".85"/>
  <path d="M452 424 C440 452 438 480 446 502" fill="none" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round" opacity=".6"/>
  <circle cx="662" cy="330" r="34" fill="#A9CFE0" opacity=".55"/>
  <circle cx="716" cy="404" r="20" fill="#A9CFE0" opacity=".4"/>
  <text x="500" y="662" text-anchor="middle" font-family="{SANS}" font-size="24" fill="{MUTED}">warm water · mild soap · air-dry</text>'''
    made.append(thumb('t-clean.svg', clean, 'EASY TO CLEAN', '#A9CFE0'))
    return made

if __name__ == '__main__':
    made = []
    for fn in (p_shukra, p_shilajit, p_oil, p_kit, p_pme, p_ed, p_yoga, p_consult,
               p_tarang, p_bindu, p_bandhan, p_yugal, p_snigdha, p_sparsh, p_jyoti,
               p_milan, p_khulibaat):
        r = fn()
        made.extend(r if isinstance(r, tuple) else [r])
    made.extend(thumbs())
    print('wrote %d files:' % len(made))
    print(' ' + ' '.join(made))
