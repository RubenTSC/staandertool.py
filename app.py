import math
import pandas as pd
import streamlit as st

# Profieldata (HEA en HEB, voorbeeldwaarden)
profiles = {
    "HEA100": {"type": "HEA", "Iy_cm4": 135, "A_cm2": 21.2},
    "HEA120": {"type": "HEA", "Iy_cm4": 238, "A_cm2": 27.6},
    "HEA140": {"type": "HEA", "Iy_cm4": 410, "A_cm2": 35.2},
    "HEA160": {"type": "HEA", "Iy_cm4": 655, "A_cm2": 43.6},
    "HEA180": {"type": "HEA", "Iy_cm4": 992, "A_cm2": 52.5},
    "HEA200": {"type": "HEA", "Iy_cm4": 1440, "A_cm2": 62.3},
    "HEA220": {"type": "HEA", "Iy_cm4": 2010, "A_cm2": 72.9},
    "HEA240": {"type": "HEA", "Iy_cm4": 2730, "A_cm2": 84.2},
    "HEA260": {"type": "HEA", "Iy_cm4": 3600, "A_cm2": 96.3},
    "HEA280": {"type": "HEA", "Iy_cm4": 4640, "A_cm2": 109},
    "HEA300": {"type": "HEA", "Iy_cm4": 5880, "A_cm2": 123},
    "HEB300": {"type": "HEB", "Iy_cm4": 7260, "A_cm2": 195},
    "HEB400": {"type": "HEB", "Iy_cm4": 18300, "A_cm2": 328},
    "HEB500": {"type": "HEB", "Iy_cm4": 33200, "A_cm2": 476},
}

E = 210000  # N/mm2

def lichte_staander(Ned_kN: float, hoogte_m: float, knikverkorter: bool = False):
    L = hoogte_m * 1000  # mm
    L_eff = L * (0.7 if knikverkorter else 1.0)

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
st.title("Lichtste veilige kolomselectie (knikcontrole)")

Ned_kN = st.number_input("Verticale belasting per kolom (kN)", min_value=10.0, max_value=3000.0, value=400.0, step=10.0)
hoogte_m = st.number_input("Kolomhoogte (m)", min_value=2.0, max_value=12.0, value=5.0, step=0.1)
knikverkorter = st.checkbox("Knikverkorter aanwezig?", value=True)

if st.button("Bepaal lichtste profiel"):
    resultaat = lichte_staander(Ned_kN, hoogte_m, knikverkorter)
    st.subheader("Resultaten (lichtste eerst)")
    st.dataframe(resultaat)
