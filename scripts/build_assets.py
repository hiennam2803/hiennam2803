"""Sinh các SVG trang trí cho profile README (chạy: python scripts/build_assets.py)."""
import os, random
from html import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

V, T, B = "#A78BFA", "#36D6C5", "#7C9CFF"
BG, PANEL, TXT, MUT, LINE = "#0D1117", "#161B22", "#E6EDF3", "#8B949E", "#30363D"
SERIF = "Georgia,'Times New Roman',serif"
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
HAND = "'Segoe Print','Bradley Hand','Comic Sans MS',cursive"


def save(name, w, h, body, title):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">'
           f'<title id="t">{escape(title)}</title>{body}</svg>')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def card(w, h, r=24):
    return f'<rect width="{w}" height="{h}" rx="{r}" fill="{BG}"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{LINE}"/>'


def grid(w, h, step=40, op=".05"):
    return (f'<pattern id="gr" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<path d="M{step} 0H0V{step}" fill="none" stroke="#fff" stroke-opacity="{op}"/></pattern>'
            f'<rect width="{w}" height="{h}" fill="url(#gr)"/>')


def glow(i, color, op=".5"):
    return (f'<radialGradient id="{i}"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')


# ───────────────────────── HERO ─────────────────────────
def hero():
    w, h = 1000, 460
    body = f'''<defs>{glow("g1", V, ".55")}{glow("g2", T, ".35")}{glow("g3", B, ".4")}
<linearGradient id="name" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">
<animate attributeName="x1" values="0;-1;0" dur="9s" repeatCount="indefinite"/>
<animate attributeName="x2" values="1;0;1" dur="9s" repeatCount="indefinite"/>
<stop offset="0" stop-color="{V}"/><stop offset=".5" stop-color="{B}"/><stop offset="1" stop-color="{T}"/></linearGradient>
<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{V}"/><stop offset="1" stop-color="{T}"/></linearGradient>
<clipPath id="c"><rect width="{w}" height="{h}" rx="24"/></clipPath>
<path id="ring" d="M 0,-118 a118,118 0 1,1 0,236 a118,118 0 1,1 0,-236"/></defs>
<g clip-path="url(#c)">{card(w, h)}{grid(w, h)}
<circle cx="180" cy="120" r="260" fill="url(#g1)"><animate attributeName="cx" values="180;320;180" dur="12s" repeatCount="indefinite"/></circle>
<circle cx="860" cy="400" r="240" fill="url(#g2)"><animate attributeName="cy" values="400;300;400" dur="10s" repeatCount="indefinite"/></circle>
<circle cx="640" cy="40" r="180" fill="url(#g3)"><animate attributeName="r" values="180;220;180" dur="8s" repeatCount="indefinite"/></circle>
<line x1="60" y1="84" x2="940" y2="84" stroke="{LINE}"/><line x1="60" y1="388" x2="940" y2="388" stroke="{LINE}"/>
<text x="60" y="64" font-family="{MONO}" font-size="19" letter-spacing="5" fill="{MUT}">ẤN BẢN CÁ NHÂN</text>
<text x="940" y="64" font-family="{MONO}" font-size="19" letter-spacing="5" fill="{MUT}" text-anchor="end">Nº 01 · 2026</text>
<text x="52" y="300" font-family="{SERIF}" font-size="230" font-style="italic" font-weight="700" fill="url(#name)" letter-spacing="-6">Hiền.</text>
<text x="64" y="352" font-family="{SANS}" font-size="26" letter-spacing="12" font-weight="600" fill="{TXT}">VÕ VĂN HIỀN</text>
<g transform="translate(790 236)">
<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="40s" repeatCount="indefinite"/>
<circle r="118" fill="none" stroke="{V}" stroke-opacity=".35" stroke-dasharray="2 8"/>
<text font-family="{MONO}" font-size="17" fill="{T}"><textPath href="#ring" startOffset="0" textLength="728" lengthAdjust="spacing">BUILD · BREAK · DEBUG · IMPROVE · BUILD · BREAK · DEBUG · IMPROVE ·</textPath></text></g>
<circle r="62" fill="none" stroke="{LINE}"/><circle r="8" fill="{T}"><animate attributeName="r" values="6;11;6" dur="2.4s" repeatCount="indefinite"/></circle>
</g>
<text x="60" y="428" font-family="{SERIF}" font-size="27" font-style="italic" fill="{TXT}">Tôi tạo ra sản phẩm công nghệ, đôi khi tạo luôn sự cố.</text>
<rect x="60" y="440" width="120" height="3" rx="1.5" fill="url(#bar)"><animate attributeName="width" values="40;260;40" dur="6s" repeatCount="indefinite"/></rect>
<text x="940" y="428" font-family="{MONO}" font-size="19" fill="{MUT}" text-anchor="end">TP. Hồ Chí Minh</text>
</g>'''
    save("hero.svg", w, h, body, "Bìa tạp chí cá nhân: Hiền. Võ Văn Hiền. Tôi tạo ra sản phẩm công nghệ, đôi khi tạo luôn sự cố.")


