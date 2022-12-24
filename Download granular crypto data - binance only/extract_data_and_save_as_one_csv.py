import zipfile
import numpy as np
import csv


def read_csv_from_zip(zip_file_name, csv_file_name):
    # Open the zip file in read-only mode
    zip_file = zipfile.ZipFile(zip_file_name, 'r')
    csv_file = zip_file.open(csv_file_name)
    # Use numpy's genfromtxt function to read the CSV file
    return list(np.genfromtxt(csv_file, delimiter=',', dtype=None))


def save_to_csv(list_of_tuples, filename):
  with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(list_of_tuples)


if __name__ == "__main__":
    from datetime import date, timedelta

    # Download the last n days of the crypto pairs in list x
    # Get the current date
    today = date.today()

    # Set the number of days to go back
    n = 7
    # Cryptocurrency pairs to download data from
    x = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "LTCUSDT", "SOLUSDT", "MANAUSDT", "DOGEUSDT", "LINKUSDT",
         "TRXUSDT", "MATICUSDT", "ADUSDT", "DREPUSDT", "ATOMUSDT", "BCHUSDT", "LUNCUSDT", "APEUSDT", "DOTUSDT", "ETCUSDT",
         "AVAXUSDT", "SANDUSDT", "HIVEUSDT", "MASKUSDT", "SHIBUSDT", "DAShUSDT", "XMRUSDT", "WAVESUSDT", "GALAUSDT", "UNIUSDT",
         "EOSUSDT", "FILUSDT", "AXSUSDT", "CHZUSDT", "FTMUSDT", "VOXELUSDT", "ZECUSDT", "XLMUSDT", "DYDXUSDT",
         "NEARUSDT", "APTUSDT", "LOOMUSDT", "AAVEUSDT", "OPUSDT", "STXUSDT", "WBTCUSDT", "MTLUSDT", "SUSHIUSDT", "ALGOUSDT"]

    for crypto_pair in x:
        print("Creating one csv file with data from:", crypto_pair, " (saving as)", crypto_pair + "_trades_data.csv ...")
        csv_contents = []
        # Iterate over the last n days (the other way - begin with old data and add newer data)
        for j in range(n, 0, -1):
            # Subtract the loop index from the current date
            dateToPrint = today - timedelta(j)
            # Format the date as a string in the desired format
            date_str = dateToPrint.strftime("%Y-%m-%d")
            # Print the date
            csv_contents = csv_contents + read_csv_from_zip(crypto_pair + "-trades-" + date_str + ".zip", crypto_pair + "-trades-" + date_str + ".csv")
        save_to_csv(csv_contents, crypto_pair + "_trades_data.csv")
        print("Csv file created!")
