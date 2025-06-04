# db.py
from sqlalchemy.orm import sessionmaker
from genera_tablas import engine

# Creamos el sessionmaker
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    """
    Retorna una nueva sesión de SQLAlchemy.
    """
    return SessionLocal()
