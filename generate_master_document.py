#!/usr/bin/env python3
"""
Génère le "Grand Document de Présentation" pour Nathalie
Utilise l'API Anthropic (Claude Sonnet 3.5) pour créer le document maître
"""

import anthropic
import os
from datetime import datetime

def generate_master_presentation_document():
    """Génère le document stratégique complet pour Nathalie"""

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = """Tu es un Strategic Advisor pour Nathalie Lourdel, fondatrice d'EAR avec 21 ans d'expertise.

Tu viens de finaliser une analyse stratégique complète. Maintenant, tu dois générer le "GRAND DOCUMENT DE PRÉSENTATION"
qui synthétise TOUT en une présentation irrésistible pour dimanche.

CONTEXTE STRATÉGIQUE À INTÉGRER:

1. LEVIER LINKEDIN ADS (300€/mois dormant)
   - Stratégie: Ads de contenu expertise (pas "cliquez ici")
   - Cible: DRH tech/RH mid-size
   - ROI: 80-100 clics/mois → 2-3 JD participants → 14-25k€/an CA

2. EXPLOITATION BAGAGE NATHALIE (21 ans certifiés Qualiopi)
   - Master Class Machine: Repurposer contenu existant → 2000€/place
   - Alumni Program: 45 contacts à activer → 91-105k€ CA supplémentaire
   - Newsletter automatisée + clips vendables

3. SCÉNARIO C IMPLACABLE
   - Déléguer 10h/semaine à VA → 200k€ → 320k€ CA
   - Libération: 15-20h/semaine pour livre + famille
   - Pas burnout (50H/week durable vs 75H actuel)

4. MESSAGE CLÉ
   - Pas parler "technique"
   - Parler "LIBÉRATION"
   - Tech = collaborateur invisible
   - Fait le travail de relance alumni
   - Cherche DRH sur LinkedIn
   - Calcule ROI temps réel

STRUCTURE DU DOCUMENT À GÉNÉRER:

1. TITRE + CONTEXTE (1 page)
   - Situation actuelle (200k€, 75H/week, bloquée)
   - Vision (320k€, 50H/week, libre)

2. LES 5 LEVIERS RÉELS + NOUVEAUX LEVIERS (5 pages)
   - Coaching tarif: +30k€
   - Master classes: +48k€
   - Alumni activation: +91k€
   - DRH B2B: +40k€
   - EAR formation: +98k€
   - PLUS: LinkedIn Ads: +14-25k€/an
   - PLUS: Master Class Machine: +déjà compté
   - PLUS: Alumni automation: +déjà compté

3. LA "VRAIE MATH" - CALCULATEUR ROI (3 pages)
   - Coût du statu quo: 75H/week × 52 = 3900H/an pour 200k€ = 51€/H
   - Coût du scenario C: 50H/week × 52 = 2600H/an pour 320k€ = 123€/H
   - VA cost: 24k€/an
   - Net gain: +96k€ profit, -1300H effort, +40H liberté

4. PLAN 12 MOIS OPÉRATIONNEL (4 pages)
   - Mois 1 (Avril): Decision + Setup (VA hiring, CRM, DRH list)
   - Mois 2-3 (Mai-Juin): First wins (+32k€)
   - Mois 4-6 (Juil-Sep): Scaling (+61k€)
   - Mois 7-9 (Oct-Dec): Closing + 2027 planning (+55k€)
   - Total year 1: 320k€ CA

5. LES 3 SCÉNARIOS (3 pages)
   A) Status quo: 200k€, 75H/week, burnout W8-W16
   B) Learn tech: 210k€, 75H/week, +200H lost, distraction
   C) Focus+déléguer: 320k€, 50H/week, durable, VIABLE

6. LA MACHINE INVISIBLE (2 pages)
   - LinkedIn Ads automation: cherche DRH pendant qu'elle coache
   - Alumni newsletter: relance automatisée
   - Master class clips: contenu vendable généré
   - ROI dashboard: calculs temps réel
   - Quoi elle ne fait PAS: technique, code, automation
   - Quoi elle FAIT: Coaching, Master classes, Relations

7. L'APPEL À L'ACTION (1 page)
   - Dimanche 27 avril: décision
   - Lundi 28 avril: lancement
   - Message: "Vous pouvez rester à 200k€ seule, ou à 320k€ avec une VA"
   - C'est pas une décision technique, c'est une décision de VIE

TONE:
- Expert mais bienveillant
- Direct et sans concession
- Data-driven (chiffres précis, pas vague)
- Perspicace (voir les paradoxes)
- Français professionnel, dynamique
- Inspirant (pas prescriptif)

Longueur: 15-20 pages, ~6000-7000 mots
Format: Texte brut, prêt pour PDF

Générez ce document maintenant."""

    message = client.messages.create(
        model="claude-opus-4-1",
        max_tokens=8000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    document_text = message.content[0].text

    # Sauvegarder le document
    output_path = "/Users/emmanuelklein/EAR NATHALIE/GRAND_DOCUMENT_PRESENTATION_2026.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("GRAND DOCUMENT DE PRÉSENTATION — NATHALIE LOURDEL\n")
        f.write("Dimanche 27 avril 2026\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Généré: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        f.write(document_text)

    print(f"✅ Document généré: {output_path}")
    return document_text

if __name__ == "__main__":
    doc = generate_master_presentation_document()
    print("\n" + "=" * 80)
    print("DOCUMENT GÉNÉRÉ AVEC SUCCÈS")
    print("=" * 80)
