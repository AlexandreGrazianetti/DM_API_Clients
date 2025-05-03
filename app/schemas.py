from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field,ConfigDict

class ClientBase(BaseModel):
    """Schéma de base pour les clients."""
    nom: str = Field(..., min_length=2, max_length=50)
    prenom: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    telephone: Optional[str] = Field(None, min_length=8, max_length=15)
    actif: bool = True

class ClientCreate(ClientBase):
    """Schéma pour la création d'un client."""
#    pass

class ClientUpdate(BaseModel):
    """Schéma pour la mise à jour d'un client."""
    nom: Optional[str] = Field(None, min_length=2, max_length=50)
    prenom: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    telephone: Optional[str] = Field(None, min_length=8, max_length=15)
    actif: Optional[bool] = None

class ClientResponse(ClientBase):
    """Schéma pour la réponse d'un client."""
    id: int
    date_creation: datetime
    date_modification: Optional[datetime] = None
    model_config =  ConfigDict(from_attributes = True)

         
class ClientList(BaseModel):
    """Schéma pour la liste des clients."""
    clients: List[ClientResponse]
    total: int