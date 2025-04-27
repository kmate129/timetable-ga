"""Contains the models for the application."""

import copy
import random
from random import randint
from typing import ClassVar, List

from pydantic import BaseModel

from timetable_ga.ga_consts import DAY_HOURS, DAYS_NUM, RAND16_MAX


class InternalModel(BaseModel):
    """
    Base model for all internal models.
    """

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
    """
    Model representing a course."""

    name: str

    def get_name(self):
        """
        Returns the name of the course.
        """
        return self.name


class Teacher(InternalModel):
    """
    Model representing a teacher.
    """

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
    """
    Model representing a group of students.
    """

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
    """
    Model representing a course class.
    """

    teacher: Teacher
    course: Course
    number_of_seats: int
    is_lab_required: bool
    duration: int
    groups: List[StudentsGroup]

    def __init__(
        self,
        teacher=None,
        course=None,
        groups=None,
        is_lab_required=False,
        duration=1,
        backend_id=None,
        name=None,
        number_of_students=None,
    ):
        """
        Initialize the course class with a teacher, course, groups, lab requirement, and duration.
        """
        super().__init__(backend_id=backend_id, name=name, number_of_students=number_of_students)
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
    """
    Model representing a classroom.
    """

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


class Configuration:
    """Configuration class to hold the timetable generation configuration."""

    global instance

    def __init__(
        self,
        teachers: List[Teacher],
        student_groups: List[StudentsGroup],
        courses: List[Course],
        classrooms: List[Classroom],
        course_classes: List[CourseClass],
    ):
        """Configuration class to hold the timetable generation configuration."""
        self.teachers = teachers
        self.student_groups = student_groups
        self.courses = courses
        self.classrooms = classrooms
        self.course_classes = course_classes

    def get_instance():
        """Singleton method to get the instance of Configuration class."""
        instance = Configuration()
        return instance

    def get_teacher_by_id(self, id):
        """Returns pointer to teacher with specified ID."""
        if id in self.teachers.keys():
            return self.teachers[id]
        return None

    def get_number_of_teachers(self):
        """Returns number of teachers."""
        return len(self.teachers.keys())

    def get_students_group_by_id(self, id):
        """Returns pointer to student group with specified ID."""
        if id in self.student_groups.keys():
            return self.student_groups[id]
        return None

    def get_number_of_student_groups(self):
        """Returns number of student groups."""
        return len(self.student_groups)

    def get_course_by_id(self, id):
        """Returns pointer to course with specified ID."""
        if id in self.courses.keys():
            return self.courses[id]
        return None

    def get_number_of_courses(self):
        """Returns number of courses."""
        return len(self.courses)

    def get_classroom_by_id(self, id):
        """Returns pointer to classroom with specified ID."""
        if id in self.classrooms.keys():
            return self.classrooms[id]
        return None

    def get_number_of_classrooms(self):
        """Returns number of classrooms."""
        return len(self.classrooms)

    def get_course_classes(self):
        """Returns pointer to course classes."""
        return self.course_classes

    def get_number_of_course_classes(self):
        """Returns number of course classes."""
        return len(self.course_classes)


