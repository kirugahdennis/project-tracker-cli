from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Task:
    title: str
    project_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    completed: bool = False
    contributors: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    


@dataclass
class Project:
    name: str
    owner_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    task_ids: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isofrmat())

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    

@dataclass
class User:
    username: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    project_ids: list = field(default_factory=list)

    def to_dict(self):
        return self.__dict__

@classmethod
def from_dict(cls, data):
    return cls(**data)


