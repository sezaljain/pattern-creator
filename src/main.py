import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV files
profile = pd.read_csv("profile_outline.csv")
front = pd.read_csv("frontLaterMeasurements.csv")
front_outline = pd.read_csv("front_outline.csv")

# Create the plot
plt.figure(figsize=(10, 8))

# Plot profile outline
plt.plot(profile["X"], profile["Y"], "b-", label="Profile Outline")

# Plot front measurements
plt.scatter(front["X1"], front["Y"], color="red", label="Front Measurements")
plt.scatter(front["X2"], front["Y"], color="red", label="Front Measurements")

# Plot front outline
plt.plot(front_outline["X1"], front_outline["Y"], "g-", label="Front Outline Left")
plt.plot(front_outline["X2"], front_outline["Y"], "g-", label="Front Outline Right")

plt.grid(True)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Profile and Front Measurements")
plt.legend()

plt.savefig("plot.png")
plt.show()
