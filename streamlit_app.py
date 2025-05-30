import streamlit as st
import pandas as pd

# Medikamentendaten
medikamente = pd.DataFrame({
    "Medikament": ["Propofol", "Ketamin"],
    "Dosis_mg_pro_kg": [2.0, 1.5],
    "Maximale_Dosis_mg": [200, 150],
    "Perfusor_Dosierung_mg_kg_h": [6.0, 0.5],  # Ziel-Dosierung in mg/kg/h
})

# Fixes Spritzenvolumen für Perfusoren
spritzenvolumen = 50  # ml

# Streamlit Setup
st.title("💉 Anästhesie-Rechner")

gewicht = st.number_input("Körpergewicht (kg)", min_value=1.0, max_value=300.0, step=0.1)

if gewicht:
    st.markdown(f"**Spritzenvolumen (fixiert):** {spritzenvolumen} ml")

    for idx, row in medikamente.iterrows():
        with st.expander(f"🧪 {row['Medikament']}"):
            ziel_dosierung = row["Perfusor_Dosierung_mg_kg_h"]  # mg/kg/h
            ziel_dosis_mg_h = ziel_dosierung * gewicht          # mg/h

            # Eingabe: Wirkstoffmenge in der Spritze (mg) → z. B. 500 mg in 50 ml
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

            st.markdown(f"""
            **Ziel-Dosierung:** {ziel_dosierung:.2f} mg/kg/h  
            🧠 Für {gewicht:.1f} kg: {ziel_dosis_mg_h:.2f} mg/h  
            💉 Konzentration: {konzentration:.2f} mg/ml  
            💧 **Laufgeschwindigkeit:** {laufrate_ml_h:.2f} ml/h
            """)