# ───────────────────── SECTION TITLES ─────────────────────
def section(n, title, sub, color):
    w, h = 1000, 120
    body = f'''<defs><linearGradient id="u" x1="0" x2="1"><stop offset="0" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect width="{w}" height="{h}" rx="20"/></clipPath></defs>
<g clip-path="url(#c)">{card(w, h, 20)}
<text x="36" y="98" font-family="{SERIF}" font-size="118" font-weight="700" fill="none" stroke="{color}" stroke-opacity=".5" stroke-width="1.5">{n}</text>
<text x="210" y="62" font-family="{SERIF}" font-size="44" font-style="italic" fill="{TXT}">{escape(title)}</text>
<text x="212" y="92" font-family="{MONO}" font-size="19" letter-spacing="3" fill="{MUT}">{escape(sub)}</text>
<rect x="210" y="108" width="200" height="3" rx="1.5" fill="url(#u)"><animate attributeName="width" values="60;780;60" dur="7s" repeatCount="indefinite"/></rect>
<circle cx="950" cy="60" r="7" fill="{color}"><animate attributeName="opacity" values="1;.2;1" dur="3s" repeatCount="indefinite"/></circle></g>'''
    save(f"sec-{n}.svg", w, h, body, f"Mục {n}: {title}")


# ───────────────────── INTERESTS ─────────────────────
def interests():
    w, h = 1000, 380
    items = [
        (f'<text x="40" y="190" font-family="{SERIF}" font-size="190" font-weight="700" font-style="italic" fill="none" stroke="{V}" stroke-width="2">AI</text>', 7),
        (f'<text x="330" y="96" font-family="{SERIF}" font-size="46" font-style="italic" fill="{TXT}">Sản phẩm dùng được thật</text>', 6),
        (f'<text x="332" y="140" font-family="{MONO}" font-size="22" letter-spacing="2" fill="{T}">→ không chỉ chạy được trong demo</text>', 8),
        (f'<text x="330" y="212" font-family="{SANS}" font-size="52" font-weight="800" fill="{B}">Android</text>', 9),
        (f'<text x="580" y="212" font-family="{SANS}" font-size="46" font-weight="300" fill="{TXT}">Desktop</text>', 7),
        (f'<text x="800" y="212" font-family="{SERIF}" font-size="52" font-style="italic" fill="{V}">Web</text>', 8),
        (f'<text x="40" y="300" font-family="{SERIF}" font-size="40" font-style="italic" fill="{TXT}">Công cụ chạy ngay trên máy mình</text>', 6),
        (f'<text x="40" y="346" font-family="{MONO}" font-size="22" letter-spacing="2" fill="{MUT}">DEBUG LÚC 2 GIỜ SÁNG · ỨNG DỤNG CHO ĐỜI THƯỜNG</text>', 9),
    ]
    g = ""
    for i, (el, d) in enumerate(items):
        g += (f'<g>{el}<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="{d}s" begin="-{i}s" repeatCount="indefinite"/></g>')
    body = f'''<defs>{glow("a", V, ".28")}{glow("b", T, ".22")}<clipPath id="c"><rect width="{w}" height="{h}" rx="24"/></clipPath></defs>
<g clip-path="url(#c)">{card(w, h)}<circle cx="880" cy="60" r="220" fill="url(#a)"/><circle cx="120" cy="380" r="200" fill="url(#b)"/>{g}</g>'''
    save("interests.svg", w, h, body, "Điều mình quan tâm: AI, sản phẩm dùng được thật, Android, Desktop, Web, công cụ chạy ngay trên máy, debug lúc 2 giờ sáng")


