from math import sqrt
from Covariance import covariance as covariance
from Variance import variance as variance


def correlation(x_values: list, y_values: list, population_or_sample: str):
    corr = covariance(x_values, y_values, population_or_sample) / sqrt(variance(x_values, population_or_sample) * variance(y_values, population_or_sample))
    return corr
