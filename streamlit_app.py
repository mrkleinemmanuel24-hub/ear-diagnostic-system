"""
EAR DIAGNOSTIC SYSTEM v2.0
Application Streamlit Professionnelle
Matrice d'Intelligence Métier + Générateur de Rapports
"""

import streamlit as st
import json
import csv
import os
from datetime import datetime
from pathlib import Path
import anthropic
from io import BytesIO

# Configuration
st.set_page_config(
    page_title="EAR Diagnostic System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.environ.get("ANTHROPIC_API_KEY", "")

# CSS Premium
st.markdown("""
<style>
    .main {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .title-section {
        font-size: 28px;
        font-weight: 700;
        margin: 20px 0 10px 0;
        color: #111827;
        border-left: 4px solid #d4af37;
        padding-left: 15px;
    }
    .subtitle {
        font-size: 14px;
        color: #9ca3af;
        margin-bottom: 20px;
    }
    .card {
        background: #f9fafb;
        padding: 15px;
        border-radius: 8px;
        border-left: 3px solid #d4af37;
        margin: 10px 0;
    }
    .metric-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 15px;
        border-radius: 6px;
        margin: 10px 0;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #d4af37;
    }
    .metric-label {
        font-size: 12px;
        color: #9ca3af;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# MATRICE D'INTELLIGENCE MÉTIER (Le "Cerveau")
# ============================================================================

DIAGNOSTIC_BLOCS = {
    "bloc_1": {
        "title": "📊 Situation Financière",
        "questions": [
            {"id": "ca_actuel", "label": "CA actuel (€)", "type": "number", "default": 200000},
            {"id": "ca_objectif", "label": "Objectif CA 12 mois (€)", "type": "number", "default": 300000},
            {"id": "effectif", "label": "Nombre de collaborateurs", "type": "slider", "min": 1, "max": 100, "default": 5},
            {"id": "marge_nette", "label": "Marge nette estimée (%)", "type": "slider", "min": 10, "max": 80, "default": 40},
        ]
    },
    "bloc_2": {
        "title": "🎯 Pipeline & Conversion",
        "questions": [
            {"id": "contacts_annuels", "label": "Contacts qualifiés/an", "type": "number", "default": 500},
            {"id": "taux_conversion", "label": "Taux conversion (%)", "type": "slider", "min": 1, "max": 30, "default": 3},
            {"id": "cycle_vente_jours", "label": "Cycle de vente (jours)", "type": "slider", "min": 7, "max": 90, "default": 30},
            {"id": "clients_actuels", "label": "Clients actifs actuellement", "type": "number", "default": 10},
        ]
    },
    "bloc_3": {
        "title": "💼 Offre & Positionnement",
        "questions": [
            {"id": "tarif_base", "label": "Tarif de base (€/H ou €/prestation)", "type": "number", "default": 300},
            {"id": "positioning", "label": "Positionnement", "type": "text", "default": "Premium, expertise, solutions sur-mesure"},
            {"id": "certifications", "label": "Certifications (Qualiopi, RNCP, etc)", "type": "text", "default": "Qualiopi"},
            {"id": "concurrents_benchmark", "label": "Positionnement vs concurrents", "type": "text", "default": "Premium"},
        ]
    },
    "bloc_4": {
        "title": "📢 Canaux & Acquisition",
        "questions": [
            {"id": "canal_principal", "label": "Canal principal (BAO, LinkedIn, etc)", "type": "text", "default": "Bouche-à-oreille"},
            {"id": "budget_pub_mensuel", "label": "Budget publicité/mois (€)", "type": "number", "default": 300},
            {"id": "heures_content_weekly", "label": "Heures/semaine en contenu", "type": "slider", "min": 0, "max": 40, "default": 5},
            {"id": "roi_canaux", "label": "Meilleur ROI canal connu?", "type": "text", "default": "Podcast (haute conversion)"},
        ]
    },
    "bloc_5": {
        "title": "⏱️ Capacité & Contraintes",
        "questions": [
            {"id": "heures_semaine", "label": "Heures travail/semaine (actuellement)", "type": "slider", "min": 20, "max": 80, "default": 55},
            {"id": "heures_core", "label": "Heures core business/semaine", "type": "slider", "min": 0, "max": 50, "default": 5},
            {"id": "niveau_fatigue", "label": "Niveau de fatigue (1-10)", "type": "slider", "min": 1, "max": 10, "default": 7},
            {"id": "projets_perso", "label": "Projets personnels importants", "type": "text", "default": "Livre, famille, créativité"},
        ]
    },
    "bloc_6": {
        "title": "🤝 Organisation & Délégation",
        "questions": [
            {"id": "delegue_actuellement", "label": "Déjà délégué", "type": "text", "default": "Compta, facturation"},
            {"id": "equipe_size", "label": "Taille équipe", "type": "slider", "min": 0, "max": 20, "default": 1},
            {"id": "capacite_delegation", "label": "Capacité à déléguer (1-10)", "type": "slider", "min": 1, "max": 10, "default": 4},
            {"id": "goulots", "label": "Goulots d'étranglement", "type": "text", "default": "Admin, email, organisation"},
        ]
    },
    "bloc_7": {
        "title": "💎 Actifs Dormants",
        "questions": [
            {"id": "alumni_count", "label": "Alumni / anciens clients", "type": "number", "default": 45},
            {"id": "email_list", "label": "Taille email list", "type": "number", "default": 300},
            {"id": "reseau_b2b", "label": "Contacts B2B exploitables", "type": "number", "default": 5},
            {"id": "actifs_autre", "label": "Autres actifs dormants", "type": "text", "default": "Salle physique, contenu archivé, réseau ICF"},
        ]
    },
    "bloc_8": {
        "title": "❓ Questions Critiques",
        "questions": [
            {"id": "frein_principal", "label": "Votre plus grand frein?", "type": "text", "default": "Manque de temps"},
            {"id": "croyance_limitante", "label": "Croyance qui vous bloque?", "type": "text", "default": "Besoin apprendre technologie"},
            {"id": "scenario_ideal", "label": "Scénario idéal dans 12 mois?", "type": "text", "default": "300k€, 40H/week, livre fini"},
            {"id": "accepterait_deleguer", "label": "Accepteriez-vous de déléguer?", "type": "text", "default": "Content, email, admin"},
        ]
    }
}

# ============================================================================
# PROMPT POUR CLAUDE (Génération Rapport Style Nathalie)
# ============================================================================

def create_claude_prompt(responses: dict) -> str:
    """Crée le prompt pour Claude incluant la matrice d'intelligence métier"""

    prompt = f"""Tu es Nathalie Lourdel, fondatrice d'EAR avec 21 ans d'expertise.
Tu rédiges un diagnostic stratégique pour un DRH/dirigeant.

RÉPONSES AU DIAGNOSTIC:
{json.dumps(responses, ensure_ascii=False, indent=2)}

INTELLIGENCE MÉTIER À INTÉGRER:

1. LEVIER LINKEDIN ADS
   - Budget dormant: 300€/mois approuvé
   - Stratégie: Ads de contenu expertise (pas vente directe)
   - Cible: DRH tech/RH mid-size
   - ROI potentiel: 80-100 clics/mois → 2-3 participants JD → 14-25k€/an

2. MASTER CLASS MACHINE
   - Repurposer contenu existant en Master Classes premium
   - Format: 12 personnes, 2000€/place
   - Potentiel: 2-3/an = 48-72k€ CA

3. ALUMNI PROGRAM AUTOMATISÉ
   - 45+ alumni dormants
   - Contact actuel: 1x/3 mois (mort)
   - Activation: 1x/mois newsletter + CRM
   - Potentiel: 91-105k€ CA supplémentaire

4. DRH B2B OUTREACH
   - Reconnu par le prospect: "Je devrai plus d'échanges avec DRH"
   - Structurer outreach + ateliers
   - Potentiel: 40-80k€ CA

5. VRAIE MATH (Variables de Conversion)
   - Absentéisme >5%: Coût = Effectif × Taux × Salaire_Moyen
   - Désengagement: Coût = 18% de masse salariale (Étude Gallup)
   - Turnover: Coût = Départs × (Salaire_Moyen × 1.5)

STYLE NATHALIE (Obligatoire)
- Ne pas dire: "Nous pourrions peut-être..."
- Dire: "Votre situation présente un risque de [X]. Sans intervention, [Z]% d'aggravation"
- Mots-clés: Écosystème, Apprenance, Posture, Alignement stratégique, Résilience
- Tone: Expert, bienveillant, sans concession
- Citer: 21 ans d'expérience avec EAR

STRUCTURE DU RAPPORT (8-10 pages):
1. Diagnostic approfondi (chaque bloc)
2. La "Vraie Math" (ROI financier)
3. Les 5-7 leviers réels (calculés)
4. 3 scénarios (A/B/C)
5. Plan 12 mois opérationnel
6. Appel à l'action

Génère un rapport complet, professionnel, data-driven, en français."""

    return prompt

# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

st.markdown('<div class="title-section">🎯 EAR Diagnostic System v2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Diagnostic stratégique automatisé | Basé sur 21 ans d\'expertise EAR</div>', unsafe_allow_html=True)

# Sidebar: Navigation
with st.sidebar:
    st.markdown("### 📍 Mode d'Utilisation")
    mode = st.radio("Sélectionner:", ["Diagnostic Complet", "Voir Résultats", "Dashboard"])

# ============================================================================
# MODE 1: DIAGNOSTIC COMPLET
# ============================================================================

if mode == "Diagnostic Complet":
    bloc_keys = list(DIAGNOSTIC_BLOCS.keys())

    # Progress bar
    progress = (st.session_state.step / len(bloc_keys)) * 100
    st.progress(progress / 100)
    st.markdown(f"**Bloc {st.session_state.step + 1}/{len(bloc_keys)}**")

    if st.session_state.step < len(bloc_keys):
        bloc_key = bloc_keys[st.session_state.step]
        bloc = DIAGNOSTIC_BLOCS[bloc_key]

        st.markdown(f'<div class="title-section">{bloc["title"]}</div>', unsafe_allow_html=True)

        # Questions du bloc
        for q in bloc["questions"]:
            q_id = q["id"]
            label = q["label"]
            q_type = q["type"]
            default = st.session_state.responses.get(q_id, q.get("default", ""))

            if q_type == "number":
                value = st.number_input(label, value=int(default) if default else 0, key=q_id)
            elif q_type == "slider":
                value = st.slider(label, q["min"], q["max"], int(default) if default else q["min"], key=q_id)
            elif q_type == "text":
                value = st.text_input(label, value=str(default) if default else "", key=q_id)

            st.session_state.responses[q_id] = value

        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.step > 0:
                if st.button("← Précédent"):
                    st.session_state.step -= 1
                    st.rerun()
        with col2:
            if st.session_state.step < len(bloc_keys) - 1:
                if st.button("Suivant →", type="primary"):
                    st.session_state.step += 1
                    st.rerun()
            else:
                if st.button("Générer Rapport", type="primary"):
                    st.session_state.step = len(bloc_keys)
                    st.rerun()

    else:  # Génération
        st.markdown('<div class="title-section">✅ Génération du Rapport</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            drh_name = st.text_input("Votre nom", placeholder="Jean Dupont")
        with col2:
            company = st.text_input("Entreprise", placeholder="ACME Corp")

        email = st.text_input("Email", placeholder="jean@acme.fr")

        if st.button("🚀 Générer mon diagnostic complet", type="primary"):
            if not drh_name or not email:
                st.error("Remplissez nom et email")
            else:
                with st.spinner("Génération du diagnostic (IA en cours)..."):
                    try:
                        # Appeler Claude
                        client = anthropic.Anthropic(api_key=st.session_state.api_key)
                        prompt = create_claude_prompt(st.session_state.responses)

                        message = client.messages.create(
                            model="claude-opus-4-1",
                            max_tokens=8000,
                            messages=[{"role": "user", "content": prompt}]
                        )

                        rapport = message.content[0].text

                        # Sauvegarder lead
                        leads_file = Path("data/leads.csv")
                        leads_file.parent.mkdir(exist_ok=True)

                        with open(leads_file, 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            if leads_file.stat().st_size == 0:
                                writer.writerow(["Date", "Nom", "Email", "Entreprise", "CA_Actuel"])
                            writer.writerow([datetime.now().isoformat(), drh_name, email, company, st.session_state.responses.get("ca_actuel", "")])

                        st.success("✅ Diagnostic généré!")
                        st.markdown("### Votre Rapport Stratégique:")
                        st.markdown(rapport)

                        # Télécharger texte
                        st.download_button(
                            label="📥 Télécharger le rapport (.txt)",
                            data=rapport,
                            file_name=f"Diagnostic_{company}_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain"
                        )

                    except Exception as e:
                        st.error(f"Erreur: {str(e)}")

        if st.button("← Revenir au diagnostic"):
            st.session_state.step = 0
            st.rerun()

# ============================================================================
# MODE 2: RÉSULTATS
# ============================================================================

elif mode == "Voir Résultats":
    st.markdown('<div class="title-section">📈 Résultats des Diagnostics</div>', unsafe_allow_html=True)

    leads_file = Path("data/leads.csv")

    if leads_file.exists():
        with open(leads_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) > 1:
            st.metric("Diagnostics réalisés", len(lines) - 1)

            st.markdown("### Derniers diagnostics:")
            for line in lines[-5:]:
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    st.markdown(f"**{parts[1]}** | {parts[3]} | CA: {parts[4]}€ | {parts[0][:10]}")
        else:
            st.info("Aucun diagnostic pour le moment")
    else:
        st.info("Aucun diagnostic réalisé")

# ============================================================================
# MODE 3: DASHBOARD NATHALIE
# ============================================================================

elif mode == "Dashboard":
    st.markdown('<div class="title-section">👤 Dashboard Nathalie</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    leads_file = Path("data/leads.csv")

    if leads_file.exists():
        count = len(open(leads_file).readlines()) - 1
        with col1:
            st.metric("Diagnostics", count)
        with col2:
            st.metric("CA moyen prospect", "~250k€")
        with col3:
            st.metric("Taux conversion", "~25%")

        st.markdown("### Opportunités (Score d'Urgence)")
        st.info("🔴 Haute urgence (CA <200k, 75H+/week): Prêts pour Scenario C immédiat")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9ca3af; font-size: 12px;'>
EAR Diagnostic System v2.0 | 21 ans d\'expertise<br>
Contactez: <a href='mailto:info@ear.fr'>info@ear.fr</a>
</div>
""", unsafe_allow_html=True)
