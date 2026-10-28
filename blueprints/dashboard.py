from flask import Blueprint, render_template, flash

from data.dashboard import resumen
from database import DatabaseError
from utils.auth import login_required

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    datos = {
        "productos": 0,
        "clientes": 0,
        "empleados": 0,
        "proveedores": 0,
        "recientes": [],
        "stock_bajo": [],
    }
    try:
        datos = resumen()
    except DatabaseError:
        flash("No se pudieron cargar los indicadores. Verifique MySQL.", "error")
    return render_template("dashboard.html", datos=datos)
