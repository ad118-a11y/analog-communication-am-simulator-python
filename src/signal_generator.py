"""
signal_generator.py
-------------------
Generates the fundamental signals used in the AM simulation:
  - Time vector
  - Message signal m(t) = Am * sin(2π fm t)
  - Carrier signal c(t) = Ac * sin(2π fc t)

MAKAUT EC401 Analog Communication – Signal Generation Module
"""

import numpy as np


def generate_time_vector(duration: float, fs: float) -> np.ndarray:
    """
    Generate a uniformly spaced time vector.

    Parameters
    ----------
    duration : float
        Total duration of the signal in seconds.
    fs : float
        Sampling frequency in Hz.

    Returns
    -------
    np.ndarray
        Time vector from 0 to duration (endpoint excluded).
    """
    num_samples = int(fs * duration)
    return np.linspace(0, duration, num_samples, endpoint=False)


def generate_message_signal(t: np.ndarray, Am: float, fm: float) -> np.ndarray:
    """
    Generate the message (modulating) signal.

    m(t) = Am × sin(2π fm t)

    Parameters
    ----------
    t  : np.ndarray  – Time vector (s)
    Am : float       – Message signal amplitude (V)
    fm : float       – Message signal frequency (Hz)

    Returns
    -------
    np.ndarray
        Message signal m(t).
    """
    return Am * np.sin(2.0 * np.pi * fm * t)


def generate_carrier_signal(t: np.ndarray, Ac: float, fc: float) -> np.ndarray:
    """
    Generate the carrier signal.

    c(t) = Ac × sin(2π fc t)

    Parameters
    ----------
    t  : np.ndarray  – Time vector (s)
    Ac : float       – Carrier amplitude (V)
    fc : float       – Carrier frequency (Hz)

    Returns
    -------
    np.ndarray
        Carrier signal c(t).
    """
    return Ac * np.sin(2.0 * np.pi * fc * t)
