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


# this function was necessary because kaitlyn has difficulty spelling
def fix_kaitlyn_spelling(file_to_be_fixed):
    fxied_datfraame = pd.DataFrame(file_to_be_fixed)
    fixed_dataframe = fxied_datfraame.replace('Borrowing', "Burrowing")
    return fixed_dataframe


# this will hopefully score the newly separated cowlog data #
# I hard coded the time bins and the behavioral columns. If these change, you MUST fix them #
def score_behavior(behaved):
    CUTOFF = 2
    time_in_behavior = pd.DataFrame(data=np.zeros(shape=(5, 6)),
                                    index=['0-2 min', '2-4 min', '4-6 min', '6-8 min', '8-10 min'],
                                    columns=["Rearing", "Burrowing", "Freezing", "Grooming", "Center", "Darting"])
    start_time = behaved['time'][0]
    end_time_run = behaved['time'][0]
    for i in range(1,len(behaved['code'])):
        # Check if the behavior has switched (e.g. Freezing to Rearing)
        if behaved['code'][i] != behaved['code'][i-1]:
            time_in_behavior[behaved['code'][i-1]][behaved['discretion'][i-1]] += end_time_run - start_time
            start_time = behaved['time'][i]
            end_time_run = behaved['time'][i]
        # Check if the chunk of behavior has switched (e.g. two bouts of Freezing back to back, but separated by some time)
        elif behaved['time'][i] > behaved['time'][i-1] + CUTOFF:
            time_in_behavior[behaved['code'][i-1]][behaved['discretion'][i-1]] += end_time_run - start_time
            start_time = behaved['time'][i]
            end_time_run = behaved['time'][i]
        # Check if the behavior spans multiple time bins
        elif behaved['discretion'][i] != behaved['discretion'][i-1]:
            time_in_behavior[behaved['code'][i-1]][behaved['discretion'][i-1]] += end_time_run - start_time
            start_time = behaved['time'][i]
            end_time_run = behaved['time'][i]
        else:
            end_time_run = behaved['time'][i]
    return time_in_behavior

# I know i was lazy here, sue me
def main(read):
    a = bin_boi(read)
    b = fix_kaitlyn_spelling(a)
    c = score_behavior(b)
    return chavior(c)
    return d
