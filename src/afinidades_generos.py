"""Perfil de preferencias usuario × género para la pregunta 2b. Responsable: D."""
import pandas as pd

from . import _dummies
from .contratos import GENEROS


def perfil_genero(ratings: pd.DataFrame, movies: pd.DataFrame, min_r: int = 5) -> pd.DataFrame:
    """Matriz con índice userId y una columna por género de contratos.GENEROS.

    Valor: proporción de los ratings del usuario en ese género que son >= 4.
    NaN si el usuario tiene menos de ``min_r`` ratings en ese género.
    Una película con varios géneros cuenta en cada uno de ellos.

    Contrato: contratos.verificar_matriz(df, "proporcion", GENEROS).

    DUMMY: reemplaza las líneas de abajo por tu código sin cambiar la firma.
    """
    _dummies.aviso("perfil_genero")
    return _dummies.matriz_usuario(GENEROS, proporcion=True, prob_nan=0.2)
