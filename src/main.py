import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV files
profile = pd.read_csv("profile_outline.csv")
front = pd.read_csv("frontLaterMeasurements.csv")

# Create the plot
plt.figure(figsize=(10, 8))

# Plot profile outline
plt.plot(profile["X"], profile["Y"], "b-", label="Profile Outline")

# Plot front measurements
plt.scatter(front["X"], front["Y"], color="red", label="Front Measurements")

plt.grid(True)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Profile and Front Measurements")
plt.legend()

plt.savefig("plot.png")
plt.close()
