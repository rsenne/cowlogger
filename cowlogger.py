#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:53:46 2020

@author: ryansenne
"""
import pandas as pd
import numpy as np


# this is intended to speed up processing of cowlog files #
# make sure you have your files in your working directory #

# this will hopefully create equally spaced 120 second bins
def bin_boi(dem_files):
    bin_range = [0, 120, 240, 360, 480, 600]
    bin_labels = ['0-2 min', '2-4 min', '4-6 min', '6-8 min', '8-10 min']
    dem_files['discretion'] = pd.cut(dem_files['time'], bins=bin_range, labels=bin_labels)
    return dem_files

def fix_all_these_stupid_fucking_problems_jesus_christ(problematic_bullshit):
    fuck_this = pd.DataFrame(problematic_bullshit)
    srsly_fuck_this = fuck_this[fuck_this.time < 600]
    return srsly_fuck_this


# this function was necessary because kaitlyn has difficulty spelling
def fix_kaitlyn_spelling(file_to_be_fixed):
    fxied_datfraame = pd.DataFrame(file_to_be_fixed)
    fixed_dataframe = fxied_datfraame.replace('Borrowing', "Burrowing")
    fixed_dataframe_nanless = fixed_dataframe.dropna()
    fixed_dataframe_nanless = fixed_dataframe_nanless.sort_values(by=['time'], na_position='last')
    fixed_dataframe_nanless = fixed_dataframe_nanless[fixed_dataframe_nanless.time < 600]
    return fixed_dataframe_nanless

# this will hopefully score the newly separated cowlog data #
# I hard coded the time bins and the behavioral columns. If these change, you MUST fix them #
def score_behavior(behaved):
    time_in_behavior = pd.DataFrame(data=np.zeros(shape=(5, 6)),
                                    index=['0-2 min', '2-4 min', '4-6 min', '6-8 min', '8-10 min'],
                                    columns=["Rearing", "Burrowing", "Freezing", "Grooming", "Center", "Darting"],
                                    )
    start_time = behaved['time'][0]
    end_time_run = behaved['time'][0]
    i = 0
    j = 1
    while j < len(behaved['code']):
        if behaved['code'][i] == behaved['code'][j]:
            end_time_run = behaved['time'][j]
            j += 1
        elif behaved['code'][i] != behaved['code'][j]:
            time_in_behavior[behaved['code'][i]][behaved['discretion'][i]] += end_time_run - start_time
            i = j
            j = i + 1
            start_time = behaved['time'][i]
            end_time_run = start_time

    return time_in_behavior

# I know i was lazy here, sue me
def main(read):
    a = bin_boi(read)
    b = fix_all_these_stupid_fucking_problems_jesus_christ(a)
    c = fix_kaitlyn_spelling(b)
    d = score_behavior(c)
    return d
