from ..models import Vote, Post
from .. import schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status, Depends, APIRouter

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Vote)
async def create_vote(
    payload: schemas.Vote,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    try:
        vote_query = db.query(Vote).filter(
            Vote.post_id == payload.post_id, Vote.user_id == curr_user.id
        )
        vote_found = vote_query.first()
        if payload.dir == 1:
            if vote_found:
                return Response(
                    content="Vote already exists", status_code=status.HTTP_409_CONFLICT
                )
            elif not vote_found:
                post_query = db.query(Post).filter(Post.id == payload.post_id)
                post_found = post_query.first()
                if not post_found:
                    return Response(
                        content="Post not found", status_code=status.HTTP_404_NOT_FOUND
                    )
            new_vote = Vote(post_id=payload.post_id, user_id=curr_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return Response(
                content="Vote created successfully", status_code=status.HTTP_201_CREATED
            )
        else:
            if not vote_found:
                return Response(
                    content="Vote not found", status_code=status.HTTP_404_NOT_FOUND
                )
            vote_query.delete(synchronize_session=False)
            db.commit()
            return Response(
                status_code=status.HTTP_204_NO_CONTENT,
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
