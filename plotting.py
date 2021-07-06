import matplotlib.pyplot as plt
import pandas as pd
import rsi
import sys

# copied from eval.py
def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

# takes prcHist as a numpy array
# stock_indx as the instrument of interest
# list of metrics as a list of functions which return an array of metric data from a column
# list of corresponding metric names, for legend
def plot_instance(prcHist, stock_indx, list_of_metrics=None, metric_names=None):
    
    df = pd.DataFrame(prcHist[stock_indx])

    plot_a = plt.figure(1)
    
    plt.plot(prcHist[stock_indx], label="price")
    
    # compute metrics and store in the df
    for i, metric in enumerate(list_of_metrics):
        metric_name = metric_names[i]
        
        # compute metric on data
        metric_data = metric(df[0])

        # store in df
        df[metric_name] = metric_data
        
        # plot
        plt.plot(df[metric_name], "--", label=metric_name)
    
    plt.legend()
    plt.xlabel("date")
    plt.ylabel("$ price")
    plt.title(f"Stock: {stock_indx}")
    #plt.show()

# takes prcHist as numpy array
# stock_indx as the instrument of interest
def plot_rsi_instance(prcHist, stock_indx):
    x = []
    plot_b = plt.figure(2)
    # generate rsi values for each day
    for i in range(0, 250):
        if i == 0:
            x.append(50)
            continue
        prcHistSoFar = prcHist[:,:i]
        x.append(rsi.ins_rsi(prcHistSoFar[stock_indx], 14))
    
    plt.plot(x, label='RSI')
    plt.axhline(y=30, color = 'r', linestyle = '-')
    plt.axhline(y=70, color = 'r', linestyle = '-')

    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.title(f"RSI of Stock: {stock_indx}")

    



# example with SMA function
def SMA(data, window):
    return pd.DataFrame(data)[0].rolling(window=window).mean()


if __name__ == '__main__':
    nInst, nt = 0, 0
    prcHist = loadPrices("prices250.txt")

    plot_instance(prcHist, 15, [lambda x : SMA(x, 10)], ["SMA10"])
    plot_rsi_instance(prcHist, 15)
    plt.show()