import pandas as pd
from bodice_block import create_bodice_block

# Read the CSV files
profile = pd.read_csv("profile_outline.csv")
front = pd.read_csv("frontLaterMeasurements.csv")
front_outline = pd.read_csv("front_outline.csv")

# Create the plot with equal aspect ratio
# plt.figure(figsize=(10, 8))
# plt.gca().set_aspect("equal")

# # Plot front measurements (shifted down)
# plt.plot(front["X1"] - 10, front["Y"], color="red", label="Front Measurements")
# plt.plot(front["X2"] - 10, front["Y"], color="red", label="Front Measurements")
# # Plot profile outline (shifted left)
# plt.plot(profile["X"] + 30, profile["Y"], "b-", label="Profile Outline")


# # Plot front outline (shifted right)
# plt.plot(front_outline["X1"] + 60, front_outline["Y"], "g-", label="Front Outline Left")
# plt.plot(
#     front_outline["X2"] + 60, front_outline["Y"], "g-", label="Front Outline Right"
# )

# plt.grid(True)
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.title("Profile and Front Measurements")
# # plt.legend()

# plt.savefig("plot.png")
# plt.show()

# Create bodice block
create_bodice_block(front, armhole_index=5)
