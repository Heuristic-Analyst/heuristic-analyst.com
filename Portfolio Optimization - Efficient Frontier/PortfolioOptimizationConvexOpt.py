import Covarianzmatrix
import PortfolioVolatility


def PortfolioOptimizationConvexOpt(prices_data: list, price_symbols: list, frequency_of_data_per_day: float, frequency_of_data_per_year: float, risk_free_rate: float):
    # Calculate returns for each asset - start with last one to affect the next return
    # (If I would start to calculate the first return I would change it and not be able to calculate the next return)
    returns = [[prices_data[i][j]/prices_data[i][j-1] for j in range(1, len(prices_data[i]))] for i in range(len(prices_data))]

    # Calculate each annualized asset return: First multiply returns (or for log returns: sum up)
    # and then return^(annualized compound factor)-1
    # if daily returns: frequency_of_data_per_day = 1; if stock data: frequency_of_data_per_year = 252
    # -> compound factor is 252/1 if only one day data is given to annualize it -> if for example 300 days worth
    # of data then: (252/1)/300 to annualize the returns
    assetReturns = [1 for i in range(len(returns))]
    for i in range(len(returns)):
        for j in range(len(returns[i])):
            assetReturns[i] *= (returns[i][j])
        assetReturns[i] = assetReturns[i] ** ((frequency_of_data_per_year/frequency_of_data_per_day) / len(returns[i])) - 1

    # Calculate covariance matrix with pure python (2d, square matrix; length = amount of assets)
    # Price data must be unweighted, because scaling affects the covariance calculation
    covarianceMatrix = Covarianzmatrix.calc_covariancematrix(returns)
    for i in range(len(covarianceMatrix)):
        for j in range(len(covarianceMatrix[i])):
            covarianceMatrix[i][j] *= (frequency_of_data_per_year/frequency_of_data_per_day)

    # optimize portfolio weights by minimizing volatility
    optimized_weights_min_volatility = PortfolioVolatility.optimize_portfolio_weights_min_volatility(len(returns), covarianceMatrix)

    # Calculate annualized portfolio return - just sum up the weighted returns
    portfolioReturn = 0
    for i in range(len(assetReturns)):
        portfolioReturn += assetReturns[i]*optimized_weights_min_volatility[i]

    # Calculate volatility sigma with the matrix multiplication formula:
    # sigma = volatility = square root( transposed(weights) * covariance matrix * weights)
    volatility = PortfolioVolatility.calc_portfolio_volatility(optimized_weights_min_volatility, covarianceMatrix)

    # Calculate the sharp ratio
    sharpRatio = (portfolioReturn-risk_free_rate) / volatility

    # Assignment of asset names to weights
    optimized_weights = {}
    for i in range(len(optimized_weights_min_volatility)):
        optimized_weights[price_symbols[i]] = optimized_weights_min_volatility[i]

    # Create dict which will contain the portfolio return, volatility, sharp ratio and weights for optimized portfolio
    portfolioMetrics = {"Portfolio return": portfolioReturn, "Volatility": volatility, "Sharp ratio": sharpRatio, "Weights": optimized_weights}

    # Return the results at the end
    return portfolioMetrics
