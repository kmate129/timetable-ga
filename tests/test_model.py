"""Unit tests for the model classes."""

import pytest

from timetable_ga.models import Classroom, InternalModel


@pytest.fixture(autouse=True)
def reset_id_counter():
    """Fixture to reset the ID counter before each test."""
    InternalModel.restart_id_counter()


def test_internal_model_auto_increment_id():
    """Test if InternalModel auto-increments the ID."""
    obj1 = InternalModel(backend_id="backend_1")
    obj2 = InternalModel(backend_id="backend_2")
    assert obj1.id == 0
    assert obj2.id == 1


def test_internal_model_custom_id():
    """Test if InternalModel accepts a custom ID."""
    obj = InternalModel(id=42, backend_id="backend_custom")
    assert obj.id == 42


def test_internal_model_get_id_and_backend_id():
    """Test if InternalModel returns the correct ID and backend ID."""
    obj = InternalModel(backend_id="backend_test")
    assert obj.get_id() == 0
    assert obj.get_backend_id() == "backend_test"


def test_internal_model_restart_id_counter():
    """Test if the ID counter can be restarted."""
    obj1 = InternalModel(backend_id="backend_a")  # noqa: F841
    InternalModel.restart_id_counter()
    obj2 = InternalModel(backend_id="backend_b")
    assert obj2.id == 0


def test_internal_model_equality_same_id():
    """Test if InternalModel equality works with the same ID."""
    obj1 = InternalModel(backend_id="backend_x")
    obj2 = InternalModel(id=obj1.id, backend_id="backend_y")
    assert obj1 == obj2


def test_internal_model_equality_different_id():
    """Test if InternalModel equality works with different IDs."""
    obj1 = InternalModel(backend_id="backend_x")
    obj2 = InternalModel(backend_id="backend_y")
    assert obj1 != obj2


def test_classroom_id_reset():
    """Test if the Classroom ID counter is properly reset."""
    Classroom.restart_id_counter()
    classroom = Classroom(backend_id="id_1", name="Room 1")
    assert classroom.id == 0

    classroom2 = Classroom(backend_id="id_2", name="Room 2")
    assert classroom2.id == 1

    Classroom.restart_id_counter()
    classroom3 = Classroom(backend_id="id_3", name="Room 3")
    assert classroom3.id == 0
