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
STREAM_SEQUENCE=["S1A", "S1B", "S2A", "S2B", "S3A", "S3B", "S4A", "S4B"]
PROFS = ("Bill Bird", "Daniela Damian", "Rich Little", "Michael Zastre")
TERMS = ("FALL", "SPRING", "SUMMER")


def rand_schedule():
    return Schedule(
        fallCourses=[rand_course() for _ in range(randint(10, 20))],
        springCourses=[rand_course() for _ in range(randint(10, 20))],
        summerCourses=[rand_course() for _ in range(randint(10, 20))])


def rand_course():
    subject, number, title = choice(COURSES)

    return Course(
        courseNumber=number,
        subject=subject,
        sequenceNumber=choice(SECTIONS),
        streamSequence=choice(STREAM_SEQUENCE),
        courseTitle=title,
        assignment=rand_assignment(),
        prof=rand_prof(),
        courseCapacity=100,
        numSections=1)


def rand_assignment():
    return Assignment(
        startDate=rand_date(),
        endDate=rand_date(),
        beginTime=rand_time(),
        endTime=rand_time(),
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
        preferences=[rand_pref() for _ in range(randint(1, 5))],
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
