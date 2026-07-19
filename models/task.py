class Task:
    """Represents a task belonging to a project, assigned to a user."""

    _id_counter = 1
    VALID_STATUSES = ("todo", "in_progress", "done")

    def __init__(self, title, status, assigned_to, project_id):
        self.id = Task._id_counter
        Task._id_counter += 1
        self._title = title
        self._status = status
        self.assigned_to = assigned_to  # a user id
        self.project_id = project_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty")
        self._title = value.strip()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in Task.VALID_STATUSES:
            raise ValueError(f"Status must be one of {Task.VALID_STATUSES}")
        self._status = value

    def __str__(self):
        return f"Task #{self.id}: {self.title} [{self.status}]"

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, status={self.status!r}, assigned_to={self.assigned_to})"

    @classmethod
    def create(cls, title, status, assigned_to, project_id):
        return cls(title, status, assigned_to, project_id)

    @classmethod
    def find_by_id(cls, tasks, task_id):
        return next((t for t in tasks if t.id == task_id), None)

    @classmethod
    def find_by_project(cls, tasks, project_id):
        """Return all tasks belonging to a given project_id."""
        return [t for t in tasks if t.project_id == project_id]