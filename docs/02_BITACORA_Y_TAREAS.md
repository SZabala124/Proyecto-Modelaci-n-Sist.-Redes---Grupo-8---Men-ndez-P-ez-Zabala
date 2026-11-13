# Bitácora y control de tareas

Última actualización **13 de noviembre de 2026**.

## 1. Convenciones

- `[x]` Completado con evidencia.
- `[ ]` Pendiente. La columna de estado distingue pendiente, en curso o a la espera de aclaración.
- Registrar fecha, tarea, cambios y comprobaciones. Si algo no se verificó, decirlo.
- No borrar el historial al cambiar una decisión; marcarla como sustituida y explicar la nueva.
- No asignar responsables o dar respuestas de los preparadores por supuestas.

## 2. Estado inicial

| Área | Estado al 05/11/2026 | Evidencia |
| --- | --- | --- |
| Análisis del enunciado | Lectura y decisiones del prototipo registradas. | Guía, secciones 2 a 4. |
| Inventario real | Completado para la topología nominal documentada. | `metro_paris_rutas_y_estaciones.md`. |
| JSON de París | Topología corregida y validada; pesos y coordenadas nuevas pendientes. | `metro-paris/README.md` y validador. |
| Documentación de control | Creada. | Los tres documentos de `docs/` y el índice raíz. |
| Lector TXT y grafo de ejecución | Pendiente. | Aún no existen módulos de solución. |
| Planificador y validación de planes | Pendiente. | El validador existente revisa datos, no misiones. |
| Reporte de solución | Pendiente. | No existe un `output.txt` de una misión resuelta. |
| Interfaz | Diseño general acordado, implementación pendiente. | Guía, sección 10. |
| Defensa | Material inicial creado; catálogo de funciones de solución pendiente. | Guía de defensa. |

## 3. Lista priorizada

| Hecho | ID | Prioridad | Tarea | Estado / condición de cierre |
| --- | --- | --- | --- | --- |
| [x] | T01 | Alta | Leer y analizar el enunciado. | Lectura inicial registrada. Las decisiones sobre detalles abiertos se documentaron en D01–D11. |
| [x] | T02 | Alta | Inventariar líneas y estaciones reales. | Documento de consulta creado. |
| [x] | T03 | Alta | Revisar el primer `metro.json`. | Se identificaron conexiones incorrectas y nodos aislados. No usar como fuente de topología corregida. |
| [x] | T04 | Alta | Corregir los dos JSON de `metro-paris`. | 19 estaciones nuevas, correspondencias, línea 8 y sentidos/ramales explícitos. |
| [x] | T05 | Alta | Validar referencias y topología JSON. | Validador ejecutado satisfactoriamente en la sesión de corrección. |
| [x] | T06 | Alta | Crear guía, bitácora y material inicial de defensa. | Documentos presentes y enlazados. |
| [x] | T07 | Alta | Decidir las reglas D01–D11 del prototipo. | Reglas propias del equipo registradas en la guía. |
| [ ] | T08 | Alta | Diseñar las operaciones de la lista de adyacencia y de las estructuras auxiliares propias. | D11 define las listas de almacenamiento y el índice por ID. Quedan por definir las operaciones y sus firmas. |
| [ ] | T09 | Alta | Definir firmas y contratos internos de datos y errores. | La gramática de entrada, los estados de salida y las reglas temporales están definidos en la guía. |
| [ ] | T10 | Alta | Implementar lector TXT y grafo dirigido. | Pendiente; probar IDs arbitrarios y aristas paralelas. |
| [ ] | T11 | Alta | Resolver rutas individuales con transbordos. | Pendiente; comparar con casos calculados manualmente. |
| [ ] | T12 | Alta | Implementar cronologías y detección de colisiones. | Aplicar D01–D04 y verificar los casos límite documentados. |
| [ ] | T13 | Alta | Elegir y justificar búsqueda conjunta. | Usar objetivo, horizonte y desempate de la guía. Explicar qué casos cubre exhaustivamente y cuándo puede demostrar imposibilidad. |
| [ ] | T14 | Alta | Implementar y verificar el planificador. | Pendiente. |
| [ ] | T15 | Alta | Generar reporte TXT y entrada por consola. | Pendiente. |
| [ ] | T16 | Media | Incorporar adaptador JSON al modelo interno. | Pendiente; filtrar metro y exigir pesos válidos. |
| [ ] | T17 | Media | Definir tiempos de simulación o conseguir tiempos reales. | Pendiente; conservar procedencia y unidades. |
| [ ] | T18 | Media | Completar o gestionar coordenadas faltantes. | 19 pendientes; el diseño automático permite dibujar sin ellas. |
| [ ] | T19 | Media | Validar la librería gráfica con una primera demostración. | Tkinter con `ttk` y `Canvas` es la recomendación inicial. Comprobar su disponibilidad en el portátil y evaluar PySide6 si el mapa requiere más interacción. |
| [ ] | T20 | Media | Implementar interfaz básica con carga TXT y mapa. | Pendiente; reutilizar lector y planificador de consola. |
| [ ] | T21 | Media | Añadir animación, zoom, arrastre y línea de tiempo. | Pendiente de interfaz básica y eventos. |
| [ ] | T22 | Alta | Preparar casos de evaluación y medir rendimiento. | Pendiente; incluir comparación independiente de optimalidad. |
| [ ] | T23 | Alta | Completar catálogo de funciones para defensa. | Pendiente a medida que se implemente cada módulo. |
| [ ] | T24 | Alta | Ensayar defensa y preparar paquete de entrega. | Pendiente de integración. |
| [ ] | T25 | Alta | Preparar redes pequeñas en TXT. | Guardar entrada y resultado calculado a mano para cada caso. Empezar por sincronización y ruta alternativa. |
| [ ] | T26 | Media | Preparar un tramo del Metro de Caracas. | Verificar el trazado y documentar la procedencia de los tiempos. Añadir una misión reproducible. |
| [ ] | T27 | Media | Preparar casos con la red de París. | Cargar un subconjunto con tiempos definidos y una misión reproducible. Medir la red completa cuando estén disponibles sus tiempos. |

