"""Algorithm 1 Schedule Generation"""

import logging
import math
import time

import numpy as np

from .times import Times
from .models import Professor, Course, ScheduleConstraints, Schedule
from .output import tensor_to_semester
from ..randopt.rand_opt import RandOpt

# Max capacity for splitting sections
MAX_SECTION_CAPACITY = 200

logger = logging.getLogger(__name__)


def generate_schedule(input: ScheduleConstraints):
    """Parses schedule generation input to prepare for algorithm

    Creates Teacher/Preference matrix and Professor availabilities. Currently
    only handles one term at a time -- assumes only one term to schedule will
    be filled.
    """

    terms = {"FALL": {}, "SPRING": {}, "SUMMER": {}}

    if len(input.coursesToSchedule.fallCourses) != 0:
        term = "FALL"
        fall_course_input = input.coursesToSchedule.fallCourses
        terms[term] = fall_course_input

    if len(input.coursesToSchedule.springCourses) != 0:
        term = "SPRING"
        spring_course_input = input.coursesToSchedule.springCourses
        terms[term] = spring_course_input

    if len(input.coursesToSchedule.summerCourses) != 0:
        term = "SUMMER"
        summer_course_input = input.coursesToSchedule.summerCourses
        terms[term] = summer_course_input

    prof_names = parse_profs(input.professors)
    profs_by_name = match_prof_name(input.professors)
    prefs = parse_prof_prefs(input.professors)

    semester_list = {"FALL": {}, "SPRING": {}, "SUMMER": {}}

    for term, semester in terms.items():
        # Array of max courses to schedule
        avails = parse_prof_availability(input.professors, term)
        course_ids = parse_courses(semester)
        courses_by_id = match_course_id(semester)
        pref_matrix = prof_pref_matrix(prof_names, prefs, course_ids)

        test_print(prof_names, prefs, course_ids, avails, pref_matrix)

        # Run algorithm on teacher preference matrix
        try:
            output = run_random_search(course_ids, Times, avails, pref_matrix)

        except Exception as e:
            logger.error(f"Failed generating Schedule: {e}")
            return None

        try:
            semester = tensor_to_semester(output, prof_names, course_ids,
                                          courses_by_id, profs_by_name)
            semester_list[term] = semester

        except Exception as e:
            logger.error(f"Failed parsing generated schedule: {e}")
            return None

    fall = semester_list["FALL"]
    spring = semester_list["SPRING"]
    summer = semester_list["SUMMER"]

    return Schedule(
        fallCourses=fall,
        springCourses=spring,
        summerCourses=summer)


def run_random_search(courses, times, avails, preferences):
    card_c, card_ti, card_te = (
        len(courses), len(times.items()), len(avails))
    dims = {"courses": card_c, "times": card_ti, "teachers": card_te}
    ro = RandOpt(dims, preferences, avails)

    max_runtime = 600
    start_time = time.time()
    while (time.time() - start_time) < max_runtime:
        ro = RandOpt(dims, preferences, avails)
        ro.solve()
        if ro.is_valid_schedule():
            break

    return ro.sparse()


def parse_courses(courses: list[Course]):
    """Parses raw course data
    
    Splits into multiple sections based on specified value.
    """
    
    courses = []

    for course in courses:
        # Split Sections based on Capacity if not set
        if course.numSections == 0:
            course.numSections = math.ceil(
                course.courseCapacity / MAX_SECTION_CAPACITY)

            if course.numSections == 0:
                course.numSections = 1

            course.courseCapacity = math.ceil(
                # Split capacity evenly amongst sections
                course.courseCapacity / course.numSections)

        course_id = course.subject + course.courseNumber

        for _ in range(course.numSections):
            courses.append(course_id)

    return courses


def match_course_id(courses: list[Course]):
    """Returns a dictionary for parsing course_id to other attributes"""

    courses_by_id = {}

    for course in courses:
        course_id = course.subject+course.courseNumber
        courses_by_id[course_id] = course

    return courses_by_id


def parse_profs(profs: list[Professor]):
    """Gets list of professor display names"""

    prof_list = []

    for prof in profs:
        prof_list.append(prof.displayName)

    return prof_list


def parse_prof_prefs(profs: list[Professor]):
    """Makes a 2D lookup table of professor preferences by professor name and
    course ID

    ```py
    prefs[prof.displayName][courseNum] = preference
    ```

    e.g `prefs["Bill Bird"]["CSC116"] = 6`
    """

    preferences = {}

    for prof in profs:
        pref = {}

        for course in prof.preferences:
            pref[course.courseNum] = course.preferenceNum

        preferences[prof.displayName] = pref

    return preferences


def match_prof_name(profs: list[Professor]):
    """Returns a dictionary for matching professor name to professor object"""
    
    profs_by_name = {}

    for prof in profs:
        profs_by_name[prof.displayName] = prof

    return profs_by_name


def parse_prof_availability(profs: list[Professor], term: str):
    """Makes an array of maximum courses a prof can be scheduled for term
    
    Indices correspond to professor array.
    
    Args:
        profs: list of P Professors
        term: string of term ["FALL", "SPRING", "SUMMER"]
    Returns:
        Array of P integers corresponding to maximum course load
    """

    num_courses = []
    for prof in profs:
        if term == "FALL":
            num_courses.append(prof.fallTermCourses)

        elif term == "SPRING":
            num_courses.append(prof.springTermCourses)

        elif term == "SUMMER":
            num_courses.append(prof.summerTermCourses)

    return num_courses


def prof_pref_matrix(profs: list[str], prefs: dict, courses=list[str]):
    """Creates a professor preference matrix
    
    Args:
        profs: List of P professors to schedule
        prefs: Preferences of profs for courses dictionary format
            `prefs[prof_display_name][course_num]`
        courses: List of C course sections to schedule e.g "CSC116"
            Duplicates correspond to multiple sections

    Returns:
        P x C matrix with professor preferences ranging from [0,6]
    """

    n_profs = len(profs)
    n_courses = len(courses)
    pref_matrix = np.zeros((n_profs, n_courses), dtype=np.int32)

    for prof_index in range(n_profs):
        for course_index in range(n_courses):
            # preference for match
            prof = profs[prof_index]
            course = courses[course_index]
            pref = prefs[prof].get(course)

            if pref is None:
                pref = 0

            pref_matrix[prof_index][course_index] = int(pref)

    return pref_matrix


def test_print(profs, prefs, courses, avails, pref_matrix):
    """For debugging purposes >:)"""

    logger.debug("PARSING INPUT")
    logger.debug(f"PROFS: {profs}")
    logger.debug(f"PREFS: {prefs}")
    logger.debug(f"AVAILABILITY: {avails}")
    logger.debug(f"COURSES: {courses}")
    logger.debug("MATRIX:")

    for i in range(pref_matrix.shape[0]):
        logger.debug(pref_matrix[i])
