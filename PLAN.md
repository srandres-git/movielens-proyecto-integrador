# Plan de trabajo — Proyecto integrador Módulo I (MovieLens)

**Entrega:** viernes 20 de noviembre de 2026, 23:59 (CDMX) · **Equipo:** 5 integrantes · **Tiempo efectivo:** 2 días

Este documento es la referencia común del equipo: qué preguntas respondemos, qué decisiones de limpieza ya tomamos (y por qué), cómo está organizado el código para trabajar en paralelo y quién hace qué.

---

## 1. Datos y preguntas

**Dataset:** MovieLens `ml-latest-small` (GroupLens, Universidad de Minnesota). 100,836 calificaciones de 610 usuarios sobre 9,742 películas, de marzo de 1996 a septiembre de 2018.
**Licencia:** uso para investigación sin fines comerciales; se puede redistribuir (incluidas transformaciones) bajo las mismas condiciones y se debe citar a Harper & Konstan (2015). Esto va en el README.

**Tablas que usamos:** `movies.csv` y `ratings.csv`.
**Tablas que no usamos:** `links.csv` (solo enlaza IDs con IMDb y TMDb) y `tags.csv` (texto libre de usuarios; limpiarlo requiere un trabajo que no cabe en el plazo). Esta exclusión se justifica en el notebook 01.

**Unidad de observación:** en `ratings`, una calificación (usuario × película); en `movies`, una película.

### Preguntas de investigación

1. **Popularidad vs. polarización.** ¿Las películas con más calificaciones generan opiniones más divididas?
2. **Afinidades entre películas y géneros.** Si a un usuario le gusta una película o un género (rating ≥ 4), ¿qué otras películas o géneros tienden a gustarle también?
   - No lo llamamos "perfiles de usuario": eso requeriría clustering, que está fuera del alcance del módulo.

**Fun facts** (subproductos de lo anterior): mejores y peores películas de todos los tiempos y por década, las más polémicas, los géneros más y menos calificados y la actividad de calificación a lo largo del tiempo.

---

## 2. Lo que ya sabemos de los datos

Verificado con una revisión preliminar. El notebook 01 debe volver a mostrar cada punto con código.

| Aspecto | Resultado |
|---|---|
| Valores vacíos | 0 en ambas tablas |
| Valores de `rating` | Todos en {0.5, 1.0, …, 5.0} |
| `movieId` como llave de `movies` | Válida, sin duplicados |
| `(userId, movieId)` como llave de `ratings` | Válida, sin duplicados |
| Integridad referencial | 0 ratings de películas inexistentes; 18 películas sin ningún rating |
| `(no genres listed)` | 34 películas (0.35 %) con 47 ratings (0.05 %) |
| Géneros | 19 distintos más `(no genres listed)`. **IMAX** (158 películas) aparece en los datos pero no en la lista del README; el README dice "Children's" y los datos "Children" |
| Títulos | 11 con espacios sobrantes; 13 sin año entre paréntesis |
| Títulos duplicados | 5 títulos con dos `movieId` distintos (Emma 1996, War of the Worlds 2005, Saturn 3, Eros, Confessions of a Dangerous Mind), con géneros diferentes; algunos usuarios calificaron ambas versiones |
| Ratings por película | Muy asimétrico: mediana 3, percentil 90 = 27, máximo 329 |
| Ratings por usuario | Mínimo 20, mediana 70, máximo 2,698; los 10 usuarios más activos suman el 16 % de los ratings |
| % de ratings ≥ 4 por usuario | De 0 % a 100 % (mediana 58 %): "gustar" no significa lo mismo para todos |

---

## 3. Decisiones de limpieza y transformación

El proyecto exige documentar al menos dos decisiones. Tenemos seis; las marcadas con ★ son las que destacaremos en el video. Todas se registran en `results/tables/bitacora_limpieza.csv` con las columnas *problema · evidencia · decisión · consecuencia*.

