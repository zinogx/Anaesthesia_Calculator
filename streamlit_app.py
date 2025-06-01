import streamlit as st
import pandas as pd

# Medikamentendaten (ggf. später getrennt für Kinder/Erwachsene anpassen)
medikamente = pd.DataFrame({
    "Medikament": ["Propofol", "Ketamin"],
    "Dosis_Bolus_mg_pro_kg_Bolus": [2.5, 0.25],
    "Min_Dosis_Bolus_mg_pro_kg_Bolus": [1.5, 0.25],
    "Max_Dosis_Bolus_mg_pro_kg_Bolus": [3, 0.25],
    "Default_Dosierung_mg_kg_h": [4.0, 0.5],
    "Min_Dosierung_mg_kg_h": [4.0, 0],
    "Max_Dosierung_mg_kg_h": [12.0, 0],
})

spritzenvolumen = 50  # ml

st.title("💉 Anästhesie-Rechner")

# Tabs erstellen
tabs = st.tabs(["🧔 Erwachsene", "🧒 Kinder"])

for i, tab in enumerate(tabs):
    with tab:
        st.subheader("📏 Patientendaten")

        gewicht = st.number_input(
            "Körpergewicht (kg)",
            min_value=1.0,
            max_value=300.0,
            step=1.0,
            key=f"gewicht_{i}"
        )

        if gewicht:
            st.markdown(f"**Spritzenvolumen (fixiert):** {spritzenvolumen} ml")

            for idx, row in medikamente.iterrows():
                with st.expander(f"🧪 {row['Medikament']}"):
                    dosierung_mg_kg_h = st.slider(
                        f"🎯 Ziel-Dosierung für {row['Medikament']} (mg/kg/h)",
                        min_value=0.0,
                        max_value=20.0,
                        value=row["Default_Dosierung_mg_kg_h"],
                        step=0.1,
                        key=f"dosierung_{i}_{idx}"
                    )

                    ziel_dosis_mg_h = dosierung_mg_kg_h * gewicht

                    wirkstoff_mg = st.number_input(
                        f"💊 Wirkstoffmenge in {spritzenvolumen} ml (mg)",
                        min_value=1.0,
                        max_value=2000.0,
                        value=500.0,
                        step=10.0,
                        key=f"wirkstoff_{i}_{idx}"
                    )

                    bolusdosis = row["Dosis_Bolus_mg_pro_kg_Bolus"] * gewicht
                    konzentration = wirkstoff_mg / spritzenvolumen
                    laufrate_ml_h = ziel_dosis_mg_h / konzentration if konzentration > 0 else 0

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 💥 Bolus")
                        st.metric("Bolusdosis (mg)", f"{bolusdosis:.2f}")
                        st.metric("Bolusdosis (mg/kg)", f"{row['Dosis_Bolus_mg_pro_kg_Bolus']:.2f}")

                        min_bolus = row.get("Min_Dosis_Bolus_mg_pro_kg_Bolus")
                        max_bolus = row.get("Max_Dosis_Bolus_mg_pro_kg_Bolus")
                        if pd.notna(min_bolus) and pd.notna(max_bolus):
                            st.markdown(f"🟢 **Empf. Bereich:** {min_bolus}–{max_bolus} mg/kg")

                    with col2:
                        st.markdown("### 💧 Perfusor")
                        st.metric("Zieldosierung (mg/kg/h)", f"{dosierung_mg_kg_h:.2f}")
                        st.metric("Laufrate (ml/h)", f"{laufrate_ml_h:.2f}")
                        st.metric("Konzentration (mg/ml)", f"{konzentration:.2f}")

                        min_perf = row.get("Min_Dosierung_mg_kg_h")
                        max_perf = row.get("Max_Dosierung_mg_kg_h")
                        if pd.notna(min_perf) and pd.notna(max_perf):
                            st.markdown(f"🟢 **Empf. Bereich:** {min_perf}–{max_perf} mg/kg/h")
