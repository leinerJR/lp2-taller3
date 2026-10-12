import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

def obtener_productos(categoria_id=None):
    try:
        params = {"categoria_id": categoria_id} if categoria_id else {}
        respuesta = requests.get(f"{API_URL}/productos/", params=params, timeout=4)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException:
        return []

def obtener_producto(sku):
    try:
        respuesta = requests.get(f"{API_URL}/productos/{sku}", timeout=4)
        if respuesta.status_code == 404:
            return None
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException:
        return None

def obtener_categorias():
    try:
        respuesta = requests.get(f"{API_URL}/categorias/", timeout=4)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException:
        return []
