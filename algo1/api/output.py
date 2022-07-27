"""Algorithm 1 Generation Output"""

import logging

import numpy as np

from .dummy import rand_block
from .models import Schedule, Course, Professor, Assignment
from .times import Times

logger = logging.getLogger(__name__)


def tensor_to_semester(tensor, profs, courses, courses_by_id, profs_by_name):
    # tensor = {(course_i, time_j, teacher_k) : pref}

    scheduled_courses = []

    for course_idx, time_idx, prof_idx in tensor:
        # Corresponding professor object
        prof_name = profs[prof_idx]
        prof = profs_by_name[prof_name]

        # Get corresponding course object
        courseID = courses[course_idx]
        course = courses_by_id[courseID]

        time = Times[time_idx]

        course_obj = create_course(course, prof, time)
        scheduled_courses.append(course_obj)
        logger.debug(
            f"Prof {course_obj.prof.displayName} is teaching "
            f"{course_obj.subject} {course_obj.courseNumber} "
            f"{course_obj.sequenceNumber}")

    return scheduled_courses


def matrix_to_schedule(matrix, profs, courses, course_by_id,
                       profMatcher, term):
    """
    matrix_to_schedule: Takes resultant professor-course assignment matrix and
                      outputs schedule
    Arguments
    @param matrix : P x C matrix representing professor-course assignments
            cells with 1 correspond to assignments
    @param profs : list of P professor displayNames corresponding to indicies
                   of matrix rows
    @param courses: list of C courseIDs corresponding to indicies of matrix
                    columns
    @param course_by_id: dictionary that maps courseID to corresponding Course
                          Object
    @param profMatcher: dictionary that maps  prof names to  Professor object
    @param term : string indicating which term was generated
                  ["FALL", "SPRING", "SUMMER"]

    return Schedule Object where list corresponding to term is populated, other
           terms are empty lists
    """

    scheduled_courses = []
    n_courses = len(courses)

    # Transpose matrix to get arrays of courses
    matrix_t = np.transpose(matrix)

    for course_idx in range(n_courses):
        # Find Professor index for course
        # index where course[prof] == 1
        prof_idx = np.where(matrix_t[course_idx] == 1)[0][0]

        # Corresponding professor object
        profID = profs[prof_idx]
        prof = profMatcher[profID]

        # Get corresponding course object
        course_id = courses[course_idx]
        course = course_by_id[course_id]

        # TODO: Actual Assignments for courses
        time = rand_block(term)

        course_obj = create_course(course, prof, time)
        scheduled_courses.append(course_obj)
        logger.debug(
            f"Prof {course_obj.prof.displayName} is teaching "
            f"{course_obj.subject} {course_obj.courseNumber} "
            f"{course_obj.sequenceNumber}")

    # Return schedule for given term, other terms are empty
    fall = []
    summer = []
    spring = []

    if term == "FALL":
        fall = scheduled_courses
    elif term == "SPRING":
        spring = scheduled_courses
    elif term == "SUMMER":
        summer = scheduled_courses

    return Schedule(
        fallCourses=fall,
        springCourses=spring,
        summerCourses=summer
    )


def create_course(course: Course, prof: Professor, time: Assignment):
    """
    Create new course object for course prof and assigmnent information

    Arguments
    @param course : corresponding Course object provided from input
    @param prof : Professor object for prof to be scheduled
    @param time : Assignment object for course-prof assignment

    @return Course object representing assignment
    """

    # Handle incrementing sequence Number
    section = "A0" + str(course.numSections)
    # Decrement Course Object Sections
    course.numSections = course.numSections - 1

    return Course(
        courseNumber=course.courseNumber,
        subject=course.subject,
        sequenceNumber=section,
        streamSequence=course.streamSequence,
        courseTitle=course.courseTitle,
        assignment=time,
        prof=prof,
        courseCapacity=course.courseCapacity,
        numSections=1)
