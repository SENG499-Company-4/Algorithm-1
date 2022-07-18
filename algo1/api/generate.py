""" Algorithm 1 Schedule Generation"""

import logging
import numpy as np
import math

from .models import Professor, Course, ScheduleConstraints
from .output import matrixToSchedule
from ..prototype.random_search import random_search

#Max capacity for splitting sections
MAX_SECTION_CAPACITY = 200

logger = logging.getLogger(__name__)


def generateSchedule(input: ScheduleConstraints):
  """
  Parses Schedule Generation Input to prepare for Algorithm
  Creates Teacher/Preference Matrix and Professor Availabilities
  Currently only handles one term at a time -- Assumes only one term to schedule will be filled
  """

  if len(input.coursesToSchedule.fallCourses) != 0:
    term = 'FALL'
    courseInput = input.coursesToSchedule.fallCourses

  elif len(input.coursesToSchedule.springCourses) != 0:
    term = 'SPRING'
    courseInput = input.coursesToSchedule.springCourses

  elif len(input.coursesToSchedule.summerCourses) != 0:
    term = 'SUMMER'
    courseInput = input.coursesToSchedule.summerCourses

  courses = parseCourses(courseInput) #course IDs
  courseMatcher = matchCourseID(courseInput) #courseID to Course object 
  
  profs = parseProfs(input.professors) #professor names
  profMatcher = matchProfName(input.professors) #professor name to Professor object

  prefs = parseProfPrefs(input.professors) #dictionary of prof preferences
  avails = parseProfAvailability(input.professors, term) # Array of max courses to schedule
  matrix = profPrefMatrix(profs, prefs, courses) #Professor preference matrix for courses

  testPrint(profs, prefs, courses, avails, matrix)

  #Run algorithm on teacher preference matrix
  try:
    output = random_search(matrix, avails)
  except Exception as e:
    logger.error(f"Failed generating Schedule: {e}")
    return None

  #Convert algorithm output to Schedule object
  try:
    schedule = matrixToSchedule(output, profs, courses, courseMatcher, profMatcher, term)
  except Exception as e:
    logger.error(f"Failed parsing generated schedule: {e}")
    return None

  return schedule


def parseCourses(courses: list[Course]):
  '''
  List of courses to schedule -- splits into multiple sections
  '''
  courseList = []

  for course in courses:
    #Split Sections based on Capacity if not set
    if course.numSections == 0:
      course.numSections = math.ceil(course.courseCapacity / MAX_SECTION_CAPACITY)

      if course.numSections == 0:
        course.numSections = 1
        
      course.courseCapacity = math.ceil(course.courseCapacity / course.numSections) #Split capacity evenly amongst sections

    courseID = course.subject + course.courseNumber

    for i in range(course.numSections):
      courseList.append(courseID)

  return courseList

def matchCourseID(courses: list[Course]):
  """
  Returns dictionary for parsing courseID to other attributes
  """
  courseDict = {}

  for course in courses:
    courseID = course.subject+course.courseNumber
    courseDict[courseID] = course

  return courseDict

def parseProfs(profs: list[Professor]):
  '''
  Gets list of profesor display names
  '''
  prof_list = []

  for prof in profs:
    prof_list.append(prof.displayName)

  return prof_list

def parseProfPrefs(profs: list[Professor]):
  '''
  Dictionary of professor preferences prefs[prof.displayName][courseNum] = preference
  e.g prefs["Bill Bird"]["CSC116"] = 6
  '''
  preferences = {}

  for prof in profs:
    pref = {}

    for course in prof.preferences:
      pref[course.courseNum] = course.preferenceNum

    preferences[prof.displayName] = pref

  return preferences


def matchProfName(profs: list[Professor]):
  """
  Returns dictionary for matching professor name to professor object
  """
  profDict = {}
  for prof in profs:
    profDict[prof.displayName] = prof

  return profDict

def parseProfAvailability(profs: list[Professor], term: str):
  """
  Creates an array holding maximum courses a prof can be scheduled a given term
  Indices correspond to professor array
    Arguments
      profs - list of P Professors 
      term - string of term ["FALL", "SPRING", "SUMMER"]
    Return: Array of P integers corresponding to maximum course load
  """
  nCourses = []
  for prof in profs:
    if term == 'FALL':
      nCourses.append(prof.fallTermCourses)

    elif term == 'SPRING':
      nCourses.append(prof.springTermCourses)

    elif term == 'SUMMER':
      nCourses.append(prof.summerTermCourses)

  return nCourses


def profPrefMatrix(profs: list[str], prefs: dict, courses = list[str]):
  """
  Creates a Professor Preference Matrix 
        Arguments:
            profs - List of P professors to schedule
            prefs - Preferences of profs for courses
                dictionary format prefs[prof_display_name][course_num]
            courses - List of C course sections to schedule e.g "CSC116"
                      Duplicates correspond to multiple sections

        return: P x C matrix with professor preferences ranging from [0,6]
  """
  n_profs = len(profs)
  n_courses = len(courses)
  prefMatrix = np.zeros((n_profs, n_courses), dtype=np.int32)

  for prof_index in range(n_profs): 
    for course_index in range(n_courses): 
      #preference for match 
      prof = profs[prof_index]
      course = courses[course_index]
      pref = prefs[prof].get(course)

      if pref is None:
        pref = 0

      prefMatrix[prof_index][course_index] = int(pref)

  return prefMatrix

def testPrint(profs, prefs, courses, avails, matrix):
  """
  For debugging purposes >:) 
  """
  logger.debug("PARSING INPUT")
  logger.debug(f"PROFS: {profs}")
  logger.debug(f"PREFS: {prefs}")
  logger.debug(f"AVAILABILITY: {avails}")
  logger.debug(f"COURSES: {courses}")
  logger.debug("MATRIX:")
  for i in range(matrix.shape[0]):
    logger.debug(matrix[i])
