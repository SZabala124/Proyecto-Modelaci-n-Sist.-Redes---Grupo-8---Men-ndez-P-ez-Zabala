# Guía de estudio para la defensa

Última actualización **13 de noviembre de 2026**. El material se ampliará al implementar el programa.

## 1. Explicación breve del proyecto

Representamos estaciones y túneles mediante un grafo dirigido. Cada conexión tiene línea y tiempo de viaje; cambiar de línea añade el tiempo de transbordo de la estación. El programa debe elegir rutas y horarios para dos personajes, evitar conflictos y hacer que lleguen simultáneamente a sus entradas del búnker con el menor tiempo total posible.

La evaluación usará un TXT que puede describir cualquier red válida. Las redes pequeñas permitirán demostrar resultados calculables a mano. El tramo propuesto de Caracas servirá para una demostración real y París permitirá medir el comportamiento con una red más grande. Todos se cargarán en el mismo modelo y compartirán el planificador.

**Estado real:** tenemos datos de París corregidos y un validador de su topología. Todavía no hay un solucionador de misiones ni una interfaz implementada.

## 2. Conceptos clave

| Concepto | Explicación para la defensa | Impacto en el proyecto |
| --- | --- | --- |
| Grafo dirigido | Una arista permite viajar de origen a destino, sin implicar la inversa. | Agregar inversas puede inventar rutas y romper los bucles. |
| Grafo ponderado | Las conexiones tienen costos, aquí tiempos. | Menos estaciones no significa menor duración. |
| Lista de adyacencia | Cada estación mantiene sus conexiones dirigidas de salida. | Representación elegida para esta etapa. Permite recorrer las salidas de una estación y conservar conexiones paralelas. |
| Aristas paralelas | Pueden existir conexiones con los mismos extremos y distinta línea o duración. | No sobrescribirlas usando solo el par de estaciones como clave. |
| Estado del algoritmo | Describe lo necesario para decidir los siguientes movimientos. | La estación sola puede ser insuficiente: importa la línea de llegada y, en la búsqueda conjunta, el tiempo. |
| Transbordo | Tiempo adicional al cambiar entre líneas. | Puede hacer mejor una ruta con más viaje pero menos cambios. |
| Tiempo absoluto | Minutos desde el inicio de la operación. | Es la referencia para comparar personajes y restricciones horarias. |
| Duración del trayecto | Viajes, transbordos y esperas autorizadas durante el recorrido. | No equivale a la hora de llegada si la salida se retrasa. |
| Sincronización | Ambas llegadas ocurren en el mismo instante. | Debe verificarse después de elegir rutas y horarios. |
| Factibilidad | El plan cumple todas las restricciones. | Un plan rápido con una colisión no es una solución válida. |
| Optimalidad | Ninguna solución válida mejora el objetivo. | Requiere justificar la búsqueda, no solo validar la solución encontrada. |

## 3. Archivos que existen actualmente

| Archivo | Qué contiene | Qué debemos saber explicar |
| --- | --- | --- |
| `metro-paris/metro-stops.json` | Paradas, IDs locales, coordenadas y pertenencia a líneas. | De 455 paradas, 321 son de metro. Las 19 nuevas tienen coordenadas pendientes; los valores desconocidos son `null`. |
| `metro-paris/metro-lines.json` | Catálogo, recorridos y conexiones dirigidas. | Filtrar metro; hay 16 líneas, 35 recorridos, 405 relaciones estación-línea y 770 aristas dirigidas. |
| `metro-paris/validar_metro.py` | Comprobaciones de consistencia y topología. | No busca planes de escape ni demuestra optimalidad de una misión. |
| `metro-paris/README.md` | Contrato y procedencia de los JSON. | IDs de proyecto, diferencias entre recorrido y conexión, sentidos especiales y datos pendientes. |
| `metro_paris_rutas_y_estaciones.md` | Inventario legible de estaciones y secuencias. | Sirve para consulta; no contiene tiempos para resolver una misión ponderada. |
| `metro.json` | Primer archivo aportado, con problemas detectados. | No es la fuente de topología corregida. Sus conexiones no deben incorporarse silenciosamente. |
| `docs/01_GUIA_DEL_PROYECTO.md` | Plan, requisitos y reglas de trabajo. | Qué pide el enunciado y qué convenciones definió el equipo. |
| `docs/02_BITACORA_Y_TAREAS.md` | Historial, evidencias y tareas. | Qué trabajo se hizo realmente y cómo se comprobó. |

