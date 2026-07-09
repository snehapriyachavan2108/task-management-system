from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException
from src.user.models import UserModel

def create_task(body: TaskSchema, db: Session, user: UserModel):
    print('reached create_task')
    data = body.model_dump()
    print('data:', data)
    
    # Here you would typically interact with the database to create the task
    new_task = TaskModel(title = data["title"], 
                         description = data["description"], 
                         completed = data["completed"]
                         , user_id = user.id)
    print('before db.add')
    db.add(new_task)
    print('before commit')
    db.commit()
    print('after commit')
    db.refresh(new_task)
    print('returning task')
    return new_task

def get_task(db: Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks

def get_one_task(task_id: int, db: Session, user: UserModel):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return one_task

def update_task(task_id: int, body: TaskSchema, db: Session, user: UserModel):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if one_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    data = body.model_dump()                     #one_task.title = body.title
    for key, value in data.items():              #one_task.description = body.description
        setattr(one_task, key, value)            #one_task.completed = body.completed
    
    db.add(one_task)
    db.commit()
    db.refresh(one_task)
    return one_task

def delete_task(task_id: int, db: Session, user: UserModel):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if one_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    db.delete(one_task)
    db.commit()
    return None