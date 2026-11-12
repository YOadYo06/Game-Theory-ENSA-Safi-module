# -*- coding: utf-8 -*-
"""
test_hors_ligne.py — tests des outils SANS LLM (faux modèle, étiqueté « scripté »).

Rôle : Développeur agent + Testeur. On vérifie que les nouveaux outils @tool
fonctionnent seuls via `.invoke(...)` (arguments et sorties JSON), avant de les
brancher sur Ollama. Aucun appel réseau n'est effectué ici.
"""
import json

from src.agent_tj_sma import MAX_DIM, MAX_FIRMES, NOUVEAUX_OUTILS, cournot, resoudre_bimatrice

DILEMME_A = [[3, 0], [5, 1]]
DILEMME_B = [[3, 5], [0, 1]]


def test_deux_nouveaux_outils_exportes():
    assert len(NOUVEAUX_OUTILS) == 2


def test_resoudre_bimatrice_dilemme():
    sortie = resoudre_bimatrice.invoke({"A": DILEMME_A, "B": DILEMME_B})
    data = json.loads(sortie)
    assert data["jeu"] == {"m": 2, "n": 2}
    assert data["n_equilibres"] == 1
    eq = data["equilibres"][0]
    assert eq["x"] == [0.0, 1.0]
    assert eq["y"] == [0.0, 1.0]
    assert eq["gain_j1"] == 1.0
    assert eq["type"] == "pur"


def test_resoudre_bimatrice_bataille_mixte():
    sortie = resoudre_bimatrice.invoke({"A": [[2, 0], [0, 1]], "B": [[1, 0], [0, 2]]})
    data = json.loads(sortie)
    assert data["n_equilibres"] == 3
    assert any(e["type"] == "mixte" for e in data["equilibres"])


def test_resoudre_bimatrice_accepte_chaine_json():
    """llama3.1 passe parfois les matrices en chaîne : l'outil doit rester robuste."""
    sortie = resoudre_bimatrice.invoke({"A": "[[3, 0], [5, 1]]", "B": "[[3, 5], [0, 1]]"})
    data = json.loads(sortie)
    assert data["n_equilibres"] == 1


def test_resoudre_bimatrice_chaine_json_invalide():
    """Une chaîne JSON malformée renvoie une erreur, jamais une exception non gérée."""
    sortie = resoudre_bimatrice.invoke({"A": "[[3, 0]", "B": "[[3, 5], [0, 1]]"})
    assert "erreur" in json.loads(sortie)


def test_schema_outil_accepte_liste_ou_chaine():
    """Le schéma de l'outil doit déclarer list|str : sinon pydantic rejette la chaîne
    AVANT l'appel de la fonction (bug observé avec le vrai LangChain)."""
    schema = resoudre_bimatrice.args_schema.model_json_schema()
    assert "A" in schema["properties"] and "B" in schema["properties"]


def test_resoudre_bimatrice_tailles_incompatibles():
    sortie = resoudre_bimatrice.invoke({"A": [[1, 2, 3]], "B": [[1, 2]]})
    assert "erreur" in json.loads(sortie)


def test_resoudre_bimatrice_plafond():
    A = [[0.0] * (MAX_DIM + 1) for _ in range(MAX_DIM + 1)]
    sortie = resoudre_bimatrice.invoke({"A": A, "B": A})
    assert "erreur" in json.loads(sortie)


def test_cournot_outil():
    sortie = cournot.invoke({"a": 100, "b": 1, "c": 10, "n_firmes": 2})
    data = json.loads(sortie)
    assert abs(data["quantite_par_firme"] - 30.0) < 1e-9
    assert abs(data["profit_par_firme"] - 900.0) < 1e-9
    assert abs(data["cartel"]["profit_par_firme"] - 1012.5) < 1e-9


def test_cournot_plafond():
    sortie = cournot.invoke({"a": 100, "b": 1, "c": 10, "n_firmes": MAX_FIRMES + 1})
    assert "erreur" in json.loads(sortie)


def test_cournot_entree_invalide():
    sortie = cournot.invoke({"a": 10, "b": 1, "c": 10})  # a > c requis
    assert "erreur" in json.loads(sortie)


def test_executer_outil_compatible_langchain_et_shim():
    """`agent_demo_ollama` doit exécuter l'outil qu'il soit un StructuredTool
    (LangChain installé) ou une simple fonction (shim hors ligne)."""
    from src.agent_demo_ollama import _executer_outil

    sortie = _executer_outil(cournot, {"a": 100, "b": 1, "c": 10, "n_firmes": 2})
    assert json.loads(sortie)["quantite_par_firme"] == 30.0
    sortie2 = _executer_outil(resoudre_bimatrice, {"A": DILEMME_A, "B": DILEMME_B})
    assert json.loads(sortie2)["n_equilibres"] == 1
