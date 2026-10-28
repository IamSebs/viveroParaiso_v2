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
        """
        term = f"%{busqueda}%"
        params.extend([term, term, term, term])
    total_row = query_one(f"SELECT COUNT(*) AS total FROM clientes {where}", tuple(params))
    sql = f"""
        SELECT id, nombres, apellidos, tipo_documento, numero_documento,
               telefono, correo, direccion, fecha_registro
        FROM clientes
        {where}
        ORDER BY apellidos ASC, nombres ASC
        LIMIT %s OFFSET %s
    """
    params.extend([limite, offset])
    return query_all(sql, tuple(params)), int(total_row["total"]) if total_row else 0


def obtener(cliente_id):
    return query_one("SELECT * FROM clientes WHERE id = %s", (cliente_id,))


def documento_existe(numero, excluir_id=None):
    if excluir_id:
        row = query_one(
            "SELECT id FROM clientes WHERE numero_documento = %s AND id <> %s",
            (numero, excluir_id),
        )
    else:
        row = query_one("SELECT id FROM clientes WHERE numero_documento = %s", (numero,))
    return row is not None


def correo_existe(correo, excluir_id=None):
    if excluir_id:
        row = query_one(
            "SELECT id FROM clientes WHERE correo = %s AND id <> %s",
            (correo, excluir_id),
        )
    else:
        row = query_one("SELECT id FROM clientes WHERE correo = %s", (correo,))
    return row is not None


def crear(data):
    sql = """
        INSERT INTO clientes
            (nombres, apellidos, tipo_documento, numero_documento, telefono, correo, direccion)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    last_id, _ = execute(
        sql,
        (
            data["nombres"],
            data["apellidos"],
            data["tipo_documento"],
            data["numero_documento"],
            data["telefono"],
            data["correo"],
            data["direccion"],
        ),
    )
    return last_id


def actualizar(cliente_id, data):
    sql = """
        UPDATE clientes
        SET nombres = %s, apellidos = %s, tipo_documento = %s, numero_documento = %s,
            telefono = %s, correo = %s, direccion = %s
        WHERE id = %s
    """
    _, count = execute(
        sql,
        (
            data["nombres"],
            data["apellidos"],
            data["tipo_documento"],
            data["numero_documento"],
            data["telefono"],
            data["correo"],
            data["direccion"],
            cliente_id,
        ),
    )
    return count


def eliminar(cliente_id):
    _, count = execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
    return count


def total():
    row = query_one("SELECT COUNT(*) AS total FROM clientes")
    return int(row["total"]) if row else 0
