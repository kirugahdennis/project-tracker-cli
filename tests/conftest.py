import pytest
from models.user import User
from models.project import Project
from models.task import Task


@pytest.fixture(autouse=True)
def reset_id_counters():
    """Reset class-level ID counters before every test, so tests don't
    interfere with each other by sharing incremented counters."""
    User._id_counter = 1
    Project._id_counter = 1
    Task._id_counter = 1
    yield