1. **Tipos al leer.** `userId` y `movieId` se leen directamente como `str` (`dtype=` en `read_csv`), así nunca aparece la forma `'x.0'`. `rating` se lee como `float` y se valida explícitamente contra el conjunto {0.5, …, 5.0}. `timestamp` se convierte con `pd.to_datetime(..., unit='s', utc=True)`.
2. ★ **Títulos duplicados: no se fusionan.** `movieId` sigue siendo la llave. Los géneros difieren entre versiones y al menos dos casos son películas distintas reales. Si los fusionáramos, aparecerían duplicados `(userId, movieId)` en ratings y tendríamos que descartar calificaciones reales. En las tablas de resultados mostramos título + `movieId`. La función general `validar_llave(df, cols)` se conserva como evidencia de que verificamos las llaves.
3. ★ **`(no genres listed)`: no se imputa.** No hay información para inferir el género, así que imputarlo sería inventarlo. Estas películas se quedan en los análisis por película (pregunta 1, fun facts) y salen solas de los análisis por género, porque todas sus columnas dummy valen 0. Impacto: 0.35 % de las películas y 0.05 % de los ratings.
4. **Normalización de géneros.** IMAX es un formato, no un género: se excluye de las columnas de género y se guarda como bandera `es_imax`. La discrepancia "Children's"/"Children" solo se documenta. Resultado: 18 columnas dummy 0/1 en `movies`.
5. **Año de estreno.** Se extrae del título después de quitar los espacios sobrantes; si no se quitan primero, la expresión regular falla en 11 títulos. Los 13 títulos sin año quedan como faltante (`<NA>`) y no se imputan.
6. ★ **Umbral mínimo de ratings por película.** Con n = 1 la desviación estándar no existe, y con n chico es puro ruido. Umbral principal: **n ≥ 20** (1,297 películas, 67 % de los ratings). Se reporta la sensibilidad con otros umbrales:

   | Umbral | Películas | % de ratings conservados |
   |---|---|---|
   | n ≥ 10 | 2,269 | 80 % |
   | n ≥ 20 | 1,297 | 67 % |
   | n ≥ 50 | 450 | 41 % |
   | n ≥ 100 | 138 | 20 % |

**Atípicos:** los usuarios con miles de ratings no son un error y se conservan. Se mencionan como limitación porque pesan mucho en las correlaciones.

---

## 4. Método por pregunta

Solo usamos herramientas vistas en el curso: `describe`, cuantiles, RIC, `groupby`/`agg`, `crosstab`, `qcut`, `log1p`, Pearson/Spearman, boxplot, histograma, `hexbin`/`imshow` con matplotlib.

### Pregunta 1 — Popularidad vs. polarización (integrante B)

- **Tabla base:** por película, número de ratings (n), media, mediana, desviación estándar (medida principal de dispersión) y RIC (medida robusta). Se aplica el umbral n ≥ 20.
- **Medida de asociación:** **Spearman** como principal, porque n es muy asimétrico; Pearson al lado como comparación.
  - Dividir n entre una constante **no cambia** ninguna de las dos correlaciones, así que no lo hacemos.
  - `log1p(n)` se usa solo para el eje de los gráficos.
- **Factor de confusión: la escala acotada.** Una película con media cercana a 5 no puede tener una desviación grande. Hay que reportar las tres correlaciones: n–std, n–media y media–std. En la revisión preliminar (n ≥ 20):
  - ρ(media, std) ≈ −0.42
  - ρ(n, media) ≈ +0.27
  - ρ(n, std) ≈ −0.03

  Es decir, **lo más probable es que la respuesta sea "no hay relación"**. Es un hallazgo válido y no hay que forzarlo.
- **Sensibilidad:** repetir ρ(n, std) con umbrales de 10, 20 y 50. Si la conclusión no cambia, es robusta.
- **Gráficos:**
  - `hexbin` de log(n) contra std, opcionalmente coloreado por media.
  - Boxplot de std por cuartil de popularidad (`pd.qcut`).
  - Histograma de ratings de las 3 películas más polémicas, para mostrar que una std alta puede ser bimodalidad (polarización real) o simplemente opiniones repartidas.

### Pregunta 2a — Afinidades entre películas (integrante C)

- **Matriz usuario × película:**
  - **1** si el rating es ≥ 4, **0** si es < 4, **NaN** si el usuario no la vio.
  - Un NaN **no** significa "no le gustó". Si rellenamos con 0, la correlación mide qué se ve junto, no qué gusta junto, y la domina la popularidad.
- **Solo películas con n ≥ 100 (138).** Con todo el catálogo, la mayoría de los pares de películas tiene 0 a 2 usuarios en común. Usar `corr(min_periods=20)`.
  - Nota: la correlación de Pearson entre dos variables 0/1 es el coeficiente phi.
- **Resultados:**
  - Tabla con los pares más correlacionados: triángulo superior de la matriz, `stack` y ordenar.
  - Heatmap (`imshow`) de unas 20 películas.
  - Un heatmap de 138 × 138 no se lee: no lo usamos.
- **"Si te gusta X, te gusta Y" es una relación asimétrica.** Para los 5 mejores pares, calcular `pd.crosstab(..., normalize='index')`, que da P(le gusta Y | le gusta X), y compararla con P(le gusta Y) en general.
- **Limitación:** los usuarios tienen escalas distintas (el % de ratings ≥ 4 va de 0 % a 100 %). Se documenta con un `describe` y no se corrige.

### Pregunta 2b — Afinidades entre géneros (integrante D)

