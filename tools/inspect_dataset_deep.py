import csv, math

test_path = r'C:\Users\Lenovo\.gemini\antigravity\brain\eee38720-ff47-4e7d-850b-b883e8c20630\.user_uploaded\media_1794846860628_25a7a190.csv'
with open(test_path, 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

# 1. 3-Sigma on Quantity
qtys = [float(r['Quantity']) for r in rows if r.get('Quantity')]
mean_q = sum(qtys) / len(qtys)
std_q = math.sqrt(sum((x - mean_q)**2 for x in qtys) / len(qtys))
thresh_q = mean_q + 3.0 * std_q
print(f"Quantity 3-sigma threshold: {thresh_q:.3f} (mean={mean_q:.2f}, std={std_q:.2f})")
for idx, r in enumerate(rows):
    q = float(r.get('Quantity', 0))
    if q > thresh_q:
        print(f"  Qty Outlier at index {idx}: Order_ID={r['Order_ID']}, Qty={q}")

# 2. 3-Sigma on Unit_Price_VND
prices = [float(r['Unit_Price_VND']) for r in rows if r.get('Unit_Price_VND')]
mean_p = sum(prices) / len(prices)
std_p = math.sqrt(sum((x - mean_p)**2 for x in prices) / len(prices))
thresh_p = mean_p + 3.0 * std_p
print(f"\nUnitPrice 3-sigma threshold: {thresh_p:.2f} (mean={mean_p:.2f}, std={std_p:.2f})")
for idx, r in enumerate(rows[:20]):
    p = float(r.get('Unit_Price_VND', 0))
    if p > thresh_p:
        print(f"  Price Outlier in top 20 at index {idx}: Order_ID={r['Order_ID']}, Price={p}")

# 3. 3-Sigma on GrossSales (UnitPrice * Quantity) or Revenue_VND
revs = [float(r['Revenue_VND']) for r in rows if r.get('Revenue_VND')]
mean_r = sum(revs) / len(revs)
std_r = math.sqrt(sum((x - mean_r)**2 for x in revs) / len(revs))
thresh_r = mean_r + 3.0 * std_r
print(f"\nRevenue 3-sigma threshold: {thresh_r:.2f} (mean={mean_r:.2f}, std={std_r:.2f})")
for idx, r in enumerate(rows[:20]):
    rev = float(r.get('Revenue_VND', 0))
    if rev > thresh_r:
        print(f"  Revenue Outlier in top 20 at index {idx}: Order_ID={r['Order_ID']}, Rev={rev}")
