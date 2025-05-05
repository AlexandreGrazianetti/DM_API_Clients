from sqlalchemy.orm import Session
from app.models import Client
from app.schemas import ClientCreate, ClientUpdate

def create_client_in_db(db: Session, client_data: ClientCreate) -> Client:
    db_client = Client(**client_data.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session, skip: int, limit: int, actif: bool = None):
    query = db.query(Client)
    if actif is not None:
        query = query.filter(Client.actif == actif)
    total = query.count()
    clients = query.offset(skip).limit(limit).all()
    return {"clients": clients, "total": total}

def get_client_by_id(db: Session, client_id: int) -> Client:
    return db.query(Client).filter(Client.id == client_id).first()

def update_client_in_db(db: Session, client_id: int, update_data: ClientUpdate) -> Client:
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise ValueError("Client non trouvé")
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

def delete_client_from_db(db: Session, client_id: int) -> bool:
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        return False
    db.delete(client)
    db.commit()
    return True
