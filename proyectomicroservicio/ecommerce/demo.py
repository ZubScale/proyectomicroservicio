# demo.py — Demostración completa de los 4 microservicios
# Ejecutar desde la carpeta ecommerce/ con: python demo.py
# (los 4 servicios deben estar corriendo)

import httpx

GATEWAY = "http://localhost:8000"

def separador(titulo: str):
    print(f"\n{'═' * 55}")
    print(f"  {titulo}")
    print('═' * 55)

def mostrar(resp: httpx.Response):
    import json
    data = resp.json()
    print(f"  Status : {resp.status_code}")
    print(f"  Resp   : {json.dumps(data, indent=4, ensure_ascii=False)}")


# ══════════════════════════════════════════════════════
#  1. SERVICIO DE USUARIOS
# ══════════════════════════════════════════════════════

separador("1. CREAR USUARIOS")

resp = httpx.post(f"{GATEWAY}/usuarios/usuarios/", json={
    "nombre": "Ana Garcia",
    "email": "ana@ejemplo.com",
    "password": "segura123"
})
mostrar(resp)
usuario_1 = resp.json()

resp = httpx.post(f"{GATEWAY}/usuarios/usuarios/", json={
    "nombre": "Carlos Lopez",
    "email": "carlos@ejemplo.com",
    "password": "clave456"
})
mostrar(resp)
usuario_2 = resp.json()

separador("2. LISTAR USUARIOS")
resp = httpx.get(f"{GATEWAY}/usuarios/usuarios/")
mostrar(resp)

separador("3. OBTENER UN USUARIO POR ID")
resp = httpx.get(f"{GATEWAY}/usuarios/usuarios/{usuario_1['id']}")
mostrar(resp)

separador("4. ERROR — EMAIL DUPLICADO")
resp = httpx.post(f"{GATEWAY}/usuarios/usuarios/", json={
    "nombre": "Ana Duplicada",
    "email": "ana@ejemplo.com",
    "password": "otra"
})
mostrar(resp)


# ══════════════════════════════════════════════════════
#  2. SERVICIO DE PRODUCTOS
# ══════════════════════════════════════════════════════

separador("5. LISTAR PRODUCTOS")
resp = httpx.get(f"{GATEWAY}/productos/productos/")
mostrar(resp)
productos = resp.json()

separador("6. OBTENER UN PRODUCTO")
resp = httpx.get(f"{GATEWAY}/productos/productos/{productos[0]['id']}")
mostrar(resp)

separador("7. CREAR UN NUEVO PRODUCTO")
resp = httpx.post(f"{GATEWAY}/productos/productos/", json={
    "nombre": "Mouse Inalambrico",
    "precio": 49.99,
    "stock": 20,
    "descripcion": "Bluetooth 5.0"
})
mostrar(resp)
nuevo_producto = resp.json()

separador("8. ACTUALIZAR STOCK DE UN PRODUCTO")
resp = httpx.patch(
    f"{GATEWAY}/productos/productos/{productos[1]['id']}/stock",
    json={"cantidad": 5}
)
mostrar(resp)


# ══════════════════════════════════════════════════════
#  3. SERVICIO DE PEDIDOS (orquesta Usuarios + Productos)
# ══════════════════════════════════════════════════════

separador("9. CREAR PEDIDO — UN PRODUCTO")
resp = httpx.post(f"{GATEWAY}/pedidos/pedidos/", json={
    "usuario_id": usuario_1["id"],
    "items": [
        {"producto_id": productos[1]["id"], "cantidad": 2}
    ]
})
mostrar(resp)
pedido_1 = resp.json()

separador("10. CREAR PEDIDO — VARIOS PRODUCTOS")
resp = httpx.post(f"{GATEWAY}/pedidos/pedidos/", json={
    "usuario_id": usuario_2["id"],
    "items": [
        {"producto_id": productos[0]["id"], "cantidad": 1},
        {"producto_id": nuevo_producto["id"], "cantidad": 3}
    ]
})
mostrar(resp)

separador("11. VERIFICAR QUE EL STOCK SE DESCONTÓ")
for p in [productos[0], productos[1], nuevo_producto]:
    resp = httpx.get(f"{GATEWAY}/productos/productos/{p['id']}")
    data = resp.json()
    print(f"  {data['nombre']:20} stock: {data['stock']}")

separador("12. LISTAR PEDIDOS")
resp = httpx.get(f"{GATEWAY}/pedidos/pedidos/")
mostrar(resp)

separador("13. OBTENER PEDIDO POR ID")
resp = httpx.get(f"{GATEWAY}/pedidos/pedidos/{pedido_1['id']}")
mostrar(resp)

separador("14. ERROR — USUARIO INEXISTENTE")
resp = httpx.post(f"{GATEWAY}/pedidos/pedidos/", json={
    "usuario_id": 9999,
    "items": [{"producto_id": productos[0]["id"], "cantidad": 1}]
})
mostrar(resp)

separador("15. ERROR — STOCK INSUFICIENTE")
resp = httpx.post(f"{GATEWAY}/pedidos/pedidos/", json={
    "usuario_id": usuario_1["id"],
    "items": [{"producto_id": productos[2]["id"], "cantidad": 9999}]
})
mostrar(resp)

separador("FIN DE LA DEMOSTRACIÓN")
print()
