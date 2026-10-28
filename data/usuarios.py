from datetime import datetime, timedelta
from database import query_one, execute


def find_by_login(identificador):
    sql = """
        SELECT id, username, email, password_hash, rol, activo
        FROM usuarios
        WHERE username = %s OR email = %s
        LIMIT 1
    """
    return query_one(sql, (identificador, identificador))


def find_by_username(username):
    return query_one("SELECT id FROM usuarios WHERE username = %s LIMIT 1", (username,))


def find_by_email(email):
    return query_one("SELECT id FROM usuarios WHERE email = %s LIMIT 1", (email,))


def create_user(username, email, password_hash, rol="admin"):
    sql = """
        INSERT INTO usuarios (username, email, password_hash, rol, activo)
        VALUES (%s, %s, %s, %s, 1)
    """
    last_id, _ = execute(sql, (username, email, password_hash, rol))
    return last_id


def count_users():
    row = query_one("SELECT COUNT(*) AS total FROM usuarios")
    return int(row["total"]) if row else 0


def get_attempt(clave):
    return query_one(
        "SELECT id, clave, intentos, bloqueado_hasta FROM intentos_acceso WHERE clave = %s",
        (clave,),
    )


def is_locked(clave):
    row = get_attempt(clave)
    if not row or not row.get("bloqueado_hasta"):
        return False
    return row["bloqueado_hasta"] > datetime.now()


def register_failed_attempt(clave, max_attempts, lock_minutes):
    row = get_attempt(clave)
    if row:
        intentos = int(row["intentos"]) + 1
        bloqueado = None
        if intentos >= max_attempts:
            bloqueado = datetime.now() + timedelta(minutes=lock_minutes)
            intentos = 0
        execute(
            "UPDATE intentos_acceso SET intentos = %s, bloqueado_hasta = %s WHERE clave = %s",
            (intentos, bloqueado, clave),
        )
        return bloqueado is not None
    execute(
        "INSERT INTO intentos_acceso (clave, intentos, bloqueado_hasta) VALUES (%s, %s, NULL)",
        (clave, 1),
    )
    return False


def clear_attempts(clave):
    execute("DELETE FROM intentos_acceso WHERE clave = %s", (clave,))
