# El escape de los coleccionistas en el metro de París

Proyecto de Modelación de Sistemas en Redes. Control documental iniciado el **5 de noviembre de 2026**.

## Documentos de trabajo

| Documento | Para qué sirve | Cuándo actualizarlo |
| --- | --- | --- |
| [Guía del proyecto](docs/01_GUIA_DEL_PROYECTO.md) | Requisitos, decisiones pendientes, arquitectura propuesta, pasos y criterios de aceptación. | Al cambiar el alcance, una regla o el diseño. |
| [Bitácora y tareas](docs/02_BITACORA_Y_TAREAS.md) | Estado real, prioridades, decisiones, avances y evidencias. | Al terminar cada sesión o tarea. |
| [Guía para la defensa](docs/03_GUIA_DE_DEFENSA.md) | Conceptos, archivos y funciones que hay que explicar, impacto y preguntas de práctica. | Al incorporar o modificar una pieza importante. |
| [Documentación de los datos](metro-paris/README.md) | Esquema de los JSON, recorridos, conexiones y límites del inventario. | Al cambiar los datos o su formato. |
| [Inventario de estaciones y líneas](metro_paris_rutas_y_estaciones.md) | Consulta de recorridos y estaciones reales. | Al corregir o ampliar el inventario. |

## Estado actual

Hay un inventario de metro corregido y un validador de su topología. El lector del TXT, el modelo de ejecución, el planificador, el reporte y la interfaz todavía están pendientes. Las funciones propuestas en los documentos no deben confundirse con código existente.

Para esta etapa, el equipo eligió una **lista de adyacencia saliente** para representar el grafo dirigido. Cada estación tendrá sus conexiones de salida. La implementación del grafo está pendiente.

El programa deberá aceptar el **TXT de los preparadores** y usar el mismo planificador con distintos sistemas ferroviarios. La secuencia de pruebas empieza con redes pequeñas en TXT, sigue con un tramo del Metro de Caracas y un subconjunto de París, y termina con una medición sobre la red completa de París. El tramo de Caracas y los casos TXT están pendientes.

Según la aclaración de la profesora del 13 de noviembre, el equipo implementará las estructuras de datos del núcleo y podrá usar librerías de terceros en la interfaz. La consola y la interfaz compartirán el mismo planificador.

Para la primera interfaz recomendamos Tkinter con `ttk` y `Canvas`. PySide6 queda como alternativa para un mapa con más interacción. La comparación y los componentes previstos están en la [guía del proyecto](docs/01_GUIA_DEL_PROYECTO.md#10-interfaz-acordada).

## Comando disponible

```powershell
python metro-paris/validar_metro.py
```

Este comando valida los datos JSON; todavía no resuelve una misión. La ejecución futura prevista será `python main.py input.txt output.txt`, cuando se implemente.

## Fuente académica

El documento rector es [el enunciado del proyecto](Modelado%20en%20Redes%20-%20Enunciado%20Proyecto.pdf). Las decisiones del equipo para los detalles abiertos del prototipo están registradas en la [guía del proyecto](docs/01_GUIA_DEL_PROYECTO.md#3-reglas-de-trabajo-del-equipo).
