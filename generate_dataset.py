import pandas as pd
from check_column_strength import bereken_kolomcapaciteit

# Parameters
L_values = [2.0, 2.5, 3.0, 3.5, 4.0]  # m
NEd_values = [100, 200, 300, 400, 500]  # kN

profielen_df = pd.read_csv("data/profiles.csv")

rows = []

for _, profiel in profielen_df.iterrows():
    for L in L_values:
        for NEd in NEd_values:
            NbRd, λ, λ_rel, chi = bereken_kolomcapaciteit(profiel['A[cm2]'], profiel['iy[mm]'], L)
            voldoende = NbRd >= NEd
            rows.append({
                'profiel': profiel['naam'],
                'L_m': L,
                'NEd_kN': NEd,
                'NbRd_kN': round(NbRd, 1),
                'lambda': round(λ, 1),
                'lambda_rel': round(λ_rel, 3),
                'chi': round(chi, 3),
                'voldoet': int(voldoende)
            })

df = pd.DataFrame(rows)
df.to_csv("kolom_dataset.csv", index=False)
print("Dataset gegenereerd: kolom_dataset.csv")
