import pytest
from app.models import Client
from app.database import SessionLocal
from sqlalchemy.exc import IntegrityError

def test_create_client(test_db):
    """Test unitaire pour la création d'un client."""
    client = Client(
        nom="Leclerc",
        prenom="Paul",
        email="paul.leclerc@example.com",
        telephone="0123456789",
        actif=True
    )
    
    test_db.add(client)
    test_db.commit()
    test_db.refresh(client)
    
    assert client.nom == "Leclerc"
    assert client.prenom == "Paul"
    assert client.email == "paul.leclerc@example.com"
    assert client.actif is True

def test_duplicate_email(test_db):
    """Test unitaire pour vérifier l'unicité de l'email (clé unique)."""
    client1 = Client(
        nom="Dupont",
        prenom="Jean",
        email="dupont.jean@example.com",
        telephone="0123456789",
        actif=True
    )
    client2 = Client(
        nom="Martin",
        prenom="Marie",
        email="dupont.jean@example.com",  # Même email
        telephone="0987654321",
        actif=True
    )

    test_db.add(client1)
    test_db.commit()
    test_db.refresh(client1)

    # Tentative d'ajouter un client avec le même email
    test_db.add(client2)

    with pytest.raises(IntegrityError):
        test_db.commit()  # Cela devrait échouer à cause de l'unicité de l'email
