# Guía de ejecución del proyecto

Última actualización **13 de noviembre de 2026**.

## 1. Propósito y estado

Construir un programa en Python que encuentre rutas y horarios para Pierre y Amélie, desde sus orígenes hasta las dos entradas del búnker, con llegada simultánea, sin colisiones y minimizando el tiempo de la operación.

Este documento contiene un plan de implementación. Actualmente existen los JSON de París y su validador; los módulos de solución e interfaz que se describen abajo son **propuestos**.

La fuente de requisitos es [el enunciado](../Modelado%20en%20Redes%20-%20Enunciado%20Proyecto.pdf). Las decisiones académicas comunicadas posteriormente por el profesor o los preparadores deberán registrarse con fecha.

## 2. Requisitos y evidencia de cumplimiento

| ID | Requisito | Evidencia que debemos poder mostrar |
| --- | --- | --- |
| R01 | Programar en Python e implementar las estructuras de datos del núcleo. La profesora permite librerías de terceros para la interfaz. | Código propio del grafo y las estructuras auxiliares, con dependencias gráficas confinadas a la interfaz. |
| R02 | Elegir una de las cinco representaciones vistas en clase y justificarla. El equipo eligió la lista de adyacencia para esta etapa. | Implementación propia y explicación del costo de recorrer las conexiones salientes. |
| R03 | Leer la red y la misión de un TXT. | Ejecución con el archivo suministrado por los preparadores. |
| R04 | Respetar aristas dirigidas, líneas y tiempos de viaje. | Recorridos que solo usan conexiones existentes en el sentido permitido. |
| R05 | Sumar el transbordo al cambiar de línea. | Cronología que muestra dónde y cuánto se transborda. |
| R06 | Evitar coincidencias temporales en estaciones y conflictos en túneles. | Comprobación independiente de las dos cronologías. |
| R07 | Llegar a las dos entradas simultáneamente. | Horas de llegada iguales y horarios de salida explícitos. |
| R08 | Minimizar el tiempo total de la operación. | Justificación del algoritmo y comparación con resultados conocidos en casos pequeños. |
| R09 | Considerar restricciones de líneas previstas por el enunciado. | Casos con prohibiciones de transbordo por horario y retrasos, una vez definido su formato. |
| R10 | Producir un reporte detallado. | `output.txt` con tiempos, salidas, rutas y resultado. |
| R11 | Entregar fuente, entrada y salida; asistir todos a la defensa con portátil. | Lista final de entrega y demostración reproducible. |

El 13 de noviembre el equipo comunicó la aclaración de la profesora sobre las librerías y su recomendación de probar varios sistemas ferroviarios. La interfaz debe consumir el mismo resultado que la consola y permitir cargar el TXT de evaluación.

## 3. Reglas de trabajo del equipo

Estas decisiones completan los detalles que deja abiertos el enunciado y sirven como contrato para la primera versión. Si los preparadores especifican otra regla o gramática, registraremos el cambio y actualizaremos los casos afectados.

