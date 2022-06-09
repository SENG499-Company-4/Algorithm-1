"""
Processes spreadsheet file to parse out preferences into pandas dataframe

"""

import pandas as pd
from server import Preference, Professor
import itertools

def process_spreadsheeet() -> list[Professor]:
    """
    Turns spreadsheets into dataframes
    
    Return list of Prof-Preference objects
    """
    df = pd.read_excel("tp.xlsx")
    df = df.iloc[0:33,:25] # filter out the excess data

    prof_list = []

    for row in df.itertuples():
        # create preference list
        pref_list = []  
        # misc data shaping
        d = row._asdict()
        d = dict(itertools.islice(d.items(),2, len(d.items())))
        # iterate through row in spreadsheet
        for course in d:
            Preference(course, d[course], "") # create a new preference
        prof = row.Instructor
        pref_list.append(Preference)
        prof_list.append(Professor(pref_list, prof, 0,0,0))
        
    return prof_list