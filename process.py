"""
Processes preferences spreadsheet file
"""

import itertools
import json
import pandas as pd
from models import Preference, Professor
import numpy as np

pref_conversion = {0:0, 20:1, 39:2, 40:3, 78:4, 100:5, 195:6}

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
                    "course_num": course,
                    "preference_num": pref_conversion[int(d[course])],
                    "term": "",
                }
                pref_list.append(Preference(**pref_data))  # create a new preference
            prof = row.Instructor
            prof_data = {
                "preference_list": pref_list,
                "display_name": prof,
                "fall_term_courses": 0,
                "spring_term_courses": 0,
                "summer_term_courses": 0,
            }
            prof_list.append(Professor(**prof_data))

            p_list.append(prof)

        li = repr(prof_list)
        json_str = json.dumps(li)

        return json_str


    def preference_list:
        p_list = {}
        df = pd.read_excel("tp.xlsx")
        df = df.iloc[0:33, :25]  # filter out the excess data

        prefs = {}

        for row in df.itertuples():
            prof = row.Instructor
            prefs[prof] = {}
            # create preference list
            pref_list = []
            # misc data shaping
            d = row._asdict()
            d = dict(itertools.islice(d.items(), 2, len(d.items())))
            # iterate through rows in spreadsheet
            for course in d:
                pref_data = {
                     course : pref_conversion[int(d[course])]
                }
                pref_list.append(Preference(**pref_data))  # create a new preference
           
            prof_data = {
                "preference_list": pref_list,
                "display_name": prof,
                "fall_term_courses": 0,
                "spring_term_courses": 0,
                "summer_term_courses": 0,
            }
            prof_list.append(Professor(**prof_data))

            p_list.append(prof)


    def teacher_list():
        t_list = []
        df = pd.read_excel("tp.xlsx")
        df = df.iloc[0:33, :25]  # filter out the excess data

        for row in df.itertuples():
            prof = row.Instructor
            t_list.append(prof)


        return t_list
    
    def course_list(): 
        c_list = []
        df = pd.read_excel("tp.xlsx")
        df = df.iloc[0:33, :25]  # filter out the excess data

        for row in df.itertuples():
            d = row._asdict()
            d = dict(itertools.islice(d.items(), 2, len(d.items())))
            # iterate through rows in spreadsheet
            for course in d:
                if course not in c_list:
                    c_list.append(course)

        return c_list

    
    def course_prof_matrix(courses = course_list(), profs = teacher_list()):
        n_courses = len(courses)
        n_profs = len(profs)
        pref_matrix = np.array(shape=(n_courses, n_profs))
        for course in range(n_courses): 
            for prof in range(n_profs): 
                #Preference for match 
                preference = profs
                pref_matrix[course][prof] = 


if __name__ == "__main__":
    print("TEACHERS")
    t_list = Process.teacher_list()
    print(t_list)
    print(len(t_list))

    print("\nCOURSES")
    c_list = Process.course_list()
    print(c_list)
    print(len(c_list))