| ID | Decisión del equipo | Motivo |
| --- | --- | --- |
| D01 | Permitir espera voluntaria en el origen antes de iniciar el recorrido. En estaciones intermedias solo se permanece el tiempo obligatorio de transbordo. | La sincronización sigue el ejemplo de desfase de salida del enunciado. |
| D02 | Cada personaje ocupa su origen desde el minuto 0 hasta el instante de salida, inclusive. | El otro personaje debe tener en cuenta la presencia de quien espera. |
| D03 | Contar como ocupación los instantes de llegada y partida y todo el transbordo entre ellos. Una parada sin transbordo ocupa el instante de paso. | Permite detectar coincidencias exactas y durante permanencias. |
| D04 | En TXT, identificar el túnel por la línea y el par no ordenado de estaciones. En JSON, usar el identificador de segmento por línea. Bloquear ocupaciones superpuestas del mismo recurso en ambos sentidos, incluido el mismo sentido. | Con la entrada disponible se adopta una exclusión conservadora por tramo. Las líneas distintas representan recursos separados. |
| D05 | Mantener el TXT básico y aceptar una sección opcional `RESTRICCIONES` después de la misión, con la gramática de la sección 4. | Los ejemplos sin restricciones se pueden leer directamente. |
| D06 | Medir todo en minutos enteros. Viaje base mayor que cero, transbordo y salida mayores o iguales a cero. | Facilita una búsqueda temporal discreta y comparaciones exactas. |
| D07 | Usar un horizonte inicial de 120 minutos, configurable e inclusivo. Aceptar los tamaños de grafo que permita el formato y medir el rendimiento con los casos previstos. | El horizonte es un parámetro del prototipo. Permite distinguir una búsqueda acotada de una imposibilidad demostrada. |
| D08 | Cualquiera puede retrasar su salida, incluso ambos si las ventanas horarias lo requieren. Minimizar primero la llegada común. Entre empates, preferir menos viajes totales, luego las salidas `(Pierre, Amélie)` en orden ascendente y, finalmente, las secuencias de IDs de aristas de Pierre y Amélie en orden lexicográfico. | Define una respuesta reproducible para una entrada. Los IDs TXT siguen el orden de lectura. |
| D09 | Admitir un trayecto vacío cuando el origen propio coincide con el destino. En ese caso la salida declarada es la llegada y el personaje ocupa la estación desde 0 hasta ese instante. Un origen compartido o un destino compartido hace imposible la misión por la regla de coincidencia. | Los casos límite se resuelven con la misma ocupación de estaciones. |
| D10 | Reportar `SOLUCION`, `SIN_SOLUCION` o `LIMITE_BUSQUEDA`. Para una entrada inválida, emitir `ENTRADA_INVALIDA` en la salida de error de la consola con línea y causa cuando corresponda. | Cada estado comunica qué pudo establecer el programa. |
| D11 | Implementar la lista de adyacencia y sus operaciones en el equipo. Usar listas nativas como almacenamiento de los registros y las salidas, un índice ordenado por ID y búsqueda binaria propia. Implementar una cola de prioridad propia si el algoritmo la necesita. | Los contenedores básicos guardan los datos. El equipo diseña la representación del grafo y las operaciones de búsqueda. |

El ejemplo usa dos IDs para las entradas del búnker. Debemos conservar ambos destinos, aunque narrativamente pertenezcan al mismo lugar; no fusionarlos en un único nodo sin indicación expresa.

## 4. Entrada de los preparadores

El TXT es la fuente de verdad para cada ejecución de evaluación. Los IDs pueden ser arbitrarios y las estaciones pueden ser ficticias. No se debe exigir coincidencia con los JSON de París, IDs consecutivos o nombres reales.

Formato básico descrito:

1. `N M`: número de estaciones y aristas dirigidas.
2. N registros: `id_estacion tiempo_transbordo`.
3. M registros: `origen destino tiempo_viaje linea`.
4. Un registro de misión: `origen_pierre origen_amelie destino_pierre destino_amelie`.

Ignorar las líneas vacías y el texto desde `#` hasta el fin de línea. Después de la misión se puede agregar `RESTRICCIONES K`, seguida de exactamente K registros. Aceptar `K = 0` y validar que las líneas mencionadas existan en el grafo. Cada ventana cumple `0 <= inicio < fin`.

| Registro opcional | Efecto |
| --- | --- |
| `CIERRE_TRANSBORDO linea inicio fin` | Impide un cambio hacia o desde esa línea si el intervalo de trabajo del transbordo `[llegada, partida)` se solapa con la ventana `[inicio, fin)`. Para un cambio de duración cero se verifica si el instante está dentro de la ventana. La ocupación para detectar colisiones sigue incluyendo ambos extremos. |
| `RETRASO linea inicio fin` | Duplica el tiempo base de un viaje de esa línea cuando se entra al túnel dentro de `[inicio, fin)`. Si coinciden varias ventanas, se duplica una sola vez. La duración queda fijada al entrar. |

Ejemplo de extensión del equipo para un caso que contenga `L1` y `L2`.

```text
RESTRICCIONES 2
CIERRE_TRANSBORDO L1 4 8
RETRASO L2 6 10
```

Ejemplo didáctico completo, con tiempos propuestos para este caso y sin transbordos:

```text
# Cuatro estaciones y dos conexiones dirigidas
4 2
1 1
2 1
3 1
4 1
1 3 5 L1
2 4 3 L2
# Orígenes y entradas del búnker
1 2 3 4
```

Resultado esperado bajo la interpretación de que se permite retrasar la salida: Pierre sale en 0, Amélie en 2 y ambos llegan en 5. Es un ejemplo pequeño para razonar, no un archivo oficial de evaluación.

