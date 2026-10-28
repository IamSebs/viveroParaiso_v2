from database import query_all, query_one, execute


def _filtros(busqueda=None, categoria=None, bajo_stock=False):
    clauses = []
    params = []
    if busqueda:
        clauses.append("(p.nombre LIKE %s OR p.categoria LIKE %s OR p.descripcion LIKE %s)")
        term = f"%{busqueda}%"
        params.extend([term, term, term])
    if categoria:
        clauses.append("p.categoria = %s")
        params.append(categoria)
    if bajo_stock:
        clauses.append("p.cantidad_disponible <= p.stock_minimo")
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    return where, params


def listar(busqueda=None, categoria=None, bajo_stock=False, limite=10, offset=0):
    where, params = _filtros(busqueda, categoria, bajo_stock)
    total_row = query_one(f"SELECT COUNT(*) AS total FROM productos p {where}", tuple(params))
    sql = f"""
        SELECT p.id, p.nombre, p.categoria, p.descripcion, p.precio_compra, p.precio_venta,
               p.cantidad_disponible, p.stock_minimo, p.proveedor_id, p.fecha_registro,
               pr.nombre_empresa AS proveedor_nombre
        FROM productos p
        INNER JOIN proveedores pr ON pr.id = p.proveedor_id
        {where}
        ORDER BY p.fecha_registro DESC
        LIMIT %s OFFSET %s
    """
    query_params = list(params)
    query_params.extend([limite, offset])
    return query_all(sql, tuple(query_params)), int(total_row["total"]) if total_row else 0


def obtener(producto_id):
    return query_one(
        """
        SELECT p.*, pr.nombre_empresa AS proveedor_nombre
        FROM productos p
        INNER JOIN proveedores pr ON pr.id = p.proveedor_id
        WHERE p.id = %s
        """,
        (producto_id,),
    )


def crear(data):
    sql = """
        INSERT INTO productos
            (nombre, categoria, descripcion, precio_compra, precio_venta,
             cantidad_disponible, stock_minimo, proveedor_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    last_id, _ = execute(
        sql,
        (
            data["nombre"],
            data["categoria"],
            data.get("descripcion") or None,
            data["precio_compra"],
            data["precio_venta"],
            data["cantidad_disponible"],
            data["stock_minimo"],
            data["proveedor_id"],
        ),
    )
    return last_id


def actualizar(producto_id, data):
    sql = """
        UPDATE productos
        SET nombre = %s, categoria = %s, descripcion = %s, precio_compra = %s,
            precio_venta = %s, cantidad_disponible = %s, stock_minimo = %s, proveedor_id = %s
        WHERE id = %s
    """
    _, count = execute(
        sql,
        (
            data["nombre"],
            data["categoria"],
            data.get("descripcion") or None,
            data["precio_compra"],
            data["precio_venta"],
            data["cantidad_disponible"],
            data["stock_minimo"],
            data["proveedor_id"],
            producto_id,
        ),
    )
    return count


def eliminar(producto_id):
    _, count = execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    return count


def total():
    row = query_one("SELECT COUNT(*) AS total FROM productos")
    return int(row["total"]) if row else 0


def recientes(limite=5):
    return query_all(
        """
        SELECT p.id, p.nombre, p.categoria, p.cantidad_disponible, p.precio_venta, p.fecha_registro
        FROM productos p
        ORDER BY p.fecha_registro DESC
        LIMIT %s
        """,
        (limite,),
    )


def stock_bajo(limite=8):
    return query_all(
        """
        SELECT id, nombre, cantidad_disponible, stock_minimo, categoria
        FROM productos
        WHERE cantidad_disponible <= stock_minimo
        ORDER BY cantidad_disponible ASC
        LIMIT %s
        """,
        (limite,),
    )


def categorias():
    rows = query_all("SELECT DISTINCT categoria FROM productos ORDER BY categoria")
    return [row["categoria"] for row in rows]
