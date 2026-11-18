"""Rutas del proyecto y funciones para guardar resultados. Responsable: E."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data" / "raw"
FIGURAS = RAIZ / "results" / "figures"
TABLAS = RAIZ / "results" / "tables"


def guardar_figura(fig, nombre: str) -> Path:
    """Guarda ``fig`` en results/figures/<nombre>.png. Prefijo sugerido: número de notebook ("02_hexbin")."""
    ruta = FIGURAS / f"{nombre}.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    return ruta


def guardar_tabla(df, nombre: str, index: bool = False) -> Path:
    """Guarda ``df`` en results/tables/<nombre>.csv (UTF-8)."""
    ruta = TABLAS / f"{nombre}.csv"
    df.to_csv(ruta, index=index, encoding="utf-8")
    return ruta
