# Technical Explanation: AM Transmitter & Receiver Simulator

## MAKAUT EC401 – Analog Communication

---

## 1. Introduction

Amplitude Modulation (AM) is one of the oldest and most fundamental modulation techniques in analog communication. In AM, the **amplitude** of a high-frequency carrier signal is varied in proportion to the instantaneous amplitude of the low-frequency message (information) signal.

This document provides a detailed technical explanation of every stage in the simulated AM communication chain.

---

## 2. Why Modulation is Needed

Direct transmission of low-frequency message signals (audio, speech) is impractical because:

1. **Antenna size**: An efficient antenna must be approximately λ/4 in length. For 5 Hz audio, λ = c/f = 3×10⁸/5 = 60,000 km — physically impossible.
2. **Bandwidth overlap**: Multiple signals at audio frequencies would interfere with each other.
3. **Propagation**: Low-frequency electromagnetic waves do not propagate efficiently.

By shifting the message to a high carrier frequency, compact antennas become feasible and multiple channels can coexist on different carrier frequencies.

---

## 3. Signal Generation

### Message Signal
```
m(t) = Aₘ × sin(2π fₘ t)
```
- Aₘ: Message amplitude (V)
- fₘ: Message frequency (Hz)
- Represents the information to be transmitted (e.g., audio)

### Carrier Signal
```
c(t) = Aꜝ × sin(2π fꜝ t)
```
- Aꜝ: Carrier amplitude (V)
- fꜝ: Carrier frequency (Hz), must be >> fₘ
- The carrier is the "vehicle" that transports the message

---

## 4. AM DSB-TC Modulation

### Modulation Index
```
μ = Aₘ / Aꜝ
```

### AM Signal
```
s(t) = Aꜝ [1 + μ sin(2π fₘ t)] sin(2π fꜝ t)
```

Expanding:
```
s(t) = Aꜝ sin(2π fꜝ t)                               ← Carrier
      + (Aꜝ μ / 2) cos[2π (fꜝ - fₘ) t]               ← Lower sideband
      − (Aꜝ μ / 2) cos[2π (fꜝ + fₘ) t]               ← Upper sideband
```

This reveals the three frequency components in AM:
- Carrier at fꜝ
- Lower Sideband (LSB) at fꜝ − fₘ
- Upper Sideband (USB) at fꜝ + fₘ

### Modulation Conditions

| Condition | μ value | Effect |
|---|---|---|
| Under Modulation | μ < 1 | Envelope never crosses zero; demodulation is clean |
| Critical Modulation | μ = 1 | Envelope just touches zero; maximum undistorted modulation |
| Over Modulation | μ > 1 | Envelope crosses zero; carrier phase reversal; envelope detector fails |

---

## 5. Bandwidth

The AM signal occupies a bandwidth of:
```
BW = 2 × fₘ   (Hz)
```

The signal spans from (fꜝ − fₘ) to (fꜝ + fₘ) in the frequency domain.

---

## 6. Power Analysis

### Carrier Power
```
Pc = Aꜝ² / (2R)   Watts
```
where R is the load resistance in ohms.

### Total Transmitted Power
```
Pt = Pc × (1 + μ²/2)
```

### Sideband Power (information-carrying power)
```
Psb = Pt − Pc = Pc × μ²/2
```

### Transmission Efficiency
```
η = μ² / (2 + μ²)   ×100%
```

Key insight: At μ = 1, η_max = 1/3 = **33.33%**. The remaining 66.67% is wasted in the carrier. This fundamental inefficiency of AM DSB-TC motivates suppressed-carrier variants (DSB-SC, SSB).

---

## 7. Noisy Channel (AWGN Model)

The channel is modelled as an Additive White Gaussian Noise (AWGN) channel:
```
r(t) = s(t) + n(t)
```
where n(t) is zero-mean Gaussian noise with variance σ².

### Signal-to-Noise Ratio
```
SNR = P_signal / P_noise = 10 log₁₀(P_signal / P_noise)   dB
```

Higher SNR → better signal quality → better envelope detection.

---

## 8. Envelope Detection

The envelope detector recovers m(t) from r(t) in three steps:

### Step 1: Rectification
```
|r(t)| = |s(t) + n(t)|
```
The rectifier (diode) passes only the positive half (or absolute value for full-wave).

### Step 2: Low-Pass Filtering
A Butterworth low-pass filter with cutoff between fₘ and fꜝ smooths out the carrier ripple, leaving the envelope.

Filter cutoff criterion:
```
fₘ  <  f_cutoff  <<  fꜝ
```

### Step 3: DC Removal & Normalisation
The DC offset introduced by rectification (≈ Aꜝ/π for a half-wave detector) is subtracted, and the signal is normalised to match the original message amplitude.

### When Envelope Detection Works
Envelope detection recovers m(t) faithfully only when:
1. μ ≤ 1 (no phase reversal in carrier)
2. fꜝ >> fₘ (carrier frequency much greater than message frequency)
3. Adequate SNR (noise level is sufficiently low)

When μ > 1, the envelope detector output is a distorted version of |m(t)| — it cannot reconstruct the original sinusoid because it loses the negative half.

---

## 9. Software Implementation

### envelope_detector.py
Uses `scipy.signal.butter` + `filtfilt` (zero-phase filtering) to implement the low-pass filter stage. Zero-phase filtering avoids any time-delay in the recovered signal, making the comparison visually cleaner.

Cutoff frequency selection:
```python
cutoff = min(sqrt(fm * fc), fc * 0.35, fm * 10.0)
cutoff = max(cutoff, fm * 2.0)
```

This geometric-mean heuristic ensures the cutoff stays well between fₘ and fꜝ across all parameter combinations.

### noise_channel.py
Uses `numpy.random.default_rng(seed)` for reproducible AWGN. A fixed seed prevents the noise pattern from regenerating on every Streamlit widget interaction.

---

## 10. Summary

| Stage | Input | Process | Output |
|---|---|---|---|
| Signal Generation | Parameters | m(t) = Aₘ sin(2π fₘ t) | Message signal |
| AM Modulation | m(t), c(t) | s(t) = Aꜝ[1+μ m̂(t)] sin(2π fꜝ t) | AM signal |
| Noisy Channel | s(t) | r(t) = s(t) + n(t) | Received signal |
| Envelope Detector | r(t) | Rectify → LPF → DC remove | Recovered signal |
