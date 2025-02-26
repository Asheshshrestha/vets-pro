import logging
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DATABASE_URL = URL.create(
    drivername="mysql+mysqldb",  # Or use "mysql+pymysql" if using PyMySQL
    username="test",
    password="P@ssword123",
    host="vetspro-db",  # <-- Change from "localhost" to "vetspro-db"
    port=3306,  # Add port explicitly
    database="vetspro-db",
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def init_db():
    # Creates tables in the database
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            logger.info("Connection successful, query result:", result.fetchone())
            logger.info("Initializing database...")
            #Base.metadata.create_all(bind=engine)
            logger.info("Database table created!")
    except Exception as e:
        logger.info(f"Connection failed: {e}")
   