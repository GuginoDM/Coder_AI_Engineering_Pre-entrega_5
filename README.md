# Coder_AI_Engineering_Pre-entrega_5
Pre-entrega 5: Agente de razonamiento cíclico con memoria persistente
Criterios de Aceptación
Para que este checkpoint se considere aprobado, el entregable debe cumplir con lo siguiente:

Autonomía: El agente debe ser capaz de determinar por sí mismo cuándo llamar a una herramienta basándose en el prompt del usuario (sin rutas manuales if/else).
Ciclo de Retorno: Si una herramienta devuelve un error o información incompleta, el agente debe ser capaz de realizar un segundo intento o pedir aclaraciones.
Resiliencia de Estado: Al proporcionar un thread_id, el agente debe ser capaz de recordar interacciones previas dentro de una misma sesión de razonamiento.
Código Limpio: Uso de Python 3.12, tipado estático (Type Hints) y gestión asíncrona (asyncio).
Guía de Implementación Sugerida
Fase 1: El Contrato de Herramientas
Define tus funciones utilizando el decorador @tool de LangChain. Asegúrate de incluir docstrings extremadamente descriptivos; recuerda que el LLM decide qué herramienta usar basándose únicamente en esa descripción.

Fase 2: Definición del Estado y el Grafo
Crea el esquema de tu estado. En LangGraph, el estado es inmutable y se actualiza mediante reducers (usualmente operator.add para la lista de mensajes). Configura el StateGraph conectando el nodo del modelo con el nodo de ejecución de herramientas mediante una arista condicional (tools_condition).

Fase 3: Persistencia
Configura un Checkpointer. Esto es lo que permite que el agente sea "arquitectónicamente escalable". Sin persistencia, tu agente es efímero; con ella, es capaz de manejar flujos de trabajo largos que requieren intervención humana o esperar procesos externos.

Errores Comunes a Evitar
Descripciones Vagaces: Si el agente no usa la herramienta que esperas, el error suele estar en el docstring de la función, no en la lógica del grafo.
Bucles Infinitos: No establecer un límite de recursión (recursion_limit) al invocar el grafo. Define siempre un techo (ej. 10 pasos) para evitar costos inesperados en la API.
Estado Sucio: Olvidar que el estado se acumula. Asegúrate de limpiar o resumir mensajes si el contexto se vuelve demasiado grande.
