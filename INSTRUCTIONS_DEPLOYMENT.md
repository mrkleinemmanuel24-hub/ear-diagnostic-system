# 🚀 EAR Diagnostic System — Instructions de Déploiement

## Structure du Projet

```
EAR NATHALIE/
├── streamlit_app.py                    # Application web Streamlit
├── generate_master_document.py         # Générateur de documents IA
├── RAPPORT_STRATEGIQUE_COMPLET_2026.txt      # Diagnostic Nathalie complet
├── GRAND_DOCUMENT_PRESENTATION_2026.txt      # Document de présentation
├── requirements.txt                    # Dépendances Python
├── .env                                # Clé API (à remplir)
└── data/
    └── leads.csv                       # Enregistrement des diagnostics
```

## Installation Locale

### 1. Installer les dépendances

```bash
cd "/Users/emmanuelklein/EAR NATHALIE"
pip install -r requirements.txt
```

### 2. Vérifier la clé API

Le fichier `.env` doit contenir:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 3. Lancer l'application Streamlit

```bash
streamlit run streamlit_app.py
```

L'app ouvrira sur `http://localhost:8501`

## Fonctionnalités

### Mode 1: Diagnostic Complet
- DRH répond 50+ questions sur 8 blocs
- IA génère rapport stratégique personnalisé
- Export PDF
- Enregistrement automatique du lead

### Mode 2: Voir Résultats
- Historique des diagnostics réalisés
- Statistiques

### Mode 3: Dashboard Nathalie
- KPI des prospects
- Score d'urgence
- Opportunités de suivi

## Deployment Cloud (Streamlit Cloud)

1. Créer un repo GitHub avec les fichiers
2. Connecter à Streamlit Cloud
3. Ajouter secrets dans Settings:
   - `ANTHROPIC_API_KEY`

URL: `https://[username]-[app-name].streamlit.app`

## Architecture

### Le "Cerveau" de la Machine (Intelligence Métier)

**8 Blocs de Diagnostic:**
1. Situation Financière (CA, marge, croissance)
2. Pipeline & Conversion (taux, cycle)
3. Offre & Positionnement (tarif, certifications)
4. Canaux & Acquisition (sources, budget)
5. Capacité & Contraintes (heures, fatigue)
6. Organisation & Délégation (équipe, bottlenecks)
7. Actifs Dormants (alumni, email list, réseaux)
8. Questions Critiques (freins, croyances, vision)

**Matrice de Décision:**
- Chaque réponse déclenche une analyse spécifique
- Formules de calcul ROI automatiques
- Solutions proposées basées sur 21 ans d'expertise

**Générateur de Rapports (Claude API):**
- Style "Nathalie Lourdel" (expert, bienveillant, direct)
- Tone: données-driven, sans jargon
- Structure: diagnostic → math → leviers → scénarios → plan 12 mois

## Leviers de Croissance Automatiquement Identifiés

Le système propose automatiquement:
1. **Coaching Tarif:** +30k€ (0H effort)
2. **Master Classes:** +48k€ (28H/an)
3. **Alumni Activation:** +91k€ (30H/an)
4. **DRH B2B:** +40k€ (20H/an)
5. **EAR Formation:** 98k€ (stable)
6. **LinkedIn Ads:** +14-25k€ (300€/mois automatisé)

**Total potentiel:** 320-350k€ CA avec 50H/week durable

## Utilisation pour Dimanche 27 Avril

1. **Présentation à Nathalie:**
   - Lire GRAND_DOCUMENT_PRESENTATION_2026.txt
   - Montrer l'app en action sur laptop
   - Démontrer génération d'un rapport en 30 secondes

2. **Message clé:**
   - "C'est pas une tech, c'est une libération"
   - "La machine fait le travail de relance alumni, recherche DRH, calcule ROI"
   - "Vous cochez pas du code, vous cochez des décisions business"

3. **Prochaines étapes:**
   - Si oui → Lancer VA hiring mardi
   - Si réflexion → Follow-up jeudi

## Support & Questions

Contacter: Emmanuel Klein (emmanuelklein24@gmail.com)

---

**Status:** Production-Ready | Prêt pour dimanche
