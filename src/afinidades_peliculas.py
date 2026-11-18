"""Matriz de gustos usuario × película para la pregunta 2a. Responsable: C."""
import pandas as pd

from . import _dummies


def matriz_gustos(ratings: pd.DataFrame, min_n: int = 100) -> pd.DataFrame:
    """Matriz con índice userId y una columna por movieId (solo películas con al menos ``min_n`` ratings).

    Valores: 1.0 si rating >= 4, 0.0 si rating < 4, NaN si el usuario no la calificó.
    Un NaN NO es un "no le gustó" (PLAN.md §4, pregunta 2a).

    Contrato: contratos.verificar_matriz(df, "gusto").

    DUMMY: reemplaza las líneas de abajo por tu código sin cambiar la firma.
    """
    _dummies.aviso("matriz_gustos")
    columnas = _dummies.tabla("movies")["movieId"].head(40)
    return _dummies.matriz_usuario(columnas, proporcion=False, prob_nan=0.3)