## 4. Decisiones y asuntos abiertos

| ID | Decisión o asunto | Estado | Motivo / siguiente acción |
| --- | --- | --- | --- |
| DEC01 | Aceptar el TXT como fuente de verdad de cada caso de evaluación. | Acordado en el diseño. | Evitar depender de que las estaciones sean reales. |
| DEC02 | Usar los JSON corregidos como base adicional de París. | Implementado en los datos. | Usar `metro-paris/`; el archivo antiguo no es la fuente corregida. |
| DEC03 | Crear la interfaz con Tkinter y Canvas. | Sustituida por DEC11 como elección cerrada de librería. | Tkinter sigue siendo candidato. |
| DEC04 | Compartir modelo y planificador entre consola e interfaz. | Propuesto para implementación. | Evitar resultados diferentes entre las dos entradas. |
| DEC05 | Mantener valores desconocidos como `null`. | Implementado en JSON. | No confundir coordenadas ni tiempos ausentes con datos reales o costo cero. |
| DEC06 | Usar una lista de adyacencia saliente para representar el grafo dirigido. | Elegida para esta etapa el 13/11. | Conservar aristas paralelas y localizar estaciones mediante un índice ordenado, según D11. |
| DEC07 | Algoritmo conjunto definitivo. | Pendiente de diseño. | Comparar las opciones con las reglas D01–D11 y los casos pequeños. |
| DEC08 | Espera en origen, ocupación de estaciones y exclusión por túnel. | Definido para el prototipo en D01–D04. | Comparar intervalos cerrados en estaciones y semiabiertos en túneles. |
| DEC09 | Restricciones horarias, minutos enteros y horizonte. | Definido para el prototipo en D05–D07. | TXT básico con sección opcional y horizonte inicial configurable de 120 minutos. |
| DEC10 | Implementar las estructuras del núcleo en el equipo. | Aclarado por la profesora el 13/11. | Diseñar la representación y las estructuras auxiliares que requiera el algoritmo. |
| DEC11 | Se permiten librerías de terceros en la interfaz. | Aclarado por la profesora el 13/11. | Elegir la librería gráfica después de definir la primera demostración. |
| DEC12 | Probar varios sistemas con la misma lista de adyacencia y el mismo planificador. | Acordado el 13/11. | Empezar con casos TXT pequeños, seguir con Caracas y un subconjunto de París, y medir luego la red completa de París. |
| DEC13 | Prototipar la interfaz con Tkinter y considerar PySide6 para el mapa interactivo. | Recomendación pendiente de validar. | Usar el mismo caso TXT para evaluar el dibujo de rutas y la interacción con el mapa. |
| DEC14 | Fijar el desempate, las misiones con orígenes o destinos coincidentes y los estados de salida. | Definido para el prototipo en D08–D10. | Dar resultados reproducibles y distinguir imposibilidad, límite y errores de entrada. |

## 5. Historial de trabajo

### 05/11/2026 — Análisis y preparación de datos

