import math

E = 210000  # N/mm²
fy = 235    # N/mm²
gamma_M1 = 1.0
alpha = 0.49  # Buckling curve c

def bereken_kolomcapaciteit(A_cm2, iy_mm, L_m):
    A = A_cm2 * 100  # cm² naar mm²
    Leff = L_m * 1000  # in mm

    λ = Leff / iy_mm
    λ_rel = λ / (math.pi * math.sqrt(E / fy))

    phi = 0.5 * (1 + alpha * (λ_rel - 0.2) + λ_rel**2)
    chi = 1 / (phi + math.sqrt(phi**2 - λ_rel**2))
    chi = min(1.0, max(0.0, chi))

    NbRd_kN = chi * A * fy / gamma_M1 / 1000  # in kN
    return NbRd_kN, λ, λ_rel, chi