# ───────────────────── TIMELINE ─────────────────────
def timeline():
    w, h = 1000, 400
    nodes = [
        (130, "HIỆN TẠI", "Sinh viên CNTT", "ĐH GTVT TP.HCM", V),
        (315, "2025", "Salud", "App Android sức khỏe", T),
        (500, "2026", "WIIS", "Lịch học cho sinh viên", B),
        (685, "2026", "C.I.R.C.A · VYRON", "Desktop AI · Chrome", V),
        (870, "TIẾP THEO", "Full-stack", "Dev trọn vẹn", T),
    ]
    g = ""
    for i, (x, k, t, s_, c) in enumerate(nodes):
        up = i % 2 == 0
        y0 = 78 if up else 258
        l1, l2 = (y0 + 76, 187) if up else (213, y0 - 28)
        g += f'''<line x1="{x}" y1="{l1}" x2="{x}" y2="{l2}" stroke="{c}" stroke-opacity=".5" stroke-dasharray="3 5"/>
<circle cx="{x}" cy="200" r="11" fill="{BG}" stroke="{c}" stroke-width="3"/><circle cx="{x}" cy="200" r="4" fill="{c}"><animate attributeName="opacity" values="1;.2;1" dur="3s" begin="-{i*.6}s" repeatCount="indefinite"/></circle>
<text x="{x}" y="{y0}" font-family="{MONO}" font-size="19" letter-spacing="3" fill="{c}" text-anchor="middle">{k}</text>
<text x="{x}" y="{y0+34}" font-family="{SERIF}" font-size="{26 if len(t) < 14 else 22}" font-style="italic" fill="{TXT}" text-anchor="middle">{escape(t)}</text>
<text x="{x}" y="{y0+64}" font-family="{SANS}" font-size="18" fill="{MUT}" text-anchor="middle">{escape(s_)}</text>'''
    body = f'''<defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{V}"/><stop offset=".5" stop-color="{B}"/><stop offset="1" stop-color="{T}"/></linearGradient>
<clipPath id="c"><rect width="{w}" height="{h}" rx="24"/></clipPath></defs>
<g clip-path="url(#c)">{card(w, h)}{grid(w, h)}
<line x1="40" y1="200" x2="960" y2="200" stroke="url(#l)" stroke-width="3" stroke-linecap="round"/>
<circle r="6" cy="200" fill="#fff"><animate attributeName="cx" values="40;960" dur="9s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" dur="9s" repeatCount="indefinite"/></circle>
{g}</g>'''
    save("timeline.svg", w, h, body, "Hành trình: sinh viên CNTT, Salud 2025, WIIS 2026, C.I.R.C.A và VYRON 2026, tiếp theo là Full-stack Developer")


# ───────────────────── PROJECT POSTERS ─────────────────────
def poster(name, label, num, color, art, w=520, h=340):
    body = f'''<defs>{glow("pg", color, ".45")}<clipPath id="c"><rect width="{w}" height="{h}" rx="22"/></clipPath></defs>
<g clip-path="url(#c)">{card(w, h, 22)}{grid(w, h, 34, ".04")}<circle cx="{w-60}" cy="40" r="200" fill="url(#pg)"/>
<text x="26" y="48" font-family="{MONO}" font-size="16" letter-spacing="4" fill="{MUT}">DỰ ÁN {num}</text>
{art}
<text x="26" y="{h-26}" font-family="{SERIF}" font-size="50" font-style="italic" font-weight="700" fill="{TXT}">{escape(label)}</text></g>'''
    save(f"project-{name}.svg", w, h, body, f"Poster dự án {label}")


def art_vyron():
    bars = ""
    random.seed(7)
    for i in range(31):
        hh = random.randint(24, 92)
        bars += (f'<rect x="{34 + i*14}" y="{196 - hh/2}" width="7" height="{hh}" rx="3.5" fill="{T if i % 3 else V}" fill-opacity=".85">'
                 f'<animate attributeName="height" values="{hh};{hh*.3:.0f};{hh}" dur="{1.1 + (i % 5) * .22:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{196 - hh/2};{196 - hh*.15:.0f};{196 - hh/2}" dur="{1.1 + (i % 5) * .22:.2f}s" repeatCount="indefinite"/></rect>')
    return (f'<rect x="26" y="70" width="468" height="72" rx="10" fill="{PANEL}" stroke="{LINE}"/>'
            f'<rect x="44" y="90" width="260" height="8" rx="4" fill="{MUT}" fill-opacity=".5"/><rect x="44" y="110" width="170" height="8" rx="4" fill="{T}"><animate attributeName="width" values="40;330;40" dur="5s" repeatCount="indefinite"/></rect>'
            f'<polygon points="446,92 446,122 470,107" fill="{V}"/>{bars}')


