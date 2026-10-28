import os

os.environ.setdefault("SECRET_KEY", "clave-de-prueba-academica-no-usar-en-produccion")
os.environ.setdefault("MYSQL_PASSWORD", "test")

from werkzeug.security import generate_password_hash, check_password_hash
from app import create_app


def test_password_no_queda_en_texto_plano():
    texto = "ClaveSegura123"
    hashed = generate_password_hash(texto)
    assert hashed != texto
    assert check_password_hash(hashed, texto)


def test_login_get_disponible():
    app = create_app()
    client = app.test_client()
    response = client.get("/login")
    assert response.status_code == 200
    assert "Iniciar sesión".encode("utf-8") in response.data


def test_dashboard_requiere_autenticacion():
    app = create_app()
    client = app.test_client()
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_empleados_requiere_autenticacion():
    app = create_app()
    client = app.test_client()
    response = client.get("/empleados/", follow_redirects=False)
    assert response.status_code == 302
