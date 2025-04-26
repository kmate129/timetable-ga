"""Unit tests for the model classes."""

from models import Classroom


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
