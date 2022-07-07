from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class Assignment1(BaseModel):
    pass


class Prof(BaseModel):
    pass


class Assignment(BaseModel):
    startDate: str = Field(..., example='Jan 07, 2019')
    endDate: str = Field(..., example='Apr 05, 2019')
    beginTime: str = Field(..., example='0830')
    endTime: str = Field(..., example='0930')
    hoursWeek: int = Field(..., example=3)
    sunday: bool = Field(..., example=False)
    monday: bool = Field(..., example=True)
    tuesday: bool = Field(..., example=False)
    wednesday: bool = Field(..., example=False)
    thursday: bool = Field(..., example=True)
    friday: bool = Field(..., example=False)
    saturday: bool = Field(..., example=False)


class Term(Enum):
    FALL = 'FALL'
    SPRING = 'SPRING'
    SUMMER = 'SUMMER'


class Preference(BaseModel):
    courseNum: str = Field(..., example='CSC111')
    preferenceNum: int = Field(..., example=0)
    term: Optional[Term] = None


class Professor(BaseModel):
    preferences: List[Preference]
    displayName: str = Field(..., example='Michael, Zastre')
    fallTermCourses: Optional[int] = Field(None, example=1)
    springTermCourses: Optional[int] = Field(None, example=1)
    summerTermCourses: Optional[int] = Field(None, example=1)


class Course(BaseModel):
    courseNumber: str = Field(..., example='111')
    subject: str = Field(..., example='CSC')
    sequenceNumber: str = Field(..., example='A01')
    streamSequence: str = Field(..., example='1A')
    courseTitle: str = Field(
        ..., example='Fundamentals of Programming with Engineering Applications'
    )
    assignment: Optional[Union[List[Assignment], Assignment1]] = None
    prof: Optional[Union[List[Professor], Prof]] = None
    courseCapacity: int = Field(..., example=100)
    numSections: int = Field(
        ...,
        description='Number of sections a course needs to be split into. Default 1.',
        example=2,
    )


class Schedule(BaseModel):
    fallCourses: List[Course]
    springCourses: List[Course]
    summerCourses: List[Course]


class ScheduleConstraints(BaseModel):
    hardScheduled: Schedule
    coursesToSchedule: Schedule
    professors: List[Professor] = Field(
        ..., description='List of professors and their preferences.'
    )
