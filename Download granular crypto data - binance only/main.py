from datetime import date, timedelta
import requests

# Where to find every available data: https://www.binance.com/en/landing/data
# BTCUSDT spot trades data: https://data.binance.vision/?prefix=data/spot/daily/trades/
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


# Get the current date
today = date.today()

# Set the number of days to go back
n = 365

# Iterate over the last n days
for i in range(1, n+1):
    # Subtract the loop index from the current date
    dateToPrint = today - timedelta(i)
    # Format the date as a string in the desired format
    date_str = dateToPrint.strftime("%Y-%m-%d")
    # Print the date
    print(date_str)
    download_file("https://data.binance.vision/data/spot/daily/trades/BTCUSDT/BTCUSDT-trades-"+date_str+".zip")
