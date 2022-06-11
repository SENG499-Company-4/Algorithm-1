from pydantic import BaseModel


class Preference(BaseModel):
    courseNum: str  # ex. CSC 226
    preferenceNum: int  # ex. 6
    term: str  # ex. fall

    def __repr__(self):
        return repr(
            {
                "courseNum": self.courseNum,
                "preferenceNum": self.preferenceNum,
                "term": self.term,
            }
        )


class Professor(BaseModel):
    prefs: list[Preference]
    displayName: str
    requiredEquipment: list[str]
    fallTermCourses: int
    springTermCourses: int
    summerTermCourses: int

    def __repr__(self):
        return repr(
            {
                "prefs": self.prefs,
                "displayName": self.displayName,
                "fallTermCourses": self.fallTermCourses,
                "springTermCourses": self.springTermCourses,
                "summerTermCourses": self.summerTermCourses,
            }
        )


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
    requiredEquipment: list[str]
    streamSequence: str
    meetingTime: Assignment
    prof: Professor


class Schedule(BaseModel):
    fallTermCourses: list[Course]
    springTermCourses: list[Course]
    summerTermCourses: list[Course]
