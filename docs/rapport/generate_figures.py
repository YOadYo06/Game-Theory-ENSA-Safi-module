# -*- coding: utf-8 -*-
"""
generate_figures.py — figures du rapport (Rôle : Chef de projet / Théorie, appui Quant).

Produit, à partir de `src.experiences` :
  - exp_jeux.csv            : 20 jeux aléatoires x tailles 2,3,4 ;
  - fig_exp_jeux.png        : nb d'équilibres et temps de calcul vs taille.

Usage (depuis la racine du dépôt) : python docs/rapport/generate_figures.py
"""
from __future__ import annotations

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from src.experiences import protocole_jeux_aleatoires  # noqa: E402

ICI = Path(__file__).resolve().parent


def main() -> None:
    df = protocole_jeux_aleatoires(tailles=(2, 3, 4), n_jeux=20, seed=0)
    df.to_csv(ICI / "exp_jeux.csv", index=False, encoding="utf-8")

    stats = df.groupby("taille").agg(
        n_eq_moy=("n_equilibres", "mean"),
        n_eq_max=("n_equilibres", "max"),
        temps_moy_ms=("temps_s", lambda s: 1000 * s.mean()),
        temps_max_ms=("temps_s", lambda s: 1000 * s.max()),
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.bar(stats.index.astype(str), stats["n_eq_moy"], color="#4472c4", label="moyenne")
    ax1.plot(stats.index.astype(str), stats["n_eq_max"], "o--", color="#c00000", label="maximum")
    ax1.set_xlabel("taille du jeu (m = n)")
    ax1.set_ylabel("nombre d'équilibres de Nash")
    ax1.set_title("Nombre d'équilibres (20 jeux par taille)")
    ax1.legend()

    ax2.bar(stats.index.astype(str), stats["temps_moy_ms"], color="#70ad47", label="moyenne")
    ax2.plot(stats.index.astype(str), stats["temps_max_ms"], "o--", color="#c00000", label="maximum")
    ax2.set_xlabel("taille du jeu (m = n)")
    ax2.set_ylabel("temps de calcul (ms)")
    ax2.set_title("Temps d'énumération des supports")
    ax2.legend()

    fig.tight_layout()
    fig.savefig(ICI / "fig_exp_jeux.png", dpi=150)
    print(stats.round(3).to_string())
    print("figures écrites dans", ICI)


if __name__ == "__main__":
    main()