- **Problema:** dos géneros pueden "gustar juntos" solo porque suelen asignarse a las mismas películas. No agrupamos géneros a priori: sería subjetivo y requeriría clustering. En su lugar comparamos dos matrices.
  1. **Preferencia.** Perfil usuario × género: proporción de ratings ≥ 4 de cada usuario en cada género, con NaN si el usuario tiene menos de 5 ratings en ese género. Correlación entre géneros con `min_periods`.
  2. **Coocurrencia.** Correlación entre las 18 columnas dummy de `movies`.
- **Resultados:**
  - Los dos heatmaps lado a lado.
  - Scatter de los 153 pares de géneros: x = coocurrencia, y = preferencia. Los pares muy por encima de la tendencia son afinidades que van más allá del etiquetado conjunto.
- **Tabla por género:** n de películas, n de ratings, media, mediana y std, más un boxplot de ratings por género. Aclarar que una película con varios géneros se cuenta en cada uno.

### Fun facts (integrante E)

- **Mejores y peores de todos los tiempos:** solo con n ≥ 20; si no, ganan películas con un único 5.0.
- **Mejores y peores por década de estreno** (`anio // 10 * 10`): por año individual hay muy pocas películas que pasen el umbral.
- **Más polémicas:** mayor std, de la tabla de la pregunta 1.
- **Géneros más y menos calificados:** de la tabla por género.
- **Ratings por año de calificación:** línea de tiempo con picos en 2000 y 2015–2017. Refleja la actividad de 610 usuarios, no la popularidad del cine; esa advertencia va en el texto.

**Regla para todo el proyecto:** cada gráfico va seguido de una celda markdown que explique **qué muestra, por qué es relevante y qué limitaciones tiene**. Esto vale el 20 % de la calificación.

---

## 5. Organización del código para trabajar en paralelo

```
movielens-proyecto-integrador/
├── README.md               # objetivo, preguntas, cómo reproducir, licencia y cita
├── PLAN.md                 # este documento
├── CONTRIBUCIONES.md       # registro de aportes por integrante
├── requirements.txt
├── data/raw/               # movies.csv, ratings.csv y README.txt originales
├── src/
│   ├── contratos.py        # columnas esperadas de cada tabla + verificar_esquema()
│   ├── carga.py            # lectura con tipos                         (A)
│   ├── limpieza.py         # validaciones, géneros, año, bitácora      (A)
│   └── metricas.py         # tablas derivadas para las preguntas       (B, C, D)
├── notebooks/
│   ├── 01_comprension_calidad.ipynb        (A)
│   ├── 02_popularidad_polarizacion.ipynb   (B)
│   ├── 03_afinidades_peliculas.ipynb       (C)
│   ├── 04_afinidades_generos.ipynb         (D)
│   └── 05_fun_facts.ipynb                  (E)
└── results/
    ├── figures/
    └── tables/
```

### Cómo funcionan los dummies

- Cada función de `src/` empieza con un **cuerpo dummy**: regresa unas pocas filas con exactamente las columnas y los tipos del contrato, y valores con forma realista.
- El responsable reemplaza el cuerpo por el código real **sin cambiar la firma ni el esquema**.
- Los demás escriben su análisis contra el dummy desde el primer momento, y su código funciona igual cuando llega la versión real.
- No hay banderas para alternar entre dummy y real: hay una sola función.
- `contratos.py` es el único lugar donde se definen las columnas. Cada notebook llama a `verificar_esquema(df, ...)` al recibir una tabla; si una versión real no respeta el contrato, falla de inmediato en lugar de fallar en silencio.

### Contratos

| Función | Salida | Responsable | La usan |
|---|---|---|---|
| `cargar_movies()` | `movieId` str · `title` str · `genres` str | A | A |
| `cargar_ratings()` | `userId` str · `movieId` str · `rating` float · `timestamp` int | A | A |
| `validar_llave(df, cols)` | resumen con número de duplicados y de nulos en `cols` | A | A |
| `movies_limpias(movies_raw)` | `movieId` (único) · `title` (sin espacios sobrantes) · `anio` Int64 · `n_generos` int · `es_imax` 0/1 · 18 columnas de género 0/1 | A | B, C, D, E |
| `ratings_limpias(ratings_raw)` | `userId` · `movieId` · `rating` · `fecha` datetime UTC · `anio_rating` int | A | B, C, D, E |
| `stats_peliculas(ratings, movies, min_n=20)` | `movieId` · `title` · `anio` · `n` · `media` · `mediana` · `std` · `ric` | B | B, E |
| `matriz_gustos(ratings, min_n=100)` | índice `userId` × columnas `movieId`; valores 1.0 / 0.0 / NaN | C | C |
| `perfil_genero(ratings, movies, min_r=5)` | índice `userId` × 18 géneros; proporción en [0, 1] o NaN | D | D |

