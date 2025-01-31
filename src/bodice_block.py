import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_princess_dart(coords: np.ndarray, armhole_index: int) -> np.ndarray:
    """
    Create a princess dart curve starting from armhole point

    Args:
        coords: 2D array of coordinates [[x1,y1], [x2,y2], ...]
        armhole_index: Index marking the armhole position

    Returns:
        2D array of curve coordinates
    """
    # Extract points below armhole
    points_below = coords[armhole_index:]
    y_coords = points_below[:, 1]

    # Create curve that bends inward
    x_start = coords[armhole_index, 0]  # Armhole x position
    x_curve = np.full_like(y_coords, x_start)

    # Add curve by moving points inward, max at middle
    curve_depth = 5.0  # cm
    t = np.linspace(0, 1, len(y_coords))
    curve = curve_depth * np.sin(t * np.pi)
    x_curve -= curve
    print(np.column_stack((x_curve, y_coords)))

    return np.column_stack((x_curve, y_coords))


def add_cut(curve_array: np.ndarray, coords: np.ndarray, armhole_index: int):
    """
    Add a cut line to the existing bodice block figure

    Args:
        curve_array: 2D array of princess dart curve coordinates
        coords: 2D array of original coordinates
        armhole_index: Index marking the armhole position
    """
    # Plot princess dart curve
    plt.plot(
        curve_array[:, 0],
        curve_array[:, 1],
        "g-",
        label="Princess Dart",
    )

    # Get points below armhole from original coords
    coords_below = coords[armhole_index:]

    # Calculate horizontal distances between curve and original points
    distances = coords_below[:, 0] - curve_array[:, 0]

    # Create new points by adding distances to max width
    max_x = np.max(coords[:, 0])
    new_x = max_x - distances
    new_points = np.column_stack((new_x, curve_array[:, 1]))

    # Plot the mirrored curve
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

    # Create and add princess dart curve
    coords = np.column_stack((x_coords, y_coords))
    princess_curve = create_princess_dart(coords, armhole_index)
    add_cut(princess_curve, coords, armhole_index)

    plt.show()
    return pd.DataFrame({"Y": y_coords, "X2": x_coords})
