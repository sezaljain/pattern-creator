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
    # Find intersection point (assuming vertical line)
    intersection_y = None
    for i in range(len(coords)):
        if np.abs(coords[i, 0] - curve_array[i, 0]) < 1e-6:
            intersection_y = coords[i, 1]
            break

    if intersection_y is not None:
        # Only plot cut line below intersection
        mask_below = curve_array[:, 1] <= intersection_y
        if np.any(mask_below):
            plt.plot(
                curve_array[mask_below, 0],
                curve_array[mask_below, 1],
                "g-",
                label="Cut Line",
            )
            # Calculate distances between curve and coords for points below intersection
            coords_below = coords[coords[:, 1] <= intersection_y]
            curve_below = curve_array[mask_below]
            distances = coords_below[:, 0] - curve_below[:, 0]
            # Create new points by adding distances to max width
            max_x = np.max(coords[:, 0])
            new_x = max_x - distances
            new_points = np.column_stack((new_x, coords_below[:, 1]))
            plt.plot(
                new_points[:, 0],
                new_points[:, 1],
                "y-",
                label="_nolegend_",
            )


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
    plt.plot(
        x_coords,
        y_coords,
        "grey",
        label="Front Profile",
        linestyle="dashed",
    )
    plt.plot(
        x_coords[armhole_index], y_coords[armhole_index], "ro", label="Armhole Point"
    )

    # Draw horizontal line through armhole and vertical line at max width
    armhole_y = y_coords[armhole_index]
    max_x = max(x_coords[armhole_index:])
    plt.axhline(
        y=armhole_y, color="powderblue", linestyle="--", label="Horizontal Line"
    )
    plt.axvline(x=max_x, color="b", label="Max Width Line")

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
