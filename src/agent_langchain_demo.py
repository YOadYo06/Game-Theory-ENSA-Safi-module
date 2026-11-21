# -*- coding: utf-8 -*-
"""
agent_langchain_demo.py — agent du cours avec le VRAI LangChain (Rôle : Développeur agent).

Complément de `agent_demo_ollama.py` :
  * `agent_demo_ollama.py`  : appel direct de l'API tool-calling d'Ollama (aucune
                              dépendance LangChain) — utile si LangChain ne s'installe pas ;
  * `agent_langchain_demo.py` (ce fichier) : la chaîne officielle du cours,
                              `create_agent(ChatOllama(...), NOUVEAUX_OUTILS)`,
                              avec les mêmes outils que `agent_tj_sma.py`.

Le second valide ce que le premier ne peut pas : le passage des arguments par le
validateur pydantic de LangChain (c'est là que llama3.1 envoyait les matrices en
chaîne, cf. le type `Matrice = Union[list, str]`).

Prérequis : Python 3.12/3.13, `pip install -r requirements.txt`, `ollama serve`,
            `ollama pull llama3.1`.
Usage :     python -m src.agent_langchain_demo
"""
from __future__ import annotations

import json

from .agent_tj_sma import NOUVEAUX_OUTILS, LANGCHAIN_DISPONIBLE

QUESTIONS = [
    "Donne les équilibres de Nash du jeu A = [[3, 0], [5, 1]] et B = [[3, 5], [0, 1]].",
    "Dans un duopole de Cournot avec a = 100, b = 1 et c = 10, quelles sont les "
    "quantités, le prix et les profits à l'équilibre, et que donnerait le cartel ?",
]


def construire_agent(model: str = "llama3.1"):
    """Agent LangChain (create_agent) branché sur le LLM local Ollama."""
    from langchain.agents import create_agent  # type: ignore
    from langchain_ollama import ChatOllama  # type: ignore

    llm = ChatOllama(model=model, temperature=0)
    return create_agent(llm, NOUVEAUX_OUTILS)


def poser_question(agent, question: str) -> None:
    """Exécute une question et affiche les appels d'outils puis la réponse finale."""
    resultat = agent.invoke({"messages": [{"role": "user", "content": question}]})
    for message in resultat["messages"]:
        for appel in getattr(message, "tool_calls", None) or []:
            print(f"  [outil] {appel['name']}({json.dumps(appel['args'], ensure_ascii=False)})")
        if type(message).__name__ == "ToolMessage":
            print(f"  [résultat] {str(message.content)[:160]}")
        if type(message).__name__ == "AIMessage" and message.content:
            print("Réponse de l'agent :", str(message.content).strip())


def main() -> None:
    print("LangChain disponible :", LANGCHAIN_DISPONIBLE)
    if not LANGCHAIN_DISPONIBLE:
        print("Installez LangChain (voir requirements.txt) puis relancez.")
        return
    agent = construire_agent()
    for i, question in enumerate(QUESTIONS, 1):
        print(f"\n=== Question {i} ===\n{question}")
        poser_question(agent, question)


if __name__ == "__main__":
    main()
