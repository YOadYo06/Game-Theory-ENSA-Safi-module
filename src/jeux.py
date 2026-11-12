# -*- coding: utf-8 -*-
"""
jeux.py — Projet 1 : solveur de Nash m x n et duopoles (Cournot, Bertrand).

Fonctions pures (sans LangChain).

Groupe 1 : ACHTOUK Fatine, ADIL Youness, BELHIMER Ikram, BOULHAIL Hiba.
Module  : Théorie des Jeux et Systèmes Multi-Agents (ENSA Safi).

Conventions (accord inter-groupes, cf. guide — « Dépendances entre projets ») :
  - A : matrice de gains du joueur 1 (lignes), taille m x n.
  - B : matrice de gains du joueur 2 (colonnes), taille m x n.
  - Les indices commencent à 0.
  - x : stratégie mixte du joueur 1 (simplexe de taille m).
  - y : stratégie mixte du joueur 2 (simplexe de taille n).

Rappel théorique (voir docs/fiche_lecture.tex) :
  (x, y) est un équilibre de Nash ssi aucune déviation pure n'est profitable :
      (A y)_i <= x^T A y   pour tout i,
      (x^T B)_j <= x^T B y  pour tout j.
  L'énumération des supports cherche, pour chaque couple de supports (I, J) de même
  taille k, une solution du système d'indifférence, puis vérifie la non-déviation.
"""
from __future__ import annotations

import itertools
from typing import List, Optional, Sequence, Tuple

import numpy as np

# Un équilibre est représenté par un couple de vecteurs (x, y).
Equilibre = Tuple[np.ndarray, np.ndarray]


# ---------------------------------------------------------------------------
# 1. Vérification d'équilibre
# ---------------------------------------------------------------------------
def est_nash(A, B, x, y, tol: float = 1e-9) -> bool:
    """Vérifie les deux conditions de non-déviation d'un profil (x, y).

    Un profil mixte (x, y) est un équilibre de Nash ssi aucune stratégie *pure*
    ne fait mieux que la stratégie mixte jouée :
        (A y)_i <= x^T A y   pour tout i (joueur 1),
        (x^T B)_j <= x^T B y  pour tout j (joueur 2).

    Paramètres
    ----------
    A, B : array-like, m x n
        Gains du joueur 1 (lignes) et du joueur 2 (colonnes).
    x, y : array-like
        Stratégies mixtes (vecteurs sur le simplexe).
    tol : float
        Tolérance de comparaison (jamais d'égalité de flottants exacte).

    Retour
    ------
    bool
    """
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    gains_j1 = A @ y          # (A y)_i : gain pur du joueur 1 face à y
    gains_j2 = x @ B          # (x^T B)_j : gain pur du joueur 2 face à x
    v1 = float(x @ gains_j1)  # x^T A y : gain espéré du joueur 1
    v2 = float(gains_j2 @ y)  # x^T B y : gain espéré du joueur 2

    return bool(np.all(gains_j1 <= v1 + tol) and np.all(gains_j2 <= v2 + tol))


def equilibres_nash_purs(A, B, tol: float = 1e-9) -> List[Tuple[int, int]]:
    """Équilibres de Nash en stratégies pures, sous forme de couples d'indices.

    (i, j) est un équilibre pur ssi A[i, j] est maximal dans la colonne j
    (meilleure réponse du joueur 1) et B[i, j] est maximal dans la ligne i
    (meilleure réponse du joueur 2).
    """
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    m, n = A.shape
    equilibres: List[Tuple[int, int]] = []
    for i in range(m):
        for j in range(n):
            if A[i, j] >= A[:, j].max() - tol and B[i, j] >= B[i, :].max() - tol:
                equilibres.append((i, j))
    return equilibres


