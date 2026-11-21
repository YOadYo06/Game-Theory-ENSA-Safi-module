# Livraison — Fatine (Chef de projet / Théorie)

Ce dossier contient **tes fichiers** du Projet 1. Tu dois les ajouter au dépôt Git et
les pousser **avec ton propre compte**, pour que l'historique porte ton nom.

## Contenu du dossier

```
README.md                         # présentation, installation, commandes, structure
docs/fiche_lecture.tex / .pdf     # fiche de lecture Phase 0 (2 pages)
docs/gantt/                       # Gantt prévisionnel + réalisé (Mermaid, CSV, PNG, script)
docs/avancement/S1_avancement.md  # point d'avancement S1
docs/rapport/                     # rapport final LaTeX + PDF (7 pages) + figures + CSV d'expériences
```

## Marche à suivre

```bash
# 1. Cloner le dépôt (c'est toi qui crées le dépôt GitHub, puis tu le clones)
git clone https://github.com/<compte>/<repo>.git
cd <repo>

# 2. Copier le contenu de ce dossier DANS le dépôt, en gardant l'arborescence
#    (README.md, pytest.ini, docs/...)

# 3. Régler ton identité Git
git config user.name  "ACHTOUK Fatine"
git config user.email "afatine919@gmail.com"

# 4. Committer tes fichiers
git add README.md docs
git commit -m "[Fatine] Cadrage S1 (fiche, Gantt, avancement) + rapport final et figures d'experiences"

# 5. Pousser
git push
```

## Note sur le rapport

`docs/rapport/rapport.pdf` est **complet** (plus aucun texte rouge « À COMPLÉTER ») et
contient la table des matières, le Gantt prévisionnel *et* réalisé, les figures
d'expériences. Pour le recompiler après modification :

```bash
cd docs/rapport
pdflatex rapport.tex
pdflatex rapport.tex     # 2e passe : indispensable pour la table des matières
```

## Important

- C'est **toi** qui crées le dépôt GitHub et invites les autres membres (Settings →
  Collaborators). Communique l'URL aux trois autres.
- Ton e-mail `afatine919@gmail.com` doit être **ajouté et vérifié** dans ton compte GitHub.
- Le dépôt ne sera **complet et exécutable** qu'après le push des **quatre** membres.
- **Python 3.12 ou 3.13 obligatoire** (voir la section Installation du README).
