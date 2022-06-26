def variance(x_values: list, population_or_sample: str):
    x_mean = 0
    squared_sum_x = 0
    n = 0

    for x in x_values:
        x_mean += x
        n += 1
    x_mean /= n

    for x in x_values:
        squared_sum_x += (x - x_mean) ** 2
    if population_or_sample == "population":
        return squared_sum_x / n
    elif population_or_sample == "sample":
        return squared_sum_x / (n - 1)