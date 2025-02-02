import matplotlib.pyplot as plt
import pandas as pd
from bodice_block import create_bodice_block

# Read the CSV files
profile = pd.read_csv("profile_outline.csv")
front_df = pd.read_csv("frontLaterMeasurements.csv")
front_outline = pd.read_csv("front_outline.csv")


# Convert front measurements to map
front_lateral_measurements = {y: x2 for y, x2 in zip(front_df["Y"], front_df["X2"])}

# Plot all data in single figure
plt.figure(1, figsize=(10, 5))
plt.plot(front_df["X2"] - 40, front_df["Y"], label="front_df")
plt.plot(front_df["X1"] - 40, front_df["Y"], label="front_df")
plt.text(
    -40,
    0,
    "Horizontal measurements \nfor the front upper body",
    fontsize=12,
    horizontalalignment="center",
)
plt.plot(front_outline["X1"], front_outline["Y"], label="front_outline", color="g")
plt.plot(front_outline["X2"], front_outline["Y"], label="front_outline", color="g")
plt.text(23, 0, "Front profile \noutline", fontsize=12, horizontalalignment="center")
plt.plot(profile["X"] + 60, profile["Y"], label="profile")
plt.text(70, 0, "Side profile \noutline", fontsize=12, horizontalalignment="center")
plt.gca().set_aspect("equal")
plt.title("Upper Body Measurements (cm)")
plt.grid(True)
plt.axis("equal")
plt.savefig("plotA.png")
# plt.show()

# Create bodice block
create_bodice_block(front_lateral_measurements, armhole_index=10)
