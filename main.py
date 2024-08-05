"""
API - SQL Lite
"""
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from models import Item, ItemDB
from database import get_db, engine
import models
# import uvicorn

# crea todas las tablas en la base de datos basada en los modelos definidos en models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# mensaje de bienvenida al directorio principal (root) de la API
@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Welcome to the Items API", "docs": "/docs"}

# Define un endpoint POST para crear un nuevo item. 
# response_model=Item especifica que la respuesta será del tipo Item. 
# db: Session = Depends(get_db) inyecta una sesión de base de datos en la función
@app.post("/items/", response_model=Item)
def create_item(item: Item, db: Session = Depends(get_db)):
    # Crea un nuevo objeto ItemDB a partir del Item recibido, lo añade a la base de datos, hace commit de los cambios, 
    # actualiza el objeto con cualquier cambio de la base de datos (como IDs autogenerados) y lo devuelve.
    db_item = ItemDB(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Define un endpoint GET para obtener todos los items. 
# Usa skip y limit para paginación.
@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(ItemDB).offset(skip).limit(limit).all()
    return items

# Define un endpoint GET para obtener un item específico por ID. Si no se encuentra, lanza una excepción HTTP 404.
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Define un endpoint PUT para actualizar un item existente. 
# Busca el item por ID, actualiza sus atributos con los nuevos valores, hace commit de los cambios y devuelve el item actualizado.
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

# Define un endpoint DELETE para eliminar un item. 
# Busca el item por ID, lo elimina de la base de datos, hace commit de los cambios y devuelve un mensaje de confirmación.
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}

# Cada método HTTP utiliza db: Session = Depends(get_db) para obtener una sesión de base de datos, 
# esto que permite interactuar con la misma de manera segura y eficiente.


# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# http://192.168.0.89:8000/docs