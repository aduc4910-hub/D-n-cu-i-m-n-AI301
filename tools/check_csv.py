import csv

path = "C:/Users/Lenovo/.gemini/antigravity/brain/eee38720-ff47-4e7d-850b-b883e8c20630/.user_uploaded/media_1794963163663_816c17b3.csv"
with open(path, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

monthly = {}
total_rev = 0
total_cogs = 0
total_prof = 0
total_orders = 0

for r in rows:
    month = r.get("Tháng", "").strip()
    if not month:
        continue
    rev = float(r.get("Doanh thu (VND)", 0))
    cogs = float(r.get("Chi phí giá vốn (VND)", 0))
    prof = float(r.get("Lợi nhuận gộp (VND)", 0))
    orders = int(float(r.get("Số đơn", 1)))
    
    total_rev += rev
    total_cogs += cogs
    total_prof += prof
    total_orders += orders
    
    if month not in monthly:
        monthly[month] = {"rev": 0, "cogs": 0, "prof": 0, "orders": 0}
    monthly[month]["rev"] += rev
    monthly[month]["cogs"] += cogs
    monthly[month]["prof"] += prof
    monthly[month]["orders"] += orders

print(f"Total Revenue: {total_rev:,.0f} VND ({total_rev/1e6:.1f} Tr)")
print(f"Total COGS: {total_cogs:,.0f} VND")
print(f"Total Profit: {total_prof:,.0f} VND")
print(f"Total Orders: {total_orders:,}")
print("Monthly:")
for m, v in sorted(monthly.items()):
    print(f"  {m}: {v['rev']:,.0f} VND ({v['rev']/1e6:.1f} Tr) | {v['orders']} orders | Profit: {v['prof']:,.0f}")
