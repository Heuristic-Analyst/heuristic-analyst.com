import sympy as smp

def generate_loss_function_and_gradient(number_of_betas: int):
    # create variables:
    #   y -> y_actual
    #   b_0 -> betas[0], b_1 -> betas[1], ...
    #   x_0 -> x_values[0], x_1 -> x_values[1], ...
    y_actual = smp.symbols("y_actual", real=True)
    beta_symbols = []
    x_symbols = []
    for i in range(number_of_betas):
        beta_symbols.append(smp.symbols(f"betas[{i}]", real=True))
    for i in range(number_of_betas-1):
        x_symbols.append(smp.symbols(f"x_values[{i}]", real=True))

    # Add variables to the function which will look like this:
    # (y-ŷ)^2 = (y-(b_0 + b_1*x_0 + b_2*x_1 + ...))^2 -> (y_actual - (betas[0] + betas[1]*x_values[0] + ...))^2
    f = beta_symbols[0]
    for i in range(1, number_of_betas):
        f = f+beta_symbols[i]*x_symbols[i - 1]
    f = (y_actual-f)**2
    # Save function as a string
    L_fct = str(f).replace(" ", "")
    # calculate gradient - derive with respect to every beta
    gradientList = []
    for i in range(len(beta_symbols)):
        gradientList.append(str(smp.diff(f, beta_symbols[i])).replace(" ", ""))
    return L_fct, gradientList


def loss_function(y_actual: float, x_values: list, betas: list, L_fct: str):
    loss_of_sample = eval(L_fct)
    return loss_of_sample


def sum_loss_function(y_actual: list, x_values_population: list, betas: list, L_fct: str):
    sum_losses = 0
    for i in range(len(y_actual)):
        sum_losses += loss_function(y_actual[i], x_values_population[i], betas, L_fct)
    return sum_losses


def gradient_descent_algorithm(learning_rate:float, y_actual_list: list, x_values_population:list, betas: list, gradient: list):
    # Create list to save temporarily new betas
    new_betas = [0 for i in range(len(betas))]
    # Iterate through each derivative of the gradient
    for i in range(len(gradient)):
        tmp = 0
        # Calculate derivative ("slope") of every sample for the derivative i in gradient and sum them up in "tmp"
        for j in range(len(x_values_population)):
            y_actual = y_actual_list[j]
            x_values = x_values_population[j]
            tmp += eval(gradient[i])
        # Calculate Step size
        step_size=tmp*learning_rate
        # Calculate new beta
        new_betas[i] = betas[i]-step_size
    # When every beta is calculated: Update them
    for i in range(len(betas)):
        betas[i] = new_betas[i]
