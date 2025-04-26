"""Unit tests for the model classes."""

import pytest

from timetable_ga.models import Classroom, Course, InternalModel, StudentsGroup, Teacher


@pytest.fixture(autouse=True)
def reset_id_counter():
    """Fixture to reset the ID counter before each test."""
    InternalModel.restart_id_counter()
    Course.restart_id_counter()
    Teacher.restart_id_counter()
    StudentsGroup.restart_id_counter()
    Classroom.restart_id_counter()


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


def test_course_creation():
    """Test if Course can be created with a backend ID and name."""
    course = Course(backend_id="backend_course_1", name="Calculus I.")
    assert course.id == 0
    assert course.backend_id == "backend_course_1"
    assert course.name == "Calculus I."


def test_course_get_name():
    """Test if Course returns the correct name."""
    course = Course(backend_id="backend_course_2", name="Calculus I.")
    assert course.get_name() == "Calculus I."


def test_course_inherits_internalmodel_methods():
    """Test if Course inherits methods from InternalModel."""
    course = Course(backend_id="backend_course_3", name="Chemistry")
    assert course.get_id() == 0
    assert course.get_backend_id() == "backend_course_3"


def test_multiple_courses_auto_increment_ids():
    """Test if multiple Course objects auto-increment their IDs."""
    course1 = Course(backend_id="backend_course_4", name="Calculus I.")
    course2 = Course(backend_id="backend_course_5", name="Programming I.")
    assert course1.id == 0
    assert course2.id == 1


def test_course_equality_by_id():
    """Test if two Course objects with the same ID are equal."""
    course1 = Course(backend_id="backend_course_6", name="Calculus I.")
    course2 = Course(id=course1.id, backend_id="backend_course_7", name="Intro to IoT")
    assert course1 == course2


def test_course_inequality_by_id():
    """Test if two Course objects with different IDs are not equal."""
    course1 = Course(backend_id="backend_course_8", name="Calculus I.")
    course2 = Course(backend_id="backend_course_9", name="Intro to IoT")
    assert course1 != course2


def test_teacher_creation_defaults():
    teacher = Teacher(backend_id="backend_teacher_1", name="John Doe")
    assert teacher.id == 0
    assert teacher.backend_id == "backend_teacher_1"
    assert teacher.name == "John Doe"
    assert teacher.lunch_break_needed is False
    assert teacher.course_classes == []


def test_teacher_get_name():
    teacher = Teacher(backend_id="backend_teacher_2", name="Jane Smith")
    assert teacher.get_name() == "Jane Smith"


def test_teacher_add_course_class():
    teacher = Teacher(backend_id="backend_teacher_3", name="Alan Turing")
    teacher.add_course_class("Calculus I.")
    teacher.add_course_class("Programming I.")
    assert teacher.course_classes == ["Calculus I.", "Programming I."]


def test_teacher_get_course_classes():
    teacher = Teacher(backend_id="backend_teacher_4", name="Ada Lovelace")
    teacher.add_course_class("Programming I.")
    classes = teacher.get_course_classes()
    assert classes == ["Programming I."]


def test_multiple_teachers_auto_increment_ids():
    teacher1 = Teacher(backend_id="backend_teacher_5", name="Einstein")
    teacher2 = Teacher(backend_id="backend_teacher_6", name="Newton")
    assert teacher1.id == 0
    assert teacher2.id == 1


def test_teacher_equality_by_id():
    teacher1 = Teacher(backend_id="backend_teacher_7", name="Galileo")
    teacher2 = Teacher(id=teacher1.id, backend_id="backend_teacher_8", name="Kepler")
    assert teacher1 == teacher2


def test_teacher_inequality_by_id():
    teacher1 = Teacher(backend_id="backend_teacher_9", name="Feynman")
    teacher2 = Teacher(backend_id="backend_teacher_10", name="Dirac")
    assert teacher1 != teacher2


