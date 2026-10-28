from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from blueprints.helpers import paginacion, form_data
from data import clientes
from database import DatabaseError
from utils.auth import login_required
from utils.validators import (
    DOCUMENT_TYPES,
    clean,
    required,
    validate_choice,
    validate_document,
    validate_email,
    validate_phone,
    collect_errors,
)

bp = Blueprint("clientes", __name__, url_prefix="/clientes")
FIELDS = ("nombres", "apellidos", "tipo_documento", "numero_documento", "telefono", "correo", "direccion")


def _validar(payload, excluir_id=None):
    values, errors = collect_errors(
        required(payload.get("nombres"), "nombres"),
        required(payload.get("apellidos"), "apellidos"),
        validate_choice(payload.get("tipo_documento"), DOCUMENT_TYPES, "tipo de documento"),
        validate_document(payload.get("numero_documento")),
        validate_phone(payload.get("telefono")),
        validate_email(payload.get("correo")),
        required(payload.get("direccion"), "dirección"),
    )
    nombres, apellidos, tipo, numero, telefono, correo, direccion = values
    if numero and clientes.documento_existe(numero, excluir_id):
        errors.append("Ya existe un cliente con ese número de documento.")
    if correo and clientes.correo_existe(correo, excluir_id):
        errors.append("Ya existe un cliente con ese correo electrónico.")
    if errors:
        return None, errors
    return {
        "nombres": nombres,
        "apellidos": apellidos,
        "tipo_documento": tipo,
        "numero_documento": numero,
        "telefono": telefono,
        "correo": correo,
        "direccion": direccion,
    }, []


@bp.route("/")
@login_required
def lista():
    busqueda = clean(request.args.get("q"))
    try:
        _, total = clientes.listar(busqueda=busqueda or None, limite=1, offset=0)
        page, per_page, offset, pages = paginacion(total)
        registros, total = clientes.listar(busqueda=busqueda or None, limite=per_page, offset=offset)
    except DatabaseError:
        flash("No se pudieron consultar los clientes.", "error")
        registros, total, page, pages = [], 0, 1, 1
    return render_template("clientes/lista.html", clientes=registros, total=total, page=page, pages=pages, q=busqueda)


@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def crear():
    if request.method == "POST":
        payload = form_data(FIELDS)
        data, errors = _validar(payload)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("clientes/formulario.html", cliente=payload, modo="crear")
        try:
            clientes.crear(data)
            flash("Cliente registrado correctamente.", "success")
            return redirect(url_for("clientes.lista"))
        except DatabaseError:
            flash("No se pudo registrar el cliente.", "error")
    return render_template("clientes/formulario.html", cliente=None, modo="crear")


@bp.route("/<int:cliente_id>")
@login_required
def detalle(cliente_id):
    cliente = clientes.obtener(cliente_id)
    if not cliente:
        abort(404)
    return render_template("clientes/detalle.html", cliente=cliente)


@bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
@login_required
def editar(cliente_id):
    cliente = clientes.obtener(cliente_id)
    if not cliente:
        abort(404)
    if request.method == "POST":
        payload = form_data(FIELDS)
        data, errors = _validar(payload, excluir_id=cliente_id)
        if errors:
            for error in errors:
                flash(error, "error")
            payload["id"] = cliente_id
            return render_template("clientes/formulario.html", cliente=payload, modo="editar")
        try:
            clientes.actualizar(cliente_id, data)
            flash("Cliente actualizado correctamente.", "success")
            return redirect(url_for("clientes.detalle", cliente_id=cliente_id))
        except DatabaseError:
            flash("No se pudo actualizar el cliente.", "error")
    return render_template("clientes/formulario.html", cliente=cliente, modo="editar")


@bp.route("/<int:cliente_id>/eliminar", methods=["POST"])
@login_required
def eliminar(cliente_id):
    cliente = clientes.obtener(cliente_id)
    if not cliente:
        abort(404)
    try:
        clientes.eliminar(cliente_id)
        flash("Cliente eliminado correctamente.", "success")
    except DatabaseError:
        flash("No se pudo eliminar el cliente.", "error")
    return redirect(url_for("clientes.lista"))
