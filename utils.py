import contextlib
import logging 
import sqlalchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
from sqlalchemy.orm import sessionmaker


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 
log = logging.getLogger(__name__)

engine = sqlalchemy.create_engine('mysql://root@localhost:3306/GuWen?charset=utf8mb4', echo=True)
Session = sessionmaker(bind=engine)

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