## 4. Funciones existentes y su impacto

Las tres funciones siguientes están en `metro-paris/validar_metro.py`.

### `require(condition, message)`

- Recibe una condición que debe cumplirse y un mensaje.
- Si falla, lanza `ValueError` y detiene la validación.
- Impacto: permite localizar un problema concreto en lugar de aceptar datos inconsistentes.
- Pregunta típica: ¿por qué un mensaje específico ayuda más que un fallo genérico?

### `reachable(start, adjacency)`

- Recibe el nodo inicial y un diccionario de conjuntos de vecinos.
- Usa un conjunto de visitados y una lista de pendientes para recorrer los nodos alcanzables.
- Devuelve el conjunto de nodos alcanzados; no calcula tiempos ni caminos mínimos.
- Es un recorrido en profundidad iterativo. Su costo es O(V + E) sobre la porción alcanzable, con memoria O(V), suponiendo operaciones promedio constantes en conjuntos y diccionarios.
- Impacto: detecta desconexiones. Aplicarlo desde un nodo en el grafo y en su inverso permite verificar conectividad fuerte.

### `main()` del validador

- Carga los JSON con rutas relativas al propio archivo, no al directorio desde el que se invoca.
- Comprueba IDs y nombres únicos, referencias a líneas y estaciones, cantidades por línea y coherencia entre recorridos, posiciones y conexiones.
- Comprueba bifurcaciones de 7 y 13 y sentidos únicos de 7bis y 10.
- Revisa conectividad dirigida de cada línea y de la red completa.
- Revisa que una duración, si existe, sea positiva; permite `null` porque esos datos siguen pendientes.
- Impacto: protege la calidad estructural de la base. No certifica coordenadas, tiempos reales, servicio del día ni factibilidad de un plan conjunto.

Comando disponible:

```powershell
python metro-paris/validar_metro.py
```

No confundir este `main()` con el futuro punto de entrada `main.py` del solucionador.

## 5. Funciones propuestas para estudiar al implementarlas

**Aún no existen.** Los nombres son contratos de diseño iniciales, no funciones disponibles. Al escribir cada una, registrar su firma real, archivo, entradas, salida, invariantes, complejidad, ejemplo y evidencia de comprobación.

| Módulo propuesto | Función candidata | Impacto esperado |
| --- | --- | --- |
| `lector_txt.py` | `leer_caso(ruta)` | Convertir el TXT en grafo y misión; conservar números de línea para errores. |
| `grafo.py` | `agregar_estacion(...)`, `agregar_conexion(...)`, `vecinos(id)` | Mantener la representación elegida sin perder direcciones ni conexiones paralelas. |
| `lector_json.py` | `cargar_metro(...)` | Adaptar París al mismo modelo, filtrando otros modos y rechazando pesos desconocidos al resolver. |
| `rutas.py` | `buscar_ruta_individual(...)` | Calcular costos considerando línea de llegada y transbordos. |
| `planificador.py` | `resolver_mision(grafo, mision, reglas)` | Elegir el plan conjunto bajo el objetivo y las restricciones acordadas. |
| `validacion_plan.py` | `validar_plan(...)`, `detectar_conflictos(...)` | Comprobar la cronología de forma independiente de la búsqueda. |
| `reporte.py` | `escribir_reporte(plan, ruta)` | Producir el TXT sin reinterpretar ni alterar el plan. |
| `mapa.py` | `distribuir_nodos(...)`, `dibujar_grafo(...)` | Mostrar redes reales o ficticias y sus sentidos. |
| `simulacion.py` | `estado_en_tiempo(plan, instante)` | Obtener posiciones y actividades a partir de eventos ya calculados. |

## 6. Ejemplos que debemos poder resolver a mano

### Sincronización básica

Pierre tarda 25 minutos y Amélie 18. Si no hay otros conflictos ni horarios variables, Pierre puede salir en 0 y Amélie en 7. Ambos llegan en 25. No se debe sumar 25 + 18 como tiempo total de la operación.

### Transbordo

Una ruta usa 4 minutos de L1, cambia a L4 en una estación con transbordo de 3 y viaja otros 5 minutos. Su duración es 12. Si las dos conexiones pertenecen a L1, el mismo trayecto dura 9, siempre que no exista otra regla de parada.

### Conflicto en un túnel

