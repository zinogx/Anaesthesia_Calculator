import streamlit as st
import pandas as pd

# Beispielhafte Medikamentendaten für Erwachsene
medikamente_erwachsene = pd.DataFrame({
    "Medikament": ["Propofol", "Ketamin", "Sufentanil", "Remifentanil", "Rocuronium", "Cisatracurium"],
    "Gruppe": ["Hypnotika", "Hypnotika", "Opioide", "Opioide", "Muskelrelaxantien", "Muskelrelaxantien"],
    "Dosis_Bolus_mg_pro_kg_Bolus": [2.0, 1.5, 0.5, 1.0, 0.6, 0.15],
    "Default_Dosierung_mg_kg_h": [6.0, 0.5, 0.2, 0.3, 0.0, 0.0],
})

# Beispielhafte Medikamentendaten für Kinder (andere Bolusdosen!)
medikamente_kinder = pd.DataFrame({
    "Medikament": ["Propofol", "Thiopental, "Ketamin", "Sufentanil", "Remifentanil", "Rocuronium", "Cisatracurium"],
    "Gruppe": ["Hypnotika", "Hypnotika", "Hypnotika", "Opioide", "Opioide", "Muskelrelaxantien", "Muskelrelaxantien"],
    "Dosis_Bolus_mg_pro_kg_Bolus": [3.0, 36.0, 2.0, 0.3, 0.5, 0.3, 0.1],
    "Default_Dosierung_mg_kg_h": [8.0, 0.0,  1.0, 0.1, 0.2, 0.0, 0.0],
})

spritzenvolumen = 50  # ml

st.title("💉 Anästhesie-Rechner")

gewicht = st.number_input("Körpergewicht (kg)", min_value=1.0, max_value=300.0, step=1.0)

tabs = st.tabs(["👶 Kinder", "🧍 Erwachsene"])

for tab, daten, label in zip(tabs, [medikamente_kinder, medikamente_erwachsene], ["Kinder", "Erwachsene"]):
    with tab:
        if gewicht:
            st.markdown(f"**Spritzenvolumen (fixiert):** {spritzenvolumen} ml")

            gruppen = daten["Gruppe"].unique()
            for gruppe in gruppen:
                st.header(f"🧪 {gruppe}")
                gruppe_df = daten[daten["Gruppe"] == gruppe]

                for idx, row in gruppe_df.iterrows():
                    with st.expander(f"{row['Medikament']}"):
                        dosierung_mg_kg_h = st.slider(
                            f"🎯 Ziel-Dosierung für {row['Medikament']} (mg/kg/h)",
                            min_value=0.0,
                            max_value=20.0,
                            value=row["Default_Dosierung_mg_kg_h"],
                            step=0.1,
                            key=f"{label}_dosierung_{row['Medikament']}"
                        )

                        ziel_dosis_mg_h = dosierung_mg_kg_h * gewicht

                        wirkstoff_mg = st.number_input(
                            f"💊 Wirkstoffmenge in {spritzenvolumen} ml (mg)",
                            min_value=1.0,
                            max_value=2000.0,
                            value=500.0,
                            step=10.0,
                            key=f"{label}_wirkstoff_{row['Medikament']}"
                        )

                        konzentration = wirkstoff_mg / spritzenvolumen  # mg/ml
                        laufrate_ml_h = ziel_dosis_mg_h / konzentration if konzentration > 0 else 0
                        bolusdosis_mg = row["Dosis_Bolus_mg_pro_kg_Bolus"] * gewicht
                        bolus_volumen_ml = bolusdosis_mg / konzentration if konzentration > 0 else 0

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("### 💥 Bolus")
                            st.metric("Konzentration in Bolus-Spritze (mg/ml)", f"{konzentration:.2f}")
                            st.metric("Bolusdosis (mg/kg)", f"{row['Dosis_Bolus_mg_pro_kg_Bolus']:.2f}")
                            st.metric("Bolusdosis gesamt (mg)", f"{bolusdosis_mg:.2f}")
                            st.metric("Volumen für Bolusgabe (ml)", f"{bolus_volumen_ml:.2f}")

                        with col2:
                            st.markdown("### 💧 Perfusor")
                            st.metric("Zieldosierung (mg/kg/h)", f"{dosierung_mg_kg_h:.2f}")
                            st.metric("Gesamtdosis (mg/h)", f"{ziel_dosis_mg_h:.2f}")
                            st.metric("Laufrate (ml/h)", f"{laufrate_ml_h:.2f}")
                            st.metric("Konzentration (mg/ml)", f"{konzentration:.2f}")
