from Covariance import covariance as covariance
from Correlation import correlation as correlation


if __name__ == "__main__":
    x = [1, 3, 5, 3, 7, 3, 5, 1, 3]
    y = [8, 4, 7, 5, 8, 1, 3, 2, 6]

    covar = covariance(x_values=x, y_values=y, population_or_sample="sample")
    corr = correlation(x_values=x, y_values=y, population_or_sample="sample")
    # When comparing values with numpy values: numpy calculates np.cov(x,y) and np.corrcoef(x,y) with "population" by default

    print("Covariance:", covar)
    print("Correlation:", corr)
