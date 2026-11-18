"""Tabla por película para la pregunta 1 y los fun facts. Responsable: B."""
import pandas as pd

from . import _dummies


def stats_peliculas(ratings: pd.DataFrame, movies: pd.DataFrame, min_n: int = 20) -> pd.DataFrame:
    """Una fila por película con al menos ``min_n`` ratings (decisión 6).

    Columnas: movieId, title, anio, n (número de ratings), media, mediana,
    std (desviación estándar muestral), ric (Q3 - Q1).

    Contrato: ESQUEMAS["stats_peliculas"].

    DUMMY: reemplaza las dos líneas de abajo por tu código sin cambiar la firma.
    """
    _dummies.aviso("stats_peliculas")
    return _dummies.stats_peliculas(min_n)
