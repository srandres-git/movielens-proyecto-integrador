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
- …

### D — Hugo
- …

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
