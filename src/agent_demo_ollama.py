# -*- coding: utf-8 -*-
"""
agent_demo_ollama.py — test « en ligne » de l'agent avec Ollama (Rôle : Développeur agent).

Pourquoi ce script ?
    L'environnement Python 3.15 de la machine n'a pas de wheel pour `zstandard`
    (dépendance de `langsmith`, elle-même tirée par `langchain-core`) : l'installation
    complète de LangChain échoue sans Visual C++ Build Tools. Ce script court-circuite
    ce problème en appelant directement l'API native de tool-calling d'Ollama
    (`POST /api/chat` avec un champ `tools`), ce qui reproduit exactement la boucle
    LangChain : prompt -> modèle -> appel d'outil -> exécution -> réponse.

    On réutilise les MÊMES outils Python que `agent_tj_sma.py`
    (`resoudre_bimatrice`, `cournot`), donc le test valide bien le comportement du modèle
    sur nos fonctions, pas une réimplémentation.

Prérequis : `ollama serve` et le modèle `llama3.1` téléchargé.
Usage :     python -m src.agent_demo_ollama
"""
from __future__ import annotations

import json
import urllib.request

from .agent_tj_sma import cournot, resoudre_bimatrice

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODELE = "llama3.1"

SYSTEM = (
    "Tu es un assistant de théorie des jeux. "
    "Pour toute question numérique, appelle l'outil approprié au lieu de calculer toi-même. "
    "Conventions : A = gains du joueur 1 (lignes), B = gains du joueur 2 (colonnes)."
)

# Schémas JSON des outils (ce que LangChain génère à partir des types annotés).
SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "resoudre_bimatrice",
            "description": (
                "Résout un jeu à deux joueurs de taille m x n et renvoie les équilibres "
                "de Nash (purs et mixtes). A = gains du joueur 1 (lignes), "
                "B = gains du joueur 2 (colonnes)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "A": {"type": "array", "items": {"type": "array", "items": {"type": "number"}},
                          "description": "matrice des gains du joueur 1"},
                    "B": {"type": "array", "items": {"type": "array", "items": {"type": "number"}},
                          "description": "matrice des gains du joueur 2"},
                },
                "required": ["A", "B"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cournot",
            "description": (
                "Duopole/oligopole de Cournot : quantités, prix, profits et comparaison avec "
                "le cartel. Demande inverse P = a - b*Q, coût marginal c."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"}, "b": {"type": "number"}, "c": {"type": "number"},
                    "n_firmes": {"type": "integer", "description": "nombre de firmes (défaut 2)"},
                },
                "required": ["a", "b", "c"],
            },
        },
    },
]

OUTILS = {"resoudre_bimatrice": resoudre_bimatrice, "cournot": cournot}


def _chat(messages, model=MODELE):
    payload = {
        "model": model,
        "messages": messages,
        "tools": SCHEMAS,
        "stream": False,
        "options": {"temperature": 0},
    }
    req = urllib.request.Request(
        OLLAMA_URL, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as rep:
        return json.loads(rep.read().decode("utf-8"))


def poser_question(question: str, model: str = MODELE, max_tours: int = 4, verbose: bool = True) -> dict:
    """Boucle agent : prompt -> (appels d'outils) -> réponse finale.

    Retourne un dict {reponse, appels} où `appels` liste les (nom, arguments, résultat).
    """
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    appels = []
    for _ in range(max_tours):
        rep = _chat(messages, model=model)
        msg = rep["message"]
        messages.append(msg)
        tool_calls = msg.get("tool_calls") or []
        if not tool_calls:
            return {"reponse": msg.get("content", ""), "appels": appels}
        for call in tool_calls:
            nom = call["function"]["name"]
            args = call["function"].get("arguments", {})
            if isinstance(args, str):
                args = json.loads(args or "{}")
            fn = OUTILS.get(nom)
            resultat = fn(**args) if fn else json.dumps({"erreur": f"outil inconnu: {nom}"})
            if verbose:
                print(f"  [outil] {nom}({json.dumps(args, ensure_ascii=False)})")
            appels.append({"nom": nom, "arguments": args, "resultat": resultat})
            messages.append({"role": "tool", "content": resultat})
    return {"reponse": "(limite de tours atteinte)", "appels": appels}


def main() -> None:
    questions = [
        "Donne les équilibres de Nash du jeu A = [[3, 0], [5, 1]] et B = [[3, 5], [0, 1]].",
        "Dans un duopole de Cournot avec a = 100, b = 1 et c = 10, quelles sont les "
        "quantités, le prix et les profits à l'équilibre, et que donnerait le cartel ?",
    ]
    for i, q in enumerate(questions, 1):
        print(f"\n=== Question {i} ===\n{q}")
        res = poser_question(q)
        print("Réponse de l'agent :", res["reponse"].strip())
        print(f"(appels d'outils : {len(res['appels'])})")


if __name__ == "__main__":
    main()
