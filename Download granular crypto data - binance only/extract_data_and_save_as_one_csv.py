import zipfile
import pandas as pd
import io


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
        print("Creating one csv file with data from:", crypto_pair, " (saving as", crypto_pair + "_trades_data.csv) ...")
        csv_contents = []
        zip_file_names = []
        # Iterate over the last n days (the other way - begin with old data and add newer data)
        for j in range(n, 0, -1):
            # Subtract the loop index from the current date
            dateToPrint = today - timedelta(j)
            # Format the date as a string in the desired format
            date_str = dateToPrint.strftime("%Y-%m-%d")
            # Print the date
            zip_file_names.append((crypto_pair + "-trades-" + date_str + ".zip"))
        for zip_file in zip_file_names:
            print("Currently at zip:", zip_file)
            # Open the zip file
            with zipfile.ZipFile(zip_file, 'r') as z:
                # Extract the CSV file from the zip file
                csv_file = z.namelist()[0]
                csv_data = z.read(csv_file)
                # Read the CSV data into a DataFrame and append it to the list
                df = pd.read_csv(io.BytesIO(csv_data))
                csv_contents.append(df)
        print("Saving csv...")
        pd.concat(csv_contents).to_csv(crypto_pair+".csv", index=False)
        print("Csv file created!")
