"""Matriz de gustos usuario × película para la pregunta 2a. Responsable: C."""
import pandas as pd

def matriz_gustos(ratings: pd.DataFrame, min_n: int = 100) -> pd.DataFrame:
    """Matriz con índice userId y una columna por movieId (solo películas con al menos ``min_n`` ratings).

    Valores: 1.0 si rating >= 4, 0.0 si rating < 4, NaN si el usuario no la calificó.
    Un NaN NO es un "no le gustó" (PLAN.md §4, pregunta 2a).

    Contrato: contratos.verificar_matriz(df, "gusto").
    """

    # 1. Contar reseñas por película
    conteo_resenas = ratings.groupby("movieId")["rating"].count()

    # 2. Identificar películas con suficientes reseñas
    peliculas_validas = conteo_resenas[conteo_resenas >= min_n]
    ids_peliculas_validas = peliculas_validas.index

    # 3. Filtrar las reseñas
    ratings_filtrados = ratings[
        ratings["movieId"].isin(ids_peliculas_validas)
    ].copy()

    # 4. Convertir calificaciones en gustos
    ratings_filtrados["gusto"] = (
        ratings_filtrados["rating"] >= 4
    ).astype(float)

    # 5. Construir matriz usuario × película
    matriz = ratings_filtrados.pivot(
        index="userId",
        columns="movieId",
        values="gusto"
    )

    return matriz