def art_circa():
    wins = ""
    for i, (x, y, n, c) in enumerate([(34, 72, "ChatGPT", T), (34, 128, "Claude", V), (34, 184, "Gemini", B)]):
        wins += (f'<rect x="{x}" y="{y}" width="130" height="46" rx="10" fill="{PANEL}" stroke="{c}" stroke-opacity=".6"/>'
                 f'<text x="{x+65}" y="{y+29}" font-family="{MONO}" font-size="17" fill="{c}" text-anchor="middle">{n}</text>'
                 f'<path d="M{x+130} {y+23} C 230 {y+23}, 250 150, 300 150" fill="none" stroke="{c}" stroke-opacity=".6" stroke-dasharray="4 6"><animate attributeName="stroke-dashoffset" values="0;-40" dur="2s" repeatCount="indefinite"/></path>')
    return (wins + f'<rect x="300" y="86" width="190" height="130" rx="14" fill="{PANEL}" stroke="{V}"/>'
            f'<rect x="300" y="86" width="190" height="26" rx="14" fill="{V}" fill-opacity=".25"/>'
            f'<rect x="316" y="132" width="100" height="8" rx="4" fill="{MUT}" fill-opacity=".6"/><rect x="316" y="152" width="150" height="8" rx="4" fill="{MUT}" fill-opacity=".4"/>'
            f'<rect x="316" y="176" width="70" height="22" rx="11" fill="{T}" fill-opacity=".9"><animate attributeName="opacity" values="1;.4;1" dur="2.4s" repeatCount="indefinite"/></rect>'
            f'<text x="351" y="192" font-family="{MONO}" font-size="12" fill="{BG}" text-anchor="middle" font-weight="700">PINNED</text>')


def art_salud():
    return (f'<circle cx="400" cy="150" r="52" fill="none" stroke="{LINE}" stroke-width="12"/>'
            f'<circle cx="400" cy="150" r="52" fill="none" stroke="{T}" stroke-width="12" stroke-linecap="round" stroke-dasharray="327" stroke-dashoffset="327" transform="rotate(-90 400 150)">'
            f'<animate attributeName="stroke-dashoffset" values="327;90;327" dur="6s" repeatCount="indefinite"/></circle>'
            f'<path d="M30 190 H100 L118 150 L142 235 L168 120 L190 190 H260 L276 170 L292 190 H330" fill="none" stroke="{V}" stroke-opacity=".3" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M30 190 H100 L118 150 L142 235 L168 120 L190 190 H260 L276 170 L292 190 H330" fill="none" stroke="{V}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="520" stroke-dashoffset="520">'
            f'<animate attributeName="stroke-dashoffset" values="520;0;0;-520" keyTimes="0;.5;.8;1" dur="3.6s" repeatCount="indefinite"/></path>'
            f'<text x="400" y="157" font-family="{MONO}" font-size="16" fill="{TXT}" text-anchor="middle">♥</text>'
            f'<g font-family="{MONO}" font-size="14" fill="{MUT}" letter-spacing="2"><text x="360" y="236">GIẤC NGỦ</text><text x="360" y="258">DINH DƯỠNG</text><text x="360" y="280">VẬN ĐỘNG</text></g>')


def art_wiis():
    cells = ""
    days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    for i, d in enumerate(days):
        c = T if d == "CN" else MUT
        cells += f'<text x="{60 + i*66}" y="86" font-family="{MONO}" font-size="15" fill="{c}" text-anchor="middle">{d}</text>'
    for r in range(3):
        for c in range(7):
            x, y = 34 + c * 66, 100 + r * 46
            sun = c == 6
            hot = (r, c) == (1, 6)
            fill = T if hot else (PANEL)
            st = T if sun else LINE
            anim = '<animate attributeName="fill-opacity" values="1;.35;1" dur="2.2s" repeatCount="indefinite"/>' if hot else ""
            cells += f'<rect x="{x}" y="{y}" width="52" height="36" rx="8" fill="{fill}" stroke="{st}" stroke-opacity="{.8 if sun else 1}">{anim}</rect>'
    cells += f'<rect x="{34+3*66}" y="{100+1*46}" width="52" height="36" rx="8" fill="{V}" fill-opacity=".3" stroke="{V}"/>'
    return cells


