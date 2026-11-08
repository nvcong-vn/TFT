#!/usr/bin/env python3
"""Chạy MỘT LẦN: python patch_index.py  (sửa phần code trong index.html).
Sau đó chạy: python update.py"""
import os, sys

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
html = open(path, encoding="utf-8").read()

EDITS = [
    # 1) Danh sách tướng lấy từ UNIT_COST (đầy đủ), cộng thêm tướng trong đội hình
    (
        "const names=[...new Set(COMPS.flatMap(c=>c.units.map(u=>u.name)))].sort(),items=CATALOG;",
        "const names=[...new Set([...Object.keys(UNIT_COST),...COMPS.flatMap(c=>c.units.map(u=>u.name))])].sort(),items=CATALOG;",
    ),
    # 2) Hiện trang bị phổ biến của các tướng đã chọn (dưới mục "Đang có")
    (
        "function renderCrafts(){let el=$('crafts');",
        "function renderPopular(){let el=$('popular');if(!el){el=document.createElement('div');el.id='popular';$('inventory').after(el)}"
        "const rows=state.units.filter(n=>typeof UNIT_ITEMS!=='undefined'&&UNIT_ITEMS[n]);"
        "el.innerHTML=rows.length?'<h3>Trang bị phổ biến theo tướng</h3>'+rows.map(n=>`<div class=\"detailrow\"><b>${esc(n)}</b> <span class=\"muted\">${UNIT_COST[n]||'?'} vàng</span><small>${UNIT_ITEMS[n].map(itemWithName).join(' / ')}</small></div>`).join(''):''}\n"
        "function renderCrafts(){renderPopular();let el=$('crafts');",
    ),
]

for old, new in EDITS:
    if new in html:
        print("Đã sửa trước đó, bỏ qua:", old[:50], "...")
        continue
    if html.count(old) != 1:
        sys.exit(f"KHÔNG tìm thấy đúng 1 vị trí để sửa (index.html có thể đã khác): {old[:60]}...")
    html = html.replace(old, new)

open(path, "w", encoding="utf-8").write(html)
print("Đã sửa index.html. Giờ chạy: python update.py")
