"""Tabla por película para la pregunta 1 y los fun facts. Responsable: B."""
import pandas as pd


def stats_peliculas(ratings: pd.DataFrame, movies: pd.DataFrame, min_n: int = 20) -> pd.DataFrame:
    """Una fila por película con al menos ``min_n`` ratings (decisión 6).

    Columnas: movieId, title, anio, n (número de ratings), media, mediana,
    std (desviación estándar muestral), ric (Q3 - Q1).

    Contrato: ESQUEMAS["stats_peliculas"].
    """
    # 1. Resumen por película a partir de los ratings.
    #    std usa ddof=1 (muestral), que es el valor por defecto de pandas.
    por_pelicula = ratings.groupby("movieId")["rating"].agg(
        n="count",
        media="mean",
        mediana="median",
        std="std",
        q1=lambda s: s.quantile(0.25),
        q3=lambda s: s.quantile(0.75),
    )
    por_pelicula["ric"] = por_pelicula["q3"] - por_pelicula["q1"]

    # 2. Umbral mínimo de ratings (decisión 6): con n chico la std es puro ruido.
    por_pelicula = por_pelicula[por_pelicula["n"] >= min_n]

    # 3. Pegar título y año de estreno desde movies (movieId es la llave).
    tabla = por_pelicula.reset_index().merge(
        movies[["movieId", "title", "anio"]], on="movieId", how="left", validate="one_to_one"
    )

    # 4. Columnas en el orden del contrato; las más populares primero.
    tabla = tabla[["movieId", "title", "anio", "n", "media", "mediana", "std", "ric"]]
    tabla["n"] = tabla["n"].astype(int)
    return tabla.sort_values("n", ascending=False).reset_index(drop=True)