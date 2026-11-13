# Datos del metro de París para el proyecto

Topología habitual revisada el **5 de noviembre de 2026**. Los dos archivos mantienen sus raíces como listas JSON y se leen con `json.load` de la biblioteca estándar de Python.

## Contenido

- `metro-stops.json`: 455 paradas, de las cuales 321 pertenecen al metro y 134 exclusivamente a otros modos. Se agregaron 19 estaciones; las 302 estaciones de metro originales se reutilizaron, normalizando nombres y conservando variantes en `aliases`.
- `metro-lines.json`: 22 líneas del catálogo original, incluidas las 16 de metro. Cada línea de metro contiene recorridos completos y conexiones dirigidas explícitas. Hay 405 relaciones estación-línea de metro.
- `validar_metro.py`: revisión de referencias, posiciones, continuidad, bifurcaciones y sentidos únicos, sin dependencias externas.

Los datos heredados de RER y tranvías se conservan con `topology_status: "legacy_unverified"`. El RER C figura en el catálogo sin paradas asociadas. Estas líneas no forman parte del grafo de metro corregido.

## Estaciones e identificadores

`id` es un entero único local del proyecto, no un identificador oficial RATP. Las estaciones originales conservan el orden de sus registros al recibir IDs; las nuevas se añaden al final. Las referencias de conexiones y recorridos usan estos IDs, nunca el índice de un array.

Cada relación de una estación con una línea de metro contiene:

- `line`: ID de línea, por ejemplo `ligne-8` o `ligne-7-bis`.
- `position`: posición, desde 1, en el primer recorrido de una línea lineal. La línea 8 queda ordenada desde Balard hasta Pointe du Lac. El campo vale `null` en las líneas 7, 7bis, 10 y 13, donde una posición global sería ambigua.
- `positions`: lista de pares `route` y `position`. Permite ubicar la estación en cada recorrido y representar más de una aparición en un viaje circular.

Las coordenadas heredadas se identifican como `coordinate_status: "inherited_unverified"`. Las 19 estaciones añadidas llevan coordenadas y descripción `null`, con `coordinate_status: "pending"`: su ubicación numérica no se ha inventado. Esto no impide utilizar la conectividad del grafo. Los tiempos de transbordo también quedan como `transfer_time_minutes: null` hasta disponer de datos o acordar valores para la simulación.

## Líneas, recorridos y conexiones

Filtrar `mode == "metro"` para construir el grafo del proyecto.

Cada elemento de `routes` contiene un `id`, `origin`, `destination` y `station_ids`: la lista de estaciones en orden real de circulación. En líneas lineales se incluyen ambos sentidos. Los IDs de ramal son etiquetas locales, no nombres oficiales de servicios.

Cada elemento de `connections` representa **una arista dirigida**:

- `source` y `target`: IDs de las dos estaciones consecutivas.
- `routes`: recorridos que utilizan esa arista, sin duplicar las conexiones de los troncos comunes.
- `segment_id`: identificador de un tramo de línea entre esas estaciones. Es el mismo para ambos sentidos y sirve para agruparlos en la simulación; no identifica oficialmente un túnel, tren, vía o andén físico. La ocupación de recursos compartidos entre líneas requeriría información adicional.
- `travel_time_minutes`: peso pendiente, actualmente `null`. No interpretar `null` como cero.

Las conexiones declaradas son la fuente para construir el grafo. No se deben generar conexiones inversas automáticamente ni conectar estaciones solamente por tener posiciones consecutivas.

## Casos especiales corregidos

- **Línea 7:** tronco La Courneuve - 8 Mai 1945 → Maison Blanche; desde Maison Blanche salen ramales independientes hacia Mairie d'Ivry y Villejuif - Louis Aragon. Hay un recorrido por sentido y ramal.
- **Línea 13:** tronco Châtillon - Montrouge → La Fourche; bifurcación hacia Les Courtilles y Saint-Denis - Université. Hay un recorrido por sentido y ramal.
- **Línea 7bis:** tronco Louis Blanc ↔ Botzaris y bucle dirigido Botzaris → Place des Fêtes → Pré-Saint-Gervais → Danube → Botzaris. Se representa un recorrido completo que regresa a Louis Blanc, con estaciones del tronco repetidas en la vuelta.
- **Línea 10 hacia Gare d'Austerlitz:** Boulogne - Jean Jaurès → Michel-Ange - Molitor → Chardon Lagache → Mirabeau → Javel - André Citroën.
- **Línea 10 hacia Boulogne:** Javel - André Citroën → Église d'Auteuil → Michel-Ange - Auteuil → Porte d'Auteuil → Boulogne - Jean Jaurès. Los tramos comunes de ambos extremos tienen circulación en ambos sentidos. Se modelan los servicios habituales entre cabeceras; quedan fuera las salidas especiales de inicio de servicio en Porte d'Auteuil.

Se completaron las ampliaciones de las líneas 4, 11, 12 y 14. Las estaciones que ya existían, como Maison Blanche, Porte de Clichy y Mairie de Saint-Ouen, recibieron su correspondencia con la línea 14.

## Alcance del modelo

Se usa una estación nominal por nodo, de acuerdo con la abstracción del proyecto. Los nombres diferentes, como Châtelet y Les Halles, se mantienen como nodos distintos. Los pasillos de conexión entre estaciones de nombres diferentes no se han convertido en viajes de metro ficticios.

Los recorridos describen conectividad habitual, sin horarios, cierres temporales ni trenes concretos. Aún deben definirse los pesos de viaje, transbordos y condiciones temporales antes de ejecutar una optimización ponderada.

## Verificación

Desde la raíz del proyecto:

```powershell
python metro-paris/validar_metro.py
```

El validador comprueba los conteos por línea, la unicidad de IDs y nombres, las referencias cruzadas, la coincidencia entre recorridos y conexiones, los puntos de bifurcación, la ausencia de inversas indebidas en los sentidos únicos y la conectividad dirigida de cada línea y de la red de metro completa. Las comprobaciones estructurales no certifican coordenadas, tiempos ni servicio en tiempo real.

## Fuentes

- [Plano de red RATP, edición enero de 2026](https://www.ratp.fr/informer/picts/plans/pdf/reseaux/metro.pdf).
- [Bonjour RATP, directorio de líneas](https://www.bonjour-ratp.fr/lignes-metro/). Cada línea de metro incluye sus enlaces específicos en `sources`.
- [RATP: estación Danube y sentido del bucle 7bis](https://www.ratp.fr/decouvrir/patrimoine/histoire-station-danube).
- [Transilien: descripción detallada de los dos sentidos de la línea 10](https://www.transilien.com/fr/page-lignes/metro-10).
- Inventario local `../metro_paris_rutas_y_estaciones.md`, usado para organizar las secuencias y normalizar los nombres.
