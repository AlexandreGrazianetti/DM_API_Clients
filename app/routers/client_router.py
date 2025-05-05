from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import client_controller
from app.database import get_db
from app.schemas import ClientCreate, ClientResponse, ClientUpdate, ClientList

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return client_controller.create_client(client, db)

@router.get("/", response_model=ClientList)
def list_clients(skip: int = 0, limit: int = 100, actif: bool = None, db: Session = Depends(get_db)):
    return client_controller.list_clients(skip, limit, actif, db)

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    return client_controller.get_client(client_id, db)

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_update: ClientUpdate, db: Session = Depends(get_db)):
    return client_controller.update_client(client_id, client_update, db)

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    return client_controller.delete_client(client_id, db)
