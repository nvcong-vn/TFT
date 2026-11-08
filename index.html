#!/usr/bin/env python3
"""Điền lại dữ liệu vào index.html từ data/*.json. Chạy: python update.py

1) Tướng + giá + trang bị phổ biến: lấy từ Google Sheet CSV (UNITS_CSV_URL) nếu có, lưu vào
   data/units.json. Không có hoặc lỗi -> dùng data/units.json hiện có (sửa tay/ChatGPT vẫn được).
2) Đội hình meta: đọc data/comps.json (bạn sửa tay, hoặc đặt COMPS_CSV_URL = link Google Sheet CSV).
3) Ghi lại index.html + ngày cập nhật.
"""
import json, os, re, sys, urllib.request, csv, io
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
COMPS_CSV_URL = os.environ.get("COMPS_CSV_URL", "")  # tùy chọn: Google Sheet publish CSV (đội hình)
UNITS_CSV_URL = os.environ.get("UNITS_CSV_URL", "")  # tùy chọn: Google Sheet publish CSV (tướng)
UNITS_SET = os.environ.get("UNITS_SET", "")          # tùy chọn: số mùa, ví dụ 18
norm = lambda n: n.strip().replace("'", "’")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "tft-compass-updater"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8-sig")


def check_units(units):
    """Kiểm tra danh sách tướng (list dict name/cost/items). Dừng bằng ValueError nếu sai."""
    groups = [[] for _ in range(5)]
    items, seen = {}, set()
    for u in units:
        name, cost = norm(u.get("name", "")), u.get("cost")
        if not name:
            raise ValueError("có dòng tướng không có tên")
        if name in seen:
            raise ValueError(f"tướng bị trùng: {name}")
        if not (isinstance(cost, int) and 1 <= cost <= 5):
            raise ValueError(f"giá không hợp lệ ở tướng {name}: {cost!r}")
        seen.add(name)
        groups[cost - 1].append(name)
        its = [norm(i) for i in u.get("items", []) if i and i.strip()]
        if its:
            items[name] = its
    if len(seen) < 40:
        raise ValueError(f"chỉ có {len(seen)} tướng, quá ít (nghi thiếu dữ liệu)")
    return [sorted(g) for g in groups], items


def units_from_csv(url):
    """CSV cột: name,cost,items  (items cách nhau bằng |). Cột tùy chọn: extra (x/1/true = đơn vị phụ)."""
    reader = csv.DictReader(io.StringIO(get(url)))
    reader.fieldnames = [(h or "").strip().lower() for h in (reader.fieldnames or [])]
    if not {"name", "cost"} <= set(reader.fieldnames):
        raise ValueError(f"CSV cần cột name,cost,items; hiện có: {reader.fieldnames}")
    out = []
    for r in reader:
        name = (r.get("name") or "").strip()
        if not name:
            continue  # bỏ dòng trống
        cost_txt = (r.get("cost") or "").strip()
        if not cost_txt.isdigit():
            raise ValueError(f"giá không phải số ở tướng {name}: {cost_txt!r}")
        u = {"name": name, "cost": int(cost_txt),
             "items": [i.strip() for i in (r.get("items") or "").split("|") if i.strip()]}
        if (r.get("extra") or "").strip().lower() in ("x", "1", "true", "yes"):
            u["extra"] = True
        out.append(u)
    return out


def load_units():
    """Trả về (5 nhóm giá, {tướng: [trang bị]}, số set). Ưu tiên Google Sheet, lỗi -> units.json cũ."""
    path = P("data", "units.json")
    data = json.load(open(path, encoding="utf-8"))
    if UNITS_CSV_URL:
        try:
            units = units_from_csv(UNITS_CSV_URL)
            check_units(units)  # chỉ ghi đè khi dữ liệu mới hợp lệ
            data["units"] = units
            data["source"] = "Google Sheet (UNITS_CSV_URL)"
            data["checked_at"] = date.today().isoformat()
            if UNITS_SET.isdigit():
                data["set"] = int(UNITS_SET)
            json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"Tướng: lấy {len(units)} tướng từ Google Sheet")
        except Exception as e:
            print("! Lỗi đọc Google Sheet tướng, giữ units.json cũ:", e)
    try:
        groups, items = check_units(data["units"])
    except ValueError as e:
        sys.exit(f"DỪNG: units.json không hợp lệ: {e}")
    print("Số tướng theo giá:", [len(g) for g in groups], "| tổng", sum(map(len, groups)))
    return groups, items, data.get("set")


def comps_from_csv(url):
    """CSV cột: name,style,tier,avg,unit,items (mỗi dòng 1 tướng; items cách nhau bằng |)"""
    rows = csv.DictReader(io.StringIO(get(url)))
    out, idx = [], {}
    for r in rows:
        k = r["name"].strip()
        if k not in idx:
            idx[k] = [k, r["style"].strip(), r["tier"].strip(), float(r["avg"]), []]
            out.append(idx[k])
        u = [r["unit"].strip()]
        if r.get("items", "").strip():
            u.append(r["items"].strip())
        idx[k][4].append(u)
    return out


def main():
    costs, unit_items, setno = load_units()
    json.dump(costs, open(P("data", "unit_cost.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"Tướng: dùng dữ liệu Set {setno}")

    if COMPS_CSV_URL:
        try:
            comps = comps_from_csv(COMPS_CSV_URL)
            json.dump(comps, open(P("data", "comps.json"), "w", encoding="utf-8"), ensure_ascii=False)
            print(f"Đội hình: lấy {len(comps)} comp từ Google Sheet")
        except Exception as e:
            print("! Lỗi đọc Google Sheet, giữ comps.json cũ:", e)
    comps = json.load(open(P("data", "comps.json"), encoding="utf-8"))
    if not comps:
        sys.exit("comps.json rỗng, dừng.")

    # kiểm tra: tướng trong comp phải có giá, nếu không web sẽ lỗi
    known = {n for g in costs for n in g}
    missing = sorted({u[0] for c in comps for u in c[4]} - known)
    if missing:
        sys.exit(f"DỪNG: tướng trong đội hình chưa có trong units.json: {missing}")

    html = open(P("index.html"), encoding="utf-8").read()
    html = re.sub(r"/\*DATA:COMPS:START\*/.*?/\*DATA:COMPS:END\*/",
                  lambda m: "/*DATA:COMPS:START*/const raw=" + json.dumps(comps, ensure_ascii=False) + ";/*DATA:COMPS:END*/",
                  html, flags=re.S)
    html = re.sub(r"/\*DATA:COST:START\*/.*?/\*DATA:COST:END\*/",
                  lambda m: "/*DATA:COST:START*/const UNIT_COST={};\n" + json.dumps(costs, ensure_ascii=False)
                  + ".forEach((group,i)=>group.forEach(n=>UNIT_COST[n]=i+1));\nconst UNIT_ITEMS="
                  + json.dumps(unit_items, ensure_ascii=False) + ";/*DATA:COST:END*/",
                  html, flags=re.S)
    today = date.today().strftime("%d/%m/%Y")
    html = re.sub(r"<!--NOTICE:START-->.*?<!--NOTICE:END-->",
                  f"<!--NOTICE:START-->● Dữ liệu cập nhật ngày {today}: {len(comps)} đội hình, {len(known)} tướng.<!--NOTICE:END-->",
                  html, flags=re.S)
    html = re.sub(r'<span class="muted">\d+ đội hình</span>', f'<span class="muted">{len(comps)} đội hình</span>', html)
    open(P("index.html"), "w", encoding="utf-8").write(html)
    print("Đã ghi index.html")


main()
