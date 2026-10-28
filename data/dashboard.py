from data import productos, clientes, empleados, proveedores


def resumen():
    return {
        "productos": productos.total(),
        "clientes": clientes.total(),
        "empleados": empleados.total(),
        "proveedores": proveedores.total(),
        "recientes": productos.recientes(),
        "stock_bajo": productos.stock_bajo(),
    }
