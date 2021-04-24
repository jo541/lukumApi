import uvicorn

from fastapi import FastAPI, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

user = "lukum"
password = "lukum"
host = "host.docker.internal"
database = "lukum"
port = "8001"

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class LeaderBoard(Base):
    __tablename__ = "leader_board"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    score = Column(Integer)


Base.metadata.create_all(bind=engine, checkfirst=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


class LeaderBoardSchema(BaseModel):
    name: str
    score: int


class Config:
    orm_mode = True


@app.post("/leader_board/", response_model=LeaderBoardSchema)
async def create_leader_board(leader_board: LeaderBoardSchema, db: Session = Depends(get_db)):
    _leader_board = LeaderBoard(
        name=leader_board.name, score=leader_board.score
    )
    db.add(_leader_board)
    db.commit()
    db.refresh(_leader_board)
    return {"name": leader_board.name, "score": leader_board.score}


@app.get("/leader_board/", response_model=List[LeaderBoardSchema])
async def get_leader_board(db: Session = Depends(get_db)):
    _leader_board = db.query(LeaderBoard).all()

    return [{'name': lb.name, 'score':lb.score } for lb in _leader_board]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
