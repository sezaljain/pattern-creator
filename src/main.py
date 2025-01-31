import pandas as pd
from bodice_block import create_bodice_block

# Read the CSV files
profile = pd.read_csv("profile_outline.csv")
front_df = pd.read_csv("frontLaterMeasurements.csv")
front_outline = pd.read_csv("front_outline.csv")


# Convert front measurements to map
front_lateral_measurements = {y: x2 for y, x2 in zip(front_df["Y"], front_df["X2"])}


# Create bodice block
create_bodice_block(front_lateral_measurements, armhole_index=10)
