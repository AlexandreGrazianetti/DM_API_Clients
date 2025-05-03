from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Client
from app.schemas import ClientCreate, ClientResponse, ClientUpdate, ClientList

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Crée un nouveau client."""
    try:
        db_client = Client(**client.model_dump())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un client avec cet email existe déjà."
        ) from exc


@router.get("/", response_model=ClientList)
def list_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    actif: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Liste tous les clients avec pagination et filtrage optionnel."""
    query = db.query(Client)
    
    # Filtrage par statut actif si spécifié
    if actif is not None:
        query = query.filter(Client.actif == actif)
    
    # Compte total pour pagination
    total = query.count()
    
    # Application pagination
    clients = query.offset(skip).limit(limit).all()
    
    return {"clients": clients, "total": total}

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """Récupère un client par son ID."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client avec l'ID {client_id} non trouvé."
        )
    return client

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_update: ClientUpdate, db: Session = Depends(get_db)):
    """Met à jour un client existant."""
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client avec l'ID {client_id} non trouvé."
        )
    
    # Mettre à jour uniquement les champs non-None
    update_data = client_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_client, key, value)
    
    try:
        db.commit()
        db.refresh(db_client)
        return db_client
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un client avec cet email existe déjà."
        )

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Supprime un client."""
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client avec l'ID {client_id} non trouvé."
        )
    
    db.delete(db_client)
    db.commit()
    #return None