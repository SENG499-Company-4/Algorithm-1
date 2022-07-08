from .models import *
import numpy as np

def parseInput(input: ScheduleConstraints):

  if len(input.coursesToSchedule.fallCourses) != 0:
    term == 'FALL'
    courses = parseCourses(input.coursesToSchedule.fallCourses)
  elif len(input.coursesToSchedule.springCourses) != 0:
    term = 'SPRING'
    courses = parseCourses(input.coursesToSchedule.springCourses)
  elif len(input.coursesToSchedule.summerCourses) != 0:
    term = 'SUMMER'
    courses = parseCourses(input.coursesToSchedule.summerCourses)
  
  profs = parseProfs(input.professors)
  prefs = parseProfPrefs(input.professors)
  avails = parseProfAvailability(input.professors, term)
  matrix = profPrefMatrix(profs, prefs, courses)
  #output = algorithm(prefs, avails)


def parseProfs(profs: list[Professor]):
  '''
  Gets list of profesor names 
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
    for course in prof.prefs:
      pref[course.courseNum] = course.preferenceNum
    preferences[prof.displayName] = pref

  return preferences

def parseCourses(courses: list[Course]):
  '''
  List of courses to schedule -- splits into multiple sections if needed
  '''
  #TODO: Handle splitting for capacity
  courseList = []
  for course in courses:
    courseID = course.subject + course.courseNumber
    courseList.append(courseID)

  return courseList

def parseProfAvailability(profs: list[Professor], term):
  nCourses = []
  for prof in profs:
    if term == 'FALL':
      nCourses.append(prof.fallTermCourses)
    elif term == 'SPRING':
      nCourses.append(prof.springTermCourses)
    elif term == 'SUMMER':
      nCourses.append(prof.summerTermCourses)

  return nCourses


def profPrefMatrix(profs, prefs, courses):
  n_profs = len(profs)
  n_courses = len(courses)
  prefMatrix = np.zeros(n_profs, n_courses)
  for prof_index in range(n_profs): 
    for course_index in range(courses): 
      #preference for match 
      prof = profs[prof_index]
      course = courses[course_index]

      pref = prefs[prof].get(course)
      if pref is None:
        pref = 0

      prefMatrix[prof_index][course_index] = pref

  return prefMatrix
