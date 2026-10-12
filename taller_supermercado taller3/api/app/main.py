from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from .database import Base, engine, get_db
from .models import Categoria, Producto
from .schemas import CategoriaSalida, ProductoSalida

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        if db.query(Categoria).count() == 0:
            frutas = Categoria(nombre="Frutas y verduras")
            lacteos = Categoria(nombre="Lácteos")
            aseo = Categoria(nombre="Aseo")
            db.add_all([frutas, lacteos, aseo])
            db.flush()
            db.add_all([
                Producto(sku="FRU001", nombre="Manzana (unidad)", precio=1200, stock=30, categoria=frutas),
                Producto(sku="FRU002", nombre="Banano (unidad)", precio=700, stock=40, categoria=frutas),
                Producto(sku="LAC001", nombre="Leche (litro)", precio=4200, stock=18, categoria=lacteos),
                Producto(sku="LAC002", nombre="Queso (250 g)", precio=6500, stock=12, categoria=lacteos),
                Producto(sku="ASE001", nombre="Jabón de baño", precio=2800, stock=25, categoria=aseo),
            ])
            db.commit()
    yield

app = FastAPI(title="API del Supermercado", version="1.0", lifespan=lifespan)

@app.get("/productos/", response_model=list[ProductoSalida])
def listar_productos(categoria_id: int | None = None, db: Session = Depends(get_db)):
    consulta = db.query(Producto).options(joinedload(Producto.categoria))
    if categoria_id is not None:
        consulta = consulta.filter(Producto.categoria_id == categoria_id)
    return consulta.order_by(Producto.id).all()

@app.get("/productos/{sku}", response_model=ProductoSalida)
def buscar_producto(sku: str, db: Session = Depends(get_db)):
    producto = db.query(Producto).options(joinedload(Producto.categoria)).filter(Producto.sku == sku).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.get("/categorias/", response_model=list[CategoriaSalida])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).order_by(Categoria.nombre).all()
