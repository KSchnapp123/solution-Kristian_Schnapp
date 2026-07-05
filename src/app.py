from fastapi import FastAPI, Depends, HTTPException
from db import create_database_and_tables, get_async_session, populate_database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Bundle
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager
from models import User, Todo
from typing import List
from helpers import todo_from_json, get_status, get_priority
from schemas import TodoResponse, TodoResponseId, TodoBody, TodoPatch

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_database_and_tables()
    await populate_database()
    yield

app = FastAPI(lifespan=lifespan)

# Get all tickets

@app.get("/tickets")
async def getTodos(session:AsyncSession = Depends(get_async_session)) -> List[TodoResponse]:
    
    stmt = select(
        Bundle("todo", 
               Todo.id,
               Todo.todo,
               Todo.status,
               Todo.priority,
               ),
        Bundle("user",
               User.first_name,
               User.last_name
               )
    ).join_from(Todo,User, Todo.user_id == User.id)

    todo_responses = []
    results = await session.execute(stmt)
    for result in results.all():
        todo_responses.append({"id" : result.todo.id, 
                               "title": result.todo.todo,
                               "status": result.todo.status,
                               "priority": result.todo.priority,
                               "assignee": f"{result.user.first_name} {result.user.last_name}"})
    
    if len(todo_responses) == 0:
        raise HTTPException(status_code=404, detail="No tickets found")

    return todo_responses

# get tickets by search query
@app.get("/tickets/search")
async def search_tickets(search_query: str, session:AsyncSession = Depends(get_async_session)) -> List[TodoResponse]:

    search_query_normalized = search_query.strip()

    stmt = select(
        Bundle("todo", 
               Todo.id,
               Todo.todo,
               Todo.completed,
               Todo.status,
               Todo.priority,
               Todo.user_id
               ),
        Bundle("user",
               User.first_name,
               User.last_name
               )
    ).join_from(Todo,User, Todo.user_id == User.id).where(Todo.todo.like(f"%{search_query_normalized}%"))

    todo_responses = []
    results = await session.execute(stmt)
    for result in results.all():
        todo_responses.append({"id" : result.todo.id, 
                               "title": result.todo.todo,
                               "status": result.todo.status,
                               "priority": result.todo.priority,
                               "assignee": f"{result.user.first_name} {result.user.last_name}"})
    
    if len(todo_responses) == 0:
        raise HTTPException(status_code=404, detail="No tickets found")

    return todo_responses

# get ticket by id

@app.get("/tickets/{id}")
async def getTodo(id: int, session:AsyncSession = Depends(get_async_session)) -> TodoResponseId:
    
    stmt = select(
        Bundle("todo", 
               Todo.id,
               Todo.todo,
               Todo.completed,
               Todo.status,
               Todo.priority,
               Todo.user_id
               ),
        Bundle("user",
               User.first_name,
               User.last_name
               )
    ).join_from(Todo,User, Todo.user_id == User.id).where(Todo.id == id)

    result = await session.execute(stmt)
    todo = result.one_or_none()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {
        "id" : todo.todo.id,
        "title": todo.todo.todo,
        "status": todo.todo.status,
        "priority" : todo.todo.priority,
        "assignee": f"{todo.user.first_name} {todo.user.last_name}",
        "completed": todo.todo.completed,
        "user_id" : todo.todo.user_id
    }

    # filter tickets by priority and status

@app.get("/tickets/")
async def get_tikets_by_status_priority(priority: str, 
                                        status: str, 
                                        session:AsyncSession = Depends(get_async_session)) -> List[TodoResponse]:

    priority_normalized = priority.capitalize()
    status_normalized = status.capitalize()

    stmt = select(
        Bundle("todo", 
               Todo.id,
               Todo.todo,
               Todo.completed,
               Todo.status,
               Todo.priority,
               Todo.user_id
               ),
        Bundle("user",
               User.first_name,
               User.last_name
               )
    ).join_from(Todo,User, Todo.user_id == User.id).where(Todo.status == status_normalized,
                                                           Todo.priority == priority_normalized)

    todo_responses = []
    results = await session.execute(stmt)
    for result in results.all():
        todo_responses.append({"id" : result.todo.id, 
                               "title": result.todo.todo,
                               "status": result.todo.status,
                               "priority": result.todo.priority,
                               "assignee": f"{result.user.first_name} {result.user.last_name}"})
    
    if len(todo_responses) == 0:
        raise HTTPException(status_code=404, detail="No tickets found")

    return todo_responses

# insert new ticket
@app.post("/tickets", response_model=TodoBody)
async def insert_ticket(ticket: TodoBody, session:AsyncSession = Depends(get_async_session)):
    new_ticket = {
        "todo": ticket.todo,
        "completed": ticket.completed,
        "userId": ticket.userId
    }

    new_ticket_object = todo_from_json(new_ticket)
    try:
        session.add(new_ticket_object)
        await session.commit()
        return new_ticket
    except IntegrityError:
        raise HTTPException(status_code=500, detail=f"user with id: {ticket.userId} does not exist")
    


# Patch a ticket
@app.patch("/tickets/{id}", response_model=TodoBody)
async def patch_ticket(id: int, ticket: TodoPatch, session:AsyncSession = Depends(get_async_session)):
    db_ticket_stmt = await session.execute(select(Todo).where(Todo.id == id))
    db_ticket_result = db_ticket_stmt.scalar_one_or_none()

    if db_ticket_result is None:
        raise HTTPException(status_code=404, detail=f"Ticket with id: {id} not found")
    
    ticket_dict = ticket.model_dump(exclude_unset=True)

    field_map = {
        "todo" : "todo",
        "completed" : "completed",
        "userId" : "user_id"
    }
    
    for key, value in ticket_dict.items():
        orm_field = field_map[key]
        setattr(db_ticket_result, orm_field, value)
    
    if "completed" in ticket_dict:
        db_ticket_result.status = get_status(db_ticket_result.completed)
    
    if "userId" in ticket_dict:
        db_ticket_result.priority = get_priority(db_ticket_result.user_id)
    try:
        await session.commit()
        await session.refresh(db_ticket_result)
    except IntegrityError:
        raise HTTPException(status_code = 500, detail=f"User with id: {ticket_dict.get('userId' )} doesn't exist")
    return {
        "id": db_ticket_result.id,
        "todo": db_ticket_result.todo,
        "completed": db_ticket_result.completed,
        "userId": db_ticket_result.user_id 

    }



@app.get("/users")
async def get_users(session:AsyncSession = Depends(get_async_session)):
     result = await session.execute(select(User))
     return result.scalars().all()

@app.get("/todos")
async def get_users(session:AsyncSession = Depends(get_async_session)):
     result = await session.execute(select(Todo))
     return result.scalars().all()


