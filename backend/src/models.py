from sqlmodel import Field, SQLModel, create_engine

from .settings import Settings

settings = Settings() # type: ignore
engine = create_engine(
    url=settings.database_url,
    connect_args=settings.connect_args,
)

class Hero(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    name: str

# test database
if __name__ == '__main__':
    from sqlmodel import Session
    heroes: list[Hero] = [
        Hero(name="Deadpond"), 
        Hero(name="Dive Wilson"),
        Hero(name="Rusty"),
        Hero(name="Tornado"),
        Hero(name="Magma"),
        Hero(name="Celeritas"),
        Hero(name="Magneta"),
    ]
    
    print('Creating database...')
    engine = create_engine("sqlite:///../db.sqlite")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        for hero in heroes:
            s.add(hero)
        s.commit()
    
    