"""
Test the utils module."""

from unittest.mock import patch

from timetable_ga.utils import restart_id_counters


@patch("timetable_ga.models.Classroom.restart_id_counter")
@patch("timetable_ga.models.Teacher.restart_id_counter")
@patch("timetable_ga.models.Course.restart_id_counter")
@patch("timetable_ga.models.StudentsGroup.restart_id_counter")
@patch("timetable_ga.models.CourseClass.restart_id_counter")
def test_restart_id_counters(
    mock_course_class_restart,
    mock_students_group_restart,
    mock_course_restart,
    mock_teacher_restart,
    mock_classroom_restart,
):
    """Test the restart_id_counters function."""
    restart_id_counters()

    mock_classroom_restart.assert_called_once()
    mock_teacher_restart.assert_called_once()
    mock_course_restart.assert_called_once()
    mock_students_group_restart.assert_called_once()
    mock_course_class_restart.assert_called_once()
