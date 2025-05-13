"""
This is the main module of the application.
It contains the entry point and setup for the FastAPI app.
"""

from celery import Celery
from celery.result import AsyncResult
from dotenv import load_dotenv
from fastapi import FastAPI

from timetable_ga.api import (
    get_classrooms,
    get_course_classes,
    get_courses,
    get_students_groups,
    get_teachers,
)
from timetable_ga.models import Algorithm, Configuration, Schedule
from timetable_ga.utils import restart_id_counters

load_dotenv()

celery_app = Celery(
    "timetable-ga", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)


app = FastAPI()


@app.get("/")
def read_root():
    """GET endpoint that starts timetable generation."""
    try:
        task = timetable_generation.delay()
    except Exception as e:
        return {"response": "error", "error": str(e)}
    return {"response": "ok", "task_id": task.id, "task_status": task.state}


@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    """GET endpoint to check the status of a Celery task."""
    task = AsyncResult(task_id, backend=celery_app.backend)
    if task.state == "PENDING":
        return {"status": "pending", "message": "Task is still waiting to be executed."}
    if task.state == "FAILURE":
        return {"status": "failed", "error": str(task.info)}
    if task.state == "SUCCESS":
        return {"status": "success", "result": task.result}
    if task.state == "REVOKED":
        return {"status": "revoked", "message": "Task was revoked."}
    return {"status": task.state}


@celery_app.task
def timetable_generation():
    """Celery task to generate the timetable."""
    restart_id_counters()

    classrooms = get_classrooms()
    teachers = get_teachers()
    courses = get_courses()
    student_groups = get_students_groups(from_dummy=True)
    course_class = get_course_classes(from_dummy=True)

    configuration = Configuration(  # noqa: F841
        classrooms=classrooms,
        teachers=teachers,
        courses=courses,
        student_groups=student_groups,
        course_class=course_class,
    )

    prototype = Schedule(2, 2, 80, 3)
    instance = Algorithm(100, 8, 5, prototype)

    global best_chromosome
    bestChromosome = instance.Start()  # noqa: F841