def test_studentsgroup_creation_defaults():
    group = StudentsGroup(backend_id="backend_group_1", name="Group A", number_of_students=30)
    assert group.id == 0
    assert group.backend_id == "backend_group_1"
    assert group.name == "Group A"
    assert group.number_of_students == 30
    assert group.course_classes == []


def test_studentsgroup_get_name():
    group = StudentsGroup(backend_id="backend_group_2", name="Group B", number_of_students=25)
    assert group.get_name() == "Group B"


def test_studentsgroup_get_number_of_students():
    group = StudentsGroup(backend_id="backend_group_3", name="Group C", number_of_students=20)
    assert group.get_number_of_students() == 20


def test_studentsgroup_add_class():
    group = StudentsGroup(backend_id="backend_group_4", name="Group D", number_of_students=28)
    group.add_class("Calculus I.")
    group.add_class("Programming I.")
    assert group.course_classes == ["Calculus I.", "Programming I."]


def test_studentsgroup_get_course_classes():
    group = StudentsGroup(backend_id="backend_group_5", name="Group E", number_of_students=18)
    group.add_class("Calculus I.")
    classes = group.get_course_classes()
    assert classes == ["Calculus I."]


def test_multiple_studentsgroups_auto_increment_ids():
    group1 = StudentsGroup(backend_id="backend_group_6", name="Group F", number_of_students=22)
    group2 = StudentsGroup(backend_id="backend_group_7", name="Group G", number_of_students=24)
    assert group1.id == 0
    assert group2.id == 1


def test_studentsgroup_equality_by_id():
    group1 = StudentsGroup(backend_id="backend_group_8", name="Group H", number_of_students=26)
    group2 = StudentsGroup(
        id=group1.id, backend_id="backend_group_9", name="Group I", number_of_students=27
    )
    assert group1 == group2


def test_studentsgroup_inequality_by_id():
    group1 = StudentsGroup(backend_id="backend_group_10", name="Group J", number_of_students=30)
    group2 = StudentsGroup(backend_id="backend_group_11", name="Group K", number_of_students=32)
    assert group1 != group2


def test_classroom_creation_defaults():
    classroom = Classroom(backend_id="backend_classroom_1", name="Room A")
    assert classroom.id == 0
    assert classroom.backend_id == "backend_classroom_1"
    assert classroom.name == "Room A"
    assert classroom.is_lab is False
    assert classroom.number_of_seats == 1000


def test_classroom_get_name():
    classroom = Classroom(backend_id="backend_classroom_2", name="Room B")
    assert classroom.get_name() == "Room B"


def test_classroom_get_is_lab_default():
    classroom = Classroom(backend_id="backend_classroom_3", name="Room C")
    assert classroom.get_is_lab() is False


def test_classroom_get_is_lab_set_true():
    classroom = Classroom(backend_id="backend_classroom_4", name="Lab 1", is_lab=True)
    assert classroom.get_is_lab() is True


def test_classroom_get_number_of_seats_default():
    classroom = Classroom(backend_id="backend_classroom_5", name="Room D")
    assert classroom.get_number_of_seats() == 1000


def test_classroom_get_number_of_seats_custom():
    classroom = Classroom(backend_id="backend_classroom_6", name="Small Room", number_of_seats=30)
    assert classroom.get_number_of_seats() == 30


def test_multiple_classrooms_auto_increment_ids():
    classroom1 = Classroom(backend_id="backend_classroom_7", name="Room E")
    classroom2 = Classroom(backend_id="backend_classroom_8", name="Room F")
    assert classroom1.id == 0
    assert classroom2.id == 1


def test_classroom_equality_by_id():
    classroom1 = Classroom(backend_id="backend_classroom_9", name="Room G")
    classroom2 = Classroom(id=classroom1.id, backend_id="backend_classroom_10", name="Room H")
    assert classroom1 == classroom2


def test_classroom_inequality_by_id():
    classroom1 = Classroom(backend_id="backend_classroom_11", name="Room I")
    classroom2 = Classroom(backend_id="backend_classroom_12", name="Room J")
    assert classroom1 != classroom2
