import pytest
from models.person import Person
from models.user import User
from models.project import Project
from models.task import Task


def test_person_str():
    p = Person("Denis", "denis@example.com")
    assert str(p) == "Denis <denis@example.com>"


def test_person_rejects_empty_name():
    p = Person("Denis", "denis@example.com")
    with pytest.raises(ValueError):
        p.name = ""


def test_person_rejects_invalid_email():
    p = Person("Denis", "denis@example.com")
    with pytest.raises(ValueError):
        p.email = "not-an-email"


def test_user_inherits_person():
    u = User.create("Denis", "denis@example.com")
    assert isinstance(u, Person)
    assert u.name == "Denis"
    assert u.email == "denis@example.com"


def test_user_ids_increment():
    u1 = User.create("Denis", "denis@example.com")
    u2 = User.create("Mary", "mary@example.com")
    assert u1.id == 1
    assert u2.id == 2


def test_user_find_by_name():
    u1 = User.create("Denis", "denis@example.com")
    u2 = User.create("Mary", "mary@example.com")
    found = User.find_by_name([u1, u2], "Mary")
    assert found is u2
    assert User.find_by_name([u1, u2], "Nobody") is None


def test_project_ids_increment():
    p1 = Project.create("CLI Tool", "desc", "2026-08-01", owner_id=1)
    p2 = Project.create("Portfolio", "desc", "2026-09-01", owner_id=1)
    assert p1.id == 1
    assert p2.id == 2


def test_project_rejects_empty_title():
    p = Project.create("CLI Tool", "desc", "2026-08-01", owner_id=1)
    with pytest.raises(ValueError):
        p.title = ""


def test_project_find_by_owner():
    p1 = Project.create("CLI Tool", "desc", "2026-08-01", owner_id=1)
    p2 = Project.create("Portfolio", "desc", "2026-09-01", owner_id=2)
    result = Project.find_by_owner([p1, p2], 1)
    assert result == [p1]


def test_task_default_status():
    t = Task.create("Implement feature", "todo", assigned_to=1, project_id=1)
    assert t.status == "todo"


def test_task_rejects_invalid_status():
    t = Task.create("Implement feature", "todo", assigned_to=1, project_id=1)
    with pytest.raises(ValueError):
        t.status = "flying"


def test_task_valid_status_update():
    t = Task.create("Implement feature", "todo", assigned_to=1, project_id=1)
    t.status = "done"
    assert t.status == "done"


def test_task_find_by_project():
    t1 = Task.create("Task A", "todo", assigned_to=1, project_id=1)
    t2 = Task.create("Task B", "todo", assigned_to=1, project_id=2)
    result = Task.find_by_project([t1, t2], 1)
    assert result == [t1]