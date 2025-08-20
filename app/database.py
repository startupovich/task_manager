from uuid import UUID
from app.models import Task, TaskCreate, TaskUpdate


class FakeDB:
    def __init__(self):
        self.tasks: dict[UUID, Task] = {}

    def get_all_tasks(self) -> list[Task]:
        return list(self.tasks.values())

    def get_task(self, task_id: UUID) -> Task | None:
        return self.tasks.get(task_id)

    def create_task(self, task_create: TaskCreate) -> Task:
        task = Task(**task_create.model_dump())
        self.tasks[task.id] = task
        return task

    def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Task | None:
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        update_data = task_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(task, field, value)
            
        return task

    def delete_task(self, task_id: UUID) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False


# Создаем глобальный экземпляр "базы данных"
db = FakeDB()