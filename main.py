import asyncio
import json
import os
from dotenv import load_dotenv

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent import build_graph

load_dotenv()

DB_PATH = "state_checkpoints.db"
TRACE_FILE = "execution_trace.json"

def serialize_message(msg) -> dict:
    """Convierte objetos de mensajes de LangChain a diccionarios serializables en JSON."""
    data = {
        "type": msg.type,
        "content": msg.content
    }
    if isinstance(msg, AIMessage) and msg.tool_calls:
        data["tool_calls"] = msg.tool_calls
    if isinstance(msg, ToolMessage):
        data["tool_call_id"] = msg.tool_call_id
        data["name"] = msg.name
    return data


async def main():
    builder = build_graph()

    # Persistencia asíncrona con SQLite
    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)

        # Identificador único de hilo de conversación
        config = {
            "configurable": {"thread_id": "sesion_cliente_102"},
            "recursion_limit": 10  # Previene bucles infinitos
        }

        print("\n" + "="*70)
        print("🤖 TURNO 1: Consulta multi-paso que requiere varias herramientas")
        print("="*70)
        
        pregunta_1 = "¿Cuántos pedidos tuvo el cliente 102, cuál está pendiente y cuál es el monto total de ese pedido pendiente?"
        print(f"👤 Usuario: {pregunta_1}\n")

        # Invocación asíncrona Turno 1
        estado_1 = await graph.ainvoke(
            {"messages": [HumanMessage(content=pregunta_1)]},
            config=config
        )

        respuesta_final_1 = estado_1["messages"][-1].content
        print(f"\n🤖 Agente: {respuesta_final_1}")

        print("\n" + "="*70)
        print("🧠 TURNO 2: Prueba de Resiliencia de Estado (Memoria con el mismo thread_id)")
        print("="*70)

        pregunta_2 = "¿Y cuál era el monto y los ítems del otro pedido que ya fue entregado?"
        print(f"👤 Usuario: {pregunta_2}\n")

        # Invocación asíncrona Turno 2 (recordando la sesión anterior)
        estado_2 = await graph.ainvoke(
            {"messages": [HumanMessage(content=pregunta_2)]},
            config=config
        )

        respuesta_final_2 = estado_2["messages"][-1].content
        print(f"\n🤖 Agente: {respuesta_final_2}")

        # Guardar la traza completa acumulada en JSON
        traza = [serialize_message(m) for m in estado_2["messages"]]
        with open(TRACE_FILE, "w", encoding="utf-8") as f:
            json.dump(traza, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Traza completa guardada con éxito en '{TRACE_FILE}'")


if __name__ == "__main__":
    asyncio.run(main())