from math import ceil
from flask import request, current_app


def paginacion(total):
    per_page = current_app.config["ITEMS_PER_PAGE"]
    page = request.args.get("page", default=1, type=int) or 1
    if page < 1:
        page = 1
    pages = max(1, ceil(total / per_page)) if total else 1
    if page > pages:
        page = pages
    offset = (page - 1) * per_page
    return page, per_page, offset, pages


def form_data(fields):
    return {key: request.form.get(key, "") for key in fields}
