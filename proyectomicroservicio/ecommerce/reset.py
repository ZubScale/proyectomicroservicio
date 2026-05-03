# reset.py — Elimina todos los datos de los tres servicios
# Ejecutar desde la carpeta ecommerce/ con: python reset.py

import httpx

GATEWAY = "http://localhost:8000"

print("Eliminando datos de los tres servicios...\n")

servicios = [
    ("Pedidos",   f"{GATEWAY}/pedidos/pedidos/reset"),
    ("Usuarios",  f"{GATEWAY}/usuarios/usuarios/reset"),
    ("Productos", f"{GATEWAY}/productos/productos/reset"),
]

for nombre, url in servicios:
    resp = httpx.delete(url)
    print(f"  {nombre:10} → {resp.json()['mensaje']}")

print("\nListo. Puedes ejecutar demo.py nuevamente.")
