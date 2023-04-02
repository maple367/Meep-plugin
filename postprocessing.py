import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def grep(file: str, pattern: str) -> str:
    out = ''
    with open(file,"r") as file:
        for line in file:
            if re.search(pattern, line):
                out = out + line
    return(out)


def bands_plot(data:str,num_bands:int,kpoints:list[str]=None,a=1):
    data = pd.read_csv(data)
    data = np.array(data)
    data = data.transpose(1,0)

    for _ in range(num_bands):
        plt.scatter(data[1],a/data[_+6].astype(np.float64))
        plt.plot(data[1],a/data[_+6].astype(np.float64))
    if kpoints != None:
        plt.xticks(range(1,len(data[1])+1,(len(data[1])-1)//(len(kpoints)-1)),kpoints)
    #plt.show()
