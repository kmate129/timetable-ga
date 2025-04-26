"""Utility functions for the application."""

from timetable_ga.models import Classroom, Course, CourseClass, StudentsGroup, Teacher


def restart_id_counters() -> None:
    """Restart the ID counters for all models."""
    Classroom.restart_id_counter()
    Teacher.restart_id_counter()
    Course.restart_id_counter()
    StudentsGroup.restart_id_counter()
    CourseClass.restart_id_counter()
