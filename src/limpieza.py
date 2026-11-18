"""Validaciones y limpieza de movies y ratings. Responsable: A.

Las decisiones 1 a 5 de PLAN.md §3 se implementan aquí y se registran en
results/tables/bitacora_limpieza.csv.
"""
import pandas as pd

from . import _dummies
from .carga import cargar_movies, cargar_ratings


def validar_llave(df: pd.DataFrame, cols: list) -> dict:
    """Indica si ``cols`` funciona como llave de ``df``.

    Debe devolver un dict con al menos:
      - "es_llave": bool (sin duplicados y sin nulos en ``cols``)
      - "duplicados": número de filas cuya combinación de ``cols`` se repite
      - "nulos": número de filas con algún nulo en ``cols``

    DUMMY: reemplaza la línea de abajo por tu código sin cambiar la firma.
    """
    _dummies.aviso("validar_llave")
    return {"es_llave": True, "duplicados": 0, "nulos": 0}


def movies_limpias(movies_raw: pd.DataFrame) -> pd.DataFrame:
    """Devuelve movies limpia.

    Lo que debe hacer (PLAN.md §3):
      - title sin espacios sobrantes (decisión 5);
      - anio extraído del título, Int64 con <NA> si no hay año; no se imputa (decisión 5);
      - una columna 0/1 por cada género de contratos.GENEROS (decisión 4);
      - es_imax 0/1; IMAX no cuenta como género (decisión 4);
      - n_generos = número de géneros de la película (0 si es "(no genres listed)");
      - movieId sigue siendo la llave: los títulos duplicados NO se fusionan (decisión 2).

    Contrato: ESQUEMAS["movies"].

    DUMMY: reemplaza las dos líneas de abajo por tu código sin cambiar la firma.
    """
    _dummies.aviso("movies_limpias")
    return _dummies.tabla("movies")


def ratings_limpias(ratings_raw: pd.DataFrame) -> pd.DataFrame:
    """Devuelve ratings limpia.

    Lo que debe hacer (PLAN.md §3):
      - validar que rating esté en {0.5, 1.0, ..., 5.0} (decisión 1);
      - fecha = timestamp convertido a datetime en UTC; anio_rating = año de esa fecha;
      - la columna timestamp puede quedarse o eliminarse (el contrato no la exige).

    Contrato: ESQUEMAS["ratings"].

    DUMMY: reemplaza las dos líneas de abajo por tu código sin cambiar la firma.
    """
    _dummies.aviso("ratings_limpias")
    return _dummies.tabla("ratings")


def datos_limpios() -> tuple:
    """Atajo para los notebooks 02 a 05: (movies, ratings) ya limpias.

    No es dummy: funciona igual en cuanto las funciones de arriba sean reales.
    """
    return movies_limpias(cargar_movies()), ratings_limpias(cargar_ratings())
