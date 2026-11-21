"""A small, single-user source catalogue. Run one API worker in this checkpoint."""
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from sqlalchemy import distinct, func, or_, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .db import Base, Source, make_engine
from .schemas import BookmarkUpdate, Overview, SourceCreate, SourceRead, Topic
from .seed import seed_sources


def create_app(database_url: str | None = None, seed: bool = True) -> FastAPI:
    engine = make_engine(
        database_url or os.getenv("DATABASE_URL", "sqlite:///./energyatlas.db")
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(engine)
        if seed:
            with Session(engine) as session:
                seed_sources(session)
        yield
        engine.dispose()

    app = FastAPI(
        title="EnergyAtlas API",
        version="0.2.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url=None,
        description="Integrated checkpoint 0C: source metadata and shared bookmarks. Report retrieval and AI answers are planned.",
        lifespan=lifespan,
    )
    app.state.engine = engine

    def get_session():
        with Session(engine) as session:
            yield session

    DB = Annotated[Session, Depends(get_session)]

    @app.get("/api/health")
    def health(session: DB):
        session.execute(text("SELECT 1"))
        return {"status": "ok", "checkpoint": "0C"}

    @app.get("/api/overview", response_model=Overview)
    def overview(session: DB):
        return {
            "sources": session.scalar(select(func.count()).select_from(Source)),
            "saved": session.scalar(
                select(func.count()).select_from(Source).where(Source.saved.is_(True))
            ),
            "publishers": session.scalar(select(func.count(distinct(Source.publisher)))),
            "database": engine.dialect.name,
        }

    @app.get("/api/sources", response_model=list[SourceRead])
    def list_sources(
        session: DB,
        q: Annotated[str, Query(max_length=100)] = "",
        topic: Topic | None = None,
        saved_only: bool = False,
    ):
        statement = select(Source)
        term = q.strip().lower()
        if term:
            statement = statement.where(or_(*[
                func.lower(column).contains(term, autoescape=True)
                for column in (Source.title, Source.publisher, Source.description)
            ]))
        if topic:
            statement = statement.where(Source.topic == topic)
        if saved_only:
            statement = statement.where(Source.saved.is_(True))
        return session.scalars(statement.order_by(Source.id)).all()

    @app.post("/api/sources", response_model=SourceRead, status_code=201)
    def add_source(body: SourceCreate, session: DB):
        data = body.model_dump()
        data["url"] = str(body.url)
        source = Source(**data, saved=False)
        session.add(source)
        try:
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            raise HTTPException(409, "This source URL already exists.") from exc
        session.refresh(source)
        return source

    @app.patch("/api/sources/{source_id}/bookmark", response_model=SourceRead)
    def bookmark(source_id: int, body: BookmarkUpdate, session: DB):
        source = session.get(Source, source_id)
        if source is None:
            raise HTTPException(404, "Source not found.")
        source.saved = body.saved
        session.commit()
        session.refresh(source)
        return source

    # A production frontend build can be served by this same Python process.
    # During development Vite proxies /api, so no permissive CORS is needed.
    frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    if frontend_dist.is_dir():
        app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

    return app


app = create_app()
