import sys
import pandas as pd

def PREPROCESS(samplenumA, samplenumB):
    og_input = pd.read_csv("nb-deainput.csv", index_col=0)
    
    samplestotal = samplenumA+samplenumB
    counts = og_input.iloc[:, samplestotal: 2*samplestotal]
    avglength = og_input.iloc[:, 2*samplestotal: 3*samplestotal]
    
    return counts, avglength


def FILTER(counts, avglength, threshold):
    counts['Total'] = counts.sum(axis=1)

    rows_to_drop = counts[counts['Total'] < threshold].index.tolist()

    counts.drop(rows_to_drop, inplace=True)
    counts.drop('Total', axis=1, inplace=True)

    avglength.drop(rows_to_drop, inplace=True)
    
    return counts, avglength