Un personaje recorre A → B durante `[2, 6)` y otro recorre el mismo recurso B → A durante `[4, 8)`. Hay solapamiento. Para el prototipo, el recurso en TXT se identifica por línea y par de estaciones sin ordenar. El mismo recurso también se reserva para viajes en el mismo sentido. Si un viaje termina en 6 y otro empieza en 6, se comprueban las estaciones por separado porque sus intervalos de túnel no se solapan.

### Conflicto en estación

Pierre llega a X en 4 y transborda hasta 7. La ocupación es `[4, 7]`. Si Amélie pasa por X en 6 o en 7, hay colisión. Un paso instantáneo se representa como `[t, t]`. La espera inicial ocupa el origen desde 0 hasta la salida, inclusive.

### Restricciones y resultado de la búsqueda

Un cierre `[4, 8)` impide un cambio hacia o desde la línea afectada si el transbordo se solapa con esa ventana. Un cambio instantáneo en 4 queda bloqueado y uno en 8 queda permitido. Si un viaje empieza durante una ventana de retraso, su tiempo base se duplica una vez.

El horizonte inicial es de 120 minutos, configurable. `SIN_SOLUCION` exige una prueba de imposibilidad. `LIMITE_BUSQUEDA` indica que se exploró hasta el horizonte sin encontrar un plan. Si varios planes llegan al mismo tiempo, se elige por número total de viajes, luego por salidas y finalmente por secuencias de IDs de aristas.

### Rutas individuales y plan conjunto

Las rutas más rápidas por separado pueden entrar en conflicto al sincronizarlas. Explicar por qué puede ser necesario cambiar una de las rutas o una espera autorizada, y por qué rechazar ese primer par no demuestra que la misión sea imposible.

## 7. Algoritmos y complejidad

No se ha seleccionado el planificador definitivo.

