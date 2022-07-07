from models import Course, Input, Schedule


def courses_to_schedule(input: Input) -> Schedule:
    return input.coursesToSchedule

def fall_courses(schedule: Schedule) -> list[Course]:
    return schedule.fallTermCourses

def spring_courses(schedule: Schedule) -> list[Course]:
    return schedule.springTermCourses

def summer_courses(schedule: Schedule) -> list[Course]:
    return schedule.summerTermCourses

"""
Each list of courses will have preferences 
"""

def fall_term_courses_to_pref_matrix(fall_courses: list[Course]):
    """
    Returns a preference matrix for fall term courses
    """
    prof_preferences = [course.prof.prefs for course in fall_courses]
      

def spring_term_courses_to_pref_matrix(spring_courses: list[Course]):
    """
    Returns a preference matrix for spring term courses
    """
    prof_preferences = [course.prof.prefs for course in spring_courses]


def summer_term_courses_to_pref_matrix(summer_courses: list[Course]):
    """
    Returns a preference matrix for summer term courses
    """    
    prof_preferences = [course.prof.prefs for course in summer_courses]
