import pytest
from fastapi import status

def test_create_client(client):
    """Test la création d'un client via l'API."""
    response = client.post(
        "/clients/",
        json={
            "nom": "Doe",
            "prenom": "John",
            "email": "john.doe@example.com",
            "telephone": "0123456789",
            "actif": True
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nom"] == "Doe"
    assert data["prenom"] == "John"
    assert data["email"] == "john.doe@example.com"
    assert data["telephone"] == "0123456789"
    assert data["actif"] == True
    assert "id" in data
    assert "date_creation" in data

def test_create_client_duplicate_email(client, sample_clients):
    """Test la création d'un client avec un email déjà existant."""
    response = client.post(
        "/clients/",
        json={
            "nom": "Dupont",
            "prenom": "Jacques",
            "email": "jean.dupont@example.com",  # Email déjà utilisé
            "telephone": "0123456789",
            "actif": True
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Un client avec cet email existe déjà" in response.json()["detail"]

def test_create_client_invalid_data(client):
    """Test la validation des données lors de la création d'un client."""
    # Email invalide
    response = client.post(
        "/clients/",
        json={
            "nom": "Doe",
            "prenom": "John",
            "email": "invalid-email",
            "telephone": "0123456789",
            "actif": True
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Nom trop court
    response = client.post(
        "/clients/",
        json={
            "nom": "D",
            "prenom": "John",
            "email": "john.doe@example.com",
            "telephone": "0123456789",
            "actif": True
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_client(client, sample_clients):
    """Test la récupération d'un client par son ID."""
    client_id = sample_clients[0].id
    
    response = client.get(f"/clients/{client_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == client_id
    assert data["nom"] == sample_clients[0].nom
    assert data["prenom"] == sample_clients[0].prenom
    assert data["email"] == sample_clients[0].email

def test_get_client_not_found(client):
    """Test la récupération d'un client inexistant."""
    response = client.get("/clients/9999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "non trouvé" in response.json()["detail"]

def test_update_client(client, sample_clients):
    """Test la mise à jour d'un client."""
    client_id = sample_clients[0].id
    
    response = client.put(
        f"/clients/{client_id}",
        json={
            "nom": "Dupont-Modifié",
            "actif": False
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == client_id
    assert data["nom"] == "Dupont-Modifié"
    assert data["prenom"] == sample_clients[0].prenom  # Non modifié
    assert data["actif"] == False

def test_update_client_not_found(client):
    """Test la mise à jour d'un client inexistant."""
    response = client.put(
        "/clients/9999",
        json={
            "nom": "Nouveau Nom"
        }
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "non trouvé" in response.json()["detail"]

def test_delete_client(client, sample_clients):
    """Test la suppression d'un client."""
    client_id = sample_clients[0].id
    
    response = client.delete(f"/clients/{client_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Vérification que le client a bien été supprimé
    get_response = client.get(f"/clients/{client_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_client_not_found(client):
    """Test la suppression d'un client inexistant."""
    response = client.delete("/clients/9999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "non trouvé" in response.json()["detail"]

def test_list_clients(client, sample_clients):
    """Test la liste de tous les clients."""
    response = client.get("/clients/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "clients" in data
    assert "total" in data
    assert data["total"] == len(sample_clients)
    assert len(data["clients"]) == len(sample_clients)

def test_list_clients_with_filter(client, sample_clients):
    """Test la liste des clients avec filtre sur le statut actif."""
    # Récupération des clients actifs
    response = client.get("/clients/?actif=true")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 2  # Deux clients actifs dans sample_clients
    assert all(client["actif"] for client in data["clients"])
    
    # Récupération des clients inactifs
    response = client.get("/clients/?actif=false")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 1  # Un client inactif dans sample_clients
    assert all(not client["actif"] for client in data["clients"])

def test_list_clients_with_pagination(client, sample_clients):
    """Test la pagination de la liste des clients."""
    # Première page avec limite de 1
    response = client.get("/clients/?skip=0&limit=1")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 3  # Total de tous les clients
    assert len(data["clients"]) == 1  # Limite de 1 client
    
    # Deuxième page avec limite de 1
    response = client.get("/clients/?skip=1&limit=1")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 3
    assert len(data["clients"]) == 1
    assert data["clients"][0]["id"] != sample_clients[0].id  # Différent du premier client