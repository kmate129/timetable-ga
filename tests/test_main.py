from unittest.mock import PropertyMock, patch

from celery.result import AsyncResult
from fastapi.testclient import TestClient

from timetable_ga.main import app

client = TestClient(app)


@patch("timetable_ga.main.timetable_generation.delay")
def test_read_root(mock_timetable_generation):
    mock_timetable_generation.return_value.id = "mock_task_id"
    mock_timetable_generation.return_value.state = "PENDING"

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "response": "ok",
        "task_id": "mock_task_id",
        "task_status": "PENDING",
    }
    mock_timetable_generation.assert_called_once()


@patch.object(AsyncResult, "state", new_callable=PropertyMock)
@patch.object(AsyncResult, "info", new_callable=PropertyMock)
@patch.object(AsyncResult, "result", new_callable=PropertyMock)
def test_task_status(mock_result, mock_info, mock_state):
    mock_state.return_value = "PENDING"
    response = client.get("/task-status/mock_task_id")
    assert response.status_code == 200
    assert response.json() == {
        "status": "pending",
        "message": "Task is still waiting to be executed.",
    }

    mock_state.return_value = "SUCCESS"
    mock_result.return_value = "Success result"
    response = client.get("/task-status/mock_task_id")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "result": "Success result"}

    mock_state.return_value = "FAILURE"
    mock_info.return_value = "Task failed"
    response = client.get("/task-status/mock_task_id")
    assert response.status_code == 200
    assert response.json() == {"status": "failed", "error": "Task failed"}

    mock_state.return_value = "REVOKED"
    response = client.get("/task-status/mock_task_id")
    assert response.status_code == 200
    assert response.json() == {"status": "revoked", "message": "Task was revoked."}

    mock_state.return_value = "STARTED"
    response = client.get("/task-status/mock_task_id")
    assert response.status_code == 200
    assert response.json() == {"status": "STARTED"}
