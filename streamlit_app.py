import streamlit as st
import pandas as pd

# Medikamentendaten
medikamente = pd.DataFrame({
    "Medikament": ["Propofol", "Ketamin"],
    "Dosis_Bolus_mg_pro_kg_Bolus": [2.0, 1.5],
    "Dosis_mg_pro_kg": [2.0, 1.5],
    "Maximale_Dosis_mg": [200, 150],
    "Default_Dosierung_mg_kg_h": [6.0, 0.5],
})

# Fixes Spritzenvolumen
spritzenvolumen = 50  # ml

# Streamlit Setup
st.title("💉 Anästhesie-Rechner")

gewicht = st.number_input("Körpergewicht (kg)", min_value=1.0, max_value=300.0, step=1.0)

if gewicht:
    st.markdown(f"**Spritzenvolumen (fixiert):** {spritzenvolumen} ml")

    for idx, row in medikamente.iterrows():
        with st.expander(f"🧪 {row['Medikament']}"):
            # Ziel-Dosierung
            dosierung_mg_kg_h = st.slider(
                f"🎯 Ziel-Dosierung für {row['Medikament']} (mg/kg/h)",
                min_value=0.0,
                max_value=20.0,
                value=row["Default_Dosierung_mg_kg_h"],
                step=0.1,
                key=f"dosierung_{idx}"
            )

            ziel_dosis_mg_h = dosierung_mg_kg_h * gewicht

            # Wirkstoffmenge in der Spritze
            wirkstoff_mg = st.number_input(
                f"💊 Wirkstoffmenge in {spritzenvolumen} ml (mg)",
                min_value=1.0,
                max_value=2000.0,
                value=500.0,
                step=10.0,
                key=f"wirkstoff_{idx}"
            )

            # Berechnung
            bolusdosis = row["Dosis_Bolus_mg_pro_kg_Bolus"] * gewicht
            konzentration = wirkstoff_mg / spritzenvolumen
            laufrate_ml_h = ziel_dosis_mg_h / konzentration if konzentration > 0 else 0

            # Ausgabe in zwei Spalten
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 💥 Bolus")
                st.metric("Bolusdosis (mg)", f"{bolusdosis:.2f}")
                st.metric("Bolus (mg/kg)", f"{row['Dosis_Bolus_mg_pro_kg_Bolus']:.2f}")

            with col2:
                st.markdown("### 💧 Perfusor")
                st.metric("Zieldosierung (mg/kg/h)", f"{dosierung_mg_kg_h:.2f}")
                st.metric("Laufrate (ml/h)", f"{laufrate_ml_h:.2f}")
                st.metric("Konzentration (mg/ml)", f"{konzentration:.2f}")
