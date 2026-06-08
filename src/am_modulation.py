"""
am_modulation.py
----------------
Implements AM DSB-TC (Double Sideband with Transmitted Carrier) modulation.

AM signal:
    s(t) = Ac × [1 + μ × sin(2π fm t)] × sin(2π fc t)
    where μ = Am / Ac  (modulation index)

MAKAUT EC401 Analog Communication – AM Modulation Module
"""

import numpy as np


def compute_modulation_index(Am: float, Ac: float) -> float:
    """
    Compute the AM modulation index.

    μ = Am / Ac

    Parameters
    ----------
    Am : float  – Message signal amplitude (V)
    Ac : float  – Carrier amplitude (V)

    Returns
    -------
    float
        Modulation index μ.
    """
    return Am / Ac


def am_modulate(
    t: np.ndarray,
    Am: float,
    Ac: float,
    fm: float,
    fc: float,
) -> tuple[np.ndarray, float]:
    """
    Perform AM DSB-TC modulation.

    s(t) = Ac × [1 + μ sin(2π fm t)] × sin(2π fc t)

    Parameters
    ----------
    t  : np.ndarray  – Time vector (s)
    Am : float       – Message amplitude (V)
    Ac : float       – Carrier amplitude (V)
    fm : float       – Message frequency (Hz)
    fc : float       – Carrier frequency (Hz)

    Returns
    -------
    s_t : np.ndarray  – AM modulated signal s(t)
    mu  : float       – Modulation index
    """
    mu = compute_modulation_index(Am, Ac)

    # Envelope = Ac × [1 + μ × sin(2π fm t)]
    envelope = Ac * (1.0 + mu * np.sin(2.0 * np.pi * fm * t))

    # Carrier
    carrier = np.sin(2.0 * np.pi * fc * t)

    # AM signal
    s_t = envelope * carrier

    return s_t, mu


def get_modulation_condition(mu: float) -> str:
    """
    Classify the modulation state based on μ.

    Parameters
    ----------
    mu : float  – Modulation index

    Returns
    -------
    str
        One of: 'Under Modulation', 'Critical Modulation', 'Over Modulation'
    """
    if abs(mu - 1.0) <= 0.02:
        return "Critical Modulation"
    elif mu < 1.0:
        return "Under Modulation"
    else:
        return "Over Modulation"