Validaciones de lectura: cantidad exacta de registros, IDs únicos, referencias existentes, tipos numéricos, tiempos dentro del dominio acordado y misión válida. Los errores deben identificar el número de línea y la causa. No descartar silenciosamente aristas paralelas: dos conexiones pueden compartir extremos y pertenecer a líneas diferentes.

No agregar inversas automáticamente. Si se permite circular en ambos sentidos, el archivo debe expresarlo o los preparadores deben especificar otra convención.

## 5. Modelo interno propuesto

El equipo eligió una **lista de adyacencia saliente** para esta etapa. Cada estación guarda sus conexiones dirigidas de salida. Cada conexión conserva su destino, línea y duración, incluidas las conexiones paralelas. El grafo admite IDs no consecutivos mediante una asociación entre el ID externo y el registro interno de la estación.

El índice ordenado permite localizar una estación en O(log V) mediante búsqueda binaria. Una vez localizado el registro, recorrer sus salidas cuesta O(grado de salida). El espacio total es O(V + E), incluido el índice.

| Entidad propuesta | Datos | Invariante |
| --- | --- | --- |
| Estación | ID, tiempo de transbordo; nombre y coordenadas opcionales. | Su ID identifica un nodo de la entrada. |
| Conexión | ID local, origen, destino, línea, duración y recurso de túnel si se define. | Conserva sentido y línea; duración válida. |
| Misión | Dos orígenes y dos destinos. | Todos existen en el grafo. |
| Evento | Personaje, tipo, inicio, fin, estación o conexión. | Los eventos de un personaje forman una cronología consistente. |
| Plan | Eventos, salidas, llegadas, objetivo y estado. | Puede validarse y reportarse sin volver a ejecutar la búsqueda. |

Los eventos representan espera inicial, viaje, transbordo y llegada. Las coordenadas se usan para dibujar el grafo.

Para calcular una ruta individual con transbordos, el estado debe recordar al menos `(estacion, linea_de_llegada)`. Llegar al mismo nodo por líneas distintas puede cambiar el costo de continuar. La primera subida al tren tiene costo de transbordo cero y los cierres de transbordo solo se aplican a cambios de línea.

## 6. Tiempo, sincronización y colisiones

Para cada personaje i:

```text
duracion_i = viajes_i + transbordos_i
llegada_i = salida_i + duracion_i
sincronizacion: llegada_P = llegada_A = T
objetivo: minimizar T, medido desde el inicio de la operación
```

Cuando no hay esperas intermedias, horarios variables ni conflictos adicionales, dos duraciones de 25 y 18 permiten salidas 0 y 7 y llegada en 25. El desfase debe recalcularse y las colisiones revisarse sobre los horarios finales. Mover una salida puede crear o eliminar un conflicto.

Para el objetivo, `T_P` y `T_A` se miden desde el minuto 0 e incluyen el desfase de salida. Con la llegada sincronizada, `max(T_P, T_A)` es el instante de llegada común.

Validación de un plan:

1. Cada viaje usa una arista existente y su duración vigente.
2. Cada cambio de línea suma el transbordo correspondiente.
3. Los eventos son consecutivos o las esperas están representadas explícitamente.
4. Se respetan restricciones horarias, aplicadas según la regla acordada.
5. Se comparan ocupaciones de estación y túnel entre personajes.
6. Ambos llegan a sus destinos asignados en el mismo instante.

Para estaciones se comparan intervalos cerrados `[inicio, fin]`, incluidos los pasos instantáneos `[t, t]`. Coinciden si `max(inicios) <= min(fines)`. Para túneles se comparan intervalos `[inicio, fin)` del mismo recurso. Se solapan si `max(inicios) < min(fines)`. Dos viajes pueden tocarse en el límite del túnel y aun así generar una coincidencia en la estación si ambos están allí en ese instante. El viaje termina al alcanzar por primera vez el destino asignado.

El reporte `SOLUCION` incluye las dos salidas, la llegada común y la cronología. Usar `SIN_SOLUCION` cuando se pueda demostrar imposibilidad, por ejemplo si algún destino es inalcanzable incluso sin restricciones. Si la exploración hasta el horizonte termina sin plan y no hay prueba de imposibilidad, devolver `LIMITE_BUSQUEDA` con el horizonte usado. En consola, los códigos previstos son 0 para solución, 1 para imposibilidad, 2 para entrada inválida y 3 para límite. Una entrada inválida se diagnostica antes de escribir el reporte de la misión.

## 7. Elección del algoritmo