# ---------------------------------------------------------------------------
# 2. Énumération des supports
# ---------------------------------------------------------------------------
def _resoudre_support(
    A: np.ndarray,
    B: np.ndarray,
    I: Sequence[int],
    J: Sequence[int],
    tol: float,
) -> Optional[Equilibre]:
    """Résout le système d'indifférence pour un couple de supports (I, J).

    Sur le support I (resp. J), le joueur 1 (resp. 2) doit être indifférent entre
    toutes ses stratégies du support :
        (A y)_i = v1   pour i dans I,   sum_{j dans J} y_j = 1,
        (x^T B)_j = v2 pour j dans J,   sum_{i dans I} x_i = 1.
    Renvoie (x, y) si la solution est sur le simplexe, sinon None.
    """
    k = len(I)
    if k == 0:
        return None

    # --- Joueur 2 : inconnues (y_j)_{j dans J} et v1 ---
    M = np.zeros((k + 1, k + 1))
    rhs = np.zeros(k + 1)
    for r, i in enumerate(I):
        for c, j in enumerate(J):
            M[r, c] = A[i, j]
        M[r, k] = -1.0
    M[k, :k] = 1.0
    rhs[k] = 1.0
    sol_y = np.linalg.lstsq(M, rhs, rcond=None)[0]
    if np.linalg.norm(M @ sol_y - rhs) > 1e-6:  # système incompatible / dégénéré
        return None
    y_J = sol_y[:k]

    # --- Joueur 1 : inconnues (x_i)_{i dans I} et v2 ---
    N = np.zeros((k + 1, k + 1))
    rhs2 = np.zeros(k + 1)
    for c, j in enumerate(J):
        for r, i in enumerate(I):
            N[c, r] = B[i, j]
        N[c, k] = -1.0
    N[k, :k] = 1.0
    rhs2[k] = 1.0
    sol_x = np.linalg.lstsq(N, rhs2, rcond=None)[0]
    if np.linalg.norm(N @ sol_x - rhs2) > 1e-6:
        return None
    x_I = sol_x[:k]

    # Composante négative -> hors du simplexe (support trop grand).
    if np.any(x_I < -tol) or np.any(y_J < -tol):
        return None

    x = np.zeros(A.shape[0])
    y = np.zeros(A.shape[1])
    x[list(I)] = np.clip(x_I, 0.0, None)
    y[list(J)] = np.clip(y_J, 0.0, None)
    if x.sum() > 0:
        x = x / x.sum()
    if y.sum() > 0:
        y = y / y.sum()
    return x, y


def _deja_present(equilibres: List[Equilibre], x, y, tol: float) -> bool:
    """Évite d'ajouter deux fois le même équilibre (comparaison avec tolérance)."""
    for px, py in equilibres:
        if np.allclose(px, x, atol=1e-6) and np.allclose(py, y, atol=1e-6):
            return True
    return False


def enumeration_supports(A, B, tol: float = 1e-9) -> List[Equilibre]:
    """Liste des équilibres de Nash (x, y), purs et mixtes, d'un jeu m x n.

    Algorithme (cf. guide, Projet 1) :
      pour k = 1 .. min(m, n) :
        pour chaque support I de lignes (|I| = k) :
          pour chaque support J de colonnes (|J| = k) :
            résoudre le système d'indifférence sur (I, J) ;
            ne garder que les solutions sur le simplexe
            qui vérifient la non-déviation (est_nash).

    Hypothèse : jeu non dégénéré (sinon des équilibres à supports de tailles
    différentes peuvent apparaître et le système devient sous-déterminé).

    Retour
    ------
    list[tuple[np.ndarray, np.ndarray]]
        Chaque équilibre est un couple (x, y) de vecteurs de probabilités.
    """
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    if A.shape != B.shape:
        raise ValueError("A et B doivent avoir la même taille (m x n).")
    m, n = A.shape

    equilibres: List[Equilibre] = []
    for k in range(1, min(m, n) + 1):
        for I in itertools.combinations(range(m), k):
            for J in itertools.combinations(range(n), k):
                sol = _resoudre_support(A, B, I, J, tol)
                if sol is None:
                    continue
                x, y = sol
                if not est_nash(A, B, x, y, tol):
                    continue
                if not _deja_present(equilibres, x, y, tol):
                    equilibres.append((x, y))
    return equilibres


