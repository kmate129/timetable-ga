"""Unit tests for API data fetching functions."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from timetable_ga.main import get_classrooms, get_courses, get_students_groups, get_teachers
from timetable_ga.models import Classroom, Course, Teacher

mock_classrooms_data = [
    {"id": "ee2e8320-e8d2-41e0-bba0-0de7a1988f36", "name": "Room 1"},
    {"id": "6793ff68-e04c-45d1-85c0-c4e62d84d4ee", "name": "Room 2"},
    {"id": "6793ff68-e04c-45d1-85c0-c4e62d84d4ff", "name": "Room 3"},
]

mock_teachers_data = [
    {"id": "teacher_1", "name": "Ms. Brown"},
    {"id": "teacher_2", "name": "Mr. Green"},
    {"id": "teacher_3", "name": "Dr. White"},
]


@patch("requests.get")
def test_fetching_classrooms_api_error(mock_get):
    """Test fetching classrooms with API error."""
    mock_get.side_effect = requests.exceptions.RequestException("Connection failed")

    classrooms = get_classrooms()

    assert classrooms == []


@patch("requests.get")
def test_fetching_classrooms_empty_list(mock_get):
    """Test fetching classrooms with an empty list."""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    classrooms = get_classrooms()

    assert classrooms == []


@patch("requests.get")
def test_fetching_classrooms_invalid_data(mock_get):
    """Test fetching classrooms with invalid data."""
    invalid_data = [
        {"id": "some-id"},
    ]

    mock_response = MagicMock()
    mock_response.json.return_value = invalid_data
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    try:
        classrooms = get_classrooms()
        assert len(classrooms) == 1
        assert classrooms[0].name is None
    except KeyError:
        pass


@patch("requests.get")
def test_fetching_classrooms_server_error(mock_get):
    """Test fetching classrooms with server error."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mock_get.return_value = mock_response

    classrooms = get_classrooms()

    assert classrooms == []


@patch("requests.get")
def test_fetching_classrooms(mock_get):
    """Test fetching classrooms with valid data."""
    mock_response = MagicMock()
    mock_response.json.return_value = mock_classrooms_data
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    classrooms = get_classrooms()

    assert len(classrooms) == len(mock_classrooms_data)

    id_ = 0
    for classroom in classrooms:
        assert isinstance(classroom, Classroom)
        assert isinstance(classroom.id, int)
        assert classroom.id == id_
        assert isinstance(classroom.name, str)
        assert len(classroom.name) > 0
        assert isinstance(classroom.is_lab, bool)
        assert isinstance(classroom.number_of_seats, int)

        id_ += 1


@patch("requests.get")
def test_fetching_teachers_api_error(mock_get):
    """Test fetching teachers with API error."""
    mock_get.side_effect = requests.exceptions.RequestException("Connection failed")

    teachers = get_teachers()

    assert not teachers


@patch("requests.get")
def test_fetching_teachers_server_error(mock_get):
    """Test fetching teachers with server error."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mock_get.return_value = mock_response

    teachers = get_teachers()

    assert not teachers


@patch("requests.get")
def test_fetching_teachers_invalid_data(mock_get):
    """Test fetching teachers with invalid data."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": "teacher_1", "name": "Ms. Brown"},
        {"id": "teacher_2"},
    ]
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    with pytest.raises(ValueError):
        get_teachers()


@patch("requests.get")
def test_fetching_teachers(mock_get):
    """Test fetching teachers with valid data."""
    mock_response = MagicMock()
    mock_response.json.return_value = mock_teachers_data
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    teachers = get_teachers()

    assert len(teachers) == len(mock_teachers_data)

    for teacher in teachers:
        assert isinstance(teacher, Teacher)
        assert isinstance(teacher.backend_id, str)
        assert len(teacher.backend_id) > 0
        assert isinstance(teacher.name, str)
        assert len(teacher.name) > 0


@patch("requests.get")
def test_fetching_courses_success(mock_get):
    """Test fetching courses with valid data."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": "course_1", "name": "Calculus I."},
        {"id": "course_2", "name": "Programming I."},
    ]
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    courses = get_courses()

    assert len(courses) == 2
    assert isinstance(courses[0], Course)
    assert courses[0].backend_id == "course_1"
    assert courses[0].name == "Calculus I."
    assert isinstance(courses[1], Course)
    assert courses[1].backend_id == "course_2"
    assert courses[1].name == "Programming I."


@patch("requests.get")
def test_fetching_courses_request_exception(mock_get):
    """Test fetching courses with request exception."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException(
        "Connection failed"
    )
    mock_get.return_value = mock_response

    courses = get_courses()

    assert not courses


@patch("requests.get")
def test_fetching_courses_validation_error(mock_get):
    """Test fetching courses with validation error."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": "course_1", "name": "Calculus I."},
        {"id": "course_2"},
    ]
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    courses = get_courses()

    assert not courses


@patch("requests.get")
def test_fetching_students_groups_success(mock_get):
    """Test fetching students groups with valid data."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": "group_1", "name": "Calculus I.", "number_of_students": 30},
        {"id": "group_2", "name": "Programming I.", "number_of_students": 25},
    ]
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    groups = get_students_groups()
    assert len(groups) == 2
    assert groups[0].backend_id == "group_1"
    assert groups[0].name == "Calculus I."
    assert groups[0].number_of_students == 30
    assert groups[1].backend_id == "group_2"
    assert groups[1].name == "Programming I."
    assert groups[1].number_of_students == 25


@patch("requests.get")
@patch("builtins.print")
def test_fetching_students_groups_api_error(mock_print, mock_get):
    """Test fetching students groups with API error."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API error")
    mock_get.return_value = mock_response

    groups = get_students_groups()

    assert groups == []
    mock_print.assert_any_call("Request error occurred: API error")


@patch("builtins.open")
@patch("requests.get")
def test_fetching_students_groups_from_dummy(_mock_get, mock_open):
    """Test fetching students groups from dummy data."""
    mock_open.return_value.__enter__.return_value.read.return_value = (
        '{"groups": ['
        '{"id": "group_1", "name": "Calculus I.", "size": 30}, '
        '{"id": "group_2", "name": "Programming I.", "size": 25}'
        "]}"
    )

    groups = get_students_groups(from_dummy=True)

    assert len(groups) == 2
    assert groups[0].backend_id == "group_1"
    assert groups[0].name == "Calculus I."
    assert groups[0].number_of_students == 30
    assert groups[1].backend_id == "group_2"
    assert groups[1].name == "Programming I."
    assert groups[1].number_of_students == 25


@patch("builtins.open", side_effect=FileNotFoundError("Dummy data file not found"))
@patch("requests.get")
def test_fetching_students_groups_dummy_file_error(_mock_get, _mock_open):
    """Test fetching students groups from dummy data with file not found error."""
    try:
        get_students_groups(from_dummy=True)
    except FileNotFoundError as e:
        assert str(e) == "Dummy data file not found"
