import math

import matplotlib.pyplot as plt


def create_princess_dart(measurements: dict, armhole_y: float) -> dict:
    """
    Create a princess dart curve starting from above armhole point

    Args:
        measurements: Dict mapping Y coordinates to X values
        armhole_y: Y coordinate of armhole point

    Returns:
        Dict mapping Y coordinates to X values for princess dart curve
    """
    # Start 4cm above armhole
    curve_points = {y: x for y, x in measurements.items() if y <= armhole_y + 4}
    start_y = max(curve_points.keys())
    start_x = measurements[start_y]  # X value at start of curve

    # Create curve by moving points inward
    curve_depth = 7.0  # cm
    i = 0
    interval = 1 / len(curve_points)
    for y in curve_points:
        # Calculate relative position in curve (0 to 1)
        t = interval * i
        i = i + 1
        # Apply sine curve for inward bend
        inward_shift = curve_depth * math.sin(t * math.pi)
        curve_points[y] = start_x - inward_shift

    # curve_points[9] = 15
    print(curve_points)
    return curve_points


def create_line_under_armhole(measurements: dict, armhole_y: float) -> dict:
    """
    Create a straight line under the armhole point

    Args:
        measurements: Dict mapping Y coordinates to X values
        armhole_y: Y coordinate of armhole point

    Returns:
        Dict mapping Y coordinates to X values for line under armhole
    """
    armhole_x = measurements[armhole_y]
    return {y: armhole_x for y in measurements.keys() if y <= armhole_y}


def create_bodice_block(front_bodice: dict, armhole_index: int):
    """
    Create a bodice block pattern from front lateral measurements

    Args:
        front_lateral_measurements: Dictionary mapping Y coordinates to X values
        armhole_index: Index marking the armhole position

    Returns:
        Dict with bodice block pattern points
    """
    # Get armhole point
    armhole_y = list(front_bodice.keys())[armhole_index]
    armhole_x = front_bodice[armhole_y]

    # Plot the measurements
    plt.figure(figsize=(5, 5))
    y_coords = list(front_bodice.keys())
    x_coords = list(front_bodice.values())
    plt.plot(x_coords, y_coords, "grey", label="Front Profile", linestyle="dashed")
    plt.plot(armhole_x, armhole_y, "ro", label="Armhole Point")

    # Create line under armhole and princess dart
    line_under_armhole = create_line_under_armhole(front_bodice, armhole_y)
    princess_dart = create_princess_dart(front_bodice, armhole_y)

    # Create dart right side
    dart_right_side = {}
    for key in line_under_armhole:
        if key in princess_dart:
            dart_right_side[key] = (
                princess_dart[key] - front_bodice[key] + line_under_armhole[key]
            )

    # Plot curves
    plt.plot(
        line_under_armhole.values(),
        line_under_armhole.keys(),
        "r--",
        label="Line Under Armhole",
    )
    plt.plot(
        list(princess_dart.values()),
        list(princess_dart.keys()),
        "g-",
        label="Princess Dart",
    )
    plt.plot(
        list(dart_right_side.values()),
        list(dart_right_side.keys()),
        "b-",
        label="Dart Right Side",
    )

    # Draw horizontal line through armhole and vertical line at max width
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
    plt.show()

    return front_bodice
