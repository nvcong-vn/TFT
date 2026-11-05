#!/usr/bin/env python3
"""Điền lại dữ liệu vào index.html từ data/*.json. Chạy: python update.py

1) Giá tướng: thử lấy từ Community Dragon (set mới nhất). Lỗi -> giữ data/unit_cost.json cũ.
2) Đội hình meta: đọc data/comps.json (bạn sửa tay, hoặc đặt COMPS_CSV_URL = link Google Sheet CSV).
3) Ghi lại index.html + ngày cập nhật.
"""
import json, os, re, sys, urllib.request, csv, io
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
CDRAGON = "https://raw.communitydragon.org/latest/cdragon/tft/en_us.json"
COMPS_CSV_URL = os.environ.get("COMPS_CSV_URL", "")  # tùy chọn: Google Sheet publish CSV
norm = lambda n: n.replace("'", "’")

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "tft-compass-updater"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8")

def refresh_costs():
    """Trả về (danh sách 5 nhóm giá, số set) hoặc None nếu lỗi/không hợp lệ."""
    try:
        d = json.loads(get(CDRAGON))
        sets = d.get("sets") or {}
        num = max(int(k) for k in sets if str(k).isdigit())
        champs = sets[str(num)]["champions"]
        groups = [[] for _ in range(5)]
        for c in champs:
            cost = c.get("cost")
            if isinstance(cost, int) and 1 <= cost <= 5 and c.get("name"):
                groups[cost - 1].append(norm(c["name"]))
        if sum(map(len, groups)) < 40:  # quá ít -> dữ liệu lạ, bỏ
            raise ValueError("số tướng bất thường")
        groups = [sorted(set(g)) for g in groups]
        return groups, num
    except Exception as e:
        print("! Không cập nhật được giá tướng, giữ dữ liệu cũ:", e)
        return None

def comps_from_csv(url):
    """CSV cột: name,style,tier,avg,unit,items  (mỗi dòng 1 tướng; items cách nhau bằng |)"""
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
    costs = json.load(open(P("data", "unit_cost.json"), encoding="utf-8"))
    r = refresh_costs()
    if r:
        costs, setno = r
        json.dump(costs, open(P("data", "unit_cost.json"), "w", encoding="utf-8"), ensure_ascii=False)
        print(f"Giá tướng: cập nhật từ Set {setno}")

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
        sys.exit(f"DỪNG: tướng chưa có giá (thêm vào unit_cost.json): {missing}")

    html = open(P("index.html"), encoding="utf-8").read()
    html = re.sub(r"/\*DATA:COMPS:START\*/.*?/\*DATA:COMPS:END\*/",
                  lambda m: "/*DATA:COMPS:START*/const raw=" + json.dumps(comps, ensure_ascii=False) + ";/*DATA:COMPS:END*/",
                  html, flags=re.S)
    html = re.sub(r"/\*DATA:COST:START\*/.*?/\*DATA:COST:END\*/",
                  lambda m: "/*DATA:COST:START*/const UNIT_COST={};\n" + json.dumps(costs, ensure_ascii=False)
                  + ".forEach((group,i)=>group.forEach(n=>UNIT_COST[n]=i+1));/*DATA:COST:END*/",
                  html, flags=re.S)
    today = date.today().strftime("%d/%m/%Y")
    html = re.sub(r"<!--NOTICE:START-->.*?<!--NOTICE:END-->",
                  f"<!--NOTICE:START-->● Dữ liệu cập nhật ngày {today}: {len(comps)} đội hình.<!--NOTICE:END-->",
                  html, flags=re.S)
    html = re.sub(r'<span class="muted">\d+ đội hình</span>', f'<span class="muted">{len(comps)} đội hình</span>', html)
    open(P("index.html"), "w", encoding="utf-8").write(html)
    print("Đã ghi index.html")

main()
