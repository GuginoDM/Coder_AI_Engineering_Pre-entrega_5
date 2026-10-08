from typing import Dict, Any, List
from langchain_core.tools import tool

# Base de datos simulada
DATABASE_PEDIDOS: Dict[int, List[Dict[str, Any]]] = {
    102: [
        {"id_pedido": "PED-8801", "fecha": "2026-09-10", "estado": "entregado"},
        {"id_pedido": "PED-8802", "fecha": "2026-09-28", "estado": "pendiente_pago"}
    ]
}

DATABASE_DETALLES: Dict[str, Dict[str, Any]] = {
    "PED-8801": {
        "id_pedido": "PED-8801",
        "monto": 14500,
        "items": ["Teclado Mecánico RGB", "Mouse Inalámbrico"],
        "descuento_aplicado": 0
    },
    "PED-8802": {
        "id_pedido": "PED-8802",
        "monto": 32000,
        "items": ["Monitor 27 Pulgadas 144Hz"],
        "descuento_aplicado": 1500
    }
}


@tool
def buscar_pedidos_cliente(cliente_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene la lista de todos los identificadores de pedidos y sus estados generales pertenecientes a un cliente.
    
    Args:
        cliente_id (int): El ID numérico único del cliente (ej. 102).
        
    Returns:
        List[Dict[str, Any]]: Lista con los pedidos del cliente (id_pedido, fecha, estado). Si no existe, retorna lista vacía.
    """
print(f" [Herramienta ejecutada] buscar_pedidos_cliente(cliente_id={cliente_id})")
    return DATABASE_PEDIDOS.get(cliente_id, [])


@tool
def obtener_detalle_pedido(id_pedido: str) -> Dict[str, Any]:
    """
    Obtiene el desglose financiero, ítems comprados y descuentos aplicados de un pedido específico.
    
    Args:
        id_pedido (str): El código identificador único del pedido (ej. 'PED-8801').
        
    Returns:
        Dict[str, Any]: Diccionario con los detalles del pedido (monto, ítems, descuento).
    """
    print(f"🛠️ [Herramienta ejecutada] obtener_detalle_pedido(id_pedido='{id_pedido}')")
    if id_pedido in DATABASE_DETALLES:
        return DATABASE_DETALLES[id_pedido]
    return {"error": f"No se encontró información para el pedido {id_pedido}"}


tools = [buscar_pedidos_cliente, obtener_detalle_pedido]