class Schedule:
    """
    Represents a schedule for classes."""

    def __init__(
        self,
        num_of_crossover_points: int,
        mutation_size: int,
        crossover_probability: float,
        mutation_probability: float,
    ):
        """
        Initialize the schedule with the given parameters.
        """
        self.num_of_crossover_points = num_of_crossover_points
        self.mutation_size = mutation_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.fitness = 0
        self.slots = []
        self.criteria = []

        self.slots = DAYS_NUM * DAY_HOURS * Algorithm.instance.get_number_of_rooms() * [None]
        self.criteria = Configuration.instance.get_number_of_course_classes() * 5

    def copy(self):
        """Create a deep copy of the schedule."""
        return copy.deepcopy(self)

    def make_new_from_prototype(self):
        """Create a new schedule from the prototype."""
        new_chromosome = self.copy()
        new_chromosome.classes = {}
        c = Configuration.instance.get_course_classes()
        for it in c:
            nr = Configuration.instance.get_number_of_rooms()
            dur = c[it].get_duration()
            day = randint(0, RAND16_MAX) % DAYS_NUM
            room = randint(0, RAND16_MAX) % nr
            time = randint(0, RAND16_MAX) % (DAY_HOURS + 1 - dur)
            pos = day * nr * DAY_HOURS + room * DAY_HOURS + time

            for i in range(dur - 1, -1, -1):
                new_chromosome.slots[pos + i].push(c[it])

            new_chromosome.classes[pos] = c[it]

        new_chromosome._calculate_fitness()
        return new_chromosome

    def crossover(self, parent2):
        """Crossover between two parents to create a new schedule."""
        if randint(0, RAND16_MAX) % 100 > self.crossover_probability:
            return Schedule.Schedule(self, False)

        n = Schedule.Schedule(self, True)
        size = len(self.classes)
        cp = size * [None]

        for _i in range(self.num_of_crossover_points, 0, -1):
            while 1:
                p = randint(0, RAND16_MAX) % size
                if not cp[p]:
                    cp[p] = True
                    break

        j = 0
        it1 = self.classes[j]
        it2 = parent2.classes[j]
        first = randint(0, 1) == 0
        for i in range(0, size):
            if first:
                n.classes[j] = it1
                for k in range(it1.get_duration() - 1, -1, -1):
                    n.slots[j + k].push(it1)
            else:
                n.classes[j] = it2
                for k in range(it2.get_duration() - 1, -1, -1):
                    n.slots[j + k].push(it2)
            if cp[i]:
                first = not first

            j = j + 1

        n.calculate_fitness()
        return n

    def mutation(self):
        """Mutate the schedule."""
        if randint(0, RAND16_MAX) % 100 > self.mutation_probability:
            return None

        number_of_classes = len(self.classes)

        for i in range(self.mutation_size, 0, -1):
            mpos = randint(0, RAND16_MAX) % number_of_classes
            pos1 = _j = mpos

            cc1 = self.classes[pos1]
            nr = Schedule.instance.get_number_of_rooms()
            dur = cc1.get_duration()
            day = randint(0, RAND16_MAX) % DAYS_NUM
            room = randint(0, RAND16_MAX) % nr
            time = randint(0, RAND16_MAX) % (DAY_HOURS + 1 - dur)
            pos2 = day * nr * DAY_HOURS + room * DAY_HOURS + time

            for _j in range(dur - 1, -1, -1):
                c1 = self.slots[pos1 + i]
                for k in range(0, len(self.slots)):
                    if c1[k] == cc1:
                        del c1[k]
                        break

                self.slots[pos2 + i].push(cc1)

            self.classes[cc1] = pos2

        self.CalculateFitness()

    def calculate_fitness(self):  # noqa: C901
        """Calculate the fitness of the schedule."""
        score = 0
        number_of_rooms = Configuration.instance.get_number_of_rooms()
        day_size = DAY_HOURS * number_of_rooms

        ci = 0

        for i in range(0, len(self.classes)):
            p = i
            day = p / day_size
            time = p % day_size
            room = time / DAY_HOURS
            time = time % DAY_HOURS
            dur = self.classes[i].get_duration()
            ro = False

            for j in range(dur - 1, -1, -1):
                if self.slots[p + j].size() > 1:
                    ro = True
                    break

            if not ro:
                score = score + 1

            self.criteria[ci + 0] = not ro

            cc = self.classes[i]
            r = Configuration.instance.get_room_by_id(room)
            self.criteria[ci + 1] = r.get_number_of_seats() >= cc.get_number_of_seats()
            if self.criteria[ci + 1]:
                score = score + 1

            self.criteria[ci + 2] = (not cc.is_lab_required()) or (
                cc.is_lab_required() and r.is_lab()
            )
            if self.criteria[ci + 2]:
                score = score + 1

            po = False
            go = False
            t = day * day_size + time
            break_point = False
            for k in range(number_of_rooms, 0, -1):
                if break_point:
                    break
                for _l in range(dur - 1, -1, -1):
                    if break_point:
                        break
                    cl = self.slots[t + k]
                    for it in range(0, len(cl)):
                        if cc != cl[it]:
                            if not po and cc.is_teacher_overlapped(cl[it]):
                                po = True
                            if not go and cc.are_groups_overlapped(cl[it]):
                                go = True
                            if po and go:
                                break_point = True

                t = t + DAY_HOURS

            if not po:
                score = score + 1
            self.criteria[ci + 3] = not po

            if not go:
                score = score + 1
            self.criteria[ci + 4] = not go

            ci += 5

        self.fitness = score / (Configuration.instance.get_number_of_course_classes() * DAYS_NUM)


