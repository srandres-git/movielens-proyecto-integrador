"""Contratos de datos: el único lugar donde se definen las columnas de cada tabla.

Cada notebook llama a ``verificar_esquema`` (o ``verificar_matriz``) al recibir una
tabla. Si una función real no respeta su contrato, el error aparece de inmediato.

Para cambiar un contrato: avisar primero al equipo y modificarlo aquí, una sola vez.
"""
import pandas as pd
from pandas.api import types as pdt

# 18 géneros finales: los 19 del archivo sin IMAX (formato, decisión 4) y sin
# "(no genres listed)" (decisión 3).
GENEROS = [
    "Action", "Adventure", "Animation", "Children", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
    "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western",
]

# Tipos lógicos admitidos: texto, entero, real, fecha, binaria (entero con valores 0/1).
ESQUEMAS = {
    "movies_raw": {"movieId": "texto", "title": "texto", "genres": "texto"},
    "ratings_raw": {"userId": "texto", "movieId": "texto", "rating": "real", "timestamp": "entero"},
    "movies": {
        "movieId": "texto", "title": "texto", "anio": "entero", "n_generos": "entero",
        "es_imax": "binaria", **{g: "binaria" for g in GENEROS},
    },
    "ratings": {
        "userId": "texto", "movieId": "texto", "rating": "real",
        "fecha": "fecha", "anio_rating": "entero",
    },
    "stats_peliculas": {
        "movieId": "texto", "title": "texto", "anio": "entero", "n": "entero",
        "media": "real", "mediana": "real", "std": "real", "ric": "real",
    },
}

_CHEQUEOS = {
    "texto": pdt.is_string_dtype,
    "entero": pdt.is_integer_dtype,
    "real": pdt.is_float_dtype,
    "fecha": pdt.is_datetime64_any_dtype,
    "binaria": lambda s: pdt.is_integer_dtype(s) and s.dropna().isin([0, 1]).all(),
}


def verificar_esquema(df: pd.DataFrame, nombre: str) -> None:
    """Lanza ValueError si a ``df`` le faltan columnas de ``ESQUEMAS[nombre]`` o tienen otro tipo.

    Las columnas extra están permitidas.
    """
    esquema = ESQUEMAS[nombre]
    faltantes = [c for c in esquema if c not in df.columns]
    tipos_malos = [
        f"{c} (esperado {t}, recibido {df[c].dtype})"
        for c, t in esquema.items()
        if c in df.columns and not _CHEQUEOS[t](df[c])
    ]
    if faltantes or tipos_malos:
        raise ValueError(
            f"'{nombre}' no cumple el contrato. Faltan: {faltantes or 'ninguna'}. "
            f"Tipos incorrectos: {tipos_malos or 'ninguno'}."
        )


def verificar_matriz(df: pd.DataFrame, valores: str, columnas=None) -> None:
    """Verifica una matriz usuario × (película o género).

    valores: "gusto" (solo 1, 0 o NaN) o "proporcion" (números en [0, 1] o NaN).
    columnas: si se da, las columnas de ``df`` deben estar contenidas en ella.
    """
    problemas = []
    if df.index.name != "userId":
        problemas.append(f"el índice debe llamarse 'userId' (es {df.index.name!r})")
    datos = df.stack().dropna()  # stack() descarta los NaN
    if valores == "gusto" and not datos.isin([0, 1]).all():
        problemas.append("hay valores distintos de 1, 0 o NaN")
    if valores == "proporcion" and not datos.between(0, 1).all():
        datos = pd.Series(df.to_numpy().ravel()).dropna()
        problemas.append("hay valores fuera de [0, 1]")
    if columnas is not None and not set(df.columns) <= set(columnas):
        problemas.append(f"columnas inesperadas: {sorted(set(df.columns) - set(columnas))}")
    if problemas:
        raise ValueError("La matriz no cumple el contrato: " + "; ".join(problemas))
