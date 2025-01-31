import matplotlib.pyplot as plt
import pandas as pd


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

    # Find maximum x below armhole point
    max_x = max(x_coords[armhole_index:])
    plt.axvline(x=max_x, color="r", linestyle="--", label="Max Width Line")

    plt.grid(True)
    plt.legend()
    plt.title("Bodice Block Front Profile")
    plt.xlabel("X (Width)")
    plt.ylabel("Y (Height)")
    plt.axis("equal")
    plt.grid(True)
    plt.gca().set_aspect("equal")
    plt.show()

    return pd.DataFrame({"Y": y_coords, "X2": x_coords})
