# tshark -r icsi525-S24_p1_trace.pcapng -T fields -e wlan.ta -e wlan.ra -e wlan_radio.data_rate -e wlan_radio.signal_dbm -e wlan_radio.noise_dbm -e wlan_radio.snr -e frame.time_relative -e wlan.fc.type -E separator=, -E header=y > icsi525-S24_p1_qc.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set font size globally for all plots
plt.rcParams.update()

def find_unique_data_rates(df):
    # Group by 'wlan.ta' and count unique 'wlan_radio.data_rate' values for each transmitter address
    count = df.groupby(['wlan.ta', 'wlan.ra'])['wlan_radio.data_rate'].nunique().reset_index()
    
    # Filter out rows where the count is greater than 1
    return count[count['wlan_radio.data_rate'] > 1]

# Load the data from icsi525-S24_p1_trace.csv into a DataFrame
df = pd.read_csv("icsi525-S24_p1_qc.csv", index_col=None)

# Remove rows where either 'wlan.ta' or 'wlan.ra' is null
df = df.dropna(subset=['wlan.ta', 'wlan.ra'])

# Round frame.time_relative to the nearest second
df['time_second'] = df['frame.time_relative'].round()

# Iterate over each unique MAC address and create scatter plot
for mac_address in find_unique_data_rates(df)[['wlan.ta', 'wlan.ra']].itertuples(index=False):
    print(mac_address)
    # Filter the DataFrame for the specific MAC address
    filtered_df = df[(df['wlan.ta'] == mac_address[0]) & (df['wlan.ra'] == mac_address[1])]

    # Group the filtered DataFrame by 'time_second' and calculate mean data rate and SNR in each group
    grouped_df = filtered_df.groupby('time_second').agg({'wlan_radio.data_rate': 'mean', 'wlan_radio.snr': 'mean'})

    # Clear previous plot
    plt.clf()

    fig, ax1 = plt.subplots(figsize=(8, 4)) 

    # Create the first y-axis for Data Rate
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Data Rate (Mbps)')
    line1, = ax1.plot(grouped_df.index, grouped_df['wlan_radio.data_rate'], color='tab:blue', label='Data Rate', linewidth=0.7 )
    ax1.tick_params(axis='y')
    # ax1.set_ylim(bottom=0)

    # Create the second y-axis for SNR
    ax2 = ax1.twinx()  
    ax2.set_ylabel('SNR (dB)')
    line2, = ax2.plot(grouped_df.index, grouped_df['wlan_radio.snr'], color='tab:orange', label='SNR', linewidth=0.7 )
    ax2.tick_params(axis='y')
    # ax2.set_ylim(bottom=0)

    # Set title and legend
    plt.title('Data Rate and SNR over Time')
    fig.tight_layout()
    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    plt.legend(lines, labels)

    # Save plot
    plt.savefig(f"data_rate_change_clients/plot_mac_{mac_address[0]}_to_{mac_address[1]}_data_rate_and_snr.png", dpi=300)  # Save as PNG with higher resolution
