from fastapi import FastAPI, APIRouter
from .routers import post, user, auth, vote
from .database import engine
from .models import Base


Base.metadata.create_all(bind=engine)


app = FastAPI()

router = APIRouter(tags=["Project Info"])

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@router.get("/")
async def root():
    context = {"project_name": "FAST PlayGround", "version": "1.0.0"}
    return context


app.include_router(router)
