# -*- coding: utf-8 -*-
"""
generate_gantt.py — dessine le Gantt prévisionnel (ou réalisé) depuis gantt_source.csv.

Usage :
    python docs/gantt/generate_gantt.py

Sortie : docs/gantt/gantt_previsionnel.png

Le CSV doit contenir les colonnes :
    Phase, Tache, Responsable, Debut, Fin, Duree_j, Statut
Statut attendu : Fait / En cours / Retard / A faire.
"""
from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ICI = Path(__file__).resolve().parent
SOURCE = ICI / "gantt_source.csv"
SORTIE = ICI / "gantt_previsionnel.png"
COULEURS = {
    "Fait": "#2e7d32",
    "En cours": "#1565c0",
    "Retard": "#c62828",
    "A faire": "#9e9e9e",
}


def _parse(jour: str) -> date:
    return datetime.strptime(jour.strip(), "%Y-%m-%d").date()


def charger(chemin: Path):
    with chemin.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main(source: Path = SOURCE, sortie: Path = SORTIE,
         titre: str = "Gantt prévisionnel — Projet 1 (Nash m×n, Cournot, Bertrand) — Groupe 1") -> None:
    lignes = charger(source)
    # Une ligne par tâche, dans l'ordre du fichier (du bas vers le haut).
    taches = list(reversed(lignes))
    y = range(len(taches))

    fig, ax = plt.subplots(figsize=(13, 8))
    for i, t in enumerate(taches):
        debut = _parse(t["Debut"])
        fin = _parse(t["Fin"])
        duree = max((fin - debut).days + 1, 1)
        couleur = COULEURS.get(t["Statut"].strip(), "#607d8b")
        ax.barh(i, duree, left=mdates.date2num(debut), height=0.55,
                color=couleur, alpha=0.9, edgecolor="white")
        ax.text(mdates.date2num(debut) + 0.2, i,
                f" {t['Responsable']}", va="center", ha="left",
                fontsize=8, color="white", fontweight="bold")

    ax.set_yticks(list(y))
    ax.set_yticklabels([f"{t['Phase']} | {t['Tache']}" for t in taches], fontsize=8)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    ax.set_title(titre, fontsize=13, fontweight="bold")
    ax.set_xlabel("Semaines (S1 → S7)")

    poignees = [plt.Rectangle((0, 0), 1, 1, color=c) for c in COULEURS.values()]
    ax.legend(poignees, list(COULEURS.keys()), loc="lower right", fontsize=8, title="Statut")

    fig.tight_layout()
    fig.savefig(sortie, dpi=150)
    print(f"Gantt écrit : {sortie}")


if __name__ == "__main__":
    import sys

    if "--realise" in sys.argv:
        main(ICI / "gantt_realise.csv", ICI / "gantt_realise.png",
             "Gantt réalisé — Projet 1 — Groupe 1 (état au 11/11/2026)")
    else:
        main()
