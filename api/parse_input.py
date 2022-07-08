from api.models import Course, Input, Schedule
import pandas as pd

def courses_to_schedule(input: Input) -> Schedule:
    """
    Extract courses from schedule object
    """
    return input.coursesToSchedule

def fall_courses(schedule: Schedule) -> list[Course]:
    """
    Extract fall courses
    """
    courses = schedule.fallTermCourses
    return fall_term_parse_prof_and_prefs(courses)

def spring_courses(schedule: Schedule) -> list[Course]:
    """
    Extract spring courses
    """
    courses = schedule.springTermCourses
    return spring_term_parse_prof_and_prefs(courses)

def summer_courses(schedule: Schedule) -> list[Course]:
    """
    Extract summer courses
    """
    courses = schedule.summerTermCourses
    return summer_term_parse_prof_and_prefs(courses)


def fall_term_parse_prof_and_prefs(fall_courses: list[Course]):
    """
    Returns a preference matrix for fall term courses
    """
    profs = [course.prof for course in fall_courses]
    li = []
    for item in profs:
       li.append((item.displayName, item.prefs))
    return li
    
      

def spring_term_parse_prof_and_prefs(spring_courses: list[Course]):
    """
    Returns a preference matrix for spring term courses
    """
    profs = [course.prof for course in spring_courses]
    li = []
    for item in profs:
       li.append((item.displayName, item.prefs))
    return li

def summer_term_parse_prof_and_prefs(summer_courses: list[Course]):
    """
    Returns a preference matrix for summer term courses
    """    
    profs = [course.prof for course in summer_courses]
    li = []
    for item in profs:
       li.append((item.displayName, item.prefs))
    return li