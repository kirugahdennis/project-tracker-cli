class Project:
    """Represents a project owned by a user, containing tasks."""

    _id_counter = 1

    def __init__(self, title, description, due_date, owner_id):
        self.id = Project._id_counter
        Project._id_counter += 1
        self._title = title
        self.description = description
        self.due_date = due_date
        self.owner_id = owner_id
        self.task_ids = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty")
        self._title = value.strip()

    def __str__(self):
        return f"Project #{self.id}: {self.title} (due {self.due_date})"

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title!r}, owner_id={self.owner_id})"

    @classmethod
    def create(cls, title, description, due_date, owner_id):
        return cls(title, description, due_date, owner_id)

    @classmethod
    def find_by_id(cls, projects, project_id):
        return next((p for p in projects if p.id == project_id), None)

    @classmethod
    def find_by_title(cls, projects, title):
        return next((p for p in projects if p.title == title), None)

    @classmethod
    def find_by_owner(cls, projects, owner_id):
        """Return all projects belonging to a given owner_id."""
        return [p for p in projects if p.owner_id == owner_id]