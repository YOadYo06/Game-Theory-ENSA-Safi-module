# Projet 1 — Solveur de Nash m×n et duopoles (Cournot, Bertrand)

**Groupe 1** — Module *Théorie des Jeux et Systèmes Multi-Agents*
Cycle Ingénieur — Informatique Décisionnelle et IA (IDIA3) — ENSA Safi
Professeur : Abdelilah JRAIFI — Année universitaire 2026-2027

## Membres et rôles

| Membre | Semaines 1 → 4 | Semaines 5 → 7 (après rotation) |
|---|---|---|
| ACHTOUK Fatine | Chef de projet / Théorie | Testeur / Expérimentateur |
| ADIL Youness | Développeur agent | Chef de projet / Théorie |
| BELHIMER Ikram | Quant / Python | Développeur agent |
| BOULHAIL Hiba | Testeur / Expérimentateur | Quant / Python |

> La rotation des rôles est obligatoire à la fin de la semaine 4 (S4).

## Objectif

Généraliser `nash_mixte_2x2` (vu en cours) en un solveur pour jeux à deux joueurs
de taille quelconque **m×n** par *énumération des supports*, le valider sur les
jeux du cours (dilemme du prisonnier, bataille des sexes, pierre-feuille-ciseaux),
puis l'appliquer aux duopoles de **Cournot** et de **Bertrand** et l'exposer à un
agent LangChain (LLM local Ollama).

## Conventions

- `A` : matrice de gains du **joueur 1** (lignes), taille `m × n`.
- `B` : matrice de gains du **joueur 2** (colonnes), taille `m × n`.
- Les indices commencent à **0**.
- `x` : stratégie mixte du joueur 1 (simplexe de taille `m`) ; `y` : joueur 2 (taille `n`).

Ces conventions sont partagées avec les Groupes 2 et 6.

## Installation

Python **3.12 ou 3.13** requis. Sur Python 3.15, `zstandard` (dépendance de
`langsmith`) n'a pas encore de wheel et `pip` échoue à le compiler.

```bash
py -3.12 -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Pour l'agent (à partir de la semaine 3), Ollama doit tourner en local :

```bash
ollama pull llama3.1
ollama serve
```

## État actuel — semaine 1 (S1)

Le dépôt contient le cadrage et le socle du projet :

| Fichier | Rôle |
|---|---|
| `docs/fiche_lecture.tex` / `.pdf` | fiche de lecture du sujet |
| `docs/gantt/` | Gantt prévisionnel : sources CSV, Mermaid, script et PNG |
| `docs/S1_mini_rapport.tex` / `.pdf` | rapport de la semaine 1 |
| `docs/avancement/S1_avancement.md` | point d'avancement |
| `src/jeux.py` | solveur de Nash m×n, Cournot et Bertrand |
| `tests/test_jeux.py` | 13 tests des résultats du cours |
| `requirements.txt`, `pytest.ini`, `.gitignore` | configuration du dépôt |

## Vérification

```bash
python -m pytest -q      # 13 tests
python src/jeux.py       # résultats du cours en console
```

## Feuille de route (S1 → S7)

| Semaine | Thème | Ce qui est ajouté |
|---|---|---|
| S1 | Cadrage et théorie | fiche de lecture, Gantt prévisionnel, solveur, tests |
| S2 | Prototype Python | notebook 01, outils `@tool` de l'agent |
| S3 | Outils LangChain | agent LangChain, protocoles d'expérience, cas limites |
| S4 | Agent et rotation | agent Ollama natif, notebook 02, Gantt réalisé |
| S5 | Expériences | 20 jeux aléatoires, banc d'essai de l'agent, notebook 03 |
| S6 | Tests et rédaction | test de non-régression, documentation des données |
| S7 | Rapport final | bilan des tests et des données, version 1.0.0 |

Chaque semaine donne **4 commits**, un par membre, avec le prénom entre crochets.

## Structure cible

```
.
├── README.md
├── requirements.txt
├── pytest.ini
├── docs/
│   ├── fiche_lecture.tex / .pdf
│   ├── S1_mini_rapport … S7_mini_rapport
│   ├── gantt/
│   ├── avancement/
│   └── rapport/
├── notebooks/
├── src/
└── tests/
```

## Convention de commit

Un commit par semaine **et par étudiant**, avec le prénom entre crochets :

```
[Fatine]  Rédaction de la fiche de lecture
[Youness] Initialisation du dépôt
[Ikram]   Énumération des supports
[Hiba]    Tests pytest du solveur
```
