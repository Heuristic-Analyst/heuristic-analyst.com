import MultipleLinearRegression


if __name__ == '__main__':
    betas_vals = [1, 1, 1, 1]  # 4 factors - random initial values (I set them to all be ones)
    x_vals = [[0.5, 2.1, 0.9],  # sample 1 - 3 features
              [2.3, 8.9, 4],  # sample 2 - 3 features
              [2.9, 12.2, 6]]  # sample 3 - 3 features
    y_vals = [-37.04, -207.0, -312.9]  # 3 outcomes

    # Generate loss function and gradient
    L_function, gradient_functions = MultipleLinearRegression.generate_loss_function_and_gradient(len(betas_vals))
    # Print loss function
    print("Loss function:", L_function)

    # Create list which will hold betas from previous iteration to compare loss function from previous to current step
    # I do it to check whether to break out of the loop because the step is small enough
    betas_previous = [0 for i in range(len(betas_vals))]

    for i in range(1):
        print("Iteration number", i)
        # fill beta values from previous step
        for j in range(len(betas_vals)):
            betas_previous[j] = betas_vals[j]
        # Optimize betas
        MultipleLinearRegression.gradient_descent_algorithm(0.0001, y_vals, x_vals, betas_vals, gradient_functions)
        # Compare losses from previous step to current -> break from loop if loss is small
        if abs(MultipleLinearRegression.sum_loss_function(y_vals, x_vals, betas_vals, L_function) - MultipleLinearRegression.sum_loss_function(y_vals, x_vals, betas_previous, L_function)) < 0.00001:
            break

    # Print optimized betas
    print("Optimized betas:", betas_vals)

    # Print actual and predicted y
    for i in range(len(x_vals)):
        print("Actual y:", y_vals[i], "- Predicted y:", betas_vals[0] + betas_vals[1] * x_vals[i][0] + betas_vals[2] * x_vals[i][1] + betas_vals[3] * x_vals[i][2])
