from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from config import settings



#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address>or<hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine is responsible for establishing that connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# making session to be able to talk to the SQL database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define our Base class: so all the models that we defined to actually create our tables in Postgres,
# they're going to be extending this base class
# Base= declarative_base()

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        print("session yielding")
        yield db
    finally:
        print("session closed")
        db.close()
        

#############################   C O N N E C T I N G    T O    D A T A B A S E    #################################

# # database vars:
# pg_host = 'localhost'
# pg_database = 'fastapi-course'
# pg_user = 'postgres'
# pg_pass = 'khalil'
# cursor_factory= RealDictCursor


# while True:
#     try:
#         # Connect to an existing database
#         conn = psycopg2.connect(host=pg_host, database=pg_database, user=pg_user, password=pg_pass, cursor_factory=RealDictCursor)
        
#         # Open a cursor to perform database operations
#         cur = conn.cursor()
#         conn.autocommit=True
#         print ("Database connection was successfull1!")
#         break
    
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ",error)
#         time.sleep(2)
#############################   E N D   O F   C O N N E C T I N G    T O    D A T A B A S E    #################################