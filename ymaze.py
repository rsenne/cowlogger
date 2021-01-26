#!/usr/bin/env python3
"""
this program is meant to work with the hand-scoring software 'cowlogger' when used in conjunction with the Y-maze test.
The purpose of this program is to calculate the (m)/(n-1) ratio, where m is the total number of times a mouse visits all
three arms of the Y-maze in a non-repeating fashion i.e. the permutation of arm visits, and where N is the total number
of arm visits.
"""

__author__ = "Ryan Senne"
__version__ = "0.1.0"
__license__ = "MIT"

import pandas as pd
import os


def ymazecount(filepath):
    # the next line was used as a test, i'm leaving it in
    # ymazedata = 'ABBBAAABAAABCCBACBAAACBCBACBACBA'
    # read your cowlog data as a string
    # i'm aware how this is an incredibly inelegant solution and i should have avoided the str datatype
    # lucky for me this works and that's all that matters to me
    ymazedata = pd.read_csv(filepath, header=None, dtype=str, usecols=[1], skiprows=1)
    ymazedata = ymazedata.transpose()
    ymazedata = ymazedata.to_string()
    ymazedata = ymazedata.replace(" ", "")
    ymazedata = ''.join(i for i in ymazedata if not i.isdigit())
    ymazedata = ymazedata.strip()  # remove that pesky trailing whitespace
    # this drops the first arm entry
    ymazedata = ymazedata[1:]
    print(ymazedata)
    # this is hardcoded as these permutations should never change
    # i'm calling these codons because it seemed analagous
    codons = ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']
    # i know dictionaries aren't fast, i also know this isn't even needed, but i slightly misunderstood the y-maze test
    # at first so i originally thought it was necessary., Empty dictionary to store counts later
    codon_counts = {}
    # the actually important for loop, basically this simply counts the amount of times each "codon" appears in cowlog
    for codon in codons:
        count = ymazedata.count(codon)
        codon_counts[codon] = count
    m = sum(codon_counts.values())  # total number of codons
    n = len(ymazedata)  # no need to subtract 1, already sliced
    y_maze_ratio = m / n  # calculate y-maze ratio
    return y_maze_ratio


# batch process files
def main():
    results = []  # list of ratios
    filepaths = []  # list of filenames
    my_dir = os.getcwd()  # get your working directory
    my_items = os.listdir(my_dir)  # find all elements in working directory
    # find all csv files
    for file in my_items:
        if file.endswith(".csv"):
            filepaths.append(file)
    # batch process all files
    for csv in filepaths:
        my_ratio = ymazecount(csv)
        results.append(my_ratio)
    final_results = {'Animal': filepaths, 'Ratio': results}  # dictionary that will store all ratios for each animal
    df = pd.DataFrame(final_results, columns=('Animal', 'Ratio'))  # create dataframe of results
    df.to_csv('y_maze_final')  # write to working directory, i can add a statement if you want to save elsewhere


if __name__ == "__main__":
    main()
