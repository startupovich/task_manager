from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict


class Status(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str | None = Field(None, max_length=1000, description="Task description")

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title must not be empty or whitespace only')
        return v

    # Новый стиль конфигурации Pydantic v2
    model_config = ConfigDict(extra='ignore')


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: UUID = Field(default_factory=uuid4, description="Unique task identifier")
    status: Status = Field(default=Status.CREATED, description="Task status")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Sample task",
                "description": "This is a sample task",
                "status": "created"
            }
        }
    )


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200, description="Task title")
    description: str | None = Field(None, max_length=1000, description="Task description")
    status: Status | None = Field(None, description="Task status")

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title must not be empty or whitespace only')
        return v

    model_config = ConfigDict(extra='ignore')