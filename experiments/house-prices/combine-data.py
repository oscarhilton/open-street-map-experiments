import csv
import json

CSV_FILE = "./raw/pp-monthly-update-new-version.csv"
JSON_FILE = "./compiled/postcode_results.json"
OUTPUT_FILE = "./compiled/combined_postcode_price_coords.json"

csv_rows = []
with open(CSV_FILE, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            price = int(row[1])
            postcode = row[3].strip()
            csv_rows.append({"postcode": postcode, "price": price})
        except:
            continue

with open(JSON_FILE, encoding='utf-8') as f:
    json_data = json.load(f)

combined = []
for csv_row, json_row in zip(csv_rows, json_data):
    result = json_row.get("result")
    if result and result.get("latitude") and result.get("longitude"):
        combined.append({
            "postcode": csv_row["postcode"],
            "price": csv_row["price"],
            "lat": result["latitude"],
            "lon": result["longitude"]
        })

with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
    json.dump(combined, f, indent=2)

print(f"Saved {len(combined)} entries to {OUTPUT_FILE}")
