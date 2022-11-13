from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import Session, create_engine, select

from .models import engine, Hero
from .settings import Settings

settings = Settings() # type: ignore
app = FastAPI(debug=settings.debug)

origins = [
    'http://localhost:4200',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/hero/list')
async def get_hero_list():
    with Session(engine) as s:
        heroes = s.exec(select(Hero)).all()
        return heroes

@app.get('/hero/{id}')
async def get_hero(id: int):
    with Session(engine) as s:
        hero = s.get(Hero, id)
        return hero

