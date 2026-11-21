"""Perfil de preferencias usuario × género para la pregunta 2b. Responsable: D."""
import pandas as pd
import numpy as np
from . import contratos
from .contratos import GENEROS


def perfil_genero(ratings: pd.DataFrame, movies: pd.DataFrame, min_r: int = 5) -> pd.DataFrame:
    """Matriz con índice userId y una columna por género de contratos.GENEROS.

    Valor: proporción de los ratings del usuario en ese género que son >= 4.
    NaN si el usuario tiene menos de ``min_r`` ratings en ese género.
    Una película con varios géneros cuenta en cada uno de ellos.

    Contrato: contratos.verificar_matriz(df, "proporcion", GENEROS).

    DUMMY: reemplaza las líneas de abajo por tu código sin cambiar la firma.
    """
    #nos quedamos con los generos de la base
    columnas = list(GENEROS)
    #hacemos el merge para quedarnos solo con los userId y los generos por columnas
    tabla_union=pd.merge(ratings[["userId","rating","movieId"]],
                         movies[["movieId"] + columnas],
                         on="movieId",
                         how='left',
                         )
    tabla_union[columnas] = tabla_union[columnas].fillna(0)
    #Calcular matriz con ratings mayores o iguales a 4
    es_buen_rating = (tabla_union['rating'] >= 4).astype(int)
    objetivos = tabla_union[columnas].multiply(es_buen_rating, axis=0)
    objetivos['userId'] = tabla_union['userId']
    
    #Calcular proporción por género (éxitos / total vistos del género)
    total_por_genero = tabla_union.groupby('userId')[columnas].sum()
    exitos_por_genero = objetivos.groupby('userId')[columnas].sum()
    
    matrix_genero = (exitos_por_genero / total_por_genero).clip(lower=0.0, upper=1.0)
    
    #Pintar NaN en los géneros a usuarios bajo el mínimo de reseñas
    matrix_genero=matrix_genero.where(total_por_genero >= min_r, np.nan)
    matrix_genero.index.name = "userId"

    return matrix_genero.astype("float64")

