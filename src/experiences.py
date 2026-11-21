# -*- coding: utf-8 -*-
"""
experiences.py — protocoles d'expérience du Projet 1.

Rôle associé : Testeur / Expérimentateur (S1–S4), puis rotation.
Toutes les expériences fixent une graine (reproductibilité) et plafonnent leurs
paramètres coûteux (nombre de jeux, taille maximale).

Fonctions fournies (extraits opérationnels) :
  - jeu_aleatoire(m, n, seed)            : un jeu m x n à graine fixée ;
  - protocole_jeux_aleatoires(...)       : 20 jeux, nb d'équilibres + temps de calcul ;
  - meilleure_reponse_cournot(...)       : itération des meilleures réponses (contraction 1/2).
Protocole « 5 énoncés x 2 modèles Ollama » : `protocole_agent_ollama` (nécessite Ollama).

Usage : `python -m src.experiences`  (import relatif : ne pas lancer `python src/experiences.py`).
"""
from __future__ import annotations

import time
from typing import Iterable, Tuple

import numpy as np

try:  # pandas est optionnel pour l'import du module
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None  # type: ignore

from .jeux import enumeration_supports


def jeu_aleatoire(m: int, n: int, seed: int | None = None,
                  lo: float = -1.0, hi: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
    """Renvoie un couple de matrices (A, B) de taille m x n, à graine fixée."""
    rng = np.random.default_rng(seed)
    A = rng.uniform(lo, hi, size=(m, n))
    B = rng.uniform(lo, hi, size=(m, n))
    return A, B


def protocole_jeux_aleatoires(tailles: Iterable[int] = (2, 3, 4),
                              n_jeux: int = 20, seed: int = 0):
    """20 jeux aléatoires par taille : nombre d'équilibres trouvés et temps de calcul.

    Le nombre de supports testés est exponentiel : on observe donc un temps de
    calcul qui croît (rapidement) avec la taille. Retourne un DataFrame
    (colonnes : taille, jeu, n_equilibres, temps_s) si pandas est disponible.
    """
    lignes = []
    for taille in tailles:
        for j in range(n_jeux):
            A, B = jeu_aleatoire(taille, taille, seed=1000 * taille + j)
            t0 = time.perf_counter()
            eqs = enumeration_supports(A, B)
            dt = time.perf_counter() - t0
            lignes.append({"taille": taille, "jeu": j,
                           "n_equilibres": len(eqs), "temps_s": dt})
    if pd is not None:
        return pd.DataFrame(lignes)
    return lignes


def meilleure_reponse_cournot(a: float, b: float, c: float,
                              iterations: int = 50) -> np.ndarray:
    """Itération des meilleures réponses de deux firmes (facteur de contraction 1/2).

    q_{t+1} = (a - c - b q_t) / (2b) pour chaque firme ; converge vers
    q* = (a - c) / (3b) pour n = 2.
    """
    q = np.array([0.0, (a - c) / b])  # départ asymétrique
    for _ in range(iterations):
        q = (a - c - b * q[::-1]) / (2 * b)
    return q


# ---------------------------------------------------------------------------
# Protocole agent : 5 énoncés x 2 modèles Ollama (S5)
# ---------------------------------------------------------------------------
ENONCES_AGENT = [
    # 1. Cournot numérique -> doit appeler `cournot`
    "Dans un duopole de Cournot avec a = 100, b = 1 et c = 10, quelles sont les "
    "quantités, le prix et les profits à l'équilibre ?",
    # 2. Bimatrice 2x2 -> doit appeler `resoudre_bimatrice`
    "Donne les équilibres de Nash du jeu A = [[3, 0], [5, 1]] et B = [[3, 5], [0, 1]].",
    # 3. Bimatrice 3x3 -> doit appeler `resoudre_bimatrice`
    "Trouve les équilibres de Nash du jeu A = [[0, 1, 2], [3, 2, 1], [1, 1, 1]] et "
    "B = [[2, 0, 1], [1, 3, 0], [0, 1, 2]].",
    # 4. Question conceptuelle -> NE doit PAS appeler d'outil
    "Explique en deux phrases ce qu'est un équilibre de Nash en stratégies mixtes.",
    # 5. Énoncé piège : valeurs en pourcentages -> doit convertir puis appeler un outil
    "Deux firmes ont une demande inverse P = 100 - Q et un coût marginal de 20% de "
    "l'ordonnée à l'origine. Quel est l'équilibre de Cournot ?",
]


def protocole_agent_ollama(enonces: list[str] | None = None,
                           modeles: Iterable[str] = ("llama3.1", "llama3.2:3b"),
                           n_repetitions: int = 1):
    """5 énoncés x 2 modèles Ollama : fréquence d'appel de l'outil et arguments corrects.

    Pour chaque couple (modèle, énoncé) on relève :
      - ``outils``     : liste des outils appelés (ex. ["cournot"]) ;
      - ``appel_outil``: True si au moins un outil a été appelé ;
      - ``a_choix``    : True si la réponse contient la ligne « CHOIX : » (le guide
                         demande de compter les sorties SANS « CHOIX : », signe que
                         le modèle n'explicite pas sa décision) ;
      - ``duree_s``    : temps de réponse.

    Nécessite `ollama serve`. Retourne un DataFrame (ou une liste) de lignes.
    """
    from .agent_demo_ollama import poser_question

    enonces = list(enonces or ENONCES_AGENT)
    lignes = []
    for modele in modeles:
        for i, enonce in enumerate(enonces, 1):
            for rep in range(n_repetitions):
                t0 = time.perf_counter()
                res = poser_question(enonce, model=modele, verbose=False)
                dt = time.perf_counter() - t0
                outils = [a["nom"] for a in res["appels"]]
                lignes.append({
                    "modele": modele,
                    "enonce": i,
                    "repetition": rep + 1,
                    "outils": outils,
                    "appel_outil": bool(outils),
                    "a_choix": "CHOIX" in (res["reponse"] or "").upper(),
                    "duree_s": dt,
                })
    if pd is not None:
        return pd.DataFrame(lignes)
    return lignes


if __name__ == "__main__":
    df = protocole_jeux_aleatoires(tailles=(2, 3, 4), n_jeux=20, seed=0)
    print(df if pd is not None else df)
