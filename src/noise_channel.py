"""
noise_channel.py
----------------
Models the noisy channel that the AM signal passes through.

Channel model:
    r(t) = s(t) + n(t)
    where n(t) is additive white Gaussian noise (AWGN).

A fixed random seed ensures reproducibility — the noise pattern
does not change on every Streamlit rerender unless the seed is changed.

MAKAUT EC401 Analog Communication – Noisy Channel Module
"""

import numpy as np


def add_awgn(
    signal: np.ndarray,
    noise_level: float,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Add Additive White Gaussian Noise (AWGN) to the transmitted signal.

    r(t) = s(t) + n(t)

    Parameters
    ----------
    signal      : np.ndarray  – Transmitted AM signal s(t)
    noise_level : float       – Standard deviation of the Gaussian noise
    seed        : int         – Random seed for reproducibility (default: 42)

    Returns
    -------
    r_t   : np.ndarray  – Received noisy signal r(t)
    noise : np.ndarray  – Noise component n(t)
    """
    rng = np.random.default_rng(seed)
    noise = noise_level * rng.standard_normal(len(signal))
    r_t = signal + noise
    return r_t, noise


def compute_snr_db(signal: np.ndarray, noise: np.ndarray) -> float:
    """
    Compute Signal-to-Noise Ratio (SNR) in dB.

    SNR_dB = 10 × log10(P_signal / P_noise)

    Parameters
    ----------
    signal : np.ndarray  – Original signal
    noise  : np.ndarray  – Noise component

    Returns
    -------
    float
        SNR in dB. Returns inf if noise power is zero.
    """
    p_signal = np.mean(signal ** 2)
    p_noise = np.mean(noise ** 2)
    if p_noise == 0:
        return float("inf")
    return 10.0 * np.log10(p_signal / p_noise)
