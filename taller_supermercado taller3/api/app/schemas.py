from pydantic import BaseModel, ConfigDict

class CategoriaSalida(BaseModel):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class ProductoSalida(BaseModel):
    id: int
    sku: str
    nombre: str
    precio: float
    stock: int
    categoria: CategoriaSalida
    model_config = ConfigDict(from_attributes=True)
