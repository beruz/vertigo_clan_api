import os
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import select,desc
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from models import Base, Clan
from schemas import ClanIn, ClanOut, ClanCreateResponse, ClanDeleteResponse


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")       # e.g., Cloud SQL Public IP
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Build connection string URL
DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create async engine & session
engine = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Vertigo Games - Clan Management API",
    lifespan=lifespan
)

async def get_db():
    async with SessionLocal() as session:
        yield session

# POST /clans → create a clan
@app.post("/clans", response_model=ClanCreateResponse, status_code=201)
async def create_clan(clan: ClanIn, db: AsyncSession = Depends(get_db)):
    new_clan = Clan(**clan.dict())
    db.add(new_clan)
    await db.commit()
    await db.refresh(new_clan)
    return {
        "id": new_clan.id,
        "message": "Clan created successfully."
    }


# GET /clans → get the list of clans
@app.get("/clans", response_model=List[ClanOut])
async def list_clans(
    region: Optional[str] = Query(
        None, description="Filter clans by region"
    ),
    sort_by_date: Optional[bool] = Query(
        False, description="Sort clans by created_at descending if true"
    ),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Clan)

    if region:
        stmt = stmt.where(Clan.region == region)

    if sort_by_date:
        stmt = stmt.order_by(desc(Clan.created_at))

    result = await db.execute(stmt)
    return result.scalars().all()

# GET /clans/{clan_id} → get one clan
@app.get("/clans/{clan_id}", response_model=ClanOut, status_code=200)
async def get_clan(clan_id: str, db: AsyncSession = Depends(get_db)):
    clan = await db.get(Clan, clan_id)
    if not clan:
        raise HTTPException(404, "Clan not found")
    return clan

# DELETE /clans/{clan_id} → delete clan
@app.delete("/clans/{clan_id}", response_model=ClanDeleteResponse, status_code=200)
async def delete_clan(clan_id: str, db: AsyncSession = Depends(get_db)):
    clan = await db.get(Clan, clan_id)
    if not clan:
        raise HTTPException(404, "Clan not found")
    await db.delete(clan)
    await db.commit()
    return {
        "id": clan.id,
        "message": "Clan deleted successfully."
    }