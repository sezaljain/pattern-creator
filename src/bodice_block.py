import math

import matplotlib.pyplot as plt
import numpy as np
from bezier_curve import bezier_point, find_t_for_y  # Same directory import


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
    curve_depth = 10.0  # cm
    i = 0
    interval = 1 / len(curve_points)
    for y in curve_points:
        # Calculate relative position in curve (0 to 1)
        t = interval * i
        i = i + 1
        # Apply sine curve for inward bend
        inward_shift = curve_depth * math.sin(t * math.pi)
        curve_points[y] = start_x - inward_shift

    return curve_points


def create_princess_dart_v2(measurements: dict, armhole_y: float) -> dict:
    """
    Create a princess dart curve using bezier curve with 4 control points

    Args:
        measurements: Dict mapping Y coordinates to X values
        armhole_y: Y coordinate of armhole point

    Returns:
        Dict mapping Y coordinates to X values for princess dart curve
    """
    curve_points = {y: x for y, x in measurements.items() if y <= armhole_y + 4}
    start_y = max(curve_points.keys())
    start_x = measurements[start_y]
    end_y = 9  # Waist level
    waist_x = measurements[end_y]
    end_x = waist_x / 2  # End at 2/3 of waist x-coordinate

    # Control points - evenly spaced in Y
    y_interval = (start_y - end_y) / 5
    control_points = np.array(
        [
            [start_x, start_y],  # P0
            [start_x / 3, start_y - y_interval],  # P1
            [2 * start_x / 3, start_y - 2 * y_interval],  # P2 (upper middle)
            [2 * start_x / 3, start_y - 3 * y_interval],  # P3 (lower middle)
            [end_x, end_y + y_interval],  # P4
            [end_x, end_y],  # P5
        ]
    )

    # Calculate points along bezier curve
    result = {}
    for y in curve_points:
        try:
            t = find_t_for_y(y, control_points)
            point = bezier_point(t, control_points)
            result[y] = np.round(point[0], 1)  # Take x coordinate
        except ValueError:
            # If y is outside curve range, use linear interpolation
            if y > start_y:
                result[y] = start_x
            else:
                result[y] = end_x

    return result


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


def create_polygons(
    front_bodice: dict,
    princess_dart: dict,
    line_under_armhole: dict,
    dart_right_side: dict,
) -> list:
    """
    Create polygons for the bodice block pattern

    Args:
        front_bodice: Dictionary mapping Y coordinates to X values
        princess_dart: Dictionary mapping Y coordinates to X values for princess dart
        line_under_armhole: Dictionary mapping Y coordinates to X values for line under armhole
        dart_right_side: Dictionary mapping Y coordinates to X values for dart right side

    Returns:
        List of numpy arrays representing polygons
    """
    # Get all y coordinates
    y_coords = sorted(list(front_bodice.keys()))

    # Create first polygon (main body)
    center_polygon = []
    # Add bottom point at x=0
    center_polygon.append([0, y_coords[0]])

    # Add princess dart curve points
    for y in sorted(princess_dart.keys()):
        center_polygon.append([princess_dart[y], y])

    # Add points from measurements up to armhole
    for y in y_coords:
        if y not in princess_dart:
            center_polygon.append([front_bodice[y], y])
    # Add top point at x=0
    center_polygon.append([0, y])
    # Close the polygon by adding first point again
    center_polygon.append(center_polygon[0])

    # Create second polygon (dart right side)
    side_polygon = []
    # Add points from dart right side
    for y in sorted(dart_right_side.keys()):
        side_polygon.append([dart_right_side[y], y])

    # Add points from princess dart not present in dart right side
    temp = []
    for y in sorted(princess_dart.keys()):
        if y not in dart_right_side:
            side_polygon.append([princess_dart[y], y])
            temp.append([front_bodice[y], y])

    temp.reverse()
    for t in temp:
        side_polygon.append(t)
    # Add points from line under armhole
    for y in line_under_armhole.keys():
        side_polygon.append([line_under_armhole[y], y])

    # Close the polygon by adding first point again
    side_polygon.append(side_polygon[0])

    # move polygons so that they dont overlap
    center_polygon = np.array(center_polygon)
    side_polygon = np.array(side_polygon)
    offset = np.max(center_polygon[:, 0]) - np.min(side_polygon[:, 0])
    side_polygon[:, 0] += offset
    return [center_polygon, side_polygon]


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
    princess_dart = create_princess_dart_v2(front_bodice, armhole_y)

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
    plt.savefig("plot1.png")
    plt.close()

    # Plot polygons in separate figure
    polygons = create_polygons(
        front_bodice, princess_dart, line_under_armhole, dart_right_side
    )
    plt.figure(figsize=(5, 5))
    for polygon in polygons:
        plt.plot(polygon[:, 0], polygon[:, 1], alpha=0.3)
        plt.plot(polygon[:, 0], polygon[:, 1], "k-")

    plt.grid(True)
    plt.title("Bodice Block Pattern")
    plt.xlabel("X (Width)")
    plt.ylabel("Y (Height)")
    plt.axis("equal")
    plt.gca().set_aspect("equal")
    plt.savefig("plot2.png")
    plt.show()
    # plt.close()

    return front_bodice
