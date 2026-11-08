#!/usr/bin/env python3
"""Chạy MỘT LẦN: python patch_index.py  (sửa phần code trong index.html).
Bản v2: dùng regex, chịu được khác biệt khoảng trắng/xuống dòng, và in chẩn đoán nếu không khớp."""
import os, re, sys

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
html = open(path, encoding="utf-8", newline="").read()  # giữ nguyên kiểu xuống dòng


def show(keyword):
    print(f"--- Các dòng có '{keyword}' trong index.html (gửi phần này cho Claude):")
    found = False
    for i, line in enumerate(html.split("\n"), 1):
        if keyword in line:
            found = True
            k = line.find(keyword)
            print(f"  dòng {i}: {line[max(0, k-40):k+220]!r}")
    if not found:
        print("  (không có dòng nào)")


# 1) Danh sách tướng lấy từ UNIT_COST (đầy đủ), cộng thêm tướng trong đội hình
if re.search(r"const\s+names\s*=[^\n]*Object\.keys\(UNIT_COST\)", html):
    print("[1] names: đã sửa trước đó, bỏ qua")
else:
    pat = re.compile(r"const\s+names\s*=\s*(\[[^\n;]*?\])\s*\.sort\(\)")
    html, n = pat.subn(lambda m: "const names=[...new Set([...Object.keys(UNIT_COST),..." + m.group(1) + "])].sort()", html, count=1)
    if n != 1:
        show("names")
        sys.exit("KHÔNG sửa được dòng 'const names'. Hãy gửi phần chẩn đoán ở trên.")
    print("[1] names: đã sửa")

# 2) Hiện trang bị phổ biến của các tướng đã chọn (dưới mục "Đang có")
POPULAR = (
    "function renderPopular(){let el=$('popular');if(!el){el=document.createElement('div');el.id='popular';$('inventory').after(el)}"
    "const rows=state.units.filter(n=>typeof UNIT_ITEMS!=='undefined'&&UNIT_ITEMS[n]);"
    "el.innerHTML=rows.length?'<h3>Trang bị phổ biến theo tướng</h3>'+rows.map(n=>`<div class=\"detailrow\"><b>${esc(n)}</b> "
    "<span class=\"muted\">${UNIT_COST[n]||'?'} vàng</span><small>${UNIT_ITEMS[n].map(itemWithName).join(' / ')}</small></div>`).join(''):''}\n"
)
if "function renderPopular" in html:
    print("[2] renderPopular: đã sửa trước đó, bỏ qua")
else:
    pat = re.compile(r"function\s+renderCrafts\s*\(\s*\)\s*\{")
    if len(pat.findall(html)) != 1:
        show("renderCrafts")
        sys.exit("KHÔNG tìm thấy đúng 1 'function renderCrafts'. Hãy gửi phần chẩn đoán ở trên.")
    html = pat.sub(lambda m: POPULAR + "function renderCrafts(){renderPopular();", html, count=1)
    print("[2] renderPopular: đã thêm")

open(path, "w", encoding="utf-8", newline="").write(html)
print("Xong. Giờ chạy: python update.py")
