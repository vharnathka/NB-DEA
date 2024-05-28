#!/usr/bin/env python

import argparse
import sys
import os
import rpy2.robjects as robjects

def main():
    parser = argparse.ArgumentParser(
        prog="nb-dea",
        description="Command-script to perform differential expression analysis"
    )
    
    #Input 
    #parser.add_argument("nb-dea", help="Whatever Whatever", \
    #                    type=str)

    parser.add_argument("input_file1", help="Contains filenames of samples with transcript abundance Condition A", type=str)
    parser.add_argument("input_file2", help="Contains filenames of samples with transcript abundance Condition B", type=str)

    #Output
    parser.add_argument("-o", "--out", help="write output to file. " \
                        "Default: stdout", metavar="FILE", type=str, \
                        required=False)

    #Other Options
    parser.add_argument("-m", "--model", \
                        help="model you want to use", \
                        type=str, required=False)

    parser.add_argument("-f", "--filter", \
                        help="lowest count you want to use", \
                        type=str, required=False)

    #Parse args
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

    robjects.r.source("inputter.R")
    perform_txiimport = robjects.globalenv['perform_tximport']

    files = file_names_A + file_names_B
    print(files)

if __name__ == "__main__":
    main()