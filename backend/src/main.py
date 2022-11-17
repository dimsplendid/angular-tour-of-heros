from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import Session, create_engine, select, col

from .models import (
    engine, 
    Hero, 
    HeroUpdate,
    create_db_and_tables,
)
from .settings import Settings

settings = Settings() # type: ignore
app = FastAPI(debug=settings.debug)

origins = [
    'http://127.0.0.1:4200',
    'http://localhost:4200',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_session():
    with Session(engine) as session:
        yield session

@app.get('/hero/list')
async def get_hero_list(session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero)).all()
    return heroes

@app.get('/hero/{id}')
async def get_hero(id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, id)
    return hero

@app.patch('/hero/{id}')
async def update_hero(
    id: int, 
    hero: HeroUpdate, 
    session: Session = Depends(get_session)
):
    db_hero = session.get(Hero, id)
    if not db_hero:
        raise HTTPException(status_code=404, detail='Hero not found')
    hero_data = hero.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.post('/hero/create')
async def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.delete('/hero/{id}')
async def delete_hero(id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, id)
    if not hero:
        raise HTTPException(status_code=404, detail='Hero not found')
    session.delete(hero)
    session.commit()
    return {'ok': True}

@app.get('/hero/search/')
async def search_heroes(name: str, session: Session = Depends(get_session)):
    heroes = session.exec(
        select(Hero).where(col(Hero.name).contains(name))
    ).all()
    return heroes

@app.on_event('startup')
def on_startup():
    create_db_and_tables()