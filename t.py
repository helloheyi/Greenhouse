import pandas as pd
import numpy as np

d  = {'col1': [1, 2,4,5,6], 'col2': [3, 4,2,4,6]}
paths = pd.DataFrame(data=d)

## find max value
max2here = pd.expanding_max(paths)
dd2here = pd.DataFrame(data=paths).divide(max2here,axis=0) - 1
## axis=0 横竖 
dateIndex = paths.index
print(dateIndex)
freqIndex = dateIndex[0:len(dateIndex):int(1)]
print(freqIndex)
DF_freq = paths.loc[freqIndex] 
print(DF_freq)
print(DF_freq.corr())