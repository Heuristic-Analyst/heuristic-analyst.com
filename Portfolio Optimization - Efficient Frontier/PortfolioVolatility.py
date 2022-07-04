from math import sqrt
import cvxpy as cp


def calc_portfolio_volatility(portfolio_weights: list, covariance_matrix: list):
    # volatility = sqrt(w.transposed() * covar-matrix * w)
    interimResultMatrix1 = [0 for i in range(len(portfolio_weights))]
    for i in range(len(covariance_matrix)):
        for j in range(len(portfolio_weights)):
            interimResultMatrix1[i] += portfolio_weights[j] * covariance_matrix[j][i]
    volatility = 0
    for i in range(len(interimResultMatrix1)):
        volatility += interimResultMatrix1[i] * portfolio_weights[i]
    volatility = sqrt(volatility)
    return volatility


# For min volatility
def optimize_portfolio_weights_min_volatility(len_prices_data: int, covariance_matrix: list):
    # portfolio volatility = sqrt(w.transposed * covar-matrix * w) = sqrt(variance)
    # We will minimize variance (volatility^2)

    # Generate weight-variables and save them in "weights" -> will be optimized values
    weights = cp.Variable(len_prices_data)

    # Create objective "risk" to be minimized:
    # See here: https://www.cvxpy.org/examples/basic/quadratic_program.html
    # that (1/2)*x.transposed*P*x+q.transposed*x is equal to (1/2)*cp.quad_form(x, P) + q.T @ x
    # This means that w.transposed() * covar-matrix * w (our risk measure "variance")
    #   is equal to cp.quad_form(weights, covariance_matrix)
    objective = cp.quad_form(weights, covariance_matrix)

    # Create constraints: sum of weights should be 1 and only long assets (every weight > 0)
    constraint = [sum(weights) == 1]
    for i in range(len_prices_data):
        constraint.append(weights[i] >= 0)

    # Solve formulated problem with cvxpy library
    problem = cp.Problem(cp.Minimize(objective), constraint)
    problem.solve()
    # Save optimized weight-values in "optimized_weights"
    optimized_weights = []
    for i in range(len(weights.value)):
        optimized_weights.append(weights.value[i])
    # Return solution
    return optimized_weights
