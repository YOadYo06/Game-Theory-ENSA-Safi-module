# Point d'avancement — Semaine 1 (S1)

**Projet 1 — Solveur de Nash m×n et duopoles (Cournot, Bertrand) — Groupe 1**
Présenté par : _à désigner_ (un membre différent chaque semaine).
Durée : 10 minutes. Appui : Gantt prévisionnel (`docs/gantt/`).

## 1. Objectif de la semaine (S1 — Cadrage et théorie)

| Attendu (guide) | État |
|---|---|
| Dépôt GitHub créé | ✅ |
| Ollama installé + `ollama pull llama3.1` | ✅ `llama3.1:latest` (8B, *tools*) + `llama3.2:3b` ; serveur sur `127.0.0.1:11434` |
| Fiche de lecture (Phase 0) rendue | ✅ `docs/fiche_lecture.tex` → PDF |
| Fonctions du cours à étendre identifiées | ✅ `nash_mixte_2x2` → `enumeration_supports`, `est_nash`, `cournot`, `cournot_grille` |
| Gantt prévisionnel déposé | ✅ `docs/gantt/` (Mermaid + CSV + PNG) |

## 2. Travail réalisé (par rôle)

- **Théorie (Fatine)** — formules Nash / indifférence sur les supports / Cournot / Bertrand
  rédigées en LaTeX et expliquées ; hypothèses et limites ; conventions `A`/`B` fixées avec les
  Groupes 2 et 6.
- **Quant / Python (Ikram)** — `src/jeux.py` : `est_nash`, `enumeration_supports`,
  `cournot`, `cournot_grille`, `bertrand` + jeux de référence du cours.
- **Développeur agent (Youness)** — `src/agent_tj_sma.py` : outils `resoudre_bimatrice(A, B)` et
  `cournot(a, b, c, n_firmes)`, avec plafonds et sortie JSON.
- **Testeur / Expérimentateur (Hiba)** — `tests/` : validation sur dilemme, bataille des sexes
  et pierre-feuille-ciseaux ; test hors ligne des outils (`.invoke`) ; squelette `experiences.py`.

## 3. Livrable concret démontrable

- `pytest -q` : tous les tests passent (fonctions pures + outils sans LLM).
- `python src/jeux.py` : affiche les équilibres des 3 jeux du cours + Cournot (q*=30, profit 900).
- `python -m src.agent_langchain_demo` : agent LangChain réel (`create_agent` + `ChatOllama`)
  qui appelle `resoudre_bimatrice` et `cournot` et rédige la réponse.
- `ollama list` : `llama3.1` (8B, *tools*) disponible pour l'agent LangChain (S3–S4).

## 4. Écarts prévu / réalisé

- Aucun écart bloquant : Ollama est installé et le modèle `llama3.1` (compatible *tools*)
  est téléchargé sur les postes de travail.
- LangChain n'était pas installable au départ (voir §5) ; résolu en travaillant sur
  Python 3.12, donc l'agent LangChain réel est opérationnel dès S1 (avance sur S3–S4).

## 5. Difficultés et blocages

- **Python 3.15 vs `zstandard`** : `langchain-core` → `langsmith` → `zstandard`, qui n'a pas
  de wheel pour Python 3.15 ; `pip` tentait de le compiler et échouait
  (« Microsoft Visual C++ 14.0 or greater is required »). Résolution : environnement
  dédié **`.venv` sur Python 3.12** (`py -3.12 -m venv .venv`), où tous les paquets
  s'installent en binaire. Documenté dans `requirements.txt`.
- **Matrices passées en chaîne** : `llama3.1` envoie parfois `A = "[[3, 0], [5, 1]]"`.
  Le validateur pydantic de LangChain rejetait la chaîne avant l'appel de l'outil.
  Corrigé par le type `Matrice = Union[list, str]` dans `src/agent_tj_sma.py` (+ test).
- Le binaire `ollama` n'est pas ajouté au `PATH` sous Windows : lancer l'application Ollama
  (le serveur écoute sur `127.0.0.1:11434`) ou appeler le chemin complet
  `%LOCALAPPDATA%\Programs\Ollama\ollama.exe`.

## 6. Plan de la semaine suivante (S2)

- ~~Faire tourner les fonctions dans `notebooks/01_theorie_prototype.ipynb`~~ ✅ fait
  (exécuté avec `nbconvert` ; résultats du cours reproduits).
- Reste en S2 : rédiger la section « formules expliquées » du rapport, lancer les 20 jeux
  aléatoires (`src/experiences.py`) et le banc d'essai 5 énoncés × 2 modèles Ollama.

## 7. État du dépôt Git

- Commits de la semaine (un par étudiant, nom entre crochets) :
  - `[Fatine] Fiche de lecture Phase 0 (formules + hypothèses)`
  - `[Ikram] Solveur de Nash m×n : énumération des supports`
  - `[Youness] Outils resoudre_bimatrice et cournot exposés à l'agent`
  - `[Hiba] Tests pytest des jeux du cours + tests hors ligne`
  - `[Youness] Test en ligne de l'agent (Ollama)`
  - `[Ikram] Environnement Python 3.12 (`requirements.txt`) + notebook exécuté via nbconvert`
  - `[Youness] Agent LangChain réel (`agent_langchain_demo.py`) + matrices en chaîne JSON`
