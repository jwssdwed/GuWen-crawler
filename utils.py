import contextlib
import logging 
import sqlalchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
from sqlalchemy.orm import sessionmaker


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 
log = logging.getLogger(__name__)

engine = sqlalchemy.create_engine('mysql://root@localhost:3306/GuWen?charset=utf8mb4', echo=True)
Session = sessionmaker(bind=engine, autoflush=False)    # Disable autoflush to avoid flush after session.add() automatically. https://stackoverflow.com/questions/32922210/why-does-a-query-invoke-a-auto-flush-in-sqlalchemy

@contextlib.contextmanager
def scopedsession():
    session = Session()
    yield session
    try:
        session.commit() 
    except IntegrityError:
        session.rollback()
    except SQLAlchemyError as sqlalchemyErr: 
        session.rollback() 
        log.error(sqlalchemyErr) 
        raise 
    except Exception as ex: 
        log.error(ex)
    session.close() # Give the connection back to the connection pool of Engine, but still enable connection to MySQL. Details: https://stackoverflow.com/questions/21738944/how-to-close-a-sqlalchemy-session
