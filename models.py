from pydantic import BaseModel


class Preference(BaseModel):
    course_num: str  # ex. CSC 226
    preference_num: int  # ex. 6
    term: str  # ex. fall

    def __repr__(self):
        return repr(
            {
                "course_num": self.course_num,
                "preference_num": self.preference_num,
                "term": self.term,
            }
        )


class Professor(BaseModel):
    preference_list: list[Preference]
    display_name: str  # ex. Michael Zastre
    fall_term_courses: int  # ex. 2
    spring_term_courses: int  # ex. 1
    summer_term_courses: int  # ex. 0

    def __repr__(self):
        return repr(
            {
                "preference_list": self.preference_list,
                "display_name": self.display_name,
                "fall_term_courses": self.fall_term_courses,
                "spring_term_courses": self.spring_term_courses,
                "summer_term_courses": self.summer_term_courses,
            }
        )
