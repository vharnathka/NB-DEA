import sys
import pandas as pd

def PREPROCESS(samplenumA, samplenumB):
    og_input = pd.read_csv("nb-deainput.csv", index_col=0)
    
    samplestotal = samplenumA+samplenumB
    counts = og_input.iloc[:, samplestotal: 2*samplestotal]
    avglength = og_input.iloc[:, 2*samplestotal: 3*samplestotal]
    
    return counts, avglength