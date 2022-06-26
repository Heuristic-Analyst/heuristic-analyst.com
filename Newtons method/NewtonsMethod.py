def newtons_method(iterations: int):
    # Starting value (near to the zero point)
    x = 2

    for i in range(iterations):
        y = function_one(x)
        m = function_one_derivative(x)
        b = y - (m * x)
        x = (0 - b) / m
    return x


# Function we want to approximate the zero point
# - This function has a zero point at sqrt(2) (read blog post for more information)
def function_one(x: float):
    return x ** 2 - 2

# Derivative of the function we want to approximate the zero point
def function_one_derivative(x: float):
    return 2 * x