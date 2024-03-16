#tshark -r icsi525-S24_p1_trace.pcapng -T fields -E separator=\ -e frame.time_relative -e wlan.fc -e frame.len > output.txt
import pandas as pd
import matplotlib.pyplot as plt


def throughputANDutilization(input):
    df = pd.read_csv(input, sep='\\')
    df['Time'] = df['Time'].astype(int)

    #Utilization
    dfutil = df.groupby(['Time']).sum()
    dfutil['Utilization'] = dfutil['Duration'].div(10000)
    dfutil['mbps'] = dfutil['Size'].div(1000000)
    dfutil.plot(y='Utilization', ylabel='Percent Utilization', xlabel='Time (s)', title='Channel Utilization', legend=False)
    plt.show()
    dfutil.plot(y='mbps', ylabel='Throughput (mbps)', xlabel='Time (s)', title='Throughput over Time', legend=False)
    plt.show()

    #Throughput
    dfthroughput = dfutil
    dfthroughput['Utilization'] = dfthroughput['Utilization'].astype(int)
    dfthroughput = dfthroughput.groupby(['Utilization']).mean()
    plt.plot(dfthroughput.index, dfthroughput['mbps'], '-o')
    plt.xlabel('Percent Utilization')
    plt.ylabel('Throughput (mbps)')
    plt.title('Channel Throughput at corresponding Utilization')
    plt.show()
    print(dfthroughput)

throughputANDutilization('output.txt')