"""Lectura de los CSV con sus tipos. Responsable: A.

Decisión 1 (PLAN.md §3): userId y movieId se leen como str desde read_csv, así
nunca aparece la forma 'x.0'. rating se lee como float y timestamp como entero.
"""
import pandas as pd

from . import _dummies
from .rutas import DATOS


def cargar_movies(ruta=DATOS / "movies.csv") -> pd.DataFrame:
    """Lee movies.csv sin transformar el contenido.

    Contrato: ESQUEMAS["movies_raw"] → movieId (texto), title (texto), genres (texto).

    DUMMY: reemplaza las dos líneas de abajo por tu código sin cambiar la firma.
    """
    _dummies.aviso("cargar_movies")
    return _dummies.tabla("movies_raw")


def cargar_ratings(ruta=DATOS / "ratings.csv") -> pd.DataFrame:
    """Lee ratings.csv sin transformar el contenido.

    Contrato: ESQUEMAS["ratings_raw"] → userId (texto), movieId (texto),
    rating (real), timestamp (entero, segundos desde 1970-01-01 UTC).

    DUMMY: reemplaza las dos líneas de abajo por tu código sin cambiar la firma.
    """
    _dummies.aviso("cargar_ratings")
    return _dummies.tabla("ratings_raw")
