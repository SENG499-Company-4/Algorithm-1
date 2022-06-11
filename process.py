"""
Processes preferences spreadsheet file
"""

import itertools
import json
import pandas as pd
from models import Preference, Professor


class Process:
    def process_spreadsheet():
        """
        Turns spreadsheets into dataframes

        Return list of Prof-Preference objects
        """
        df = pd.read_excel("tp.xlsx")
        df = df.iloc[0:33, :25]  # filter out the excess data

        prof_list = []

        for row in df.itertuples():
            # create preference list
            pref_list = []
            # misc data shaping
            d = row._asdict()
            d = dict(itertools.islice(d.items(), 2, len(d.items())))
            # iterate through rows in spreadsheet
            for course in d:
                pref_data = {
                    "courseNum": course,
                    "preferenceNum": d[course],
                    "term": "",
                }
                pref_list.append(Preference(**pref_data))  # create a new preference
            prof = row.Instructor
            prof_data = {
                "prefs": pref_list,
                "displayName": prof,
                "requiredEquipment": [],
                "fallTermCourses": 0,
                "springTermCourses": 0,
                "summerTermCourses": 0,
            }
            prof_list.append(Professor(**prof_data))
        li = repr(prof_list)
        json_str = json.dumps(li)

        return json_str
