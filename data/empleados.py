from database import query_all, query_one, execute


def listar(busqueda=None, limite=10, offset=0):
    where = ""
    params = []
    if busqueda:
        where = """
            WHERE nombres LIKE %s
               OR apellidos LIKE %s
               OR numero_documento LIKE %s
               OR correo LIKE %s
               OR cargo LIKE %s
        """
        term = f"%{busqueda}%"
        params.extend([term, term, term, term, term])
    total_row = query_one(f"SELECT COUNT(*) AS total FROM empleados {where}", tuple(params))
    sql = f"""
        SELECT id, nombres, apellidos, tipo_documento, numero_documento, cargo,
               telefono, correo, fecha_contratacion, estado_laboral, fecha_registro
        FROM empleados
        {where}
        ORDER BY apellidos ASC, nombres ASC
        LIMIT %s OFFSET %s
    """
    params.extend([limite, offset])
    return query_all(sql, tuple(params)), int(total_row["total"]) if total_row else 0


def obtener(empleado_id):
    return query_one("SELECT * FROM empleados WHERE id = %s", (empleado_id,))


def documento_existe(numero, excluir_id=None):
    if excluir_id:
        row = query_one(
            "SELECT id FROM empleados WHERE numero_documento = %s AND id <> %s",
            (numero, excluir_id),
        )
    else:
        row = query_one("SELECT id FROM empleados WHERE numero_documento = %s", (numero,))
    return row is not None


def correo_existe(correo, excluir_id=None):
    if excluir_id:
        row = query_one(
            "SELECT id FROM empleados WHERE correo = %s AND id <> %s",
            (correo, excluir_id),
        )
    else:
        row = query_one("SELECT id FROM empleados WHERE correo = %s", (correo,))
    return row is not None


def crear(data):
    sql = """
        INSERT INTO empleados
            (nombres, apellidos, tipo_documento, numero_documento, cargo,
             telefono, correo, fecha_contratacion, estado_laboral)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    last_id, _ = execute(
        sql,
        (
            data["nombres"],
            data["apellidos"],
            data["tipo_documento"],
            data["numero_documento"],
            data["cargo"],
            data["telefono"],
            data["correo"],
            data["fecha_contratacion"],
            data["estado_laboral"],
        ),
    )
    return last_id


def actualizar(empleado_id, data):
    sql = """
        UPDATE empleados
        SET nombres = %s, apellidos = %s, tipo_documento = %s, numero_documento = %s,
            cargo = %s, telefono = %s, correo = %s, fecha_contratacion = %s, estado_laboral = %s
        WHERE id = %s
    """
    _, count = execute(
        sql,
        (
            data["nombres"],
            data["apellidos"],
            data["tipo_documento"],
            data["numero_documento"],
            data["cargo"],
            data["telefono"],
            data["correo"],
            data["fecha_contratacion"],
            data["estado_laboral"],
            empleado_id,
        ),
    )
    return count


def eliminar(empleado_id):
    _, count = execute("DELETE FROM empleados WHERE id = %s", (empleado_id,))
    return count


def total():
    row = query_one("SELECT COUNT(*) AS total FROM empleados")
    return int(row["total"]) if row else 0
