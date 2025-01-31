import numpy as np
from scipy.optimize import brentq
from scipy.special import comb


def bezier_curve(t, points):
    """
    Compute a Bezier curve for a set of control points and parameter t.

    Args:
        t (float or np.array): Parameter between 0 and 1.
        points (np.array): Array of control points, shape (n_points, 2).

    Returns:
        np.array: Points on the Bezier curve.
    """
    n = len(points) - 1
    curve = np.zeros((len(t), 2))
    for i in range(n + 1):
        bin_coeff = comb(n, i)
        term = bin_coeff * (t**i) * ((1 - t) ** (n - i))
        curve += np.outer(term, points[i])
    return curve


def bezier_point(t, points):
    """
    Compute a single point on the Bezier curve.

    Args:
        t (float): Parameter between 0 and 1.
        points (np.array): Array of control points, shape (n_points, 2).

    Returns:
        np.array: (x, y) coordinates of the point on the Bezier curve.
    """
    n = len(points) - 1
    point = np.zeros(2)
    for i in range(n + 1):
        bin_coeff = comb(n, i)
        term = bin_coeff * (t**i) * ((1 - t) ** (n - i))
        point += term * points[i]
    return point


def find_t_for_y(y_target, points, tol=1e-6):
    """
    Find the parameter t such that y(t) = y_target on the Bezier curve.

    Args:
        y_target (float): The target y-coordinate.
        points (np.array): Array of control points, shape (n_points, 2).
        tol (float): Tolerance for the root-finding.

    Returns:
        float: The parameter t in [0, 1] such that y(t) ≈ y_target.
    """

    # Define the function y(t) - y_target
    def func(t):
        return bezier_point(t, points)[1] - y_target

    # Initial guesses for t
    t_lower = 0.0
    t_upper = 1.0

    # Check if y_target is within the y range of the curve
    y_min = min(points[:, 1])
    y_max = max(points[:, 1])
    if not (y_min <= y_target <= y_max):
        raise ValueError(
            f"y_target={y_target} is outside the y range of the curve ({y_min}, {y_max})."
        )

    # Use brentq to find the root
    t_solution = brentq(func, t_lower, t_upper, xtol=tol)
    return t_solution
