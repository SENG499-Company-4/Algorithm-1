from pydantic import BaseModel


class Preference(BaseModel):
    courseNum: str
    preferenceNum: int
    term: str


class Professor(BaseModel):
    prefs: list[Preference]
    displayName: str
    fallTermCourses: int
    springTermCourses: int
    summerTermCourses: int


class Assignment(BaseModel):
    startDate: str
    endDate: str
    beginTime: str
    endtime: str
    hoursWeek: float
    sunday: bool
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool


class Course(BaseModel):
    courseNumber: str
    subject: str
    sequenceNumber: str
    courseTitle: str
    meetingTime: Assignment
    prof: Professor


class Schedule(BaseModel):
    fallTermCourses: list[Course]
    springTermCourses: list[Course]
    summerTermCourses: list[Course]


class Input(BaseModel):
    hardScheduled: Schedule
    coursesToSchedule: Schedule
    professors: list[Professor]
