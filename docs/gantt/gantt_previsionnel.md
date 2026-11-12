# Gantt prévisionnel — Projet 1 (Groupe 1)

> Semaine 1 — dépôt initial. Les dates sont des **placeholders** (lundi de S1 = 2026-09-07) :
> à ajuster sur le calendrier réel du module. Source éditable : `gantt_source.csv`.
> Version PNG : `python docs/gantt/generate_gantt.py`.

```mermaid
gantt
    title Gantt prévisionnel — Projet 1 (Nash m×n, Cournot, Bertrand) — Groupe 1
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m

    section Phase 0 — Fiche de lecture (S1)
    Fiche de lecture 2 pages (LaTeX)          :done,   p0, 2026-09-07, 5d
    Dépôt GitHub + Gantt prévisionnel         :done,   p0b, 2026-09-07, 5d
    Jalon S1                                  :milestone, m1, 2026-09-11, 0d

    section Phase 1 — Théorie
    Formules Nash / Cournot / Bertrand        :p1, 2026-09-07, 10d
    Hypothèses, limites, conventions A/B      :p1b, 2026-09-14, 5d

    section Phase 2 — Données et paramètres
    Jeux du cours (PD, BoS, PFC)              :p2, 2026-09-14, 5d
    Jeux aléatoires m×n (graines fixées)      :p2b, 2026-09-21, 5d

    section Phase 3 — Python
    est_nash + enumeration_supports           :p3, 2026-09-14, 10d
    cournot + cournot_grille                  :p3b, 2026-09-21, 5d
    Tests pytest sur les jeux du cours        :p3c, 2026-09-28, 5d
    Jalon S2 (prototype notebook)             :milestone, m2, 2026-09-18, 0d
    Jalon S3 (outils .invoke)                 :milestone, m3, 2026-09-25, 0d

    section Phase 4 — Agents LangChain
    Outils resoudre_bimatrice + cournot       :p4, 2026-09-28, 5d
    Agent Ollama (verbose=True)               :p4b, 2026-09-28, 7d
    Rotation des rôles                        :crit, p4c, 2026-10-02, 1d
    Jalon S4 (agent + rotation)               :milestone, m4, 2026-10-02, 0d

    section Phase 5 — Expériences
    20 jeux aléatoires (nb équilibres, temps) :p5, 2026-10-05, 7d
    5 énoncés × 2 modèles Ollama              :p5b, 2026-10-05, 7d
    Jalon S5 (protocole complet)              :milestone, m5, 2026-10-09, 0d

    section Rédaction et bilan
    Rapport à 80 % (Gantt inclus)             :p6, 2026-10-12, 7d
    Gantt réalisé + analyse des écarts        :p6b, 2026-10-12, 7d
    Jalon S6 (code finalisé)                  :milestone, m6, 2026-10-16, 0d
    Jalon S7 (rapport + code zippé)           :milestone, m7, 2026-10-23, 0d
```

## Rotation des rôles (fin S4)

| Membre | Rôle S1–S4 | Rôle S5–S7 (proposé) |
|---|---|---|
| ACHTOUK Fatine | Chef de projet / Théorie | Testeur / Expérimentateur |
| ADIL Youness | Développeur agent | Chef de projet / Théorie |
| BELHIMER Ikram | Quant / Python | Développeur agent |
| BOULHAIL Hiba | Testeur / Expérimentateur | Quant / Python |
