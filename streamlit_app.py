import streamlit as st
import pandas as pd

# Medikamentendaten
medikamente = pd.DataFrame({
    "Medikament": ["Propofol", "Ketamin"],
    "Dosis_mg_pro_kg": [2.0, 1.5],
    "Maximale_Dosis_mg": [200, 150],
    "Default_Dosierung_mg_kg_h": [6.0, 0.5],  # Vorschlagswert für Schieberegler
})

# Fixes Spritzenvolumen
spritzenvolumen = 50  # ml

# Streamlit Setup
st.title("💉 Anästhesie-Rechner")

gewicht = st.number_input("Körpergewicht (kg)", min_value=1.0, max_value=300.0, step=0.1)

if gewicht:
    st.markdown(f"**Spritzenvolumen (fixiert):** {spritzenvolumen} ml")

    for idx, row in medikamente.iterrows():
        with st.expander(f"🧪 {row['Medikament']}"):
            # Benutzer wählt die Ziel-Dosierung (mg/kg/h)
            dosierung_mg_kg_h = st.slider(
                f"🎯 Ziel-Dosierung für {row['Medikament']} (mg/kg/h)",
                min_value=0.0,
                max_value=20.0,
                value=row["Default_Dosierung_mg_kg_h"],
                step=0.1,
                key=f"dosierung_{idx}"
            )

            ziel_dosis_mg_h = dosierung_mg_kg_h * gewicht

            # Eingabe: Wirkstoffmenge in der Spritze (mg)
            wirkstoff_mg = st.number_input(
                f"💊 Wirkstoffmenge in {spritzenvolumen} ml (mg)",
                min_value=1.0,
                max_value=2000.0,
                value=500.0,
                step=10.0,
                key=f"wirkstoff_{idx}"
            )

            konzentration = wirkstoff_mg / spritzenvolumen  # mg/ml
            laufrate_ml_h = ziel_dosis_mg_h / konzentration if konzentration > 0 else 0

            st.success(f"""
            🔸 **Zieldosierung:** {dosierung_mg_kg_h:.2f} mg/kg/h  
            🔸 **Gesamtdosis:** {ziel_dosis_mg_h:.2f} mg/h  
            🔸 **Konzentration:** {konzentration:.2f} mg/ml  
            💧 → **Laufrate:** {laufrate_ml_h:.2f} ml/h
            """)
