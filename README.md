# Vivero El Paraíso de las Plantas

Sistema de información web académico para administrar productos, clientes, empleados y proveedores. Está construido con **Python, Flask, MySQL, HTML5 y CSS3**.

## Requisitos

- Windows 10 o 11
- Visual Studio Code
- Python 3.11 o superior
- MySQL 8 o superior
- PowerShell

## 1. Instalar Python

1. Descargue Python desde [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Durante la instalación, active **Add python.exe to PATH**.
3. Compruebe la instalación:

```powershell
python --version
```

## 2. Instalar y configurar MySQL

1. Instale MySQL Server y MySQL Workbench (opcional).
2. Recuerde la contraseña del usuario `root`.
3. Inicie el servicio MySQL desde Servicios de Windows o:

```powershell
Get-Service *mysql*
```

## 3. Crear la base de datos con `schema.sql`

Abra MySQL y ejecute el script del proyecto. Desde PowerShell, si `mysql` está en el PATH:

```powershell
cd C:\Users\LENOVO\Documents\vivero-paraiso
mysql -u root -p < schema.sql
```

Si el operador `<` no funciona en PowerShell, use:

```powershell
Get-Content .\schema.sql | mysql -u root -p
```

También puede abrir MySQL Workbench, crear una conexión local y ejecutar todo el contenido de `schema.sql`. Eso crea la base `vivero_paraiso` y las tablas `usuarios`, `clientes`, `empleados`, `proveedores`, `productos` e `intentos_acceso`.

## 4. Crear el entorno virtual

```powershell
cd C:\Users\LENOVO\Documents\vivero-paraiso
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución de scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## 5. Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Configurar variables de entorno

```powershell
Copy-Item .env.example .env
notepad .env
```

Complete al menos:

- `SECRET_KEY`: una cadena larga y aleatoria.
- `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`.
- `ADMIN_USERNAME`, `ADMIN_EMAIL` y `ADMIN_PASSWORD` para crear el administrador (no se guardan en el código fuente).

Ejemplo para generar una clave secreta:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

## 7. Crear el usuario administrador

```powershell
python init_admin.py
```

Si las variables `ADMIN_*` no están en `.env`, el script las solicitará. La contraseña se almacena con hash de Werkzeug, nunca en texto plano.

Datos de demostración opcionales:

```powershell
python seed.py
```

## 8. Ejecutar Flask

```powershell
$env:FLASK_APP = "app.py"
python app.py
```

## 9. Abrir la aplicación

En el navegador entre a:



## 10. Probar el sistema

1. Inicie sesión con el usuario administrador creado.
2. Revise el dashboard: los contadores salen de MySQL.
3. Cree, consulte, edite y elimine registros en productos, clientes y proveedores.
4. El módulo de empleados solo está disponible para el rol `admin`.
5. Busque productos por nombre o categoría y active el filtro de stock bajo.
6. Intente eliminar un proveedor con productos asociados: el sistema lo impide.
7. Cierre sesión con el botón del menú.

## 11. Errores frecuentes

**No fue posible conectar con MySQL**

- Confirme que el servicio MySQL está en ejecución.
- Verifique `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER` y `MYSQL_PASSWORD` en `.env`.
- Confirme que ejecutó `schema.sql` y que existe la base `vivero_paraiso`.

**SECRET_KEY no está definida**

- Copie `.env.example` a `.env` y asigne una clave.

**pip o python no se reconocen**

- Reinstale Python marcando *Add to PATH* y abra una nueva terminal.

**Execution Policy**

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Access denied for user**

- Pruebe la contraseña de MySQL en MySQL Workbench o con `mysql -u root -p`.

## Pruebas automatizadas básicas

```powershell
pytest -q
```

Estas pruebas cubren validaciones, hash de contraseñas y protección de rutas privadas. Las pruebas de CRUD completo requieren MySQL en ejecución y se validan de forma manual según la sección 10.

## Estructura

```
vivero-paraiso/
  app.py
  config.py
  database.py
  init_admin.py
  seed.py
  schema.sql
  blueprints/
  data/
  templates/
  static/
  tests/
```

## Seguridad implementada

- Sesiones de Flask con cookies HTTPOnly.
- CSRF en formularios con Flask-WTF.
- Contraseñas con `generate_password_hash` / `check_password_hash`.
- Consultas parametrizadas (`%s`) para prevenir inyección SQL.
- Decoradores `login_required` y `roles_required`.
- Bloqueo temporal tras intentos fallidos de inicio de sesión.
- Integridad referencial: no se elimina un proveedor si tiene productos.
