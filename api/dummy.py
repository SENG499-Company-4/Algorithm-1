from datetime import date
from random import choice, randint, random

from .models import Assignment, Course, Preference, Professor, Schedule

COURSES = (
    ("SENG", "499", "Design Project II"),
    ("SENG", "440", "Embedded Systems"),
    ("SENG", "426", "Software Quality Engineering"),
    ("ECE", "355", "Microprocessor-Based Systems"),
    ("SENG", "360", "Security Engineering"),
    ("ECE", "260", "Continuous-Time Signals and Systems"),
    ("CSC", "110", "Fundamentals of Programming: I"),
    ("CSC", "320", "Foundations of Computer Science"),
    ("CSC", "225", "Algorithms and Data Structures: I"),
    ("CSC", "226", "Algorithms and Data Structures: II"))
SECTIONS = ("A01", "A02")
PROFS = ("Bill Bird", "Daniela Damian", "Rich Little", "Michael Zastre")
TERMS = ("FALL", "SPRING", "SUMMER")


def rand_schedule():
    return Schedule(
        fallTermCourses=[rand_course() for _ in range(randint(10, 20))],
        springTermCourses=[rand_course() for _ in range(randint(10, 20))],
        summerTermCourses=[rand_course() for _ in range(randint(10, 20))])


def rand_course():
    subject, number, title = choice(COURSES)

    return Course(
        courseNumber=number,
        subject=subject,
        sequenceNumber=choice(SECTIONS),
        courseTitle=title,
        meetingTime=rand_assignment(),
        prof=rand_prof())


def rand_assignment():
    return Assignment(
        startDate=rand_date(),
        endDate=rand_date(),
        beginTime=rand_time(),
        endtime=rand_time(),
        hoursWeek=6*random(),
        sunday=bool(randint(0, 1)),
        monday=bool(randint(0, 1)),
        tuesday=bool(randint(0, 1)),
        wednesday=bool(randint(0, 1)),
        thursday=bool(randint(0, 1)),
        friday=bool(randint(0, 1)),
        saturday=bool(randint(0, 1)))


def rand_date():
    return date(randint(2010, 2022), randint(1, 12), randint(1, 28)).strftime("%b %d, %Y")


def rand_time():
    return f"{randint(0, 23):0>2}{randint(0, 59):0>2}"


def rand_prof():
    return Professor(
        prefs=[rand_pref() for _ in range(randint(1, 5))],
        displayName=choice(PROFS),
        fallTermCourses=randint(1, 10),
        springTermCourses=randint(1, 10),
        summerTermCourses=randint(1, 10))


def rand_pref():
    subject, number, _ = choice(COURSES)

    return Preference(
        courseNum=f"{subject}{number}",
        preferenceNum=randint(1, 10),
        term=choice(TERMS))
