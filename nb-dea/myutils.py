import sys
import pandas as pd
import numpy as np

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

def NORMALIZE(counts):
    ##using a geometric mean
    counts2 = counts.copy()
    arr_counts = counts2.to_numpy()
    arr_counts[arr_counts == 0] = 1

    pseudoref = np.prod(arr_counts, axis=1)**(1/samplestotal)
    counts2["Psuedo-Reference"] = pseudoref

    #ratios of each sample to reference
    for i in range(samplestotal):
        colname = counts.columns[i]
        counts2['ratio.' + str(i+1)] = counts2[colname]/counts2["Psuedo-Reference"]
        #median of each column is that sample's sizefactor
        median = counts2['ratio.' + str(i+1)].median()
    
        #divide by size factor
        counts[colname] = counts[colname]/median
    return counts