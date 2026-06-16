from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(create_tables: bool = False):
    """Prepare DB metadata for the application.

    By default this only imports model modules so `Base.metadata` is populated
    for tools like Alembic. It will NOT call `Base.metadata.create_all()`
    unless `create_tables=True` is passed explicitly. Prefer running Alembic
    migrations instead of using `create_all()` in production.
    """
    # import models so they are registered with Base.metadata
    try:
        import app.models.product  # noqa: F401
    except Exception:
        pass

    if create_tables:
        Base.metadata.create_all(bind=engine)




