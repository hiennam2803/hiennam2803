"""Sinh bản theme sáng (*-light.svg) từ các SVG tối trong assets/.

Chạy: python scripts/make_light.py
- Bản tối (tên gốc) là nguồn; bản sáng chỉ đổi bảng màu, giữ nguyên bố cục/animation.
- README dùng <picture> để GitHub tự chọn theo theme người xem.
"""
import os, re

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
FILES = ["hero", "interests", "timeline", "notes", "divider",
         "sec-01", "sec-02", "sec-03", "sec-04", "sec-05", "sec-06", "sec-07",
         "project-vyron", "project-circa", "project-salud", "project-wiis"]

# Màu nhấn đậm hơn để đạt tương phản trên nền trắng; màu nền/chữ theo GitHub light.
MAP = {
    "#0D1117": "#FFFFFF",  # nền thẻ
    "#161B22": "#F6F8FA",  # panel
    "#30363D": "#D0D7DE",  # viền
    "#E6EDF3": "#1F2328",  # chữ chính
    "#8B949E": "#59636E",  # chữ phụ
    "#A78BFA": "#6D4FD8",  # tím
    "#36D6C5": "#0E8F80",  # xanh ngọc
    "#7C9CFF": "#3F5FD6",  # xanh dương
    "#F0E6A6": "#F5DF72",  # giấy ghi chú
    "#6B5F1E": "#7A6A10",
    "#1B1F27": "#3B3410",
}


def convert(svg: str) -> str:
    # lưới nền: vạch trắng mờ -> vạch tím mờ (trắng trên nền trắng sẽ vô hình)
    svg = re.sub(r'stroke="#fff" stroke-opacity="(\.\d+)"',
                 lambda m: f'stroke="#6D4FD8" stroke-opacity="{float(m.group(1)) * 1.8:.3f}"', svg)
    svg = svg.replace('fill="#fff"', 'fill="#6D4FD8"')  # chấm chạy trên timeline
    return re.sub(r"#[0-9A-Fa-f]{6}\b", lambda m: MAP.get(m.group(0).upper(), m.group(0)), svg)


if __name__ == "__main__":
    for name in FILES:
        src = os.path.join(ASSETS, f"{name}.svg")
        with open(src, encoding="utf-8") as f:
            out = convert(f.read())
        with open(os.path.join(ASSETS, f"{name}-light.svg"), "w", encoding="utf-8") as f:
            f.write(out)
    print(f"ok: {len(FILES)} files")