class Algorithm:
    """
    Genetic Algorithm class to manage the evolution of schedules."""

    def __init__(self, number_of_chromosomes, replace_by_generation, track_best, prototype):
        """Initialize the genetic algorithm with the given parameters."""
        self.replace_by_generation = replace_by_generation
        self.prototype = prototype
        self.current_best_size = 0
        self.current_generation = 0

        if number_of_chromosomes < 2:
            number_of_chromosomes = 2

        if track_best < 1:
            track_best = 1

        if self.replace_by_generation < 1:
            self.replace_by_generation = 1
        elif self.replace_by_generation > number_of_chromosomes - track_best:
            self.replace_by_generation = number_of_chromosomes - track_best

        self.chromosomes = number_of_chromosomes * [None]
        self.best_flags = number_of_chromosomes * [False]
        self.best_chromosomes = track_best * [None]

    def get_instance():
        """Singleton method to get the instance of Algorithm class."""
        prototype = Schedule(2, 2, 80, 3)
        instance = Algorithm(100, 8, 5, prototype)

        return instance

    def start(self):
        """Starts the genetic algorithm."""
        for it in range(len(self.chromosomes)):
            if self.chromosomes[it]:
                del self.chromosomes[it]

            self.chromosomes[it] = self.prototype.make_new_from_prototype()
            self.add_to_best(it)

        self.current_generation = 0
        random.seed()
        length_of_chromosomes = len(self.chromosomes)

        while 1:
            best = self.get_best_chromosome()
            if best.get_fitness() >= 1:
                print("best", best.get_fitness(), best.score)
                break

            offspring = self.replace_by_generation * [None]
            for j in range(0, self.replace_by_generation):
                a = randint(0, RAND16_MAX) % length_of_chromosomes
                b = randint(0, RAND16_MAX) % length_of_chromosomes
                p1 = self.chromosomes[a]
                p2 = self.chromosomes[b]
                offspring[j] = p1.crossover(p2)
                offspring[j].mutation()

            for j in range(0, self.replace_by_generation):
                ci = randint(0, RAND16_MAX) % len(self.chromosomes)
                while self.is_in_best(ci):
                    ci = randint(0, RAND16_MAX) % len(self.chromosomes)

                self.chromosomes[ci] = offspring[j]
                self.add_to_best(ci)

            self.current_generation = self.current_generation + 1

    def get_best_chromosome(self):
        """Returns the best chromosome."""
        return self.chromosomes[self.best_chromosomes[0]]

    def add_to_best(self, chromosome_index):
        """Adds a chromosome to the best chromosomes list."""
        if (
            self.current_best_size == len(self.best_chromosomes)
            and self.chromosomes[self.best_chromosomes[self.current_best_size - 1]].get_fitness()
            >= self.chromosomes[chromosome_index].get_fitness()
        ) or self.best_flags[chromosome_index]:
            return

        i = self.current_best_size
        j = 0
        for i in range(self.current_best_size, 0, -1):
            if i < len(self.best_chromosomes):
                if (
                    self.chromosomes[self.best_chromosomes[i - 1]].get_fitness()
                    > self.chromosomes[chromosome_index].get_fitness()
                ):
                    j = i
                    break

                self.best_chromosomes[i] = self.best_chromosomes[i - 1]
            else:
                self.best_flags[self.best_chromosomes[i - 1]] = False
            j = i - 1

        self.best_chromosomes[j] = chromosome_index
        self.best_flags[chromosome_index] = True

        if self.current_best_size < len(self.best_chromosomes):
            self.current_best_size = self.current_best_size + 1

    def is_in_best(self, chromosome_index):
        """Checks if a chromosome is in the best chromosomes list."""
        return self.best_flags[chromosome_index]

    def clear_best(self):
        """Clears the best chromosomes list."""
        for i in range(len(self.best_flags), -1, -1):
            self.best_flags[i] = False

        self.current_best_size = 0