# ───────────────────── NOTES (scrapbook) ─────────────────────
def notes():
    w, h = 1000, 420
    data = [
        (40, 40, -3, V, "đang học", ["Làm việc với AI", "như một người", "cộng sự."]),
        (270, 70, 2, T, "đang khám phá", ["Quản lý ngữ cảnh", "cục bộ & ứng dụng", "desktop (Electron)."]),
        (500, 36, -2, B, "đang làm", ["C.I.R.C.A —", "không gian làm việc", "AI trên desktop."]),
        (730, 66, 3, "#F0E6A6", "tiếp theo", ["Kiến trúc Android,", "rồi Full-stack.", "Đích đến rõ rồi."]),
    ]
    g = ""
    for i, (x, y, rot, c, head, lines) in enumerate(data):
        ink = "#1b1f27" if c == "#F0E6A6" else TXT
        fill = c if c == "#F0E6A6" else PANEL
        stroke = c
        t = "".join(f'<text x="22" y="{108 + j*34}" font-family="{HAND}" font-size="23" fill="{ink}">{escape(l)}</text>' for j, l in enumerate(lines))
        g += f'''<g transform="translate({x} {y}) rotate({rot} 110 130)">
<animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;0 -6;0 0" dur="{6 + i}s" begin="-{i*1.3}s" repeatCount="indefinite"/>
<rect width="220" height="262" rx="6" fill="{fill}" stroke="{stroke}" stroke-opacity=".7"/>
<rect x="70" y="-12" width="80" height="26" fill="{c}" fill-opacity=".55" transform="rotate(-2 110 0)"/>
<text x="22" y="56" font-family="{MONO}" font-size="16" letter-spacing="3" fill="{c if c != '#F0E6A6' else '#6b5f1e'}">{escape(head.upper())}</text>
<line x1="22" y1="68" x2="198" y2="68" stroke="{c}" stroke-opacity=".5" stroke-dasharray="2 5"/>{t}</g>'''
    body = f'''<defs><clipPath id="c"><rect width="{w}" height="{h}" rx="24"/></clipPath></defs>
<g clip-path="url(#c)">{card(w, h)}{grid(w, h, 28, ".035")}{g}
<text x="40" y="392" font-family="{MONO}" font-size="17" fill="{MUT}">// ghi chú cập nhật theo những gì mình đang làm</text></g>'''
    save("notes.svg", w, h, body, "Góc ghi chú: đang học làm việc với AI, đang khám phá quản lý ngữ cảnh cục bộ và Electron, đang làm C.I.R.C.A, tiếp theo là Android và Full-stack")


# ───────────────────── DIVIDER ─────────────────────
def divider():
    w, h = 1000, 24
    body = f'''<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{V}" stop-opacity="0"/><stop offset=".5" stop-color="{B}"/><stop offset="1" stop-color="{T}" stop-opacity="0"/></linearGradient></defs>
<line x1="0" y1="12" x2="1000" y2="12" stroke="url(#d)" stroke-opacity=".6"/>
<circle cy="12" r="4" fill="{T}"><animate attributeName="cx" values="60;940;60" dur="12s" repeatCount="indefinite"/></circle>'''
    save("divider.svg", w, h, body, "")


if __name__ == "__main__":
    hero(); interests(); timeline(); notes(); divider()
    for n, t, s, c in [("01", "Một chút về tôi", "BEHIND THE PROFILE", V),
                       ("02", "Những điều tôi quan tâm", "WHAT KEEPS ME CURIOUS", T),
                       ("03", "Hành trình", "THE STORY SO FAR", B),
                       ("04", "Những thứ tôi đã tạo ra", "SELECTED WORKS", V),
                       ("05", "Không gian của tôi", "RIGHT NOW", T),
                       ("06", "Dấu ấn trên GitHub", "THE TRACES", B),
                       ("07", "Kết nối", "SAY HELLO", V)]:
        section(n, t, s, c)
    poster("vyron", "VYRON", "01", T, art_vyron())
    poster("circa", "C.I.R.C.A", "02", V, art_circa())
    poster("salud", "Salud", "03", T, art_salud())
    poster("wiis", "WIIS", "04", B, art_wiis())
    print("ok")
