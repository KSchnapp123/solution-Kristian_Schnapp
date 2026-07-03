from fastapi import FastAPI
from db import create_database_and_tables, get_async_session, populate_database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
from models import User

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_database_and_tables()
    await populate_database()
    yield

app = FastAPI(lifespan=lifespan)


