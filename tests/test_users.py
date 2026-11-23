from fastapi.testclient import TestClient
from main import app
import pytest
import schemas
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from database import get_db, Base

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address>or<hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:khalil@localhost:5432/fastapi_test'
# engine is responsible for establishing that connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# making session to be able to talk to the SQL database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define our Base class: so all the models that we defined to actually create our tables in Postgres,
# they're going to be extending this base class
# Base= declarative_base()



def override_get_db():
    db = TestingSessionLocal()
    try:
        print("session yielding...")
        yield db
    finally:
        print("session closed")
        db.close()
        
        
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

def test_root(client):
    response= client.get("/")
    print(response.json().get('message'))
    assert response.json().get('message') == 'Hello World!'
    assert response.status_code == 200

# @pytest.mark.parametrize("email, password, expected", [
#     ("zein@outlook.com","123456",201)
# ])


def test_create_user(client):
    response= client.post("/users", json={"email": "doaa@outlook.com", "password": "123456"})
    print(response.json())
    new_user = schemas.UserResponse(**response.json())

    assert new_user.email == "khalid@outlook.com"
    assert response.status_code == 201