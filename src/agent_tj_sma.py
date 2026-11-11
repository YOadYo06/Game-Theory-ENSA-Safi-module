# -*- coding: utf-8 -*-
"""
agent_tj_sma.py — agent du cours ÉTENDU (Projet 1, Groupe 1).

Rôle associé : Développeur agent (S1–S4), puis rotation.

On repart du fichier du cours `agent_tj_sma.py` (10 outils) et on AJOUTE deux
nouveaux outils, exposés au LLM local (Ollama) :

    - resoudre_bimatrice(A, B)   : équilibres purs et mixtes d'un jeu m x n ;
    - cournot(a, b, c, n_firmes) : quantités, prix, profits + comparaison cartel.

Sécurité (Règle n°5) :
  * jamais d'eval()/exec() sur du texte produit par le LLM ;
  * les outils reçoivent des *données* (matrices, scalaires), jamais du code ;
  * plafonds sur m, n et le nombre de firmes.

Test sans LLM : `resoudre_bimatrice.invoke({...})` puis, avec Ollama, verbose=True.
"""
from __future__ import annotations

import json
from typing import Any, List

import numpy as np

from .jeux import cournot as _cournot
from .jeux import enumeration_supports

# --- Import de @tool : LangChain si disponible, sinon un mini-shim hors ligne -----
try:  # pragma: no cover - dépend de l'environnement
    from langchain_core.tools import tool  # type: ignore

    LANGCHAIN_DISPONIBLE = True
except Exception:  # pragma: no cover
    LANGCHAIN_DISPONIBLE = False

    def tool(fn):  # type: ignore
        """Shim minimal : fournit .invoke(dict|valeur) sans installer LangChain."""
        def _invoke(args: Any):
            if isinstance(args, dict):
                return fn(**args)
            return fn(args)

        fn.invoke = _invoke  # type: ignore[attr-defined]
        return fn


# Plafonds de sécurité
MAX_DIM = 8        # m, n maximum pour resoudre_bimatrice
MAX_FIRMES = 20    # n_firmes maximum pour cournot


def _json(obj: Any) -> Any:
    """Convertit récursivement les types NumPy en types JSON natifs.

    Corrige le « TypeError dans un outil » de l'annexe B du guide (types NumPy).
    """
    if isinstance(obj, dict):
        return {k: _json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return _json(obj.tolist())
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def _comme_matrice(v: Any) -> Any:
    """Accepte une matrice déjà sous forme de liste, ou une chaîne JSON la représentant.

    Certains modèles (ex. llama3.1) passent parfois les matrices sous forme de
    chaîne « "[[3, 0], [5, 1]]" ». On la décode avec json.loads (sûr : jamais
    eval()/exec(), cf. Règle n°5).
    """
    if isinstance(v, str):
        return json.loads(v)
    return v


@tool
def resoudre_bimatrice(A: list, B: list) -> str:
    """Résout un jeu à deux joueurs m x n : équilibres de Nash purs et mixtes.

    Args:
        A: matrice des gains du joueur 1 (lignes), liste de listes m x n
           (ou chaîne JSON la représentant).
        B: matrice des gains du joueur 2 (colonnes), liste de listes m x n
           (ou chaîne JSON la représentant).

    Returns:
        Une chaîne JSON avec la taille du jeu, le nombre d'équilibres et, pour
        chacun, les stratégies mixtes x et y, les gains et le type (pur/mixte).
        En cas d'entrée invalide, renvoie {"erreur": "..."}.
    """
    try:
        Aa = np.asarray(_comme_matrice(A), dtype=float)
        Bb = np.asarray(_comme_matrice(B), dtype=float)
    except (TypeError, ValueError, json.JSONDecodeError):
        return json.dumps({"erreur": "A et B doivent être des matrices numériques."})

    if Aa.ndim != 2 or Bb.ndim != 2 or Aa.shape != Bb.shape:
        return json.dumps({"erreur": "A et B doivent être deux matrices de même taille."})

    m, n = Aa.shape
    if m > MAX_DIM or n > MAX_DIM:
        return json.dumps({"erreur": f"Taille {m}x{n} refusée (plafond {MAX_DIM}x{MAX_DIM})."})

    equilibres = enumeration_supports(Aa, Bb)
    resultat = {
        "jeu": {"m": int(m), "n": int(n)},
        "n_equilibres": len(equilibres),
        "equilibres": [
            {
                "x": [round(float(v), 9) for v in x],
                "y": [round(float(v), 9) for v in y],
                "gain_j1": round(float(x @ Aa @ y), 9),
                "gain_j2": round(float(x @ Bb @ y), 9),
                "type": "mixte" if (np.count_nonzero(x > 1e-9) > 1 or np.count_nonzero(y > 1e-9) > 1) else "pur",
            }
            for x, y in equilibres
        ],
    }
    return json.dumps(_json(resultat), ensure_ascii=False)


@tool
def cournot(a: float, b: float, c: float, n_firmes: int = 2) -> str:
    """Duopole / oligopole de Cournot : quantités, prix, profits et comparaison cartel.

    Args:
        a: ordonnée à l'origine de la demande inverse P(Q) = a - b Q (a > c).
        b: pente de la demande inverse (b > 0).
        c: coût marginal constant.
        n_firmes: nombre de firmes (1 <= n_firmes <= 20).

    Returns:
        Une chaîne JSON avec l'équilibre de Cournot (quantité par firme, quantité
        totale, prix, profit par firme) et les valeurs de cartel correspondantes.
    """
    if n_firmes < 1:
        return json.dumps({"erreur": "n_firmes doit être >= 1."})
    if n_firmes > MAX_FIRMES:
        return json.dumps({"erreur": f"n_firmes plafonné à {MAX_FIRMES}."})
    try:
        res = _cournot(a, b, c, n=int(n_firmes))
    except ValueError as exc:
        return json.dumps({"erreur": str(exc)})
    return json.dumps(_json(res), ensure_ascii=False)


# Liste des outils ajoutés par le Groupe 1 (à concaténer aux 10 outils du cours).
NOUVEAUX_OUTILS: List[Any] = [resoudre_bimatrice, cournot]


def construire_agent(model: str = "llama3.1"):
    """Construit l'agent LangChain branché sur Ollama avec les nouveaux outils.

    Prérequis : `pip install langchain langchain-ollama` et `ollama pull llama3.1`.
    Utiliser verbose=True pour relire les arguments des appels d'outils
    (voir notebooks/02_outils_agent.ipynb).
    """
    from langchain.agents import create_agent  # type: ignore  # import paresseux
    from langchain_ollama import ChatOllama  # type: ignore

    llm = ChatOllama(model=model, temperature=0)
    return create_agent(llm, NOUVEAUX_OUTILS)


if __name__ == "__main__":
    print("LangChain disponible :", LANGCHAIN_DISPONIBLE)
    print(resoudre_bimatrice.invoke({"A": [[3, 0], [5, 1]], "B": [[3, 5], [0, 1]]}))
    print(cournot.invoke({"a": 100, "b": 1, "c": 10, "n_firmes": 2}))
