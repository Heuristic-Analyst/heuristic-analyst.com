# Where to find every available data: https://www.binance.com/en/landing/data
# BTCUSDT spot trades data: https://data.binance.vision/?prefix=data/spot/daily/trades/
import requests

def download_file(url):
    # Send a request to the URL
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        # Get the filename from the URL
        file_name = url.split("/")[-1]

        # Open a file in write mode
        with open(file_name, "wb") as f:
            # Write the contents of the response (in binary format) to the file
            f.write(response.content)

        print(f'Successfully downloaded {file_name}')
    else:
        print(f'Failed to download file. Status code: {response.status_code}')


# Download the last n days of the crypto pairs in list x
if __name__ == "__main__":
    from datetime import date, timedelta

    # Get the current date
    today = date.today()

    # Set the number of days to go back
    n = 7

    # Cryptocurrency pairs to download data from
    x = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "LTCUSDT", "SOLUSDT", "MANAUSDT", "DOGEUSDT", "LINKUSDT",
         "TRXUSDT",
         "MATICUSDT", "ADUSDT", "DREPUSDT", "ATOMUSDT", "BCHUSDT", "LUNCUSDT", "APEUSDT", "DOTUSDT", "ETCUSDT",
         "AVAXUSDT",
         "SANDUSDT", "HIVEUSDT", "MASKUSDT", "SHIBUSDT", "DAShUSDT", "XMRUSDT", "WAVESUSDT", "GALAUSDT", "UNIUSDT",
         "EOSUSDT", "FILUSDT", "AXSUSDT", "CHZUSDT", "FTMUSDT", "VOXELUSDT", "ZECUSDT", "XLMUSDT", "DYDXUSDT",
         "NEARUSDT",
         "APTUSDT", "LOOMUSDT", "AAVEUSDT", "OPUSDT", "STXUSDT", "WBTCUSDT", "MTLUSDT", "SUSHIUSDT", "ALGOUSDT"]
    
    # Iterate over each pair in list x
    for crypto_pair in x:
        # Iterate over the last n days
        for j in range(1, n + 1):
            # Subtract the loop index from the current date
            dateToPrint = today - timedelta(j)
            # Format the date as a string in the desired format
            date_str = dateToPrint.strftime("%Y-%m-%d")
            # Print the date
            print("Downloading", crypto_pair, date_str, "data...")
            download_file(
                "https://data.binance.vision/data/spot/daily/trades/" + crypto_pair + "/" + crypto_pair + "-trades-" + date_str + ".zip")
