import matplotlib.pyplot as plt
import numpy as np


def dtw(ts1, ts2):
    n, m = len(ts1), len(ts2)
    dtw_cost_matrix = np.zeros((n + 1, m + 1))
    dtw_trace_matrix = np.zeros((n + 1, m + 1))
    dtw_path = []
    for i in range(n + 1):
        for j in range(m + 1):
            dtw_cost_matrix[i, j] = np.inf
            dtw_trace_matrix[i, j] = np.inf
    dtw_cost_matrix[0, 0] = 0
    dtw_trace_matrix[0, 0] = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(ts1[i - 1] - ts2[j - 1])
            last_min = np.min([dtw_cost_matrix[i - 1, j - 1], dtw_cost_matrix[i - 1, j], dtw_cost_matrix[i, j - 1]])
            # 0 from diagonal before - 1 from above - 2 from left
            from_where = np.argmin([dtw_cost_matrix[i - 1, j - 1], dtw_cost_matrix[i - 1, j], dtw_cost_matrix[i, j - 1]])
            dtw_cost_matrix[i, j] = cost + last_min
            dtw_trace_matrix[i, j] = from_where

    while True:
        if n == 0 and m == 0:
            break
        else:
            dtw_path.append((n - 1, m - 1))
            if dtw_trace_matrix[n, m] == 0:
                n, m = n - 1, m - 1
            elif dtw_trace_matrix[n, m] == 1:
                n, m = n - 1, m
            else:
                n, m = n, m - 1
    dtw_path = dtw_path[::-1]
    return dtw_cost_matrix, dtw_path

if __name__ == "__main__":
    # Define the two time series
    x = np.array([0, 0, 1, 1, 0, 0, -1, 0, 0, 0, 0])
    y = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, -1, -0.5, 0, 0])

    # Perform dynamic time warping
    # cost matrix and the path (tuple is matched indices in time series 1 and 2)
    cost_matrix, dtw_path = dtw(x, y)

    plt.plot(x)
    # Shifting signal y to illustrate the connections made by DTW
    plt.plot(y-2)
    for i in range(len(dtw_path)):
        plt.plot([dtw_path[i][0], dtw_path[i][1]], [x[dtw_path[i][0]], y[dtw_path[i][1]]-2], c="C7")
    plt.show()
