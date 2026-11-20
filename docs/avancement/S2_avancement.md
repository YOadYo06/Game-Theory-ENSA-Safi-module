# Point d'avancement — Semaine 2 (S2)

**Projet 1 — Solveur de Nash m×n et duopoles (Cournot, Bertrand) — Groupe 1**
Présenté par : Ikram · Durée : 10 minutes · Appui : Gantt prévisionnel.

## 1. Objectif de la semaine
Faire tourner les fonctions et retrouver les résultats du cours dans un notebook.

## 2. Attendu vs réalisé
| Attendu (guide) | État |
|---|---|
| Formules écrites et expliquées | ✅ section Théorie du rapport |
| Fonctions dans un notebook | ✅ `notebooks/01_theorie_prototype.ipynb` exécuté |
| Résultats du cours reproduits | ✅ (Trahir,Trahir) ; 3 éq. Bataille ; (1/3,1/3,1/3) ; q*=30 |

## 3. Travail par rôle
- **Fatine** — section Théorie du rapport (Nash, Cournot, Bertrand).
- **Ikram** — `src/jeux.py` + notebook 01.
- **Youness** — branchement des outils sur le solveur.
- **Hiba** — tests pytest des jeux du cours.

## 4. Livrable démontrable
`python src/jeux.py` et `python -m pytest -q`.

## 5. Difficultés
Précision numérique (tolérance 1e-9) ; jeux dégénérés documentés comme limite.

## 6. Plan S3
Finaliser les outils LangChain et écrire les tests hors ligne.

## 7. Commits
- `[Ikram] Notebook 01 : resultats du cours reproduits`
- `[Fatine] Section Theorie du rapport`
- `[Hiba] Tests des jeux du cours`
- `[Youness] Branchement des outils`
