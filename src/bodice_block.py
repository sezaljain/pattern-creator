import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def add_cut(curve_array: np.ndarray, coords: np.ndarray):
    """
    Add a cut line to the existing bodice block figure

    Args:
        curve_array: 2D array of cut line coordinates [[x1,y1], [x2,y2], ...]
        coords: 2D array of coordinates to match [[x1,y1], [x2,y2], ...]
    """
    plt.plot(curve_array[:, 0], curve_array[:, 1], "g-", label="Cut Line")


def create_bodice_block(front_lateral_measurements: pd.DataFrame, armhole_index: int):
    """
    Create a bodice block pattern from front lateral measurements

    Args:
        front_lateral_measurements: DataFrame with columns [Y, X2]
        armhole_index: Index marking the armhole position

    Returns:
        DataFrame with bodice block pattern points
    """
    # Extract measurements
    y_coords = front_lateral_measurements["Y"].values
    x_coords = front_lateral_measurements["X2"].values
    print(x_coords[armhole_index], y_coords[armhole_index])
    # Plot the measurements
    plt.figure(figsize=(5, 5))
    plt.plot(x_coords, y_coords, "b-", label="Front Profile")
    plt.plot(
        x_coords[armhole_index], y_coords[armhole_index], "ro", label="Armhole Point"
    )

    # Draw horizontal line through armhole and vertical line at max width
    armhole_y = y_coords[armhole_index]
    max_x = max(x_coords[armhole_index:])
    plt.axhline(y=armhole_y, color="r", linestyle="--", label="Horizontal Line")
    plt.axvline(x=max_x, color="b", linestyle="--", label="Max Width Line")

    plt.grid(True)
    plt.legend()
    plt.title("Bodice Block Front Profile")
    plt.xlabel("X (Width)")
    plt.ylabel("Y (Height)")
    plt.axis("equal")
    plt.grid(True)
    plt.gca().set_aspect("equal")

    # Add vertical line through armhole as 2D array
    cut_x = np.full_like(y_coords, x_coords[armhole_index])
    cut_line = np.column_stack((cut_x, y_coords))
    coords = np.column_stack((x_coords, y_coords))
    add_cut(cut_line, coords)

    plt.show()
    return pd.DataFrame({"Y": y_coords, "X2": x_coords})
