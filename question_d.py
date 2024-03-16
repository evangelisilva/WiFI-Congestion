#tshark -r icsi525-S24_p1_trace.pcapng -T fields -E separator=\ -e frame.time_relative -e wlan_radio.snr > snr.txt
import pandas as pd
import matplotlib.pyplot as plt

def snr(input):
    df = pd.read_csv(input, sep='\\')
    df['time'] = df['time'].astype(int)
    df['bin'] = pd.cut(df['snr'], [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    bar = df['bin'].value_counts().sort_index().plot.bar()
    bar.set_title('SNR Distribution')
    bar.set_xlabel('SNR')
    bar.set_ylabel('Frequency')
    plt.show()

snr('snr.txt')