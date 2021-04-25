import uvicorn

from fastapi import FastAPI, Depends, HTTPException
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
    id: int
    name: str
    score: int

class LeaderBoardCreateSchema(BaseModel):
    name: str
    score: int

class LeaderBoardUpdateSchema(BaseModel):
    score: int

class LeaderBoardsSchema(BaseModel):
    lead_boards: list

class Config:
    orm_mode = True


@app.post("/leader_board/", response_model=LeaderBoardCreateSchema)
async def create_leader_board(leader_board: LeaderBoardCreateSchema, db: Session = Depends(get_db)):
    name = leader_board.name.strip().upper() if leader_board.name else "ANONYMOUS"
    _leader_board = db.query(LeaderBoard).filter_by(name=name.strip().upper()).first()
    if _leader_board:
        raise HTTPException(status_code=500, detail="User already exist with  this name")
    _leader_board = LeaderBoard(
        name=name, score=leader_board.score
    )
    db.add(_leader_board)
    db.commit()
    db.refresh(_leader_board)
    return {"name": leader_board.name, "score": leader_board.score}


@app.patch("/leader_board/{board_id}", response_model=LeaderBoardUpdateSchema)
async def create_leader_board(board_id: int, leader_board: LeaderBoardUpdateSchema, db: Session = Depends(get_db)):
    _leader_board = db.query(LeaderBoard).filter_by(id=board_id).first()
    _leader_board.score = leader_board.score
    db.commit()
    db.refresh(_leader_board)
    return {"id": _leader_board.id, "score": _leader_board.score}


@app.get("/leader_board/", response_model=LeaderBoardsSchema)
async def get_leader_board(db: Session = Depends(get_db)):
    _leader_board = db.query(LeaderBoard).all()
    return {"lead_boards":[{"id": lb.id, 'name': lb.name, 'score': lb.score} for lb in _leader_board]}


@app.get("/leader_board/{name}", response_model=LeaderBoardSchema)
async def get_leader_board_name(name: str, db: Session = Depends(get_db)):
    _leader_board = db.query(LeaderBoard).filter_by(name=name.strip().upper()).first()
    if not _leader_board:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": _leader_board.id, 'name': _leader_board.name, 'score': _leader_board.score}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
