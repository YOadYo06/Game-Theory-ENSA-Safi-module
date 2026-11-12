# -*- coding: utf-8 -*-
"""
test_jeux.py — tests pytest des fonctions pures (Rôle : Testeur / Expérimentateur).

On valide le solveur sur les résultats connus du cours :
  - dilemme du prisonnier  -> (Trahir, Trahir) unique ;
  - bataille des sexes     -> 3 équilibres, dont le mixte (2/3, 1/3) ;
  - pierre-feuille-ciseaux -> solution uniforme (1/3, 1/3, 1/3) ;
  - Cournot a=100, b=1, c=10 -> q* = 30, profit 900 ; cartel 22,5 / 1012,5 ;
  - toute solution renvoyée passe est_nash.
"""
import numpy as np
import pytest

from src.jeux import (
    BATAILLE_A,
    BATAILLE_B,
    DILEMME_A,
    DILEMME_B,
    PFC_A,
    PFC_B,
    bertrand,
    cournot,
    cournot_grille,
    enumeration_supports,
    equilibres_nash_purs,
    est_nash,
)


# --------------------------------------------------------------------------- #
# est_nash
# --------------------------------------------------------------------------- #
def test_est_nash_accepte_et_rejette():
    A, B = DILEMME_A, DILEMME_B
    assert est_nash(A, B, [0, 1], [0, 1])            # (Trahir, Trahir)
    assert not est_nash(A, B, [1, 0], [1, 0])        # (Coopérer, Coopérer) n'est pas un équilibre


def test_est_nash_tolere_les_flottants():
    A, B = BATAILLE_A, BATAILLE_B
    x = [2 / 3 + 1e-12, 1 / 3]
    y = [1 / 3, 2 / 3]
    assert est_nash(A, B, x, y)


# --------------------------------------------------------------------------- #
# Équilibres purs et énumération des supports
# --------------------------------------------------------------------------- #
def test_equilibres_nash_purs_dilemme():
    assert equilibres_nash_purs(DILEMME_A, DILEMME_B) == [(1, 1)]


def test_dilemme_un_seul_equilibre():
    eqs = enumeration_supports(DILEMME_A, DILEMME_B)
    assert len(eqs) == 1
    x, y = eqs[0]
    assert np.allclose(x, [0, 1])
    assert np.allclose(y, [0, 1])


def test_bataille_trois_equilibres():
    eqs = enumeration_supports(BATAILLE_A, BATAILLE_B)
    assert len(eqs) == 3
    # équilibre mixte : p = 2/3 (joueur 1), q = 1/3 (joueur 2)
    assert any(
        np.allclose(x, [2 / 3, 1 / 3], atol=1e-6) and np.allclose(y, [1 / 3, 2 / 3], atol=1e-6)
        for x, y in eqs
    )
    # deux équilibres purs
    assert any(np.allclose(x, [1, 0]) and np.allclose(y, [1, 0]) for x, y in eqs)
    assert any(np.allclose(x, [0, 1]) and np.allclose(y, [0, 1]) for x, y in eqs)


def test_pierre_feuille_ciseaux_uniforme():
    eqs = enumeration_supports(PFC_A, PFC_B)
    assert len(eqs) == 1
    x, y = eqs[0]
    assert np.allclose(x, [1 / 3, 1 / 3, 1 / 3], atol=1e-6)
    assert np.allclose(y, [1 / 3, 1 / 3, 1 / 3], atol=1e-6)


def test_tous_les_equilibres_passent_est_nash():
    """Propriété générale : chaque équilibre renvoyé doit vérifier la non-déviation."""
    rng = np.random.default_rng(0)
    for _ in range(15):
        A = rng.normal(size=(3, 3))
        B = rng.normal(size=(3, 3))
        for x, y in enumeration_supports(A, B):
            assert est_nash(A, B, x, y)


def test_enumeration_tailles_differentes_refusee():
    with pytest.raises(ValueError):
        enumeration_supports(np.zeros((2, 3)), np.zeros((3, 2)))


# --------------------------------------------------------------------------- #
# Cournot / Bertrand
# --------------------------------------------------------------------------- #
def test_cournot_formules_du_cours():
    r = cournot(a=100, b=1, c=10, n=2)
    assert r["quantite_par_firme"] == pytest.approx(30.0)
    assert r["quantite_totale"] == pytest.approx(60.0)
    assert r["prix"] == pytest.approx(40.0)
    assert r["profit_par_firme"] == pytest.approx(900.0)
    assert r["cartel"]["quantite_par_firme"] == pytest.approx(22.5)
    assert r["cartel"]["profit_par_firme"] == pytest.approx(1012.5)


def test_cournot_n_firmes():
    r = cournot(a=100, b=1, c=10, n=3)
    assert r["quantite_par_firme"] == pytest.approx((100 - 10) / (4 * 1))
    assert r["profit_par_firme"] == pytest.approx((100 - 10) ** 2 / (1 * 16))


def test_cournot_grille_retrouve_q_etoile():
    eqs = cournot_grille(a=100, b=1, c=10, qmax=100)
    assert any(abs(q1 - 30) < 1e-9 and abs(q2 - 30) < 1e-9 for q1, q2 in eqs)


def test_meilleure_reponse_converge_vitesse_un_demi():
    """L'itération des meilleures réponses converge (facteur de contraction 1/2)."""
    a, b, c = 100.0, 1.0, 10.0
    q = np.array([0.0, (a - c) / b])
    ecarts = []
    for _ in range(20):
        q_suivant = (a - c - b * q[::-1]) / (2 * b)
        ecarts.append(np.linalg.norm(q_suivant - q))
        q = q_suivant
    assert np.allclose(q, [30.0, 30.0], atol=1e-6)
    # le rapport des écarts successifs tend vers 1/2
    assert ecarts[-1] / ecarts[-2] == pytest.approx(0.5, abs=0.05)


def test_bertrand_paradoxe():
    r = bertrand(a=100, b=1, c=10)
    assert r["prix_equilibre"] == pytest.approx(10.0)
    assert r["profit_par_firme"] == 0.0
    assert r["prix_monopole"] == pytest.approx(55.0)
