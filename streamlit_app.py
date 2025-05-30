import streamlit as st
import pandas as pd

# Medikamentendaten
medikamente = pd.DataFrame({
    "Medikament": ["Propofol", "Ketamin"],
    "Dosis_mg_pro_kg": [2.0, 1.5],
    "Maximale_Dosis_mg": [200, 150],
    "Perfusor_Dosierung_mg_kg_h": [6.0, 0.5],  # Ziel-Dosierung
})

# Streamlit Setup
st.title("💉 Anästhesie-Rechner")

gewicht = st.number_input("Körpergewicht (kg)", min_value=1.0, max_value=300.0, step=0.1)

if gewicht:
    spritzenvolumen = st.selectbox("Spritzenvolumen (ml)", [20, 30, 50], index=2)

    for idx, row in medikamente.iterrows():
        with st.expander(f"🧪 {row['Medikament']}"):
            st.markdown(f"""
            **Ziel-Perfusordosis:** {row['Perfusor_Dosierung_mg_h_kg']} mg/kg/h  
            📝 *{row['Zusatzinfo']}*
            """)

            # Eingabe: Wirkstoffmenge in der Spritze (mg)
            wirkstoff_mg = st.slider(
                f"💊 Wirkstoffmenge in {spritzenvolumen} ml (mg)",
                min_value=0.0,
                max_value=1500.0,
                value=500.0,
                step=10.0,
                key=f"spritze_{idx}"
            )

            konzentration = wirkstoff_mg / spritzenvolumen  # mg/ml
            ziel_dosis_mg_h = row["Perfusor_Dosierung_mg_kg_h"] * gewicht
            laufrate_ml_h = ziel_dosis_mg_h / konzentration if konzentration > 0 else 0

            st.success(f"""
            🔸 Konzentration: {konzentration:.2f} mg/ml  
            🕒 Ziel-Dosierung: {ziel_dosis_mg_h:.2f} mg/h  
            💧 → Laufgeschwindigkeit: **{laufrate_ml_h:.2f} ml/h**
            """)
