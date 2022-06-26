from Variance import variance as variance
from StandardDeviation import standard_deviation as standard_deviation

if __name__ == "__main__":
    x = [1, 3, 5, 3, 7, 3, 5, 1, 3]

    var = variance(x_values=x, population_or_sample="sample")
    std = standard_deviation(x_values=x, population_or_sample="sample")
    # When comparing values with numpy values: numpy calculates np.var(x) and np.std(x) with "population" by default

    print("Variance:", var)
    print("Standard deviation:", std)