"""Rutas del proyecto y funciones para guardar resultados. Responsable: E."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data" / "raw"
FIGURAS = RAIZ / "results" / "figures"
TABLAS = RAIZ / "results" / "tables"


def guardar_figura(fig, nombre: str) -> Path:
    """Guarda la figura en results/figures/<nombre>.png. Prefijo sugerido: número de notebook ("02_hexbin").

    ``fig`` puede ser:
      - una Figure de matplotlib (``fig, ax = plt.subplots()``);
      - un Axes, que es lo que devuelven las funciones de seaborn a nivel de ejes
        (``sns.heatmap``, ``sns.boxplot``, ``sns.histplot``, ...);
      - un FacetGrid/JointGrid, que es lo que devuelven las funciones de seaborn a nivel
        de figura (``sns.relplot``, ``sns.catplot``, ``sns.displot``, ``sns.jointplot``).
    """
    if not hasattr(fig, "savefig"):  # un Axes no tiene savefig; su figura sí
        fig = fig.figure
    ruta = FIGURAS / f"{nombre}.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    return ruta


def guardar_tabla(df, nombre: str, index: bool = False) -> Path:
    """Guarda ``df`` en results/tables/<nombre>.csv (UTF-8)."""
    ruta = TABLAS / f"{nombre}.csv"
    df.to_csv(ruta, index=index, encoding="utf-8")
    return ruta
