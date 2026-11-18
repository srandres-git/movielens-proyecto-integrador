# Proyecto integrador — Módulo I (MovieLens)

Diplomado *Métodos estadísticos y matemáticos para la ciencia de datos* (DMEMCDM 2026) · Módulo I: Preprocesamiento y técnicas básicas de visualización de datos.

## Objetivo

Análisis exploratorio del dataset MovieLens `ml-latest-small` para responder dos preguntas descriptivas:

1. **Popularidad vs. polarización:** ¿las películas con más calificaciones generan opiniones más divididas?
2. **Afinidades:** si a un usuario le gusta una película o un género (rating ≥ 4), ¿qué otras películas o géneros tienden a gustarle también?

El plan completo, las decisiones de limpieza y el reparto del trabajo están en [PLAN.md](PLAN.md).

## Datos

`data/raw/` contiene `movies.csv`, `ratings.csv` y el `README.txt` original de `ml-latest-small` (descargado de <https://grouplens.org/datasets/movielens/latest/>). Las tablas `links.csv` y `tags.csv` no se usan y no se incluyen.

**Licencia:** el dataset se usa con fines académicos y no comerciales, y se redistribuye bajo las mismas condiciones de GroupLens (ver `data/raw/README.txt`).

**Cita:**

> F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems (TiiS)* 5, 4: 19:1–19:19. <https://doi.org/10.1145/2827872>

## Cómo reproducir el análisis

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/srandres-git/movielens-proyecto-integrador.git
   cd movielens-proyecto-integrador
   ```
2. Crear un entorno con Python 3.10 o superior e instalar las dependencias:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate   ·   macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Abrir y ejecutar los notebooks **en orden** (*Restart & Run All*):

   | Notebook | Contenido |
   |---|---|
   | `notebooks/01_comprension_calidad.ipynb` | Descripción de los datos, validaciones y decisiones de limpieza |
   | `notebooks/02_popularidad_polarizacion.ipynb` | Pregunta 1 |
   | `notebooks/03_afinidades_peliculas.ipynb` | Pregunta 2a |
   | `notebooks/04_afinidades_generos.ipynb` | Pregunta 2b |
   | `notebooks/05_fun_facts.ipynb` | Hallazgos complementarios y conclusiones generales |

Las figuras se guardan en `results/figures/` y las tablas en `results/tables/`, incluida la bitácora de limpieza.

## Organización del código

```
src/
├── contratos.py             # columnas esperadas de cada tabla y funciones de verificación
├── rutas.py                 # rutas del proyecto y guardado de resultados
├── carga.py                 # lectura de los CSV con sus tipos
├── limpieza.py              # validaciones y limpieza de movies y ratings
├── polarizacion.py          # tabla por película (pregunta 1)
├── afinidades_peliculas.py  # matriz de gustos usuario × película (pregunta 2a)
├── afinidades_generos.py    # perfil usuario × género (pregunta 2b)
└── _dummies.py              # temporal: datos inventados mientras se desarrolla
```

Los notebooks contienen el análisis, las visualizaciones y las interpretaciones. `src/` contiene las funciones que producen las tablas que comparten varios notebooks.

## Para el equipo: cómo trabajar con los dummies

- Cada función de `src/` empieza con un **cuerpo dummy**: devuelve datos inventados con las columnas y tipos exactos de su contrato (`src/contratos.py`), y al ejecutarse muestra un aviso `DUMMY`.
- El responsable reemplaza el cuerpo por su código real, **sin cambiar la firma ni las columnas de salida**. Los demás no tienen que cambiar nada.
- Los datos dummy **no** son consistentes entre tablas ni parecidos a los reales: sirven para escribir y probar código, no para interpretar.
- Cada notebook verifica las tablas que recibe con `contratos.verificar_esquema` o `contratos.verificar_matriz`. Si una versión real rompe un contrato, el error aparece ahí.
- Cuando ya no quede ningún aviso `DUMMY` al ejecutar los notebooks, se borra `src/_dummies.py`.
- Una persona por archivo y una rama por persona (ver PLAN.md §5).

## Contribuciones

Ver [CONTRIBUCIONES.md](CONTRIBUCIONES.md).
