import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import time
import gc
from app.database import Base, get_db
from app.main import app
from app.routers.client_router import router as client_router
from app.models import Client

# Base de données de test
TEST_DB_URL = "sqlite:///./test_client_db.sqlite"


@pytest.fixture(scope="session")
def test_engine():
    """Crée un moteur de base de données de test."""
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})

    # Création des tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Nettoyage après les tests
    Base.metadata.drop_all(bind=engine)

    # Ferme toutes les connexions
    engine.dispose()

    # Force le garbage collection (utile sur Windows pour SQLite)
    gc.collect()

    time.sleep(0.2)

    # Supprimer le fichier SQLite
    try:
        if os.path.exists("./test_client_db.sqlite"):
            os.remove("./test_client_db.sqlite")
    except PermissionError as e:
        print(f"Impossible de supprimer test_client_db.sqlite : {e}")

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Crée une session de base de données de test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(test_db):
    """Crée un client de test pour l'API FastAPI."""
    
    # Override de la dépendance de base de données
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Nettoyage après chaque test
    for table in reversed(Base.metadata.sorted_tables):
        test_db.execute(table.delete())
    test_db.commit()

@pytest.fixture(scope="function")
def sample_clients(test_db):
    """Crée des clients de test dans la base de données."""
    clients = [
        Client(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@example.com",
            telephone="0123456789",
            actif=True
        ),
        Client(
            nom="Martin",
            prenom="Marie",
            email="marie.martin@example.com",
            telephone="0987654321",
            actif=True
        ),
        Client(
            nom="Durand",
            prenom="Pierre",
            email="pierre.durand@example.com",
            telephone="0654321789",
            actif=False
        )
    ]
    
    test_db.add_all(clients)
    test_db.commit()
    
    # Rafraîchir pour obtenir les IDs
    for client in clients:
        test_db.refresh(client)
    
    return clients