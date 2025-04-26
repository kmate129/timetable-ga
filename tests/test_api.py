from unittest.mock import MagicMock, patch

import requests

from timetable_ga.main import get_classrooms
from timetable_ga.models import Classroom

mock_classrooms_data = [
    {"id": "ee2e8320-e8d2-41e0-bba0-0de7a1988f36", "name": "Room 1"},
    {"id": "6793ff68-e04c-45d1-85c0-c4e62d84d4ee", "name": "Room 2"},
    {"id": "6793ff68-e04c-45d1-85c0-c4e62d84d4ff", "name": "Room 3"},
]


@patch("requests.get")
def test_fetching_classrooms_api_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Connection failed")

    classrooms = get_classrooms()

    assert classrooms == []


@patch("requests.get")
def test_fetching_classrooms_empty_list(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    classrooms = get_classrooms()

    assert classrooms == []


@patch("requests.get")
def test_fetching_classrooms_invalid_data(mock_get):
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
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mock_get.return_value = mock_response

    classrooms = get_classrooms()

    assert classrooms == []


@patch("requests.get")
def test_fetching_classrooms(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = mock_classrooms_data
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    classrooms = get_classrooms()

    assert len(classrooms) == len(mock_classrooms_data)

    id = 0
    for classroom in classrooms:
        assert isinstance(classroom, Classroom)
        assert isinstance(classroom.id, int)
        assert classroom.id == id
        assert isinstance(classroom.name, str)
        assert len(classroom.name) > 0
        assert isinstance(classroom.is_lab, bool)
        assert isinstance(classroom.number_of_seats, int)

        id += 1