Primero implementar y explicar la búsqueda de rutas individuales. Dijkstra es candidato si los costos son no negativos y el estado incluye la línea. Con restricciones dependientes del tiempo hay que justificar además cómo se incorporan horarios y esperas; no reutilizar sin más una búsqueda estática.

Después elegir una búsqueda conjunta de rutas y horarios. Candidatos para estudiar: estados temporales conjuntos o búsqueda que resuelva conflictos mediante restricciones. Registrar la elección, las reglas que soporta, su argumento de optimalidad y sus límites.

Dos Dijkstra independientes y una comprobación posterior no garantizan encontrar el mejor plan conjunto. Si fallan, puede existir una solución usando rutas distintas. Tampoco garantiza optimalidad revisar solo las primeras K rutas sin demostrar que ese límite es suficiente.

Si se usa una red expandida en el tiempo, justificar la unidad temporal, el horizonte y cómo detectar que no hay solución. Alcanzar un límite de búsqueda no demuestra imposibilidad. No eliminar ciclos o esperas por comodidad sin demostrar que no son necesarios para la sincronización.

## 8. Arquitectura propuesta

Todos estos módulos están pendientes. Los nombres concretos podrán ajustarse al implementar, actualizando también la guía de defensa.

```text
main.py                     Entrada por consola
proyecto/
    modelos.py              Entidades de la red, misión, eventos y plan
    grafo.py                Representación y operaciones del grafo
    lector_txt.py           TXT → grafo y misión
    lector_json.py          Inventarios JSON → el mismo modelo interno
    rutas.py                Búsqueda individual con transbordos
    planificador.py         Búsqueda conjunta y sincronización
    validacion_plan.py      Revisión independiente de un plan
    reporte.py              Plan → output.txt
    interfaz.py             Ventana y controles gráficos
    mapa.py                 Distribución, dibujo y navegación del grafo
    simulacion.py           Reproducción de eventos ya calculados
```

Flujo: lector → modelo → planificador → validación independiente → reporte e interfaz. La interfaz no cambia rutas ni tiempos para hacer que la animación se vea mejor.

El contrato futuro por consola será `python main.py input.txt output.txt`. No existe todavía ese ejecutable. La interfaz podrá exponerse mediante una opción que se documentará al implementarla.

## 9. Redes para verificar y demostrar el programa

Cada ejecución carga un sistema y una misión. Un sistema define estaciones y conexiones. Una misión define los dos orígenes y los dos destinos. Preparar misiones distintas sobre una misma red permite comprobar más reglas con pocos datos. El TXT de los preparadores reúne ambas partes en un archivo. Todos los sistemas se cargarán en la misma lista de adyacencia y usarán el mismo planificador. La integración de los casos nuevos está pendiente.

| Red | Alcance propuesto | Para qué usarla |
| --- | --- | --- |
| Redes de laboratorio en TXT | Casos de 4 a 10 estaciones con tiempos enteros diseñados por el equipo. | Verificar sincronización, dirección, transbordos, colisiones, rutas alternativas y destinos inalcanzables. Calcular la respuesta esperada antes de implementar. |
| Metro de Caracas | Empezar con un tramo verificado de la línea 1 y sumar una conexión con otra línea cuando se necesite demostrar un transbordo. | Probar con nombres, secuencias y correspondencias de una red real en una escala manejable. |
| Metro de París | Usar primero un subconjunto de los JSON existentes y después medir el comportamiento con la red completa. | Mostrar ramales, sentidos únicos y la visualización de una red de mayor tamaño. |

Orden de integración propuesto. Primero ejecutar los casos TXT con resultado conocido. Después preparar una misión sobre Caracas y otra sobre un subconjunto de París. Por último, probar la red completa de París cuando tenga los tiempos necesarios y registrar el rendimiento observado. Para cada caso, guardar la fuente de la red, la misión, los tiempos usados y el resultado esperado cuando se pueda calcular a mano.

Para Caracas, registrar fuente, fecha, tramo cubierto y procedencia de los tiempos. Un tramo de una sola línea puede mostrar viajes y sincronización. Para demostrar transbordos hace falta incorporar otra línea con una correspondencia real verificada. Si faltan duraciones medidas, un caso de simulación puede usar valores definidos por el equipo y marcados como tales.

