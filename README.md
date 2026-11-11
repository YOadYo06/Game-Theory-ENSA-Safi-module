# Projet 1 — Solveur de Nash m×n et duopoles (Cournot, Bertrand)

**Groupe 1** — Module *Théorie des Jeux et Systèmes Multi-Agents*
Cycle Ingénieur — Informatique Décisionnelle et IA (IDIA3) — ENSA Safi
Professeur : Abdelilah JRAIFI — Année universitaire 2026-2027

| Membre | Rôle (S1–S4) |
|---|---|
| ACHTOUK Fatine | Chef de projet / Théorie |
| ADIL Youness | Développeur agent |
| BELHIMER Ikram | Quant / Python |
| BOULHAIL Hiba | Testeur / Expérimentateur |

> ⚠️ Répartition proposée : à confirmer avec le groupe. **Rotation obligatoire à la fin de la S4**
> (à reporter sur le Gantt prévisionnel *et* réalisé).

## Objectif

Généraliser `nash_mixte_2x2` (cours) en un solveur pour jeux à deux joueurs de taille
quelconque **m×n** par *énumération des supports*, le valider sur les jeux du cours, puis
l'appliquer aux duopoles de **Cournot** et de **Bertrand** et l'exposer à l'agent LangChain
(LLM local Ollama).

## Conventions (accord inter-groupes, cf. guide — « Dépendances entre projets »)

- `A` : matrice de gains du **joueur 1** (lignes), taille `m × n`.
- `B` : matrice de gains du **joueur 2** (colonnes), taille `m × n`.
- Les indices commencent à **0**.
- `x` : stratégie mixte du joueur 1 (simplexe de taille `m`) ; `y` : joueur 2 (taille `n`).

Ces conventions sont partagées avec les Groupes 2 et 6 (le solveur de Nash sert à leurs
sous-jeux simultanés / jeux répétés).

## Installation

> ⚠️ **Python 3.12 ou 3.13 requis.** Sur Python 3.15, `zstandard` (dépendance de
> `langsmith`, tirée par `langchain-core`) n'a pas encore de wheel : `pip` tente de le
> compiler et échoue sans *Visual C++ Build Tools*. Avec 3.12/3.13, tout s'installe en binaire.

```bash
# 1. Environnement Python 3.12
py -3.12 -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
python3.12 -m venv .venv && source .venv/bin/activate

pip install -r requirements.txt

# 2. Ollama (agent local) — Règle n°5 : Ollama n'écoute que sur 127.0.0.1
#    Installer Ollama puis :
ollama pull llama3.1
ollama serve          # (si l'application ne tourne pas déjà)
```

## Comment lancer

```bash
# Tests des fonctions pures et des outils (sans LLM)
pytest -q

# Résultats du cours en console
python src/jeux.py

# Notebooks (exécution en ligne de commande, sans interface)
python -m nbconvert --to notebook --execute --inplace notebooks/01_theorie_prototype.ipynb

# Agent : version LangChain réelle (nécessite ollama serve)
python -m src.agent_langchain_demo
# Agent : version sans LangChain (API tool-calling native d'Ollama)
python -m src.agent_demo_ollama

# Expériences : 20 jeux aléatoires -> CSV + figure
python docs/rapport/generate_figures.py
# Expériences : 5 énoncés x 2 modèles (nécessite ollama serve)
python -c "from src.experiences import protocole_agent_ollama as p; p()"

# Gantts -> PNG
python docs/gantt/generate_gantt.py            # prévisionnel
python docs/gantt/generate_gantt.py --realise  # réalisé
```

## Structure du dépôt (Annexe A du guide)

```
projet-groupe1/
├── README.md
├── requirements.txt
├── pytest.ini
├── docs/
│   ├── fiche_lecture.tex            # Phase 0 (PDF livré)
│   ├── gantt/
│   │   ├── gantt_previsionnel.mmd   # source Mermaid
│   │   ├── gantt_previsionnel.md    # version rendue (Mermaid)
│   │   ├── gantt_source.csv         # source éditable (tâches/responsables)
│   │   ├── gantt_realise.csv        # état réel par tâche
│   │   └── generate_gantt.py        # -> gantt_previsionnel.png / gantt_realise.png
│   ├── avancement/                  # points d'avancement hebdomadaires (S1..S7)
│   └── rapport/                     # sources LaTeX (Gantt + figures inclus)
│       ├── rapport.tex / rapport.pdf
│       ├── generate_figures.py      # -> fig_exp_jeux.png
│       └── exp_jeux.csv / exp_agent.csv
├── notebooks/
│   ├── 01_theorie_prototype.ipynb
│   ├── 02_outils_agent.ipynb
│   └── 03_experiences.ipynb
├── src/
│   ├── jeux.py                      # fonctions pures (sans LangChain)
│   ├── experiences.py               # protocoles, graines, tableaux
│   ├── agent_tj_sma.py              # agent du cours ÉTENDU (nouveaux @tool)
│   ├── agent_langchain_demo.py      # agent LangChain réel (create_agent)
│   └── agent_demo_ollama.py         # agent sans LangChain (API Ollama native)
└── tests/
    ├── test_jeux.py                 # tests pytest des fonctions pures
    └── test_hors_ligne.py           # outils + faux modèle (« scripté »)
```

## Convention de commit (Règle n°4)

Un commit par semaine **et par étudiant**, avec le prénom entre crochets :

```
[Ikram]   Ajout de l'énumération des supports
[Hiba]    Test pytest du solveur sur la bataille des sexes
[Youness] Outil resoudre_bimatrice exposé à l'agent
[Fatine]  Rédaction des formules de Cournot en LaTeX
```

> Un nom absent de l'historique Git entraîne une **note individuelle** au lieu de la note collective.

## État d'avancement

Voir `docs/avancement/` (un mini-compte rendu par semaine, appuyé sur le Gantt).