- La lista de adyacencia se implementará con listas de almacenamiento y un índice propio ordenado por ID. La búsqueda binaria cuesta O(log V) y recorrer las conexiones del registro localizado cuesta O(grado de salida). El conjunto ocupa O(V + E). Explicar cómo se preservan los pesos, las líneas y las aristas paralelas.
- Si dos representaciones conservan el mismo grafo y la búsqueda aplica las mismas reglas, el óptimo y la existencia de solución deben coincidir. Cuando varias soluciones empatan, una regla fija de desempate permite reproducir el mismo recorrido en el reporte.
- Un recorrido DFS o BFS encuentra alcanzabilidad en O(V + E), pero no minimiza en general tiempos desiguales.
- Para una red estática con costos no negativos, Dijkstra es candidato. Al incorporar transbordos se aplica sobre estados que incluyen línea de llegada.
- Con una cola de prioridad binaria, el costo habitual se expresa usando los estados expandidos: O((V' + E') log V'). La complejidad definitiva depende de la implementación y de cómo se construyan esos estados.
- La búsqueda de dos personajes y tiempo puede tener muchos más estados que una ruta individual. No atribuirle el costo de un único Dijkstra.
- Un horizonte de tiempo o un límite de rutas exploradas necesita justificación. Si limita la búsqueda, debe reportarse como límite y no como demostración de ausencia de solución.

Al elegir el algoritmo, añadir aquí su argumento de corrección, optimalidad, terminación y costo temporal y espacial reales.

## 8. Casos particulares del metro real

| Línea | Qué hay que explicar |
| --- | --- |
| 7 | Bifurca en Maison Blanche hacia Mairie d'Ivry y Villejuif - Louis Aragon. |
| 13 | Bifurca en La Fourche hacia Les Courtilles y Saint-Denis - Université. |
| 7bis | El bucle circula Botzaris → Place des Fêtes → Pré-Saint-Gervais → Danube → Botzaris. |
| 10 | Hacia París pasa por Molitor, Chardon Lagache y Mirabeau; hacia Boulogne, por Église d'Auteuil, Auteuil y Porte d'Auteuil. |
| 8 | Las posiciones originales estaban en cero; se reconstruyó el orden completo desde Balard. |

Un recorrido es una secuencia completa de estaciones; una conexión es un paso dirigido entre dos estaciones consecutivas. Varios recorridos comparten conexiones del tronco común. Duplicarlas como aristas diferentes solo por pertenecer a varios recorridos alteraría el modelo.

`segment_id` es una agrupación local por línea y par de estaciones para la simulación. No prueba qué túnel físico comparten trenes o líneas. No calcular el costo de un transbordo a partir de la distancia visual del dibujo.

## 9. Interfaz y núcleo de cálculo

La profesora aclaró que las estructuras de datos del núcleo deben ser implementadas por el equipo y que se permiten librerías de terceros para la interfaz. Para el prototipo recomendamos Tkinter con `ttk` para los controles y `Canvas` para dibujar el grafo. La alternativa es PySide6 con `QGraphicsScene` y `QGraphicsView` para el mapa. La elección se confirmará al probar el prototipo.

Para explicar la animación, distinguir el tiempo de la misión del ritmo de reproducción. `after()` en Tkinter o `QTimer` en PySide6 pueden programar las actualizaciones de pantalla. La posición de cada personaje se obtiene de los eventos del plan calculado por el núcleo.

En la defensa, identificar dónde se implementan el grafo y las estructuras auxiliares, qué operaciones ofrecen y qué costos tienen. Explicar qué parte de la aplicación depende de la librería gráfica y cómo se ejecuta el núcleo desde consola.

Debemos poder explicar que el mapa consume el grafo, el resultado consume el plan y la animación consume sus eventos. Arrastrar un nodo cambia su dibujo, no su tiempo de viaje. Cambiar la velocidad de animación cambia la reproducción, no la duración de la misión.

Una red TXT puede no tener coordenadas y aun así debe poder resolverse y dibujarse. El programa por consola debe funcionar sin abrir una ventana.

## 10. Preguntas para practicar en equipo

1. ¿Cómo se lee un TXT con IDs 10, 50 y 900 sin asumir que son índices de una lista?
2. ¿Por qué cada arista guarda su línea?
3. ¿Cuándo se cobra un transbordo y por qué importa la línea de llegada?
4. ¿Por qué minimizar estaciones visitadas no minimiza necesariamente tiempo?
5. ¿Por qué no basta calcular dos rutas mínimas independientes?
6. ¿Qué ocupa cada personaje mientras espera o transborda?
7. ¿Cómo se detecta un cruce de túnel con horas de salida diferentes?
8. ¿Qué diferencia existe entre plan válido y plan óptimo?
9. ¿Cómo se demuestra que no hay solución? ¿Qué pasa si se alcanza un límite de búsqueda?
10. ¿Cómo se representan los dos ramales sin inventar conexiones entre ellos?
11. ¿Por qué no se agregan todas las aristas inversas automáticamente?
12. ¿Qué significa `null` en los datos y por qué no se convierte a cero?
13. ¿Por qué el TXT de evaluación no depende de los nombres de París?
14. ¿Qué verifica el validador actual y qué no puede verificar?
15. ¿Qué función cambiaríamos para modificar el formato del reporte sin tocar el algoritmo?
16. ¿Cómo se incorpora un cierre horario y qué regla define cuándo se aplica?
17. ¿Qué estructuras implementamos nosotros, qué operaciones requieren los algoritmos y qué responsabilidades tiene la librería gráfica?
18. ¿Qué ocurre si el origen ya es el destino o ambos personajes comparten origen?
19. ¿Qué cambia entre un TXT ficticio, un tramo de Caracas y París? ¿Cómo comprobamos que los tres usan el mismo modelo y planificador?
20. ¿Por qué elegimos la lista de adyacencia y qué costos dependen del modo en que localizamos una estación por su ID?

Para responder las preguntas sobre D01–D11, indicar qué dice el enunciado y qué convención adoptó el equipo para completar cada detalle.

## 11. Ficha para cada función importante nueva

```markdown
### nombre_funcion(firma_real)

- Archivo:
- Estado: implementada / propuesta.
- Propósito:
- Entradas, unidades y precondiciones:
- Salida y posibles errores:
- Pasos principales:
- Invariantes que mantiene:
- Funciones que la llaman y de las que depende:
- Impacto si falla:
- Complejidad temporal y espacial:
- Ejemplo mínimo:
- Evidencia de comprobación:
- Decisión o regla académica relacionada:
```

## 12. Ensayo final de defensa

- [ ] Cada integrante presenta el problema en un minuto.
- [ ] Cada integrante explica el modelo de datos y la representación del grafo.
- [ ] Todos siguen a mano un caso con transbordo y otro con conflicto.
- [ ] Se demuestra carga de TXT, solución, reporte y visualización.
- [ ] Se explica un caso imposible y uno con entrada inválida.
- [ ] Se conoce la justificación de optimalidad y los límites de rendimiento.
- [ ] El catálogo de funciones corresponde al código final, sin firmas propuestas presentadas como existentes.
- [ ] Se identifican con claridad los datos reales, los parámetros simulados y los valores pendientes.
