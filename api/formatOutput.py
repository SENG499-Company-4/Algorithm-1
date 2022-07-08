from calendar import c
from .models import *
from .dummy import rand_assignment
import numpy as np



def matrixToSchedule(matrix, profs, courses, courseMatcher, profMatcher, term): 
  scheduledCourses = []
  n_courses = len(courses)

  matrix_t = np.transpose(matrix) # Transpose matrix to get arrays of courses

  for course_idx in range(n_courses): 
    #Find Professor index for course
    prof_idx = np.where(matrix_t[course_idx] == 1)
    profID = profs[prof_idx]
    prof = profMatcher[profID]

    courseID = courses[course_idx]
    course = courseMatcher[courseID]

    courseObj = createCourse(course, prof, rand_assignment())
    scheduledCourses.append(courseObj)

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
  Create new course object using provided fields and calculated assignment
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

    
