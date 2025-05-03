import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app  # Assure-toi que 'app' est bien importé depuis le bon module
from app.database import Base, get_db, SQLALCHEMY_DATABASE_URL  # Importe Base aussi

# Configuration pour la base de données de test
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_client_db.sqlite"  # Base de test

# Création du moteur et session pour la base de données de test
test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override de la dépendance get_db pour les tests
def override_get_db():
    """
    Remplace la dépendance get_db pour utiliser la base de données de test.
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crée les tables si elles n'existent pas déjà
Base.metadata.create_all(bind=test_engine)

@pytest.fixture(scope="module", autouse=True)
def override_dependency():
    """
    Remplace la dépendance get_db de l'application avec celle pour les tests.
    """
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides = {}

@pytest.fixture(scope="module")
def client():
    """
    Fournit un client de test FastAPI avec gestion automatique des ressources.
    """
    with TestClient(app) as c:
        yield c

class TestAPIValidation:
    """Tests de validation de l'API client complète."""

    def test_full_client_lifecycle(self, client):
        """
        Test de l'ensemble du cycle de vie d'un client :
        création, récupération, mise à jour, liste et suppression.
        """
        # 1. Création d'un client
        create_response = client.post(
            "/clients/",
            json={
                "nom": "Smith",
                "prenom": "John",
                "email": "john.smith@example.com",
                "telephone": "0611223344",
                "actif": True
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        client_data = create_response.json()
        client_id = client_data["id"]

        # 2. Récupération du client créé
        get_response = client.get(f"/clients/{client_id}")
        assert get_response.status_code == status.HTTP_200_OK
        get_data = get_response.json()
        assert get_data["nom"] == "Smith"
        assert get_data["prenom"] == "John"
        assert get_data["email"] == "john.smith@example.com"

        # 3. Mise à jour du client
        update_response = client.put(
            f"/clients/{client_id}",
            json={
                "nom": "Smith-Updated",
                "telephone": "0699887766"
            }
        )
        assert update_response.status_code == status.HTTP_200_OK
        update_data = update_response.json()
        assert update_data["nom"] == "Smith-Updated"
        assert update_data["telephone"] == "0699887766"
        assert update_data["prenom"] == "John"  # Non modifié

        # 4. Vérification dans la liste des clients
        list_response = client.get("/clients/")
        assert list_response.status_code == status.HTTP_200_OK
        list_data = list_response.json()
        assert list_data["total"] >= 1

        # Recherche du client dans la liste
        found = False
        for c in list_data["clients"]:
            if c["id"] == client_id:
                found = True
                assert c["nom"] == "Smith-Updated"
                assert c["telephone"] == "0699887766"
                break
        assert found, "Le client mis à jour n'a pas été trouvé dans la liste"

        # 5. Suppression du client
        delete_response = client.delete(f"/clients/{client_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # 6. Vérification que le client a bien été supprimé
        get_after_delete = client.get(f"/clients/{client_id}")
        assert get_after_delete.status_code == status.HTTP_404_NOT_FOUND

    def test_api_error_handling(self, client):
        """Test de la gestion des erreurs de l'API."""
        # 1. Test d'erreur 404 pour un client inexistant
        get_response = client.get("/clients/9999")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

        # 2. Test d'erreur 422 pour des données invalides
        create_invalid = client.post(
            "/clients/",
            json={
                "nom": "T",  # Trop court
                "prenom": "User",
                "email": "invalid-email",  # Email invalide
                "telephone": "123"  # Téléphone trop court
            }
        )
        assert create_invalid.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
