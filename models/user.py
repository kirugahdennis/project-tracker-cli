from .person import Person

class User(Person):
    """Represents a user who owns projects. Inherits from Person."""

    _id_counter = 1  # class attribute — shared across all instances, tracks next ID to assign

    def __init__(self, name, email):
        super().__init__(name, email)
        self.id = User._id_counter
        User._id_counter += 1
        self.project_ids = []

    def __str__(self):
        return f"User #{self.id}: {self.name} <{self.email}>"

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"

    @classmethod
    def create(cls, name, email):
        """Factory method to create a new User."""
        return cls(name, email)

    @classmethod
    def find_by_id(cls, users, user_id):
        """Given a list of User instances, return the one matching user_id, or None."""
        return next((u for u in users if u.id == user_id), None)

    @classmethod
    def find_by_name(cls, users, name):
        """Given a list of User instances, return the one matching name, or None."""
        return next((u for u in users if u.name == name), None)