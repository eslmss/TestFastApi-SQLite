from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Esta URL indica que se está usando SQLite, y que la base de datos se almacenará en un archivo llamado items.db en el directorio actual '.'
# SQLite es una base de datos relacional que se almacena en un único archivo, lo que la hace muy ligera y fácil de usar para proyectos pequeños y medianos.
SQLALCHEMY_DATABASE_URL = "sqlite:///./items.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()