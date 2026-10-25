"""
resonant_freq.py
----------------
Find the resonant frequency of a rectangular microstrip patch from its
dimensions and substrate.  (The inverse of patch_design.py.)

Required inputs:
    er  - relative permittivity
    L   - patch length (mm)   <- the resonance-determining dimension
    W   - patch width  (mm)   <- needed for eps_eff and fringing
    h   - substrate height (mm)

Model (transmission-line / Balanis):
    eps_eff = (er+1)/2 + (er-1)/2 * [1 + 12 h/W]^(-1/2)
    dL      = 0.412 h (eps_eff+0.3)(W/h+0.264) / [(eps_eff-0.258)(W/h+0.8)]
    f_r     = c / ( 2 (L + 2 dL) sqrt(eps_eff) )

Lengths in mm, frequency returned in GHz.
"""

import sys
from math import sqrt

C0_MM_GHZ = 299.792458          # c in mm*GHz


def resonant_frequency(er: float, L: float, W: float, h: float) -> dict:
    """Return the resonant frequency (GHz) and the intermediate values."""
    if er < 1 or L <= 0 or W <= 0 or h <= 0:
        raise ValueError("Need er>=1, L>0, W>0, h>0.")

    eps_eff = (er + 1.0) / 2.0 + (er - 1.0) / 2.0 * (1.0 + 12.0 * h / W) ** -0.5
    delta_L = 0.412 * h * ((eps_eff + 0.3) * (W / h + 0.264)) / \
        ((eps_eff - 0.258) * (W / h + 0.8))
    L_eff = L + 2.0 * delta_L
    f0 = C0_MM_GHZ / (2.0 * L_eff * sqrt(eps_eff))

    return {"f0": f0, "eps_eff": eps_eff, "delta_L": delta_L, "L_eff": L_eff}


def get_inputs():
    """Take er, L, W, h from the user (CLI args or prompt)."""
    if len(sys.argv) >= 5:
        return (float(sys.argv[1]), float(sys.argv[2]),
                float(sys.argv[3]), float(sys.argv[4]))
    er = float(input("Enter relative permittivity er: ").strip())
    L = float(input("Enter patch length L (mm): ").strip())
    W = float(input("Enter patch width  W (mm): ").strip())
    h = float(input("Enter substrate height h (mm): ").strip())
    return er, L, W, h


def main():
    er, L, W, h = get_inputs()
    r = resonant_frequency(er, L, W, h)

    print("\n=== Patch resonant frequency ===")
    print(f"  Permittivity er   : {er:7.2f}")
    print(f"  Patch length L    : {L:7.3f} mm")
    print(f"  Patch width  W    : {W:7.3f} mm")
    print(f"  Substrate h       : {h:7.3f} mm")
    print(f"  ---------------------------------")
    print(f"  eps_eff           : {r['eps_eff']:7.3f}")
    print(f"  Fringing dL       : {r['delta_L']:7.3f} mm")
    print(f"  Effective length  : {r['L_eff']:7.3f} mm  (L + 2dL)")
    print(f"  Resonant freq f0  : {r['f0']:7.3f} GHz\n")


if __name__ == "__main__":
    main()