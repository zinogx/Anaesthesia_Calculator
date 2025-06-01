import streamlit as st
import pandas as pd

# Medikamentendaten für Erwachsene
medikamente_erwachsene = pd.DataFrame({
    "Medikament": ["Propofol", "Ketamin", "Remifentanil", "Sufentanil"],
    "Gruppe": ["Hypnotika", "Hypnotika", "Opioide", "Opioide"],
    "Dosis_Bolus_mg_pro_kg_Bolus": [2.0, 1.5, 1.0, 0.5],
    "Maximale_Dosis_mg": [200, 150, 15, 10],
    "Default_Dosierung_mg_kg_h": [6.0, 0.5, 0.12, 0.06],
    "Einheit": ["mg/kg/h", "mg/kg/h", "µg/kg/min", "µg/kg/min"]
})

# Medikamentendaten für Kinder
medikamente_kinder = pd.DataFrame({
    "Medikament": ["Midazolam", "Clonidin", "Lorazepam", "Esketamin", "Methohexital", "Diazepam", "Chloralhydrat", "Promethazin", "Levomepromazin",
                   "Thiopental", "Propofol", "Etomidate", "Mivacurium", "Rocuronium", "Succinylcholin", "Fentanyl", "Sufentanil", "Remifentanil"],
    "Gruppe": ["Sedativa"]*9 + ["Hypnotika"]*3 + ["Relaxantien"]*3 + ["Opioide"]*3,
    "Dosis_Bolus_mg_pro_kg_Bolus": [0.5, 0.004, 0.1, 4.0, 30.0, 0.5, 50.0, 1.0, 1.0,
                                    7.0, 6.0, 0.3, 0.2, 0.9, 2.0, 5.0, 1.0, 2.0],
    "Maximale_Dosis_mg": [15, None, 2.5, None, None, None, None, None, None,
                          None, None, None, None, None, None, None, None, None],
    "Default_Dosierung_mg_kg_h": [None]*10 + [8.0, None, None, None, None, None, 1.0, 0.12],
    "Einheit": ["mg/kg", "µg/kg", "mg/kg", "mg/kg", "mg/kg", "mg/kg", "mg/kg", "mg/kg", "mg/kg",
                "mg/kg", "mg/kg/h", "mg/kg", "mg/kg", "mg/kg", "mg/kg", "µg/kg", "µg/kg/h", "µg/kg/min"]
})

spritzenvolumen = 50  # ml

st.set_page_config(page_title="Anästhesie-Rechner", layout="wide")
st.title("💉 Anästhesie-Rechner")

tabs = st.tabs(["👤 Erwachsene", "🧒 Kinder"])
tab_daten = [medikamente_erwachsene, medikamente_kinder]
tab_labels = ["Erwachsene", "Kinder"]

for tab, medikamente, label in zip(tabs, tab_daten, tab_labels):
    with tab:
        st.header(f"Berechnung für {label}")
        gewicht = st.number_input(f"Körpergewicht ({label}) in kg", min_value=1.0, max_value=300.0, step=1.0, key=f"gewicht_{label}")

        if gewicht:
            st.markdown(f"**Fixiertes Spritzenvolumen (Perfusor):** {spritzenvolumen} ml")

            gruppen = medikamente["Gruppe"].unique()
            for gruppe in gruppen:
                with st.expander(f"🧪 {gruppe}", expanded=True):
                    df_gruppe = medikamente[medikamente["Gruppe"] == gruppe]
                    for idx, row in df_gruppe.iterrows():
                        st.markdown(f"### 💊 {row['Medikament']}")
                        einheit = row.get("Einheit", "mg/kg/h")
                        unique_key = f"{label}_{row['Medikament']}_{idx}"

                        if pd.isna(row["Default_Dosierung_mg_kg_h"]):
                            continue

                        if einheit == "µg/kg/min":
                            dosierung_ug_kg_min = st.slider(
                                "Ziel-Dosierung (ug/kg/min)", 0.0, 5.0,
                                value=row["Default_Dosierung_mg_kg_h"] * 1000 / 60,
                                step=0.01, key=f"{unique_key}_slider")
                            ziel_dosis_mg_h = dosierung_ug_kg_min * gewicht / 1000 * 60
                            dosierung_mg_kg_h = ziel_dosis_mg_h / gewicht
                        else:
                            dosierung_mg_kg_h = st.slider(
                                "Ziel-Dosierung (mg/kg/h)", 0.0, 20.0,
                                value=row["Default_Dosierung_mg_kg_h"],
                                step=0.1, key=f"{unique_key}_slider")
                            ziel_dosis_mg_h = dosierung_mg_kg_h * gewicht

                        wirkstoff_mg_perfusor = st.number_input(
                            f"Wirkstoffmenge in Perfusor (mg / {spritzenvolumen} ml)",
                            min_value=1.0, max_value=2000.0,
                            value=500.0, step=10.0, key=f"{unique_key}_perfusor_mg")
                        konzentration_perfusor = wirkstoff_mg_perfusor / spritzenvolumen
                        laufrate_ml_h = ziel_dosis_mg_h / konzentration_perfusor if konzentration_perfusor > 0 else 0

                        konzentration_bolus = st.number_input(
                            "Konzentration der Bolus-Spritze (mg/ml)",
                            min_value=0.1, max_value=100.0,
                            value=konzentration_perfusor, step=0.1,
                            key=f"{unique_key}_konz_bolus")

                        bolusdosis_mg = row["Dosis_Bolus_mg_pro_kg_Bolus"] * gewicht
                        bolus_volumen_ml = bolusdosis_mg / konzentration_bolus if konzentration_bolus > 0 else 0

                        st.markdown("#### 💥 Bolus")
                        st.table({
                            "Parameter": ["Bolusdosis (mg/kg)", "Bolusdosis gesamt (mg)", "Volumen für Bolusgabe (ml)", "Konzentration Bolus-Spritze (mg/ml)"],
                            "Wert": [
                                f"{row['Dosis_Bolus_mg_pro_kg_Bolus']:.2f}",
                                f"{bolusdosis_mg:.2f}",
                                f"{bolus_volumen_ml:.2f}",
                                f"{konzentration_bolus:.2f}"
                            ]
                        })

                        st.markdown("#### 💧 Perfusor")
                        st.table({
                            "Parameter": [
                                "Zieldosierung ({})".format(einheit),
                                "Gesamtdosis (mg/h)",
                                "Konzentration Perfusor (mg/ml)",
                                "Laufrate (ml/h)"
                            ],
                            "Wert": [
                                f"{dosierung_ug_kg_min:.2f}" if einheit == "µg/kg/min" else f"{dosierung_mg_kg_h:.2f}",
                                f"{ziel_dosis_mg_h:.2f}",
                                f"{konzentration_perfusor:.2f}",
                                f"{laufrate_ml_h:.2f}"
                            ]
                        })
