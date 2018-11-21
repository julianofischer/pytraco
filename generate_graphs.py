# -*- coding: future_fstrings -*-
import os.path
import pandas as pd
import gc

# import numpy as np
# import matplotlib.pyplot as plt
import matplotlib as mpl
import os, psutil
from sys import getsizeof

def usage():
    process = psutil.Process(os.getpid())
    return process.memory_info()[0] / float(2 ** 20)


def smooth(df):
    return df.reindex(range(1, df.index.max()+1), method='ffill')


def main():
    for i in range(0, 73):
        if os.path.isfile(f'reachabilityt1d15.{i}.in'):
            df = pd.read_table(f'reachabilityt1d15.{i}.in', header=None, index_col=0)
            smoothed = smooth(df)
            myplot = smoothed.plot()
            myplot.set_xlabel("Time (s)")
            myplot.set_ylabel("Indegree")
            fig = myplot.get_figure()
            fig.savefig(f'{i}.in.png')
            print(usage())
            del [[fig, myplot, smoothed, df]]
            gc.collect()
            #print(f"getsizeof fig:{fig} myplot:{myplot} smoothed:{smoothed} df:{df}")
            print(usage())


if __name__ == '__main__':
    mpl.use('Agg')
    main()
