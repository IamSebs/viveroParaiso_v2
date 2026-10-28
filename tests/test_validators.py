from utils.validators import validate_email, validate_password, validate_decimal, validate_document


def test_email_valido():
    valor, error = validate_email("contacto@vivero.com")
    assert error is None
    assert valor == "contacto@vivero.com"


def test_email_invalido():
    valor, error = validate_email("correo-malo")
    assert valor is None
    assert error


def test_password_corta():
    valor, error = validate_password("123")
    assert valor is None
    assert "8" in error


def test_precio_invalido():
    valor, error = validate_decimal("abc", "precio")
    assert valor is None
    assert error


def test_documento_valido():
    valor, error = validate_document("1020304050")
    assert error is None
    assert valor == "1020304050"
