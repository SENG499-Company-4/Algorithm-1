"""Algorithm 1 Generation Output"""

from calendar import c
from .models import *
from .dummy import rand_assignment
import numpy as np


def matrixToSchedule(matrix, profs, courses, courseMatcher, profMatcher, term): 
  """
  matrixToSchedule: Takes resultant professor-course assignment matrix and outputs schedule
  Arguments
  @param matrix : P x C matrix representing professor-course assignments
      cells with 1 correspond to assignments 
  @param profs : list of P professor displayNames corresponding to indicies of matrix rows
  @param courses: list of C courseIDs corresponding to indicies of matrix columns
  @param courseMatcher: dictionary that maps courseID to corresponding Course Object 
  @param profMatcher: dictionary that maps  prof names to  Professor object
  @param term : string indicating which term was generated ["FALL", "SPRING", "SUMMER"]

  return Schedule Object where list corresponding to term is populated, other terms are empty lists 
  """
  scheduledCourses = []
  n_courses = len(courses)

  matrix_t = np.transpose(matrix) # Transpose matrix to get arrays of courses

  for course_idx in range(n_courses): 
    #Find Professor index for course
    prof_idx = np.where(matrix_t[course_idx] == 1)[0][0] #index where course[prof] == 1

    #Corresponding professor object
    profID = profs[prof_idx]
    prof = profMatcher[profID] 

    #Get corresponding course object
    courseID = courses[course_idx]
    course = courseMatcher[courseID] 

    courseObj = createCourse(course, prof, rand_assignment()) #TODO: Actual Assignments for courses
    scheduledCourses.append(courseObj)
    print(f"Prof {courseObj.prof.displayName} is teaching {courseObj.subject} {courseObj.courseNumber} {courseObj.sequenceNumber}")

  #Return schedule for given term, other terms are empty
  fall = []
  summer = []
  spring = []

  if term == 'FALL':
    fall = scheduledCourses
  elif term == "SPRING":
    spring == scheduledCourses
  elif term == "SUMMER":
    summer = scheduledCourses

  return Schedule(
    fallCourses=fall,
    springCourses=spring,
    summerCourses=summer
  )

  
def createCourse(course: Course, prof:Professor, time:Assignment):
  """
  Create new course object for course prof and assigmnent information

  Arguments
  @param course : corresponding Course object provided from input
  @param prof : Professor object for prof to be scheduled
  @param time : Assignment object for course-prof assignment

  @return Course object representing assignment
  """
  #Handle incrementing sequence Number
  section = "A0" + str(course.numSections)
  course.numSections = course.numSections - 1 #Decrement Course Object Sections

  return Course(
    courseNumber=course.courseNumber,
    subject=course.subject,
    sequenceNumber=section,
    streamSequence=course.streamSequence,
    courseTitle=course.courseTitle,
    assignment=time,
    prof = prof,
    courseCapacity=course.courseCapacity,
    numSections=1
    )

    
