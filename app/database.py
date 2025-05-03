from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# Utilisation d'une base de données SQLite pour simplifier
SQLALCHEMY_DATABASE_URL = "sqlite:///./client_db.sqlite"

# Création du moteur de base de données
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Création d'une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles ORM
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()