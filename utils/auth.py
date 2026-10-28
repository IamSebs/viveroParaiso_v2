from functools import wraps
from flask import session, redirect, url_for, flash, request, abort


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Debe iniciar sesión para continuar.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                flash("Debe iniciar sesión para continuar.", "warning")
                return redirect(url_for("auth.login", next=request.path))
            if session.get("rol") not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


def current_user():
    if not session.get("user_id"):
        return None
    return {
        "id": session.get("user_id"),
        "username": session.get("username"),
        "email": session.get("email"),
        "rol": session.get("rol"),
    }
