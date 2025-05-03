from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    """Modèle de données pour la table client."""
  
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telephone = Column(String)
    actif = Column(Boolean, default=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())