**Ruta crítica:** `movies_limpias` y `ratings_limpias` bloquean a todos, y `stats_peliculas` bloquea a E. Son cortas, así que A y B las priorizan para tener la versión real a mediodía del día 1.

### Reglas de Git (para evitar conflictos con notebooks)

- **Cada archivo tiene un solo dueño:** solo su responsable lo edita. Los notebooks de Jupyter casi no se pueden fusionar cuando dos personas los tocan.
- Cada integrante trabaja en su rama (`a-limpieza`, `b-polarizacion`, …) y la fusiona a `main` cuando su versión funciona.
- Para cambiar un contrato, primero se avisa al equipo y luego se modifica `contratos.py`, una sola vez.
- Antes de cada fusión: *Restart & Run All* del propio notebook.

---

## 6. Reparto

| Integrante | Responsabilidad | Entregables |
|---|---|---|
| **A** — Datos y calidad | Carga, validaciones, decisiones de limpieza 1–5, bitácora | `carga.py`, `limpieza.py`, notebook 01, `bitacora_limpieza.csv` |
| **B** — Pregunta 1 | Tabla por película, umbral y sensibilidad (decisión 6), correlaciones y gráficos | `stats_peliculas`, notebook 02 |
| **C** — Pregunta 2a | Matriz de gustos, mejores pares, probabilidades condicionales | `matriz_gustos`, notebook 03 |
| **D** — Pregunta 2b | Preferencia vs. coocurrencia de géneros, tabla y boxplot por género | `perfil_genero`, notebook 04 |
| **E** — Fun facts e integración | Fun facts; README, `requirements.txt`, CONTRIBUCIONES; ejecución completa desde cero; guion y edición del video | notebook 05, documentación, tag final |

Cada integrante presenta su parte en el video (requisito: todos participan con una aportación sustantiva).

---

## 7. Calendario

| Cuándo | Qué | Quién |
|---|---|---|
| **Día 1, inicio (30 min)** | Reunión breve: revisar este plan, confirmar contratos y asignaciones, clonar el repo con el esqueleto y los dummies | Todos |
| **Día 1, mañana** | Limpieza real · análisis sobre dummies | A · B, C, D, E |
| **Día 1, mediodía** | Fusionar `movies_limpias` y `ratings_limpias` reales; todos vuelven a correr con datos reales. Fusionar `stats_peliculas` real | A, B |
| **Día 1, tarde** | Resultados numéricos y primeros gráficos · cerrar notebook 01 y bitácora | B, C, D, E · A |
| **Día 2, mañana** | Interpretaciones de cada gráfico, sensibilidad, conclusiones parciales por notebook | Todos |
| **Día 2, tarde** | README y CONTRIBUCIONES; ejecución completa de todos los notebooks en orden desde un clon limpio; exportar figuras y tablas a `results/`; `git tag v1.0` | E (con todos) |
| **Día 2, noche / viernes** | Grabar el video (≤ 20 min); llenar el formulario con el enlace al repo, el enlace al video y el tag | Todos · E |

**Margen:** si algo se atrasa, se recortan primero los fun facts, nunca las interpretaciones.

---

## 8. Conclusiones: qué se puede afirmar y qué no

Esta sección va en el notebook final y en el video.

- 610 usuarios autoseleccionados, todos con al menos 20 ratings: **no representan** al público general ni a toda la base de MovieLens.
- Los usuarios eligen qué películas ver; las afinidades reflejan esa elección, no gustos "puros".
- Todo es descriptivo: una afinidad entre X y Y **no implica** que ver X cause que te guste Y.
- La relación popularidad–polarización está confundida por la media, debido a la escala acotada de 0.5 a 5.
- "Gustar" se definió como rating ≥ 4, un umbral absoluto que no significa lo mismo para usuarios generosos y para usuarios exigentes.

---

## 9. Checklist de entrega (contra la rúbrica)

- [ ] **Planteamiento y exploración (20 %):** contexto, unidad de observación, preguntas y por qué los datos sirven para responderlas (notebook 01); estadística descriptiva en cada notebook.
- [ ] **Limpieza y transformación (25 %):** bitácora con las 6 decisiones; al menos 3 desarrolladas con evidencia y consecuencias.
- [ ] **Visualización e interpretación (20 %):** cada gráfico con su interpretación y sus limitaciones.
- [ ] **Código y reproducibilidad (25 %):** README con instrucciones paso a paso, `requirements.txt`, datos con licencia y cita, `results/` con figuras y tablas, CONTRIBUCIONES, ejecución completa sin errores desde un clon limpio.
- [ ] **Video (10 %):** ≤ 20 min, todos participan, sigue el orden sugerido (contexto → preguntas → exploración → limpieza → hallazgos → código → conclusiones).
- [ ] **Formulario:** enlaces probados, con acceso de lectura para el profesor; hash del commit o tag `v1.0`.
