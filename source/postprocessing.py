import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import io

def grep(file: str, pattern: str) -> str:
    out = io.StringIO()
    data_frame = io.StringIO()
    file = open(file,"r")
    for line in file:
        if re.search(pattern, line):
            out.writelines(line)
    data = out.getvalue()
    for _ in data:
        data_frame.writelines(_) 
    out.close()
    return(data_frame)


def bands_plot(data,num_bands:int,kpoints:list[str]=None):
    data = pd.read_csv(data)
    data = data.T
    x = range(len(data.iloc[1]))
    for _ in range(num_bands):
        plt.scatter(x,data.iloc[_+6].astype(np.float64))
        plt.plot(x,data.iloc[_+6].astype(np.float64))
    if kpoints != None:
        points_in_between = (len(data.iloc[1])-len(kpoints))/(len(kpoints)-1)
        tick_locs = [i*points_in_between+i for i in range(len(kpoints))]
        plt.xticks(tick_locs,kpoints, size=16)
        plt.xlim([x[0], x[-1]])
        plt.ylabel('frequency (c/a)', size=16)
    return(data)
    #plt.show()
