def covariance(x_values: list, y_values: list, population_or_sample: str):
    x_mean = 0
    y_mean = 0
    sum_x_y_diff = 0
    n = 0

    for i in range(len(x_values)):
        x_mean += x_values[i]
        y_mean += y_values[i]
        n += 1
    x_mean /= n
    y_mean /= n

    for i in range(len(x_values)):
        sum_x_y_diff += (x_values[i] - x_mean) * (y_values[i] - y_mean)

    if population_or_sample == "population":
        return sum_x_y_diff / n
    elif population_or_sample == "sample":
        return sum_x_y_diff / (n - 1)
