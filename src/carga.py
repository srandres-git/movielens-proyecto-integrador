"""Lectura de los CSV con sus tipos. Responsable: A.

Decisión 1 (PLAN.md §3): userId y movieId se leen como str desde read_csv, así
nunca aparece la forma 'x.0'. rating se lee como float y timestamp como entero.
"""
import pandas as pd
from .rutas import DATOS


def cargar_movies(ruta=DATOS / "movies.csv") -> pd.DataFrame:
    """Lee movies.csv sin transformar el contenido.

    Contrato: ESQUEMAS["movies_raw"] → movieId (texto), title (texto), genres (texto).
    """
    df = pd.read_csv(ruta, dtype={
        'movieId':str,
        'title':str,
        'genres':str,
    })
    return df


def cargar_ratings(ruta=DATOS / "ratings.csv") -> pd.DataFrame:
    """Lee ratings.csv sin transformar el contenido.

    Contrato: ESQUEMAS["ratings_raw"] → userId (texto), movieId (texto),
    rating (real), timestamp (entero, segundos desde 1970-01-01 UTC).
    """
    df = pd.read_csv(ruta, dtype={
        'userId':str,
        'movieId':str,
        'rating':float,
        'timestamp':int
    })
    return df