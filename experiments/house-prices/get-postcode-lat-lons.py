import csv
import json
import requests
from time import sleep
import os

CSV_FILE = './raw/pp-monthly-update-new-version.csv'
PROGRESS_FILE = './compiled/progress.json'
RESULTS_FILE = './compiled/postcode_results.json'
BATCH_SIZE = 100
API_URL = 'https://api.postcodes.io/postcodes'

def extract_postcodes(file_path):
    postcodes = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 4:
                postcodes.append(row[3].strip())
    return postcodes

def batch_postcodes(postcodes):
    for i in range(0, len(postcodes), BATCH_SIZE):
        yield i // BATCH_SIZE, postcodes[i:i + BATCH_SIZE]

def query_postcodes_api(postcode_batch):
    response = requests.post(API_URL, json={"postcodes": postcode_batch})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"last_batch_index": -1}

def save_progress(index):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump({"last_batch_index": index}, f)

def append_results(batch_results):
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    else:
        existing = []

    existing.extend(batch_results)
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

def main():
    postcodes = extract_postcodes(CSV_FILE)
    progress = load_progress()
    start_index = progress["last_batch_index"] + 1

    for i, batch in batch_postcodes(postcodes):
        if i < start_index:
            continue

        print(f"Processing batch {i}...")
        data = query_postcodes_api(batch)
        if data:
            append_results(data['result'])
            save_progress(i)
        sleep(5)

if __name__ == "__main__":
    main()
