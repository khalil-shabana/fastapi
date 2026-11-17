'''first-fastapi-program'''

from fastapi import FastAPI, Request, HTTPException, status, Response
from fastapi.templating import Jinja2Templates
from enum import Enum
from typing import List
###### SQLALCEHMY SETUP ########
import models, schemas
from database import *
from sqlalchemy.orm import Session
from fastapi import Depends
from routers import posts, users, auth, votes
from config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://www.youtube.com",
    "https://www.google.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)



templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False) # FastAPI uses decorators to register routes.
async def home(request: Request):
    # return templates.TemplateResponse(request, "home.html", {"posts": posts})
    return {"message":"Hello World sort of"}






posts:  list[dict] = [
    {
        "title": "Python is Great for Web Dev.",
        "content": "Python is a great lang. for web development, and FastAPI makes it even better.",
        "id": 1
    },
    {
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast",
        "id": 2

    }
]



mock_items_db= [{"item_name":"apple"},{"item_name":"Ball"},{"item_name":"Car"},{"item_name":"Dog"},{"item_name":"Earth"}]

class Mode(str, Enum):
    mode1 = "dev"
    mode2 = "view"







@app.get("/api/items/")
async def read_item(skip: int =0, limit: int=10):
    return mock_items_db[skip: skip+limit]


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
from random import randrange


    
@app.get("/postss", response_model=List[schemas.PostResponse]) # FastAPI uses decorators to register routes.
async def get_posts(): 
    # EXECUTE THE SQL QUERY
    cur.execute("SELECT * FROM posts")
    # FETCH ALL THE ROWS FROM THE CURSOR
    db_posts = cur.fetchall()
    
    # print (db_posts)
    return db_posts



@app.post("/postss", status_code=status.HTTP_201_CREATED) # want to change status code
async def create_posts(post: schemas.Post):
    post_dict = post.dict()
    cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # post_dict["id"] = randrange(0,100000)
    # print (type(post_dict))
    # posts.append(post_dict)
    db_post = cur.fetchone()
    
    # commit the insertion query, (commented as we enabled the automatic commit)
    # conn.commit()
    # return {"data": db_post}
    return db_post


def find_post(target_id):
    for p in posts:
        if p["id"] == target_id:
            return p
        
def find_post_index(target_id):
    i: int = 0
    for p in posts:
        if p["id"] != target_id:
            i += 1
            continue
        elif p["id"] == target_id:
            return i
    return None
            
    
@app.get("/postss/{post_id}") 
async def get_post(post_id: int, response: Response):  # we changed the id from :int to :str
    cur.execute(" SELECT * FROM posts WHERE id = %s", (post_id,))
    # print(type(post_id))
    target_post = cur.fetchone()
    

    if not target_post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id:{post_id}, DNE'} 
        # OR 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with id:{post_id}, DNX')
    return {"result": f"Here is post with ID: {post_id}", "Data": target_post}

# @app.post("/createpost")
# async def create_post(new_post: Post):
#     print (new_post.publish)
#     return {"data": "new post"}

@app.delete("/postss/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):   # we changed the id from :int to :str
    cur.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (post_id,))
    target_post = cur.fetchone()
    # target_index = find_post_index(post_id)
    # if target_index == None:
    if not target_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the post with id:{post_id} not found')
    # else:
        # posts.pop(target_index)
    return {'result': f'Post with id {post_id} is deleted',"deleted_data": target_post}


@app.put("/postss/{post_id}")
async def update_post(post_id: int, post: schemas.Post):
    #post_dict = post.model_dump()
    cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;", (post.title, post.content, post.published, post_id))
    target_post = cur.fetchone()
    # target_index = find_post_index(post_id)
    # if target_index == None:
    if not target_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the post with id:{post_id} not found')
    
    # post_dict = post.dict()
    # posts[target_index]=post_dict
    # post_dict["id"] = post_id
    
    return {'msg':'updated post', 'data':target_post}





@app.patch("/postss/{post_id}")
async def patch_post(post_id: int, post: schemas.Post_PATCH):
    
    # get the target row with id => cur_post
    # compare with the payload >> AND statement  
    cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    cur_post_keys = list(cur.fetchone())
    payload_post = post.model_dump(exclude_none=True)
    print(payload_post)
    
    cols_builder = []
    vars = []
    for key in payload_post:
        #if payload_post and payload_post[key]:
          cols_builder.append(str(key)+"= %s")
          vars.append(payload_post[key])
          
    updated_cols = ', '.join(cols_builder)
    
    cur.execute("UPDATE posts SET "+ updated_cols + " WHERE id = %s RETURNING *;", vars+[post_id])
    patched_post= cur.fetchone()
    return {"Data":patched_post}
    
    
################################# SQLALCHEMY ROUTES #############################3
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"Status":"Success"}

'''_______________________________________________________
|                   SQLAlchemy ORM                        |
|               db.query(models.Post).all()               |
|           Python list of Post ORM instances             |
|                         ↓                               |
|                   FastAPI + Pydantic                    |
|           Validates each object against 'PostResponse'  |
|           and serializes its declared fields            |
|                         ↓                               |
|                   HTTP JSON respon                      |
|            Content-Type: application/json               |
|           JSON array returned to the client             |
|_______________________________________________________'''


