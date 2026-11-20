# Registro de contribuciones

Cada integrante llena su fila y su sección. El historial de commits de GitHub complementa este registro.

| Rol | Integrante | Archivos principales |
|---|---|---|
| A — Datos y calidad | Alan | `src/carga.py`, `src/limpieza.py`, `notebooks/01_comprension_calidad.ipynb`, `results/tables/bitacora_limpieza.csv` |
| B — Pregunta 1 | Pau | `src/polarizacion.py`, `notebooks/02_popularidad_polarizacion.ipynb` |
| C — Pregunta 2a | Jonathan | `src/afinidades_peliculas.py`, `notebooks/03_afinidades_peliculas.ipynb` |
| D — Pregunta 2b | Hugo | `src/afinidades_generos.py`, `notebooks/04_afinidades_generos.ipynb` |
| E — Fun facts e integración | Andrés | `src/rutas.py`, `notebooks/05_fun_facts.ipynb`, `README.md`, `requirements.txt` |

## Detalle por integrante

### A — Alan
- …

### B — Pau
- …

### C — Jonathan
- Desarrollo de `src/afinidades_peliculas.py`, implementando la función `matriz_gustos()` para construir una matriz usuario-película a partir de las calificaciones.
- Filtrado de películas con al menos 100 calificaciones para trabajar con observaciones suficientes.
- Transformación de las calificaciones en una variable binaria de aceptación: 1 si la calificación es igual o superior a 4 y 0 en caso contrario, conservando los valores faltantes como `NaN`.
- Análisis de las diferencias en los hábitos de calificación de los usuarios mediante el porcentaje de películas que calificaron con 4 o más.
- Cálculo de correlaciones de Pearson entre películas, utilizando un mínimo de 20 observaciones compartidas.
- Identificación y ordenamiento de las parejas de películas con mayor correlación, incorporando sus títulos.
- Elaboración de un mapa de calor (*heatmap*) para visualizar las afinidades entre las películas más reseñadas.
- Comparación de las probabilidades condicionadas \(P(Y=1 \mid X=1)\) con las probabilidades generales \(P(Y=1)\) para las cinco parejas con mayor correlación.
- Interpretación de los resultados y documentación de las limitaciones del análisis, incluyendo el sesgo de calificación, los datos faltantes y la interpretación de las correlaciones.

### D — Hugo

- Desarrollo de `src/afinidades_generos.py`, implementando la función `perfil_genero()` para construir una matriz usuario+generos a partir de las calificaciones.
-Elaboración de tabla resumen con número de películas, númer de ratings, media de ratings, mediana de ratings y std de raitings agrupada por género.
-Elaboración de BoxPlot para la visualización de ratings por género.
-Elaboración de las matrices de correlación (coocurrencia y preferenica).
- Elaboración de los mapas de calor para visualizar las diferencias entre las correlaciones de coocurrencia y preferencia.
- Elaboración de gráfico scatterplot para visualizar la relación entre las correlaciones de coocurrencia y preferencias.
- Interpretación de los resultados y documentación de las limitaciones del análisis, incluyendo el sesgo de calificación y la interpretación de la relación entre las correlaciones de coocurrencia y preferencia.

### E — Andrés

- **Esqueleto del repositorio:** estructura de carpetas, plantillas de los notebooks y datos dummy (`src/_dummies.py`), que permitieron al equipo trabajar en paralelo antes de tener la limpieza real.
- **`src/rutas.py`:** rutas del proyecto y funciones `guardar_figura()` (acepta una Figure, un Axes o un FacetGrid de seaborn) y `guardar_tabla()`, usadas por todos los notebooks para exportar resultados.
- **Notebook 05 — Fun facts:**
  - Función reutilizable `worst_best_n_movies()` para ordenar la tabla de la pregunta 1 por cualquier métrica. Con ella se obtienen las mejores y peores películas de todos los tiempos (n ≥ 20), las mejores y peores por década de estreno y las 10 más polémicas (mayor desviación estándar).
  - Número de ratings por género (una película con varios géneros cuenta en cada uno).
  - Serie de tiempo de ratings por año de calificación, con el año de mayor actividad y la mayor caída señalados automáticamente (`results/figures/05_ratings_por_anio.png`).
- **Documentación y reproducibilidad:** `README.md` (objetivo, datos, licencia, cita e instrucciones para reproducir), `requirements.txt` y este registro.

## Trabajo conjunto

- Plan de trabajo y contratos de datos (`PLAN.md`, `src/contratos.py`): todo el equipo.
- Video de exposición: todo el equipo.
