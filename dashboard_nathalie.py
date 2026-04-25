"""
Dashboard pour Nathalie Lourdel
Visualise les prospects, leurs scores d'urgence, et les opportunités
"""

import streamlit as st
import pandas as pd
import csv
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="EAR Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .metric-container {
        background: linear-gradient(135deg, #d4af37 0%, #f0e6d2 100%);
        padding: 20px;
        border-radius: 8px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
    }
    .metric-label {
        font-size: 12px;
        opacity: 0.9;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 EAR Dashboard — Nathalie Lourdel")
st.markdown("Vue d'ensemble des prospects et scores d'urgence")

# Load leads
leads_file = Path("data/leads.csv")

if leads_file.exists():
    df = pd.read_csv(leads_file)

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📈 Total Diagnostics", len(df))

    with col2:
        ca_moyen = df["CA_Actuel"].mean() if "CA_Actuel" in df.columns else 0
        st.metric("💰 CA Moyen Prospect", f"€{int(ca_moyen):,}")

    with col3:
        urgent = len(df[df["CA_Actuel"] < 200000]) if "CA_Actuel" in df.columns else 0
        st.metric("🔴 Prospects Urgents", urgent)

    with col4:
        taux = (urgent / len(df) * 100) if len(df) > 0 else 0
        st.metric("⚡ % Urgence", f"{taux:.0f}%")

    # Tableau des prospects
    st.markdown("### 📋 Tous les Prospects")

    display_df = df[["Date", "Nom", "Email", "Entreprise", "CA_Actuel"]].copy()

    # Ajouter score d'urgence
    def get_urgency_score(ca):
        try:
            ca = int(ca)
            if ca < 150000:
                return "🔴 HAUTE"
            elif ca < 250000:
                return "🟡 MOYENNE"
            else:
                return "🟢 BASSE"
        except:
            return "❓ INCONNU"

    if "CA_Actuel" in display_df.columns:
        display_df["Urgence"] = display_df["CA_Actuel"].apply(get_urgency_score)

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Filter par urgence
    st.markdown("### 🎯 Prospects par Urgence")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🔴 Haute Urgence")
        urgent_df = df[df["CA_Actuel"] < 200000] if "CA_Actuel" in df.columns else pd.DataFrame()
        for _, row in urgent_df.iterrows():
            st.write(f"**{row['Nom']}** | {row['Entreprise']}")
            st.caption(f"CA: €{int(row['CA_Actuel']):,} | {row['Email']}")

    with col2:
        st.markdown("#### 🟡 Moyenne Urgence")
        medium_df = df[(df["CA_Actuel"] >= 200000) & (df["CA_Actuel"] < 350000)] if "CA_Actuel" in df.columns else pd.DataFrame()
        for _, row in medium_df.iterrows():
            st.write(f"**{row['Nom']}** | {row['Entreprise']}")
            st.caption(f"CA: €{int(row['CA_Actuel']):,} | {row['Email']}")

    with col3:
        st.markdown("#### 🟢 Basse Urgence")
        low_df = df[df["CA_Actuel"] >= 350000] if "CA_Actuel" in df.columns else pd.DataFrame()
        for _, row in low_df.iterrows():
            st.write(f"**{row['Nom']}** | {row['Entreprise']}")
            st.caption(f"CA: €{int(row['CA_Actuel']):,} | {row['Email']}")

    # Export
    st.markdown("### 💾 Export")
    csv_export = df.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger CSV",
        data=csv_export,
        file_name=f"Leads_EAR_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

else:
    st.info("Aucun diagnostic réalisé pour le moment.")

st.markdown("---")
st.caption("EAR Dashboard | Accès réservé")
