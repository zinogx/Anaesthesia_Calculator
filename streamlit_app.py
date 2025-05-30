import streamlit as st
import pandas as pd

st.title("💊 Medikamentendosierung & Perfusor-Rechner")

# Körperdaten
gewicht = st.number_input("Körpergewicht (kg)", min_value=1.0, max_value=300.0, step=0.1, value=70.0)
groesse = st.number_input("Körpergröße (cm)", min_value=30.0, max_value=250.0, step=0.1, value=175.0)

# Medikamentendaten direkt im Code
medikamente = pd.DataFrame({
    "Medikament": ["Propofol", "Ketamin", "Midazolam", "Ondansetron"],
    "Dosis_mg_kg": [2.0, 1.0, 0.1, 0.15],
    "Max_Dosis_mg": [200, 100, 15, 8],
    "Perfusor_mg_kg_h": [3.0, 0.5, 0.05, 0.0],  # Zielwertvorschlag (anpassbar)
    "Standard_Konz_mg_ml": [10, 50, 1, 2]  # Beispielkonzentrationen
})

if gewicht and groesse:
    st.subheader("📋 Dosierung & Perfusor je Medikament")

    for _, row in medikamente.iterrows():
        name = row["Medikament"]
        st.markdown(f"### 💉 {name}")

        # Bolus-Dosisberechnung
        berechnete_dosis = row["Dosis_mg_kg"] * gewicht
        empfohlene_dosis = min(berechnete_dosis, row["Max_Dosis_mg"])

        st.write(f"**Empfohlene Bolus-Dosis:** {empfohlene_dosis:.2f} mg "
                 f"(Berechnet: {berechnete_dosis:.2f} mg, Max: {row['Max_Dosis_mg']} mg)")

        # Perfusor: Schieberegler für Konzentration
        konzentration = st.slider(
            f"Konzentration in der Spritze (mg/ml) – {name}",
            min_value=1.0, max_value=100.0,
            value=row["Standard_Konz_mg_ml"], step=1.0,
            key=f"konz_{name}"
        )

        # Schieberegler für Zieldosierung in mg/kg/h
        ziel_dosis_mg_kg_h = st.slider(
            f"Ziel-Perfusordosis (mg/kg/h) – {name}",
            min_value=0.0, max_value=20.0, step=0.1,
            value=row["Perfusor_mg_kg_h"],
            key=f"dosis_{name}"
        )

        # Berechnung Laufgeschwindigkeit
        zieldosis_mg_h = ziel_dosis_mg_kg_h * gewicht
        laufrate_ml_h = zieldosis_mg_h / konzentration if konzentration > 0 else 0

        st.write(f"💧 **Laufrate Perfusor:** {laufrate_ml_h:.2f} ml/h "
                 f"(Zieldosis: {zieldosis_mg_h:.2f} mg/h bei {konzentration:.1f} mg/ml)")

        st.divider()
