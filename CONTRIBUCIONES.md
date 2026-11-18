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
- …

### E — Andrés
- …

## Trabajo conjunto

- Plan de trabajo y contratos de datos (`PLAN.md`, `src/contratos.py`): todo el equipo.
- Video de exposición: todo el equipo.
