from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas import ClientCreate, ClientUpdate
from app.services import client_service

def create_client(client_data: ClientCreate, db: Session):
    try:
        new_client = client_service.create_client_in_db(db, client_data)
        return new_client
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un client avec cet email existe déjà."
        )

def list_clients(skip: int, limit: int, actif: bool, db: Session):
    return client_service.get_clients(db, skip, limit, actif)

def get_client(client_id: int, db: Session):
    client = client_service.get_client_by_id(db, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

def update_client(client_id: int, client_update: ClientUpdate, db: Session):
    try:
        updated = client_service.update_client_in_db(db, client_id, client_update)
        return updated
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

def delete_client(client_id: int, db: Session):
    if not client_service.delete_client_from_db(db, client_id):
        raise HTTPException(status_code=404, detail="Client non trouvé")
