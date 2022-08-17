from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import Settings
from utils.errors import IntegrityErrorException

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
db_string_connection = f"postgresql://{Settings().db_username}:{Settings().db_password}@"\
                       f"{Settings().db_host}:{Settings().db_port}/{Settings().db_name}"

engine = create_engine(db_string_connection)

# create a configured "Session" class
Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except IntegrityError as exc:
        raise IntegrityErrorException(exc.orig.diag)
    except:
        session.rollback()
        raise
    finally:
        session.close()
