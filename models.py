"""Contains the models for the application."""

from typing import ClassVar, List

from pydantic import BaseModel


class InternalModel(BaseModel):
    id: int
    backend_id: str

    _next_id: ClassVar[int] = 0

    def __init__(self, **data):
        """Initialize the model with a unique ID and backend ID."""
        if "id" not in data:
            data["id"] = InternalModel._next_id
            InternalModel._next_id += 1
        super().__init__(**data)

    def get_id(self):
        """
        Returns the ID of the object.
        """
        return self.id

    def get_backend_id(self):
        """
        Returns the backend ID of the object.
        """
        return self.backend_id

    @classmethod
    def restart_id_counter(cls):
        """
        Restart the ID counter for the model."""
        InternalModel._next_id = 0

    def __eq__(self, rhs):
        """
        Check if two objects are equal based on their IDs.
        """
        return self.id == rhs.id


class Course(InternalModel):
    name: str

    def get_name(self):
        """
        Returns the name of the course.
        """
        return self.name


class Teacher(InternalModel):
    name: str
    lunch_break_needed: bool = False
    course_classes: List = []

    def get_name(self) -> str:
        """
        Returns the name of the teacher.
        """
        return self.name

    def add_course_class(self, course_class) -> None:
        """
        Adds a course class to the list of classes that the teacher teaches.
        """
        self.course_classes.append(course_class)

    def get_course_classes(self) -> List:
        """
        Returns the list of classes that the teacher teaches.
        """
        return self.course_classes


class StudentsGroup(InternalModel):
    name: str
    number_of_students: int
    course_classes: List = []

    def add_class(self, course_class) -> None:
        """
        Adds a class to the list of classes that the student group attends.
        """
        self.course_classes.append(course_class)

    def get_name(self) -> str:
        """
        Returns the name of the student group.
        """
        return self.name

    def get_number_of_students(self) -> int:
        """
        Returns the number of students in the group.
        """
        return self.number_of_students

    def get_course_classes(self) -> List:
        """
        Returns the list of classes that the student group attends.
        """
        return self.course_classes


class CourseClass(InternalModel):
    teacher: Teacher
    course: Course
    number_of_seats: int
    is_lab_required: bool
    duration: int
    groups: List[StudentsGroup]

    def __init__(self, teacher, course, groups, is_lab_required, duration):
        """
        Initialize the course class with a teacher, course, groups, lab requirement, and duration.
        """
        self.teacher = teacher
        self.course = course
        self.number_of_seats = 0
        self.is_lab_required = is_lab_required
        self.duration = duration
        self.groups = groups

        self.teacher.add_course_class(self)

        group_count = len(self.groups)
        for i in range(group_count):
            self.groups[i].add_class(self)
            self.number_of_seats = self.number_of_seats + StudentsGroup.get_number_of_students(
                self.groups[i]
            )

    def are_groups_overlapped(self, _class) -> bool:
        """
        Check if the student groups are the same.
        """
        for self_group in self.groups:
            for class_group in _class.groups:
                if self_group == class_group:
                    return True
        return False

    def is_teacher_overlapped(self, _class) -> bool:
        """
        Check if the teacher is already teaching a class at the same time.
        """
        return self.teacher == _class.teacher

    def get_teacher(self) -> Teacher:
        """
        Returns the teacher who teaches the class.
        """
        return self.teacher

    def get_course(self) -> Course:
        """
        Returns the course to which the class belongs.
        """
        return self.course

    def get_groups(self) -> List[StudentsGroup]:
        """
        Returns the list of student groups that attend the class.
        """
        return self.groups

    def get_number_of_seats(self) -> int:
        """
        Returns the number of seats required for the class.
        """
        return self.number_of_seats

    def get_is_lab_required(self) -> bool:
        """
        Returns whether the class requires a lab.
        """
        return self.is_lab_required

    def get_duration(self) -> int:
        """
        Returns the duration of the class.
        """
        return self.duration


class Classroom(InternalModel):
    name: str
    is_lab: bool = False
    number_of_seats: int = 1000

    def get_name(self) -> str:
        """
        Returns the name of the classroom.
        """
        return self.name

    def get_is_lab(self) -> bool:
        """
        Returns whether the classroom is a lab or not.
        """
        return self.is_lab

    def get_number_of_seats(self) -> int:
        """
        Returns the number of seats in the classroom.
        """
        return self.number_of_seats
