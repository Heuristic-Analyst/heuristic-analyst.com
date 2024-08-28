import os
import requests
import json

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def fetch_data(exchange):
    url = f"https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange={exchange}&download=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def process_exchange_data(exchange, data):
    base_dir = os.path.join(os.getcwd(), exchange)
    create_directory(base_dir)

    # Save full tickers
    with open(os.path.join(base_dir, f"{exchange}_full_tickers.json"), "w") as f:
        json.dump(data["data"]["rows"], f)

    return data["data"]["rows"]

def concat_all_data(all_data):
    all_dir = os.path.join(os.getcwd(), "all")
    create_directory(all_dir)

    # Check for duplicates
    seen = set()
    duplicates = []
    unique_data = []

    for item in all_data:
        symbol = item['symbol']
        if symbol in seen:
            duplicates.append(item)
        else:
            seen.add(symbol)
            unique_data.append(item)

    # Print duplicates
    if duplicates:
        print("Duplicates found:")
        for dup in duplicates:
            print(f"Symbol: {dup['symbol']}, Name: {dup['name']}, Exchange: {dup['exchange']}")
    else:
        print("No duplicates found.")

    # Save unique data
    with open(os.path.join(all_dir, "all_exchanges_data.json"), "w") as f:
        json.dump(unique_data, f)

    print(f"Total items before removing duplicates: {len(all_data)}")
    print(f"Total items after removing duplicates: {len(unique_data)}")

def main():
    exchanges = ["nasdaq", "nyse", "amex"]
    all_data = []
    
    for exchange in exchanges:
        data = fetch_data(exchange)
        exchange_data = process_exchange_data(exchange, data)
        all_data.extend(exchange_data)

    concat_all_data(all_data)
    print("Data fetching and processing completed.")

if __name__ == "__main__":
    main()