# ---------------------------------------------------------------------------
# 3. Duopoles : Cournot et Bertrand
# ---------------------------------------------------------------------------
def cournot(a: float, b: float, c: float, n: int = 2) -> dict:
    """Cournot symétrique : formules fermées + comparaison avec le cartel.

    Demande inverse P(Q) = a - b Q, coût marginal constant c (a > c).

    Résultats utilisés (cf. guide) :
      q*        = (a - c) / ((n + 1) b)
      Q*        = n q*,   P* = a - b Q*,   profit = (a - c)^2 / (b (n + 1)^2)
      Cartel    : Q = (a - c) / (2b), profit total (a - c)^2 / (4b)
    """
    if b <= 0:
        raise ValueError("On suppose b > 0.")
    if not a > c:
        raise ValueError("On suppose a > c.")

    q = (a - c) / ((n + 1) * b)
    Q = n * q
    P = a - b * Q
    profit = (a - c) ** 2 / (b * (n + 1) ** 2)

    Q_cartel = (a - c) / (2 * b)
    q_cartel = Q_cartel / n
    P_cartel = a - b * Q_cartel
    profit_cartel_total = (a - c) ** 2 / (4 * b)
    profit_cartel = profit_cartel_total / n

    return {
        "n": int(n),
        "quantite_par_firme": float(q),
        "quantite_totale": float(Q),
        "prix": float(P),
        "profit_par_firme": float(profit),
        "cartel": {
            "quantite_par_firme": float(q_cartel),
            "quantite_totale": float(Q_cartel),
            "prix": float(P_cartel),
            "profit_par_firme": float(profit_cartel),
            "profit_total": float(profit_cartel_total),
        },
    }


def cournot_grille(a: float, b: float, c: float, qmax: float, pas: float = 1.0) -> List[Tuple[float, float]]:
    """Cournot approché par une grille entière de quantités.

    Construit les matrices de gains sur {0, pas, 2 pas, ..., qmax} puis renvoie
    les équilibres de Nash purs (meilleures réponses mutuelles). Sert à vérifier
    que q* de la formule fermée est retrouvé sur la grille.

    Retour
    ------
    list[tuple[float, float]] : couples de quantités (q1, q2) en équilibre.
    """
    quantites = np.arange(0.0, qmax + pas, pas, dtype=float)
    taille = len(quantites)
    A = np.zeros((taille, taille))
    B = np.zeros((taille, taille))
    for i, qi in enumerate(quantites):
        for j, qj in enumerate(quantites):
            prix = max(a - b * (qi + qj), 0.0)
            A[i, j] = (prix - c) * qi   # profit de la firme 1
            B[i, j] = (prix - c) * qj   # profit de la firme 2
    return [(float(quantites[i]), float(quantites[j])) for (i, j) in equilibres_nash_purs(A, B)]


def bertrand(a: float, b: float, c: float) -> dict:
    """Duopole de Bertrand (biens homogènes, coûts marginaux égaux c).

    Paradoxe de Bertrand : l'unique équilibre est p1 = p2 = c, profit nul.
    On renvoie aussi la référence de monopole pour comparaison.
    """
    return {
        "prix_equilibre": float(c),
        "profit_par_firme": 0.0,
        "prix_monopole": (a + c) / 2.0,
        "profit_monopole": (a - c) ** 2 / (4 * b),
    }


# ---------------------------------------------------------------------------
# 4. Jeux de référence du cours (utilisés par les tests et les notebooks)
# ---------------------------------------------------------------------------
# Dilemme du prisonnier : lignes/colonnes = [Coopérer, Trahir]
DILEMME_A = np.array([[3.0, 0.0], [5.0, 1.0]])
DILEMME_B = np.array([[3.0, 5.0], [0.0, 1.0]])

# Bataille des sexes : lignes/colonnes = [Opéra, Football]
BATAILLE_A = np.array([[2.0, 0.0], [0.0, 1.0]])
BATAILLE_B = np.array([[1.0, 0.0], [0.0, 2.0]])

# Pierre-feuille-ciseaux : lignes/colonnes = [Pierre, Feuille, Ciseaux].
# Jeu à somme nulle : le gain du joueur 2 est l'opposé de celui du joueur 1,
# donc B = -A (terme à terme), et non -A^T.
PFC_A = np.array([[0.0, -1.0, 1.0], [1.0, 0.0, -1.0], [-1.0, 1.0, 0.0]])
PFC_B = -PFC_A


if __name__ == "__main__":  # petite démonstration
    for nom, (A, B) in {
        "Dilemme": (DILEMME_A, DILEMME_B),
        "Bataille des sexes": (BATAILLE_A, BATAILLE_B),
        "Pierre-feuille-ciseaux": (PFC_A, PFC_B),
    }.items():
        eqs = enumeration_supports(A, B)
        print(f"\n{nom} : {len(eqs)} équilibre(s)")
        for x, y in eqs:
            print(f"  x = {np.round(x, 4)}  y = {np.round(y, 4)}")

    print("\nCournot a=100, b=1, c=10 :", cournot(100, 1, 10, n=2))
    print("Cournot sur grille :", cournot_grille(100, 1, 10, qmax=100))
