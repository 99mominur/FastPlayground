from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status, Depends, APIRouter
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
async def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    try:
        results = (
            db.query(
                models.Post, func.count(models.Vote.post_id).label("votes"), models.User
            )
            .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
            .join(
                models.User, models.User.id == models.Post.user_id
            )  # Join with User table
            .group_by(models.Post.id, models.User.id)  # Group by Post and User
            .filter(models.Post.title.contains(search))
            .offset(skip)
            .limit(limit)
            .all()
        )

        posts = [
            {
                **post.__dict__,
                "votes": votes,
                "owner": user.__dict__,
            }
            for (post, votes, user) in results
        ]

        if not posts:
            return Response(
                content="No posts found", status_code=status.HTTP_404_NOT_FOUND
            )
        return posts

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{id}", response_model=schemas.Post)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if post is None:
            return Response(
                content="Post not found", status_code=status.HTTP_404_NOT_FOUND
            )

        return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/", status_code=201)
async def create_posts(
    payload: schemas.PayloadPost,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        print(curr_user)
        post = models.Post(**payload.dict(), user_id=curr_user.id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.put("/{id}", response_model=schemas.Post)
async def update_post(
    id: int,
    payload: schemas.PayloadPost,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()
        if post is None:
            return Response(
                content="Post not found", status_code=status.HTTP_404_NOT_FOUND
            )
        if post.user_id != curr_user.id:
            return Response(
                content="Not authorized to update this post",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        post_query.update(payload.dict(), synchronize_session=False)
        db.commit()
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/{id}")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oauth2.get_current_user),
):

    try:
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()

        if post is None:
            return Response(
                content="Post not found", status_code=status.HTTP_404_NOT_FOUND
            )

        if post.user_id != curr_user.id:
            return Response(
                content="Not authorized to delete this post",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(
            content=f"Post with ID {id} deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred from delete_post function: {str(e)}",
        )
