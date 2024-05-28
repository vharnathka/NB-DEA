#!/usr/bin/env python

import argparse
import sys
import os
import rpy2.robjects as robjects
from rpy2.robjects.vectors import StrVector
from . import myutils as myutils

def main():
    parser = argparse.ArgumentParser(
        prog="nb-dea",
        description="Command-script to perform differential expression analysis"
    )

    parser.add_argument("input_file1", help="Filename of samples with transcript abundance for Condition A", type=str)
    parser.add_argument("input_file2", help="Filename of samples with transcript abundance for Condition B", type=str)

    # Output
    parser.add_argument("-o", "--out", help="Write output to file. Default: stdout", metavar="FILE", type=str, required=False)

    # Other Options
    parser.add_argument("-m", "--model", help="Model you want to use", type=str, required=False)
    parser.add_argument("-f", "--filter", help="Lowest count you want to use", type=str, required=False)

    # Parse args
    args = parser.parse_args()
    #Setup output file
    if args.out is None:
        outf = sys.stdout
    else:
        outf = open(args.out, "w")

    #Load input files
    file_names_A = []
    file_names_B = []
    
    input_file = args.input_file1
    with open(input_file, 'r') as f:
        file_names_A = [line.strip() for line in f if line.strip()]  
        #Read non-empty lines

    input_file = args.input_file2
    with open(input_file, 'r') as f:
        file_names_B = [line.strip() for line in f if line.strip()]

    #getting the correct input format
    files = file_names_A + file_names_B
    samplenumA = len(file_names_A)
    samplenumB = len(filenames_B)
    
    condition1 = os.path.splitext(os.path.basename(args.input_file1))[0]
    condition2 = os.path.splitext(os.path.basename(args.input_file2))[0]
    condition1 = [condition1] * samplenumA
    condition2 = [condition2] * samplenumB
    
    conditions = condition1+condition2
    
    robjects.r.source("inputter.R")
    files_r = StrVector(files)
    conditions_r = StrVector(conditions)
    
    perform_tximport = robjects.globalenv['perform_tximport']
    perform_tximport(files, conditions_r)
    
    #Preprocessing:
    
    counts, avglength = myutils.PREPROCESS(samplenumA, samplenumB)

if __name__ == "__main__":
    main()