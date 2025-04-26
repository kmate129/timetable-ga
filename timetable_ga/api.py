import json
import os
from typing import List

import requests
from pydantic import ValidationError

from timetable_ga.models import Classroom, Course, CourseClass, StudentsGroup, Teacher


def get_classrooms() -> List[Classroom]:
    """
    Fetches the list of classrooms from the API.
    """
    url = "http://localhost:3080/classrooms"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        classrooms = [Classroom(backend_id=item["id"], name=item["name"]) for item in data]

        return classrooms

    except requests.exceptions.RequestException as e:
        print(f"Error fetching classrooms: {e}")
        return []


def get_teachers() -> List[Teacher]:
    """
    Fetches the list of teachers from the API.
    """
    url = "http://localhost:3080/users"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        teachers = []

        for item in data:
            if "name" not in item:
                raise ValueError(f"Missing 'name' for teacher with id {item['id']}")

            teachers.append(Teacher(backend_id=item["id"], name=item["name"]))

        return teachers

    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
        return []

    except ValueError as e:
        print(f"ValueError occurred: {e}")
        raise


def get_courses() -> List[Course]:
    """
    Fetches the list of courses from the API.
    """
    url = "http://localhost:3080/courses"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        courses = []

        for item in data:
            if "name" not in item:
                raise ValueError(f"Missing 'name' for course with id {item['id']}")
            courses.append(Course(backend_id=item["id"], name=item["name"]))

        return courses

    except ValueError as e:
        print(f"ValueError occurred: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
        return []


def get_students_groups(from_dummy: bool = False) -> List[StudentsGroup]:
    """
    Fetches student groups from a specified URL.
    Args:
        from_dummy (bool): If True, fetches data from a dummy source. Defaults to False.
    Returns:
        List[StudentsGroup]: A list of StudentsGroup objects.
    Raises:
        ValidationError: If there is a validation error while processing the response.
        requests.exceptions.RequestException: If there is an error during the HTTP request.
    """

    if from_dummy:
        with open(os.getenv("DUMMY_DATA_FILE"), encoding="utf-8") as f:
            json_data = json.load(f)

        groups = [
            StudentsGroup(
                backend_id=group["id"], name=group["name"], number_of_students=group["size"]
            )
            for group in json_data["groups"]
        ]
        return groups
    else:
        url = os.getenv("BACKEND_URL") + "/student-groups"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        student_groups = []

        for item in data:
            if "name" not in item or "number_of_students" not in item:
                raise ValueError(f"Missing required fields in student group: {item}")
            student_groups.append(
                StudentsGroup(
                    backend_id=item["id"],
                    name=item["name"],
                    number_of_students=item["number_of_students"],
                )
            )
        return student_groups

    except ValueError as e:
        print(f"ValueError occurred: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
        return []


def get_course_classes(
    courses: List[Course],
    teachers: List[Teacher],
    groups: List[StudentsGroup],
    from_dummy: bool = False,
) -> List[CourseClass]:
    """
    Fetches course classes from a specified URL.
    Args:
        from_dummy (bool): A flag to indicate whether to use dummy data. Defaults to False.
    Returns:
        List[CourseClass]: A list of CourseClass objects.
    Raises:
        ValidationError: If there is a validation error while processing the response.
        requests.exceptions.RequestException: If there is an error during the HTTP request.
    """
    if from_dummy:
        with open(os.getenv("DUMMY_DATA_FILE"), encoding="utf-8") as f:
            json_data = json.load(f)

        course_classes = [
            CourseClass(
                backend_id=group["id"], name=group["name"], number_of_students=group["size"]
            )
            for group in json_data["groups"]
        ]
        return course_classes
    else:
        url = os.getenv("BACKEND_URL") + "/courses"

    for course in courses:
        url += f"/{course.backend_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            # _teacher = next((t for t in teachers if t.id == data["teachers"][0]), None)
            _course = course  # noqa: F841
            _duration = 1  # noqa: F841
            _group = next((g for g in groups if g.id == data["groups"][0]), None)  # noqa: F841

            course_classes = [
                CourseClass(teacher=teachers.item["teachers"][0], course=item["course"])
                for item in data
            ]

        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")
            return []

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        course_classes = [
            CourseClass(backend_id=item["id"], teacher=item["teacher"], course=item["course"])
            for item in data
        ]
        return course_classes

    except ValidationError as e:
        print(f"Validation error occurred: {e.json()}")
        return []

    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
        return []
