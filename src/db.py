from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy import select, event
from models import Base, User
from helpers import user_from_json
import httpx
from helpers import user_from_json, todo_from_json



# database url
DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# creating database engine
engine = create_async_engine(DATABASE_URL)

# Enabling foreign key
@event.listens_for(engine.sync_engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

#creating async session
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_database_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def populate_database() -> None:

    # Check if database is already populated

    async with async_session_maker() as session:
        result = await session.execute(select(User).limit(1))
        existing_user = result.scalar_one_or_none()

        if existing_user is not None:
            return

    async with httpx.AsyncClient() as client:
        user_response = await client.get("https://dummyjson.com/users?limit=0")
        todo_response = await client.get("https://dummyjson.com/todos?limit=0")
        
    # parse users
    users_list = user_response.json().get("users",[])
    user_objects = [user_from_json(user_json) for user_json in users_list]

    # parse todos
    todo_list = todo_response.json().get("todos", [])
    todo_objects = [todo_from_json(todo_json) for todo_json in todo_list]

    async with async_session_maker() as session:   
        session.add_all(user_objects)
        await session.commit()
        session.add_all(todo_objects)
        await session.commit()