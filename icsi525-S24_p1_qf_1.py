import pandas as pd
import matplotlib.pyplot as plt

def analyze_rts_cts_pairs(df):
    rts_pairs = set()
    non_rts_pairs = set()

    # Filter dataframe for RTS and CTS frames
    rts_frames = df[df['wlan.fc.type_subtype'] == 27]
    cts_frames = df[df['wlan.fc.type_subtype'] == 28]

    # Extract source and destination MAC addresses for RTS and CTS frames
    rts_pairs.update(zip(rts_frames['wlan.ta'], rts_frames['wlan.ra']))
    rts_pairs.update(zip(cts_frames['wlan.ra'], cts_frames['wlan.ta']))

    # Extract source and destination MAC addresses for non-RTS/CTS frames
    all_pairs = set(zip(df['wlan.ta'], df['wlan.ra']))
    non_rts_pairs = all_pairs - rts_pairs

    return rts_pairs, non_rts_pairs

# Load the data from icsi525-S24_p1_trace.csv into a DataFrame
df = pd.read_csv("icsi525-S24_p1_qf.csv", index_col=None)

# Remove rows where either 'wlan.ta' or 'wlan.ra' is null
df = df.dropna(subset=['wlan.ta', 'wlan.ra'])

# Convert hexadecimal values to integers in 'wlan.fc.type_subtype' column
df['wlan.fc.type_subtype'] = df['wlan.fc.type_subtype'].apply(lambda x: int(x, 16))

# Round frame.time_relative to the nearest second
df['time_second'] = df['frame.time_relative'].round()

rts_pairs, non_rts_pairs = analyze_rts_cts_pairs(df)

# Group DataFrame by source and destination MAC addresses
grouped_client_df = df.groupby(['wlan.ta', 'wlan.ra'])

# Group DataFrame by source and destination MAC addresses
grouped_time_df = df.groupby(['time_second'])

# Initialize lists to store data for scatter plot
rts_scatter_data = {'time_second': [], 'throughput': []}
non_rts_scatter_data = {'time_second': [], 'throughput': []}

for time, group_time_df in grouped_time_df:
    rts_group_df = group_time_df[group_time_df.apply(lambda row: (row['wlan.ta'], row['wlan.ra']) in rts_pairs, axis=1)]
    non_rts_group_df = group_time_df[group_time_df.apply(lambda row: (row['wlan.ta'], row['wlan.ra']) in non_rts_pairs, axis=1)]

    rts_throughput = rts_group_df['frame.len'].sum() / rts_group_df['wlan_radio.duration'].sum() if not rts_group_df.empty else 0
    non_rts_throughput = non_rts_group_df['frame.len'].sum() / non_rts_group_df['wlan_radio.duration'].sum() if not non_rts_group_df.empty else 0

    rts_scatter_data['time_second'].append(time)
    rts_scatter_data['throughput'].append(rts_throughput)

    non_rts_scatter_data['time_second'].append(time)
    non_rts_scatter_data['throughput'].append(non_rts_throughput)
    
# Create scatter plot for RTS/CTS pairs throughput
plt.scatter(rts_scatter_data['time_second'], rts_scatter_data['throughput'], label='RTS/CTS Clients', alpha=0.8, s=10)

# # Create scatter plot for non-RTS/CTS pairs throughput
plt.scatter(non_rts_scatter_data['time_second'], non_rts_scatter_data['throughput'], label='Non-RTS/CTS Clients', alpha=0.8, s=10)

plt.xlabel('Time (Seconds)')
plt.ylabel('Average Throughput')
plt.title('Throughput Comparison between \n RTS/CTS and Non-RTS/CTS Clients over Time')
plt.legend()
# plt.show()

# Save plot
plt.savefig("plot.png", dpi=300)  # Save as PNG with higher resolution
