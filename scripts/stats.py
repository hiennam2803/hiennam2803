"""Sinh assets/stats.svg và assets/langs.svg từ dữ liệu thật của GitHub API.

Dùng: GH_USER=<username> GH_TOKEN=<token> python scripts/stats.py
Không có GH_TOKEN/GH_USER thì chỉ sinh ảnh "chờ dữ liệu" (không có số liệu giả).
"""
import json, os, sys, urllib.request
from datetime import datetime, timedelta, timezone
from html import escape

USER = os.environ.get("GH_USER", "")
TOKEN = os.environ.get("GH_TOKEN", "")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
PALETTE = ["#B4A7F5", "#36D6C5", "#7B6CD9", "#2AA89B", "#D9D2FA", "#4B3F8F"]


def api(url, data=None):
    req = urllib.request.Request(url, data=data)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    repos, page = [], 1
    while True:
        chunk = api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}")
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        for k, v in api(r["languages_url"]).items():
            langs[k] = langs.get(k, 0) + v
    now = datetime.now(timezone.utc)
    q = {"query": "query($u:String!,$from:DateTime!,$to:DateTime!){user(login:$u){followers{totalCount} "
                  "contributionsCollection(from:$from,to:$to){contributionCalendar{totalContributions}}}}",
         "variables": {"u": USER, "from": (now - timedelta(days=365)).isoformat(), "to": now.isoformat()}}
    g = api("https://api.github.com/graphql", json.dumps(q).encode())["data"]["user"]
    return {
        "repos": len(own),
        "stars": sum(r["stargazers_count"] for r in own),
        "followers": g["followers"]["totalCount"],
        "contribs": g["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "langs": langs,
    }


def frame(title, body, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 495 165" role="img" aria-labelledby="t">
<title id="t">{escape(label)}</title>
<rect x="1" y="1" width="493" height="163" rx="10" fill="#15131F" stroke="#2A2640" stroke-width="2"/>
<text x="25" y="35" font-family="{FONT}" font-size="18" font-weight="700" fill="#B4A7F5">{escape(title)}</text>
{body}
</svg>
'''


def stats_svg(d):
    if not d:
        body = f'<text x="25" y="90" font-family="{MONO}" font-size="13" fill="#9690AA">Chờ workflow "Update Stats" chạy lần đầu…</text>'
    else:
        rows = [("Public repositories", d["repos"]), ("Total stars", d["stars"]),
                ("Followers", d["followers"]), ("Contributions (12 tháng)", d["contribs"])]
        body = ""
        for i, (k, v) in enumerate(rows):
            y = 70 + i * 24
            body += (f'<circle cx="31" cy="{y-5}" r="4" fill="#36D6C5"/>'
                     f'<text x="46" y="{y}" font-family="{FONT}" font-size="14" fill="#9690AA">{escape(k)}</text>'
                     f'<text x="470" y="{y}" font-family="{FONT}" font-size="15" font-weight="700" fill="#F2EFFA" text-anchor="end">{v:,}</text>\n')
    return frame("GitHub Stats", body, f"Thống kê GitHub của {USER or 'người dùng'}")


def langs_svg(d):
    if not d or not d["langs"]:
        body = f'<text x="25" y="90" font-family="{MONO}" font-size="13" fill="#9690AA">Chờ workflow "Update Stats" chạy lần đầu…</text>'
    else:
        items = sorted(d["langs"].items(), key=lambda x: -x[1])[:6]
        total = sum(d["langs"].values())
        body = ""
        for i, (k, v) in enumerate(items):
            y = 62 + i * 16
            pct = v / total * 100
            w = max(2, 190 * pct / 100 / (items[0][1] / total))  # thanh dài nhất = 190px
            c = PALETTE[i % len(PALETTE)]
            body += (f'<text x="25" y="{y+4}" font-family="{FONT}" font-size="12" fill="#F2EFFA">{escape(k)}</text>'
                     f'<rect x="140" y="{y-5}" width="190" height="9" rx="4.5" fill="#2A2640"/>'
                     f'<rect x="140" y="{y-5}" width="{w:.1f}" height="9" rx="4.5" fill="{c}"><animate attributeName="width" from="0" to="{w:.1f}" dur="1s" fill="freeze"/></rect>'
                     f'<text x="470" y="{y+4}" font-family="{FONT}" font-size="12" fill="#9690AA" text-anchor="end">{pct:.1f}%</text>\n')
    return frame("Top Languages", body, f"Ngôn ngữ dùng nhiều nhất của {USER or 'người dùng'}")


if __name__ == "__main__":
    data = collect() if (USER and TOKEN) else None
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "stats.svg"), "w", encoding="utf-8").write(stats_svg(data))
    open(os.path.join(OUT, "langs.svg"), "w", encoding="utf-8").write(langs_svg(data))
    print("done", "(placeholder)" if not data else data)
