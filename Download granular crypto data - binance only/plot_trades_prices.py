import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Use BTCUSDT's trades to plot - load in data
data = np.genfromtxt('BTCUSDT_trades_data.csv', delimiter=',')
# x: date time (timestamp in ms) - y: price the trade was made
plt.plot(np.array([datetime.fromtimestamp(ts/1000) for ts in data[:, 4]]), data[:, 1])
plt.show()