- Se leyeron las cuatro páginas del enunciado y se identificaron ambigüedades temporales y de formato.
- Se creó el inventario de líneas y estaciones. Se corrigió la cifra inicial de 303 estaciones frente al inventario ampliado de 321 nombres de estación.
- Se revisó `metro.json`: 314 nodos, 296 conexiones, 43 nodos aislados y conexiones que saltan estaciones. Queda como archivo histórico del usuario.
- Se revisaron los dos JSON originales de `metro-paris`: 436 paradas totales, 302 de metro; línea 8 con todas sus posiciones en cero, ramales ambiguos y ampliaciones faltantes.
- Se corrigieron esos JSON: 455 paradas totales, 321 de metro, 405 relaciones estación-línea, 35 recorridos y 770 conexiones dirigidas. Se añadieron 19 estaciones y correspondencias con estaciones existentes.
- Se creó `metro-paris/validar_metro.py` y se ejecutó satisfactoriamente. Revisó referencias, conteos, bifurcaciones, sentidos únicos y conectividad dirigida.
- Pendientes de datos: 19 coordenadas nuevas, tiempos de viaje y transbordo. Los datos de otros modos se mantienen como heredados y no verificados.

### 05/11/2026 — Organización del proyecto

- Se acordó diseñar la solución para aceptar TXT arbitrarios de los preparadores.
- Se acordó una interfaz propia con Tkinter y un núcleo compartido con la consola.
- Se crearon guía de ejecución, bitácora, resumen de defensa e índice documental.
- No se implementó todavía el lector de misiones, el grafo de ejecución, el algoritmo ni la interfaz. La creación de documentos no implica que esas etapas estén terminadas.
- En esta etapa documental se revisaron archivos existentes y enlaces locales; no se volvió a ejecutar el validador de topología ni se hicieron pruebas del planificador, que aún no existe.

### 13/11/2026 — Aclaraciones de la profesora

- El usuario comunicó que la profesora recomienda preparar varios sistemas ferroviarios.
- El equipo debe implementar las estructuras de datos. La interfaz puede usar librerías de terceros.
- Se actualizó el plan para empezar con redes pequeñas en TXT, preparar un tramo real de Caracas y aprovechar el inventario de París para medir escala.
- Se incorporó a la guía un ejemplo calculado a mano que exige una ruta alternativa. Los archivos TXT y el tramo de Caracas siguen pendientes.

### 13/11/2026 — Elección de la representación y plan de pruebas

- Se eligió la lista de adyacencia saliente para esta etapa. La implementación del grafo y el diseño de sus estructuras auxiliares están pendientes.
- Se acordó probar el mismo núcleo con varios sistemas. T25 cubre las redes pequeñas, T26 cubre Caracas y T27 cubre París.

### 13/11/2026 — Reglas del prototipo

- Se documentaron las decisiones D01–D11 del equipo para iniciar la implementación. Se conservó el formato TXT básico y se añadió la gramática opcional para las restricciones.
- Se fijaron la ocupación de estaciones y túneles, el objetivo, el desempate y los estados de salida. Se anotaron los casos límite esperados para comprobar esas reglas cuando exista el planificador.
- Se definió el almacenamiento de la lista de adyacencia y la búsqueda por ID. El diseño de las firmas y la implementación siguen pendientes.

## 6. Próxima sesión

1. Revisar el contrato del prototipo con los ejemplos documentados.
2. Diseñar las operaciones de la lista de adyacencia y del índice ordenado por ID.
3. Definir el contrato de grafo, misión, eventos y errores del lector.
4. Implementar la lectura del formato TXT básico y guardar dos casos pequeños con resultado esperado.
5. Actualizar la guía de defensa con los archivos y funciones que efectivamente se incorporen.

## 7. Plantilla para nuevos avances

```markdown
### AAAA-MM-DD — Título de la sesión

- Tareas: Txx, Tyy.
- Responsable(s): por completar.
- Objetivo:
- Cambios realizados:
- Archivos y funciones afectados:
- Decisiones tomadas y motivo:
- Comprobaciones ejecutadas y resultado:
- Limitaciones o dudas pendientes:
- Próximo paso:
- Documentación actualizada:
```

## 8. Plantilla para decisiones técnicas

```markdown
### DECxx — Nombre de la decisión

- Fecha:
- Estado: propuesta / aceptada / sustituida.
- Problema que resuelve:
- Alternativas consideradas:
- Elección y justificación:
- Efecto en corrección, rendimiento e interfaz:
- Evidencia o aclaración académica:
- Archivos y tareas relacionados:
```

## 9. Control final de entrega

- [ ] Confirmar fechas oficiales y plataforma de entrega.
- [ ] Fuente completa con estructuras propias y dependencias gráficas limitadas a la interfaz.
- [ ] Entrada TXT completa y salida regenerada por el programa.
- [ ] Ejecución de consola comprobada en el portátil de defensa.
- [ ] Interfaz y librería gráfica elegida comprobadas en ese equipo.
- [ ] Casos de colisión, transbordo, sincronización y ausencia de solución preparados.
- [ ] Supuestos y límites conocidos documentados.
- [ ] Todos pueden explicar estructuras, funciones y complejidad.
- [ ] Portátil preparado y asistencia de todos los integrantes coordinada.
- [ ] Confirmación de carga correcta de los archivos en el aula virtual.