Además del ejemplo de cuatro estaciones de la sección 4, preparar un caso que obligue a cambiar de ruta. Pierre tiene `1 → 3 → 4` con dos viajes de 2 minutos. Amélie tiene `2 → 3 → 5`, también con dos viajes de 2 minutos, y una alternativa `2 → 6 → 5` de 3 y 2 minutos. Todas las aristas de cada ruta usan la misma línea y solo existen las indicadas. La única opción para llegar en el minuto 4 obliga a ambos a pasar por la estación 3 en el minuto 2. Con la alternativa, Amélie sale en 0 y Pierre en 1. Ambos llegan en 5. Bajo la convención de minutos enteros y desfase de salida permitido, 5 es el mínimo. Guardar el caso y su resultado esperado al implementar el lector.

### Datos disponibles de París

Estado existente: 321 estaciones de metro, 16 líneas, 405 relaciones estación-línea, 35 recorridos y 770 conexiones dirigidas. Los archivos contienen también datos heredados de otros modos; el adaptador debe filtrar `mode == "metro"`.

Usar `connections` para construir aristas y `routes` para consultar recorridos. No inferir aristas ordenando posiciones globales en líneas con ramales o bucles. Cada conexión cuenta una sola vez aunque la usen varios recorridos.

Pendientes: coordenadas de 19 estaciones, tiempos de viaje y transbordo. `null` significa desconocido, nunca cero. Se puede dibujar una estación sin coordenadas usando una disposición automática. Para resolver una misión ponderada debe haber duraciones válidas.

Si se acuerdan tiempos ficticios para demostraciones, registrarlos como parámetros de simulación y distinguirlos de datos reales. La conversión de JSON a TXT es una herramienta futura; no es una condición para aceptar el TXT de los preparadores.

## 10. Interfaz acordada

La profesora permite librerías de terceros para la interfaz. Estas son las dos opciones previstas para el proyecto.

| Opción | Componentes | Uso previsto |
| --- | --- | --- |
| Tkinter, biblioteca estándar de Python | `ttk` para controles, `filedialog` para abrir el TXT, `Canvas` para dibujar el grafo y `after()` para programar los pasos de la animación. | Opción recomendada para la primera versión. Permite cargar un caso, dibujar estaciones y flechas, resaltar rutas y mostrar horarios. Comprobar en el portátil con `python -m tkinter`. |
| PySide6, librería de terceros | Qt Widgets para controles y paneles, `QGraphicsScene` y `QGraphicsView` para el mapa, `QTimer` para la reproducción. | Alternativa para una vista con zoom, desplazamiento y selección de estaciones. Requiere instalar PySide6 en el equipo que ejecute la interfaz. |

