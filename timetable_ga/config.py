from typing import List

from timetable_ga.models import Classroom, Course, CourseClass, StudentGroup, Teacher


class Configuration:
    def __init__(
        self,
        teachers: List[Teacher],
        studentGroups: List[StudentGroup],
        courses: List[Course],
        rooms: List[Classroom],
        courseClasses: List[CourseClass],
    ):
        """Configuration class to hold the timetable generation configuration."""
        self.is_empty = True
        self.teachers = teachers
        self.studentGroups = studentGroups
        self.courses = courses
        self.rooms = rooms
        self.courseClasses = courseClasses
