# tshark -r icsi525-S24_p1_trace.pcapng -T fields -e wlan.fc.type_subtype -E separator=, -E header=y > icsi525-S24_p1_qb.csv

import pandas as pd

# Load the data from icsi525-S24_p1_trace.csv into a DataFrame
df = pd.read_csv("icsi525-S24_p1_qb.csv", index_col=None)

# Convert hexadecimal values to integers in 'wlan.fc.type_subtype' column
df['wlan.fc.type_subtype'] = df['wlan.fc.type_subtype'].apply(lambda x: int(x, 16))

# Define all subtype labels
all_subtype_labels = {
    27: 'Ready To Sends (RTS)',
    28: 'Clear To Sends (CTS)'
}

# Initialize counts for all subtypes, including zero counts
subtype_counts_all = {label: 0 for label in all_subtype_labels.values()}

# Calculate the counts of wlan.fc.type_subtype
subtype_counts = df['wlan.fc.type_subtype'].map(all_subtype_labels).value_counts()

# Update the counts dictionary with actual counts
subtype_counts_all.update(subtype_counts)

# Print the counts
for subtype, count in subtype_counts_all.items():
    print(f"{subtype}: {count}")