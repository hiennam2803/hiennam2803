"""Sinh assets/stats*.svg và assets/langs*.svg (bản sáng + tối) từ dữ liệu thật của GitHub API.

Dùng: GH_USER=<username> GH_TOKEN=<token> python scripts/stats.py
Không có GH_TOKEN/GH_USER thì chỉ sinh ảnh "chờ dữ liệu" (không có số liệu giả).
"""
import json, os, urllib.error, urllib.request
from datetime import datetime, timedelta, timezone
from html import escape

USER = os.environ.get("GH_USER", "")
TOKEN = os.environ.get("GH_TOKEN", "")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
PAL = {
    "": dict(surface="#FFFFFF", border="#DDD6F5", track="#E6E1FA", pri="#6A58D1", sec="#0E9C8C", text="#1B1730", muted="#5E5878",
             bars=["#6A58D1", "#0E9C8C", "#8F7FE8", "#2AA89B", "#A99CF0", "#4B3F8F"]),
    "-dark": dict(surface="#15131F", border="#2A2640", track="#2A2640", pri="#B4A7F5", sec="#36D6C5", text="#F2EFFA", muted="#9690AA",
                  bars=["#B4A7F5", "#36D6C5", "#7B6CD9", "#2AA89B", "#D9D2FA", "#4B3F8F"]),
}


def api(url, data=None):
    req = urllib.request.Request(url, data=data)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"::error::{e.code} {e.reason} tại {url}: {e.read().decode('utf-8', 'ignore')[:300]}")
        raise


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
        try:
            for k, v in api(r["languages_url"]).items():
                langs[k] = langs.get(k, 0) + v
        except Exception:
            pass
    now = datetime.now(timezone.utc)
    q = {"query": "query($u:String!,$from:DateTime!,$to:DateTime!){user(login:$u){followers{totalCount} "
                  "contributionsCollection(from:$from,to:$to){contributionCalendar{totalContributions}}}}",
         "variables": {"u": USER, "from": (now - timedelta(days=365)).isoformat(), "to": now.isoformat()}}
    followers, contribs = None, None
    try:
        g = api("https://api.github.com/graphql", json.dumps(q).encode())["data"]["user"]
        followers = g["followers"]["totalCount"]
        contribs = g["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except Exception:
        print("::warning::Không lấy được followers/contributions qua GraphQL, bỏ qua hai số này")
    return {"repos": len(own), "stars": sum(r["stargazers_count"] for r in own),
            "followers": followers, "contribs": contribs, "langs": langs}


def frame(P, title, body, label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 495 165" role="img" aria-labelledby="t">
<title id="t">{escape(label)}</title>
<rect x="1" y="1" width="493" height="163" rx="10" fill="{P['surface']}" stroke="{P['border']}" stroke-width="2"/>
<text x="25" y="35" font-family="{FONT}" font-size="18" font-weight="700" fill="{P['pri']}">{escape(title)}</text>
{body}
</svg>
"""


def waiting(P):
    return f'<text x="25" y="90" font-family="{MONO}" font-size="13" fill="{P["muted"]}">Chờ workflow "Update Stats" chạy lần đầu…</text>'


def stats_svg(P, d):
    if not d:
        body = waiting(P)
    else:
        rows = [("Public repositories", d["repos"]), ("Total stars", d["stars"]),
                ("Followers", d["followers"]), ("Contributions (12 tháng)", d["contribs"])]
        rows = [(k, v) for k, v in rows if v is not None]
        body = ""
        for i, (k, v) in enumerate(rows):
            y = 70 + i * 24
            body += (f'<circle cx="31" cy="{y-5}" r="4" fill="{P["sec"]}"/>'
                     f'<text x="46" y="{y}" font-family="{FONT}" font-size="14" fill="{P["muted"]}">{escape(k)}</text>'
                     f'<text x="470" y="{y}" font-family="{FONT}" font-size="15" font-weight="700" fill="{P["text"]}" text-anchor="end">{v:,}</text>\n')
    return frame(P, "GitHub Stats", body, f"Thống kê GitHub của {USER or 'người dùng'}")


def langs_svg(P, d):
    if not d or not d["langs"]:
        body = waiting(P)
    else:
        items = sorted(d["langs"].items(), key=lambda x: -x[1])[:6]
        total = sum(d["langs"].values())
        body = ""
        for i, (k, v) in enumerate(items):
            y = 62 + i * 16
            pct = v / total * 100
            w = max(2, 190 * v / items[0][1])
            c = P["bars"][i % len(P["bars"])]
            body += (f'<text x="25" y="{y+4}" font-family="{FONT}" font-size="12" fill="{P["text"]}">{escape(k)}</text>'
                     f'<rect x="140" y="{y-5}" width="190" height="9" rx="4.5" fill="{P["track"]}"/>'
                     f'<rect x="140" y="{y-5}" width="{w:.1f}" height="9" rx="4.5" fill="{c}"><animate attributeName="width" from="0" to="{w:.1f}" dur="1s" fill="freeze"/></rect>'
                     f'<text x="470" y="{y+4}" font-family="{FONT}" font-size="12" fill="{P["muted"]}" text-anchor="end">{pct:.1f}%</text>\n')
    return frame(P, "Top Languages", body, f"Ngôn ngữ dùng nhiều nhất của {USER or 'người dùng'}")


if __name__ == "__main__":
    data = collect() if (USER and TOKEN) else None
    os.makedirs(OUT, exist_ok=True)
    for suffix, P in PAL.items():
        open(os.path.join(OUT, f"stats{suffix}.svg"), "w", encoding="utf-8").write(stats_svg(P, data))
        open(os.path.join(OUT, f"langs{suffix}.svg"), "w", encoding="utf-8").write(langs_svg(P, data))
    print("done", "(placeholder)" if not data else data)
