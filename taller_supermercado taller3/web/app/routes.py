from flask import Blueprint, render_template, request, abort
from .api_client import obtener_productos, obtener_producto, obtener_categorias

bp = Blueprint("main", __name__)

@bp.route("/")
def inicio():
    categoria_id = request.args.get("categoria", type=int)
    productos = obtener_productos(categoria_id)
    categorias = obtener_categorias()
    return render_template("index.html", productos=productos, categorias=categorias, categoria_id=categoria_id)

@bp.route("/producto/<sku>")
def detalle(sku):
    producto = obtener_producto(sku)
    if producto is None:
        abort(404)
    return render_template("detalle.html", producto=producto)

@bp.route("/categorias")
def categorias():
    return render_template("categorias.html", categorias=obtener_categorias())
