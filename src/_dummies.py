"""Generador de datos inventados que respetan los contratos de ``contratos.py``.

Solo existe para que cada integrante pueda trabajar antes de que estén listas las
funciones de los demás. Cuando todas las funciones reales estén terminadas, ningún
módulo debe importar este archivo y se puede borrar.

Los valores son inventados: tienen la forma de los reales (tipos, rangos, algunos
casos especiales), pero no son consistentes entre tablas. Por ejemplo, ``n`` en
stats_peliculas no coincide con el conteo de ratings dummy. No saquen conclusiones
de ellos.
"""
import warnings
from functools import lru_cache

import numpy as np
import pandas as pd

from .contratos import GENEROS

SEMILLA = 2026
N_PELIS = 300
N_USUARIOS = 120
VALORES_RATING = np.arange(0.5, 5.01, 0.5)
PROB_RATING = np.array([1.4, 2.8, 1.8, 7.5, 5.5, 19.9, 13.0, 26.6, 8.5, 13.0]) / 100


def aviso(nombre: str) -> None:
    warnings.warn(
        f"{nombre}() es un DUMMY: devuelve datos inventados con el esquema del contrato.",
        stacklevel=3,
    )


def _sigmoide(x):
    return 1 / (1 + np.exp(-x))


@lru_cache(maxsize=None)
def _universo():
    rng = np.random.default_rng(SEMILLA)
    ids = np.sort(rng.choice(np.arange(1, 200_000), N_PELIS, replace=False)).astype(str)

    anio = pd.array(rng.integers(1920, 2019, N_PELIS), dtype="Int64")
    anio[[10, 20]] = pd.NA                      # títulos sin año
    generos = (rng.random((N_PELIS, len(GENEROS))) < 0.13).astype(int)
    generos[:3] = 0                             # películas sin género
    es_imax = (rng.random(N_PELIS) < 0.03).astype(int)

    titulos = [
        f"Película {i:03d}" + ("" if pd.isna(a) else f" ({a})") for i, a in enumerate(anio)
    ]
    titulos[41] = titulos[40]                   # título duplicado con otro movieId

    movies = pd.DataFrame({"movieId": ids, "title": titulos, "anio": anio})
    movies["n_generos"] = generos.sum(axis=1)
    movies["es_imax"] = es_imax
    movies[GENEROS] = generos

    texto_generos = [
        "|".join([g for g, v in zip(GENEROS, fila) if v] + (["IMAX"] if imax else []))
        or "(no genres listed)"
        for fila, imax in zip(generos, es_imax)
    ]
    titulos_raw = [t + " " if i % 37 == 0 else t for i, t in enumerate(titulos)]
    movies_raw = pd.DataFrame({"movieId": ids, "title": titulos_raw, "genres": texto_generos})

    # Ratings: popularidad muy asimétrica, como en los datos reales.
    popularidad = rng.lognormal(0, 1.2, N_PELIS)
    popularidad /= popularidad.sum()
    filas = []
    inicio, fin = pd.Timestamp("1996-03-29").timestamp(), pd.Timestamp("2018-09-24").timestamp()
    for u in range(1, N_USUARIOS + 1):
        k = int(rng.integers(20, 120))
        vistas = rng.choice(ids, k, replace=False, p=popularidad)
        filas.append(pd.DataFrame({
            "userId": str(u),
            "movieId": vistas,
            "rating": rng.choice(VALORES_RATING, k, p=PROB_RATING),
            "timestamp": rng.integers(int(inicio), int(fin), k),
        }))
    ratings_raw = pd.concat(filas, ignore_index=True)

    ratings = ratings_raw.copy()
    ratings["fecha"] = pd.to_datetime(ratings["timestamp"], unit="s", utc=True)
    ratings["anio_rating"] = ratings["fecha"].dt.year.astype(int)
    ratings = ratings.drop(columns="timestamp")

    return {"movies_raw": movies_raw, "ratings_raw": ratings_raw,
            "movies": movies, "ratings": ratings}


def tabla(nombre: str) -> pd.DataFrame:
    return _universo()[nombre].copy()


def stats_peliculas(min_n: int) -> pd.DataFrame:
    rng = np.random.default_rng(SEMILLA + 1)
    movies = tabla("movies")
    media = np.clip(rng.normal(3.4, 0.5, N_PELIS), 0.5, 5.0)
    std = rng.uniform(0.4, 1.4, N_PELIS)
    return pd.DataFrame({
        "movieId": movies["movieId"],
        "title": movies["title"],
        "anio": movies["anio"],
        "n": (min_n + rng.geometric(0.03, N_PELIS)).astype(int),
        "media": media,
        "mediana": np.clip(np.round((media + rng.normal(0, 0.2, N_PELIS)) * 2) / 2, 0.5, 5.0),
        "std": std,
        "ric": np.round(std * 1.35 * 2) / 2,
    })


def matriz_usuario(columnas, proporcion: bool, prob_nan: float) -> pd.DataFrame:
    """Matriz usuario × columnas con algo de estructura (gustos latentes) para que
    las correlaciones y los heatmaps no salgan planos."""
    rng = np.random.default_rng(SEMILLA + 2)
    gusto_u = rng.normal(0, 1, (N_USUARIOS, 2))
    perfil_c = rng.normal(0, 1, (2, len(columnas)))
    p = _sigmoide(gusto_u @ perfil_c + 0.3)
    valores = p if proporcion else (rng.random(p.shape) < p).astype(float)
    valores[rng.random(p.shape) < prob_nan] = np.nan
    indice = pd.Index([str(u) for u in range(1, N_USUARIOS + 1)], name="userId")
    return pd.DataFrame(valores, index=indice, columns=list(columnas))
