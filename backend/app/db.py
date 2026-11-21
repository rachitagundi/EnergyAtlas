"""SQLAlchemy configuration: SQLite for the first run; PostgreSQL via DATABASE_URL."""
from sqlalchemy import Boolean, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    publisher: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String(2000), unique=True)
    topic: Mapped[str] = mapped_column(String(30))
    kind: Mapped[str] = mapped_column(String(30))
    saved: Mapped[bool] = mapped_column(Boolean, default=False)


def make_engine(url: str):
    options = {}
    if url.startswith("sqlite"):
        options["connect_args"] = {"check_same_thread": False}
        if url.endswith(":memory:"):
            options["poolclass"] = StaticPool
    return create_engine(url, **options)
