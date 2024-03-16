# tshark -r icsi525-S24_p1_trace.pcapng -T fields -e wlan.fc.type -E separator=, -E header=y > icsi525-S24_p1_qa.csv

import pandas as pd
import matplotlib.pyplot as plt

# Load the data from icsi525-S24_p1_trace.csv into a DataFrame
df = pd.read_csv("icsi525-S24_p1_qa.csv", index_col=None)

# Calculate the counts of wlan.fc.type
type_counts = df['wlan.fc.type'].value_counts()

# Data
types = [str(t) for t in type_counts.index.tolist()]
counts = type_counts.values.tolist()

# Map numeric labels to corresponding names
type_names = {0: 'Management Frames', 1: 'Control Frames', 2: 'Data Frames'}
types_mapped = [type_names[int(t)] for t in types]

# Define a light color palette
colors = ['#FF9999', '#66B2FF', '#99FF99']  # You can adjust these colors as needed

# Create a pie chart with light colors
plt.pie(counts, labels=types_mapped, autopct=lambda p: '{:.0f} \n ({:.1f}%)'.format(p * sum(counts) / 100, p), startangle=140, colors=colors)
plt.title('Distribution of WLAN Frame Types')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Save the pie chart as an image file
plt.savefig('wlan_frame_types_pie_chart.png')

# Show the plots
plt.tight_layout()
plt.show()