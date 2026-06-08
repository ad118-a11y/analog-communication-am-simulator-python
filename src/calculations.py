"""
calculations.py
---------------
All analytical formulas for AM DSB-TC as per MAKAUT EC401 Analog Communication.

Formulas implemented
--------------------
  μ  = Am / Ac                         (modulation index)
  BW = 2 × fm                          (bandwidth)
  Pc = Ac² / (2R)                      (carrier power)
  Pt = Pc × (1 + μ²/2)                 (total transmitted power)
  Psb = Pt − Pc                        (total sideband power)
  η  = μ² / (2 + μ²)                   (transmission efficiency)
  η% = η × 100                         (efficiency in percent)
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Individual formula functions
# ---------------------------------------------------------------------------

def modulation_index(Am: float, Ac: float) -> float:
    """μ = Am / Ac"""
    return Am / Ac


def bandwidth(fm: float) -> float:
    """BW = 2 × fm  (Hz)"""
    return 2.0 * fm


def carrier_power(Ac: float, R: float) -> float:
    """Pc = Ac² / (2R)  (Watts)"""
    return (Ac ** 2) / (2.0 * R)


def total_power(Pc: float, mu: float) -> float:
    """Pt = Pc × (1 + μ²/2)  (Watts)"""
    return Pc * (1.0 + (mu ** 2) / 2.0)


def sideband_power(Pt: float, Pc: float) -> float:
    """Psb = Pt − Pc  (Watts)"""
    return Pt - Pc


def transmission_efficiency(mu: float) -> float:
    """η = μ² / (2 + μ²)  (dimensionless, 0–1)"""
    return (mu ** 2) / (2.0 + mu ** 2)


def modulation_condition(mu: float) -> str:
    """Classify modulation state."""
    if abs(mu - 1.0) <= 0.02:
        return "Critical Modulation"
    elif mu < 1.0:
        return "Under Modulation"
    else:
        return "Over Modulation"


# ---------------------------------------------------------------------------
# Aggregate function – returns a dict of all results
# ---------------------------------------------------------------------------

def compute_all(Am: float, Ac: float, fm: float, R: float) -> dict:
    """
    Compute all AM parameters and return as an ordered dict.

    Parameters
    ----------
    Am : float  – Message amplitude (V)
    Ac : float  – Carrier amplitude (V)
    fm : float  – Message frequency (Hz)
    R  : float  – Load resistance (Ω)

    Returns
    -------
    dict
        Keys are human-readable labels; values are floats or strings.
    """
    mu   = modulation_index(Am, Ac)
    bw   = bandwidth(fm)
    pc   = carrier_power(Ac, R)
    pt   = total_power(pc, mu)
    psb  = sideband_power(pt, pc)
    eta  = transmission_efficiency(mu)
    cond = modulation_condition(mu)

    return {
        "Modulation Index (μ)":         round(mu,      4),
        "Bandwidth BW (Hz)":            round(bw,      4),
        "Carrier Power Pc (W)":         round(pc,      6),
        "Total Transmitted Power Pt (W)": round(pt,    6),
        "Sideband Power Psb (W)":       round(psb,     6),
        "Efficiency η (%)":             round(eta * 100, 4),
        "Modulation Condition":         cond,
    }
