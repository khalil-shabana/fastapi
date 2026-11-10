from fastapi import APIRouter, HTTPException, status, Response
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends
import models, schemas, tokengen
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)
'''
    /* get total votes for each post*/
    SELECT posts.id, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id ORDER BY id ASC;
'''


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
async def get_posts(db: Session = Depends(get_db),
                      curr_user: schemas.TokenData = Depends(tokengen.get_current_user),
                      limit: int =20, skip: int =0, search: Optional[str] = ""):
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    
    print(f"value 0f result: {results}")
    print("-------------------------------------------------------------------\n")
    print(f"value 0f dict-result: {dict(results)}")
    print("-------------------------------------------------------------------\n")
    print(f"type 0f result: {type(results)}")
    print("-------------------------------------------------------------------\n")
    
    #     # 1. Loop through your list of tuples: post is the object, votes is the integer count
    # formatted_results = []
    # for post, votes in results:
    #     post_dict = post.__dict__.copy()  # Convert the Post object attributes into a dict
    #     post_dict["votes"] = votes        # Add the votes count key
    #     post_dict.pop("_sa_instance_state", None)  # Clean out SQLAlchemy internal flags
    #     formatted_results.append(post_dict)
        
    # print(f"Value of formated result: {formatted_results}")
    
    return results
    # return {"data": posts}

@router.get("/{post_id}", response_model=schemas.PostOut) 
async def get_post(post_id: int, db: Session = Depends(get_db),
                      curr_user: schemas.TokenData = Depends(tokengen.get_current_user)):
    post = db.query(models.Post).filter_by(id=post_id).first()
    result =  (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == post_id)
        .first()
    )
    '''Method 	    Returns 
    .first()	    one object, or None if not found
    .one()	        exactly one — raises if not found or if multiple
    .one_or_none()	one object or None; raises if multiple
    .all()	        a list of all matching rows
    .count()	    integer count'''
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the post with id:{post_id} not found')
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                      curr_user: schemas.TokenData = Depends(tokengen.get_current_user)):
    """
    This route requires a valid Authorization: Bearer <token> header.
    If the token is missing, expired, or invalid, FastAPI automatically
    stops execution and returns a 401 Unauthorized error.
    """
    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    # db.add(models.Post(**post.model_dump()))
    new_post = models.Post(user_id=curr_user.id, **post.model_dump()) # ** — the unpacking operator
    # new_post.user_id=curr_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # ← reload from DB to get id, created_at, server defaults
    
    return {"data": new_post}

    
    
@router.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db),
                      curr_user: schemas.TokenData = Depends(tokengen.get_current_user)):  
    target_post = db.query(models.Post).filter_by(id=post_id).first()
    if not target_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the post with id:{post_id} not found')
        
    if target_post.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    db.delete(target_post)
    db.commit()
    
    return {'result': f'Post with id {post_id} is deleted'}

        
@router.put("/{post_id}")
async def update_post(post_id: int, post: schemas.Post, db: Session = Depends(get_db),
                      curr_user: schemas.TokenData = Depends(tokengen.get_current_user)):
    post_query = db.query(models.Post).filter_by(id=post_id)
    target_post = post_query.update({**post.model_dump()})
    
    
    print(type({**post.model_dump()}))
    print(type(target_post))
    
    if not target_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the post with id:{post_id} not found')
    
    # Rereiving the id of the post owner, as no one but the owner can update the post
    target_post_owner_id = db.query(models.Post).filter_by(id=post_id).first().user_id
    
    # curr_user.id : is the user who is logged in and wants to update the post
    if target_post_owner_id != curr_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        
    db.commit()    # push changes from staging to the database
    
    return {'msg':'post updated', 'data':post_query.first()}



@router.patch("/{post_id}")
async def patch_post(post_id: int, post: schemas.Post_PATCH, db: Session = Depends(get_db),
                      curr_user: schemas.TokenData = Depends(tokengen.get_current_user)):
    
    payload_post = post.model_dump(exclude_unset=True) 
    target_post = db.query(models.Post).filter_by(id=post_id).update(payload_post)
    print(type(payload_post))
    
    
    if not target_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the post with id:{post_id} not found')
    
    # Rereiving the id of the post owner, as no one but the owner can update the post
    target_post_owner_id = db.query(models.Post).filter_by(id=post_id).first().user_id
        
    if target_post_owner_id != curr_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        
    db.commit()   
    target_post = db.query(models.Post).filter_by(id=post_id).first()   # re-fetch
    return {"Data":target_post}
