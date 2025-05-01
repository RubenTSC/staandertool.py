import math
import pandas as pd
import streamlit as st
import json

# Profieldata laden uit extern JSON-bestand
with open("uitgebreide_profielen_HEA_HEB.json", "r") as f:
    profiles = json.load(f)

E = 210000  # N/mm2

def lichte_staander(Ned_kN: float, hoogte_m: float):
    L = hoogte_m * 1000  # mm
    L_eff = L  # Geen knikverkorter

    resultaten = []
    for naam, props in profiles.items():
        I_mm4 = props["Iy_cm4"] * 1e4
        A_mm2 = props["A_cm2"] * 100

        Ncr = (math.pi ** 2 * E * I_mm4) / (L_eff ** 2)  # in N
        utilisation = (Ned_kN * 1000) / Ncr
        veilig = utilisation <= 1.0

        if veilig:
            resultaten.append({
                "Profiel": naam,
                "Profieltype": props["type"],
                "Utilisatie": round(utilisation, 2),
                "Ncr_kN": round(Ncr / 1000, 1),
                "A_cm2": props["A_cm2"]
            })

    if not resultaten:
        return pd.DataFrame([{"Profiel": "GEEN", "Profieltype": "-", "Utilisatie": "-", "Ncr_kN": "-", "A_cm2": "-"}])

    df = pd.DataFrame(resultaten)
    df = df.sort_values("A_cm2")
    return df.reset_index(drop=True)

# Streamlit interface
st.title("Lichtste veilige kolom (zonder knikverkorter)")

Ned_kN = st.number_input("Verticale belasting per kolom (kN)", min_value=10.0, max_value=25000.0, value=400.0, step=10.0)
hoogte_m = st.number_input("Kolomhoogte (m)", min_value=2.0, max_value=20.0, value=5.0, step=0.1)

if st.button("Bepaal lichtste profiel"):
    resultaat = lichte_staander(Ned_kN, hoogte_m)
    st.subheader("Resultaten (lichtste eerst)")
    st.dataframe(resultaat)
