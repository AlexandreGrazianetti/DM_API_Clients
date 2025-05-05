# 📦 API Clients – FastAPI

Cette API permet de gérer une liste de clients : création, consultation, modification et suppression.  
Elle est développée avec **FastAPI**, suit une **architecture modulaire (Router → Controller → Service)** et utilise **SQLAlchemy** pour l'accès à la base de données.

---

## 🛠️ Prérequis

- Python **3.11.9** recommandé
- `pip` installé
- Un terminal ou invite de commande

---

## 📁 Structure du projet

```

client\_api/
├── app/
│   ├── **init**.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── controllers/
│   │   └── client\_controller.py
│   ├── services/
│   │   └── client\_service.py
│   └── routes/
│       └── client\_router.py
├── tests/
│   ├── unit/
│   │   └── test\_models.py
│   ├── integration/
│   │   └── test\_routes.py
│   └── conftest.py
├── requirements.txt
└── run.py

````

---

## 🚀 Installation

### 1. Créer un environnement virtuel

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
````

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## ▶️ Lancer l'application

```bash
python run.py
```

L'API sera disponible à :

* **[http://localhost:8000](http://localhost:8000)**
* Documentation interactive : **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 📡 Endpoints disponibles

| Méthode | URL                    | Description                               | Code retour                                  |
| ------- | ---------------------- | ----------------------------------------- | -------------------------------------------- |
| POST    | `/clients/`            | Créer un nouveau client                   | `201 Created`                                |
| GET     | `/clients/`            | Lister les clients (filtrage, pagination) | `200 OK`                                     |
| GET     | `/clients/{client_id}` | Récupérer un client par ID                | `200 OK`, `404 Not Found`                    |
| PUT     | `/clients/{client_id}` | Mettre à jour un client                   | `200 OK`, `404 Not Found`, `400 Bad Request` |
| DELETE  | `/clients/{client_id}` | Supprimer un client                       | `204 No Content`, `404 Not Found`            |

### Paramètres disponibles pour `GET /clients/`

* `skip` (int, default: 0) : décalage pour la pagination
* `limit` (int, default: 100) : nombre maximum de résultats
* `actif` (bool) : filtrer par statut actif

---

## ✅ Exécution des tests

### Exécuter tous les tests

```bash
pytest
```

### Par catégorie

```bash
pytest tests/unit/
pytest tests/integration/
```

---

## 🧯 Dépannage

### Erreur d'import

Ajoutez la racine du projet à votre `PYTHONPATH` :

```bash
# Windows
set PYTHONPATH=%PYTHONPATH%;.
# Linux/macOS
export PYTHONPATH=$PYTHONPATH:.
```

### Installer manuellement les paquets si besoin

```bash
pip install fastapi==0.109.2
pip install pydantic==1.10.13
pip install sqlalchemy==2.0.27
pip install pytest==8.0.0
pip install email-validator==2.1.0
```
## ✒️ Auteurs

Marine ADAM
Colas CHASSAGNON
Alexandre GRAZIANETTI