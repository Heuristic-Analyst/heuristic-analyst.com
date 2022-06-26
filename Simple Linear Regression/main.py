import random
import matplotlib.pyplot as plt
from SimpleLinearRegression import linear_regression as linear_regression


if __name__ == "__main__":
    # Create very simple random data
    x = [i for i in range(1000)]
    y = [-70 * (i - (random.random() * 1000 - 250)) + 130 for i in range(1000)]

    # Show the generated data
    plt.scatter(x, y)
    plt.show()

    # Calculate linear regression coefficients
    m, b = linear_regression(x, y)
    print("linear model: y=m*x+b")
    print("Coefficient m:", m)
    print("Coefficient b:", b)

    # Calculated predicted values y that the model suggest for every input x
    y_predict = []
    for x_values in x:
        y_predict.append(m * x_values + b)

    # Plot generated data and linear model
    plt.scatter(x, y)
    plt.plot(y_predict, "red")
    plt.show()
