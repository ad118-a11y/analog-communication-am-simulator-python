"""
envelope_detector.py
--------------------
Implements a simple software envelope detector for AM DSB-TC signals.

Detection steps:
  1. Full-wave rectification  →  |r(t)|
  2. Low-pass filtering       →  smooth out the carrier ripple
  3. DC removal               →  remove the DC bias introduced by rectification
  4. Amplitude normalisation  →  scale recovered signal to match Am

This mirrors the behaviour of a diode + RC low-pass filter circuit that is the
standard envelope detector covered in MAKAUT EC401 Analog Communication.

MAKAUT EC401 Analog Communication – Envelope Detector Module
"""

import numpy as np
from scipy.signal import butter, filtfilt


def _design_lpf(cutoff_hz: float, fs: float, order: int = 4):
    """
    Design a Butterworth low-pass filter.

    Parameters
    ----------
    cutoff_hz : float  – Cutoff frequency (Hz)
    fs        : float  – Sampling frequency (Hz)
    order     : int    – Filter order

    Returns
    -------
    b, a  – Filter coefficients for scipy.signal.filtfilt
    """
    nyquist = fs / 2.0
    # Clamp normalised cutoff to a valid range
    wn = min(max(cutoff_hz / nyquist, 1e-4), 0.99)
    b, a = butter(order, wn, btype="low", analog=False)
    return b, a


def envelope_detect(
    received: np.ndarray,
    fs: float,
    fc: float,
    fm: float,
) -> np.ndarray:
    """
    Recover the envelope (message) from a received AM signal.

    Parameters
    ----------
    received : np.ndarray  – Noisy received AM signal r(t)
    fs       : float       – Sampling frequency (Hz)
    fc       : float       – Carrier frequency (Hz) – used to set LPF cutoff
    fm       : float       – Message frequency (Hz) – used to set LPF cutoff

    Returns
    -------
    np.ndarray
        Envelope-detected signal (DC removed, not yet amplitude-scaled).
    """
    # --- Step 1: Rectification (half-wave equivalent via abs = full-wave) ---
    rectified = np.abs(received)

    # --- Step 2: Low-pass filter ---
    # Cutoff must be:  fm  <  f_cutoff  <<  fc
    # We choose the geometric mean of fm and fc to stay safely between them.
    cutoff = min(
        np.sqrt(fm * fc),   # geometric mean heuristic
        fc * 0.35,          # hard upper bound: well below carrier
        fm * 10.0,          # hard upper bound: not too far from message
    )
    cutoff = max(cutoff, fm * 2.0)   # must be above fm to pass the signal

    b, a = _design_lpf(cutoff, fs, order=4)
    smoothed = filtfilt(b, a, rectified)

    # --- Step 3: Remove DC bias ---
    smoothed = smoothed - np.mean(smoothed)

    return smoothed


def normalize_to_amplitude(signal: np.ndarray, target_amplitude: float) -> np.ndarray:
    """
    Scale a signal so its peak matches target_amplitude.

    Parameters
    ----------
    signal           : np.ndarray  – Input signal
    target_amplitude : float       – Desired peak amplitude

    Returns
    -------
    np.ndarray
        Amplitude-normalised signal.
    """
    peak = np.max(np.abs(signal))
    if peak < 1e-12:
        return signal
    return signal * (target_amplitude / peak)