La recomendación inicial es **Tkinter con `ttk` y `Canvas`**. La elección se confirmará con una primera demostración que cargue un TXT y muestre las dos rutas. Si el mapa requiere más interacción, evaluaremos PySide6 con el mismo caso. [Documentación de Tkinter](https://docs.python.org/3/library/tkinter.html) · [Documentación de QGraphicsView](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QGraphicsView.html) · [Documentación de QTimer](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QTimer.html).

La interfaz recibirá la red y los eventos calculados por el núcleo. Las librerías gráficas se limitarán a presentación e interacción. El punto de entrada por consola deberá funcionar sin instalarlas. El primer control será cargar un TXT o elegir un sistema de demostración que tenga una misión válida.

Primera versión:

1. Cargar TXT y mostrar errores legibles.
2. Dibujar el grafo con flechas y colores por línea.
3. Mostrar orígenes y destinos leídos de la misión.
4. Resolver, resaltar las dos rutas y mostrar horarios.
5. Exportar `output.txt`.

Segunda versión: zoom, desplazamiento, arrastre de estaciones, filtros, reproducción, pausa, velocidad y línea de tiempo. Pierre y Amélie se distinguirán por color y forma.

Para redes ficticias, la distribución automática no depende de coordenadas reales. Una búsqueda costosa debe permitir que la ventana responda; la estrategia de ejecución y cancelación se definirá al implementar. Las actualizaciones de widgets deben realizarse desde el hilo de la interfaz.

## 11. Etapas y condiciones para cerrarlas

| Etapa | Trabajo | Se cierra cuando… |
| --- | --- | --- |
| E0 | Documentación y decisiones. | Las reglas del equipo están registradas en D01–D11 para implementar el prototipo. |
| E1 | Modelos, grafo y lector TXT. | Se representa cualquier caso válido; errores claros; sentido y aristas paralelas preservados. |
| E2 | Rutas individuales. | Hay ejemplos resueltos manualmente con cambios de línea, dirección y falta de ruta. |
| E3 | Cronologías y colisiones. | Detecta ocupaciones superpuestas, transbordos y conflictos en los límites acordados. |
| E4 | Planificación conjunta. | Produce planes válidos, justifica su objetivo y distingue imposibilidad de límite de búsqueda. |
| E5 | Reporte y consola. | Se puede ejecutar una misión y entregar fuente, TXT y salida sin intervención manual. |
| E6 | Redes de demostración e interfaz básica. | Carga el TXT y los sistemas de demostración con el mismo modelo y muestra el mismo plan que la consola. |
| E7 | Animación y navegación. | La reproducción coincide con la cronología y puede pausarse o recorrerse en el tiempo. |
| E8 | Preparación de entrega y defensa. | El equipo reproduce los ejemplos y explica cada decisión y función importante. |

La selección del algoritmo y sus pruebas de optimalidad tienen prioridad sobre el acabado visual. El estado real de cada etapa se mantiene en la bitácora.

## 12. Verificación prevista

Casos significativos: arista de un solo sentido, IDs no consecutivos, aristas paralelas, transbordo que cambia la mejor ruta, llegada simultánea sencilla, conflicto durante un transbordo, cruce de túnel con salidas distintas, ruta alternativa necesaria, destino inalcanzable, ramales, bucles y restricciones horarias.

| Caso límite | Resultado esperado |
| --- | --- |
| Pierre sale de X en 4 y Amélie llega a X en 4. | Colisión en X porque ambos ocupan ese instante. |
| Dos viajes usan el mismo túnel en `[2, 6)` y `[6, 9)`. | Sus ocupaciones de túnel son compatibles. Se verifican por separado las estaciones de ambos viajes. |
| Un cambio de duración cero ocurre en 4 y hay un cierre de transbordo `[4, 8)` para la línea de destino. | Cambio prohibido. En el minuto 8 el cierre ya terminó. |
| Un viaje comienza en 6 con dos ventanas de retraso activas para su línea. | Duración igual al doble del tiempo base. |
| Ambos orígenes coinciden. | `SIN_SOLUCION` por ocupación compartida en el minuto 0. |
| Pierre tiene origen igual a su propio destino y Amélie llega a un destino distinto en 5 sin pasar por la estación de Pierre. | Llegada común en 5. Pierre permanece en su estación hasta ese instante y su recorrido tiene cero viajes. |
| El mejor plan llega en 6 y se prueba con horizonte 5. | `LIMITE_BUSQUEDA`. Con horizonte 6 el plan entra en la búsqueda. |

Para casos muy pequeños, comparar el objetivo del planificador con una enumeración independiente y finita, cuyos límites estén justificados. La validación del plan comprueba factibilidad; no demuestra por sí sola optimalidad.

Medir tiempos y tamaño de estados en casos de distinto tamaño. Registrar límites reales en la bitácora; no prometer soporte de toda la red con un método aún sin medir.

## 13. Fechas y entrega

El PDF indica entrega el **domingo 29 de noviembre antes de medianoche** y defensa el **martes 1 de diciembre en clase**, sin escribir el año. El calendario de trabajo usa provisionalmente 2026 por el contexto del trimestre; confirmar las fechas oficiales.

Hitos internos propuestos, sujetos al avance y a la disponibilidad del equipo:

- 13–16 de noviembre: fijar reglas del prototipo, implementar grafo y lector, y preparar casos pequeños.
- 17–22 de noviembre: priorizar planificación, reporte y ejecución completa de los casos TXT.
- 23–26 de noviembre: integrar un tramo real e interfaz básica según el avance del núcleo.
- 27–28 de noviembre: ensayo, revisión del paquete y margen de corrección. Añadir animación según el tiempo disponible.
- 29 de noviembre: entregar con antelación al cierre.
- 30 de noviembre: repaso final; 1 de diciembre: defensa.

Antes de entregar: verificar nombres y rutas de archivos, dependencias permitidas, código propio comprendido por todos, ejemplos completos, salida regenerable, portátil y asistencia de todo el equipo.

## 14. Mantenimiento de la documentación

Al cerrar una tarea: registrar qué cambió y su evidencia en la bitácora; actualizar reglas o arquitectura aquí; incorporar archivos, funciones y preguntas nuevas en la guía de defensa. Una tarea no pasa a completada solo por estar descrita en estos documentos.
