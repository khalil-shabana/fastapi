from fastapi import APIRouter, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
import models, schemas, tokengen
from typing import List, Optional



router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_200_OK)
async def vote(vote: schemas.Vote, curr_user: schemas.TokenData = Depends(tokengen.get_current_user),
               db: Session = Depends(get_db)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == curr_user.id)
    
    found_vote = vote_query.first()
    
    if found_vote: # existed
        if vote.dir == 1:  # existed && wants to vote (again) >> impossible
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user with id: {curr_user.id} already voted to post with id: {vote.post_id}")
        db.delete(found_vote)
        db.commit()
        return {"message":f"The vote of user with id [{curr_user.id}] to the post with id [{vote.post_id}] was deleted successfully!"}
    
    else: # does not existed
        if vote.dir == 0: # the user wants to remove not existed vote >> impossible
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"There is no vote by user with id: [{curr_user.id}] to post with id: [{vote.post_id}] to be removed")
        new_vote= models.Vote(post_id= vote.post_id, user_id= curr_user.id)
        
        target_post = db.query(models.Post).filter_by(id= vote.post_id).first()
        if not target_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=f"There is no post with id: [{vote.post_id}] to vote to")
        db.add(new_vote)
        db.commit()
        return {"message":f"The vote of user with id [{curr_user.id}] to the post with id [{vote.post_id}] was added successfully!"}

    