"""
Processes preferences spreadsheet file
"""

import itertools
import json
import pandas as pd
from .models import Preference, Professor
import numpy as np

pref_conversion = {0:0, 20:1, 39:2, 40:3, 78:4, 100:5, 195:6}

class Process:   
    @staticmethod
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
        
        # Serialize Pydantic models using built-in json method
        json_str = json.dumps(prof_list, default=lambda o: o.json())

        return json_str

    @staticmethod
    def preference_list():
        '''
        Gets preference list from spreadsheet data
        Return: Dictionary of profs and courses and preferences
        prefs[displayName][courseNum] = preference
        '''
        p_list = {}
        df = pd.read_excel("tp.xlsx")
        df = df.iloc[0:33, :25]  # filter out the excess data

        prefs = {}

        for row in df.itertuples():
            prof = row.Instructor
            prefs[prof] = {}
            # create preference list
            d = row._asdict()
            d = dict(itertools.islice(d.items(), 2, len(d.items())))
            # iterate through rows in spreadsheet
            for course in d:
                preference = pref_conversion[int(d[course])] # Converts preferences to range [0,6]
                prefs[prof][course] = preference
        return prefs

    @staticmethod
    def professor_list():
        """
        Returns list of professors from excel spreadsheet
        """
        p_list = []
        df = pd.read_excel("tp.xlsx")
        df = df.iloc[0:33, :25]  # filter out the excess data

        for row in df.itertuples():
            prof = row.Instructor
            p_list.append(prof)

        return p_list
    
    @staticmethod
    def course_list(): 
        """
        Returns list of courses from spreadsheet
        """
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

    @classmethod
    def course_prof_matrix(cls, course_list=None, prof_list=None, pref_list=None):
        """Creates a Professor Preference Matrix 

        Arguments:
            course_list - List of C courses to schedule 
            prof_list - List of P professors to schedule
            pref_list - Preferences of profs for courses
                dictionary format prefs[prof_display_name][course_num]

        return: P x C matrix with professor preferences ranging from [0,6]
        """

        if course_list is None:
            course_list = cls.course_list()

        if prof_list is None:
            prof_list = cls.professor_list()

        if pref_list is None:
            pref_list = cls.preference_list()

        n_courses = len(course_list)
        n_profs = len(prof_list)
        pref_matrix = np.zeros((n_profs, n_courses))
        for prof_index in range(n_profs): 
            for course_index in range(n_courses):
                #Preference for match 
                preference = pref_list[prof_list[prof_index]][course_list[course_index]]
                pref_matrix[prof_index][course_index] = preference

        return pref_matrix


if __name__ == "__main__":
    #Testing Output...
    logger.debug("TEACHERS")
    t_list = Process.professor_list()
    logger.debug(t_list)
    logger.debug(len(t_list))

    logger.debug("\nCOURSES")
    c_list = Process.course_list()
    logger.debug(c_list)
    logger.debug(len(c_list))

    p_list = Process.preference_list()
    matrix = Process.course_prof_matrix()
    for i in range(matrix.shape[0]):
        logger.debug(matrix[i])
