import pandas_datareader.data as web
import datetime
import PortfolioOptimizationConvexOpt

if __name__ == '__main__':
    start = datetime.datetime(2018,1,1)
    end = datetime.datetime(2020, 12, 31)

    CNP = web.DataReader("CNP", "yahoo", start, end).Close.tolist()
    WMT = web.DataReader("WMT", "yahoo", start, end).Close.tolist()
    F = web.DataReader("F", "yahoo", start, end).Close.tolist()
    GE = web.DataReader("GE", "yahoo", start, end).Close.tolist()
    TSLA = web.DataReader("TSLA", "yahoo", start, end).Close.tolist()

    price_symbols = ["CNP", "WMT","F", "GE", "TSLA"]
    price_data = [CNP, WMT, F, GE, TSLA]

    portfolioMetricsCVXOPT = PortfolioOptimizationConvexOpt.PortfolioOptimizationConvexOpt(price_data, price_symbols, 1, 252, 0.03)
    print(portfolioMetricsCVXOPT)



