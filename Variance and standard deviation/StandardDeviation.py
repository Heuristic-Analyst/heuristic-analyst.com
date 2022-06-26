from Variance import variance as variance
from math import sqrt


def standard_deviation(x_values: list, population_or_sample: str):
    var = variance(x_values, population_or_sample)
    return sqrt(var)