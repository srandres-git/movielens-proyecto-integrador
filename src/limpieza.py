"""Validaciones y limpieza de movies y ratings. Responsable: A.

Las decisiones 1 a 5 de PLAN.md §3 se implementan aquí y se registran en
results/tables/bitacora_limpieza.csv.
"""
import numpy as np
import pandas as pd

from .carga import cargar_movies, cargar_ratings
from .contratos import GENEROS

# Valores que puede tomar un rating: 0.5, 1.0, ..., 5.0
RATINGS_VALIDOS = np.arange(0.5, 5.01, 0.5)


def validar_llave(df: pd.DataFrame, cols: list) -> dict:
    """Indica si ``cols`` funciona como llave de ``df``.

    Devuelve un dict con:
      - "es_llave": bool (sin duplicados y sin nulos en ``cols``)
      - "duplicados": número de filas cuya combinación de ``cols`` se repite
      - "nulos": número de filas con algún nulo en ``cols``
    """
    nulos = int(df[cols].isna().any(axis=1).sum())
    duplicados = int(df.duplicated(subset=cols, keep=False).sum())  # keep=False: cuenta todas las filas repetidas
    return {"es_llave": nulos == 0 and duplicados == 0, "duplicados": duplicados, "nulos": nulos}


def movies_limpias(movies_raw: pd.DataFrame) -> pd.DataFrame:
    """Devuelve movies limpia.

    Lo que hace (PLAN.md §3):
      - title sin espacios sobrantes (decisión 5);
      - anio extraído del título, Int64 con <NA> si no hay año; no se imputa (decisión 5);
      - una columna 0/1 por cada género de contratos.GENEROS (decisión 4);
      - es_imax 0/1; IMAX no cuenta como género (decisión 4);
      - n_generos = número de géneros de la película (0 si es "(no genres listed)");
      - movieId sigue siendo la llave: los títulos duplicados NO se fusionan (decisión 2).

    Contrato: ESQUEMAS["movies"].
    """
    movies = movies_raw[["movieId", "title"]].copy()

    # Decisión 5: primero se quitan los espacios y después se extrae el año.
    # Si no se quitan primero, la expresión regular falla en 11 títulos.
    movies["title"] = movies["title"].str.strip()
    anio = movies["title"].str.extract(r"\((\d{4})\)$")[0]
    movies["anio"] = pd.to_numeric(anio).astype("Int64")

    # Decisión 4: una columna 0/1 por género. IMAX es un formato, no un género.
    lista_generos = movies_raw["genres"].str.split("|")
    for genero in GENEROS:
        movies[genero] = lista_generos.apply(lambda lista: int(genero in lista))
    movies["es_imax"] = lista_generos.apply(lambda lista: int("IMAX" in lista))

    # "(no genres listed)" no es ninguna de las 18 columnas, así que n_generos = 0 (decisión 3).
    movies["n_generos"] = movies[GENEROS].sum(axis=1).astype(int)

    columnas = ["movieId", "title", "anio", "n_generos", "es_imax"] + GENEROS
    return movies[columnas]


def ratings_limpias(ratings_raw: pd.DataFrame) -> pd.DataFrame:
    """Devuelve ratings limpia.

    Lo que hace (PLAN.md §3):
      - valida que rating esté en {0.5, 1.0, ..., 5.0} (decisión 1);
      - fecha = timestamp convertido a datetime en UTC; anio_rating = año de esa fecha;
      - la columna timestamp se elimina (el contrato no la exige).

    Contrato: ESQUEMAS["ratings"].
    """
    fuera_de_escala = ~ratings_raw["rating"].isin(RATINGS_VALIDOS)
    if fuera_de_escala.any():
        raise ValueError(f"{fuera_de_escala.sum()} ratings fuera de {{0.5, 1.0, ..., 5.0}}")

    ratings = ratings_raw.copy()
    ratings["fecha"] = pd.to_datetime(ratings["timestamp"], unit="s", utc=True)
    ratings["anio_rating"] = ratings["fecha"].dt.year.astype(int)
    return ratings.drop(columns="timestamp")


def datos_limpios() -> tuple:
    """Atajo para los notebooks 02 a 05: (movies, ratings) ya limpias.

    No es dummy: funciona igual en cuanto las funciones de arriba sean reales.
    """
    return movies_limpias(cargar_movies()), ratings_limpias(cargar_ratings())

