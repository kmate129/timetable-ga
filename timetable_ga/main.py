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
from timetable_ga.utils import restart_id_counters

load_dotenv()

celery_app = Celery(
    "timetable-ga", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)


app = FastAPI()


@celery_app.task
def long_running_task():
    import time

    time.sleep(60)
    return "Task completed"


@app.get("/")
def read_root():
    """GET endpoint that returns a simple JSON response."""
    try:
        task = long_running_task.delay()
    except Exception as e:
        return {"response": "error", "error": str(e)}
    return {"response": "ok", "task_id": task.id, "task_status": task.state}


@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    task = AsyncResult(task_id, backend=celery_app.backend)
    if task.state == "PENDING":
        return {"status": "pending", "message": "Task is still waiting to be executed."}
    elif task.state == "FAILURE":
        return {"status": "failed", "error": str(task.info)}
    elif task.state == "SUCCESS":
        return {"status": "success", "result": task.result}
    elif task.state == "REVOKED":
        return {"status": "revoked", "message": "Task was revoked."}
    else:
        return {"status": task.state}


def fetch_all_data():
    restart_id_counters()

    classrooms = get_classrooms()  # noqa: F841
    teachers = get_teachers()  # noqa: F841
    courses = get_courses()  # noqa: F841
    student_groups = get_students_groups(from_dummy=True)  # noqa: F841
    course_class = get_course_classes(from_dummy=True)  # noqa: F841
