"""
app.py
------
Main Streamlit application for the AM Transmitter & Receiver Simulator.

Simulation of AM Transmitter and Envelope Detector Receiver under Noisy Channel
MAKAUT EC401 – Analog Communication (EC401)

Communication Chain:
    Message Signal → AM Modulator → Noisy Channel → Envelope Detector → Recovered Signal

Run with:
    streamlit run app.py
"""

import numpy as np
import pandas as pd
import streamlit as st

from src.signal_generator import (
    generate_time_vector,
    generate_message_signal,
    generate_carrier_signal,
)
from src.am_modulation import am_modulate, get_modulation_condition
from src.noise_channel import add_awgn, compute_snr_db
from src.envelope_detector import envelope_detect, normalize_to_amplitude
from src.calculations import compute_all
from src.plot_utils import (
    plot_all_signals,
    plot_comparison,
    plot_power_distribution,
    plot_single_signal,
    COLOURS,
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AM Simulator | MAKAUT EC401",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# HEADER
# ============================================================================

st.markdown(
    """
    <h1 style='text-align:center; color:#1565C0; margin-bottom:0;'>
        📡 AM Transmitter & Receiver Simulator
    </h1>
    <h3 style='text-align:center; color:#37474F; margin-top:4px;'>
        Simulation of AM Transmitter and Envelope Detector Receiver under Noisy Channel
    </h3>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# Objective + Syllabus relevance
col_obj, col_chain = st.columns([1, 1])

with col_obj:
    st.markdown(
        """
        **Objective**

        This tool simulates the complete Amplitude Modulation (AM DSB-TC) communication
        chain — from message generation and modulation, through a noisy channel, to
        envelope detection and signal recovery. All parameters are adjustable in real-time.

        **MAKAUT EC401 Syllabus Coverage**

        | Concept | Covered |
        |---------|---------|
        | Analog communication system | ✅ |
        | Need for modulation | ✅ |
        | AM DSB-TC & modulation index | ✅ |
        | Under / Critical / Over modulation | ✅ |
        | AM bandwidth | ✅ |
        | Carrier power & total transmitted power | ✅ |
        | AM transmission efficiency | ✅ |
        | Channel noise (AWGN) | ✅ |
        | Envelope detection | ✅ |
        | Signal recovery | ✅ |
        """
    )

with col_chain:
    st.markdown("**Communication Chain**")
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #E3F2FD, #F3E5F5);
            border-radius: 12px;
            padding: 20px 10px;
            text-align: center;
            font-size: 15px;
            font-weight: 500;
            color: #1A237E;
            border: 1px solid #BBDEFB;
        ">
            🎵 Message Signal
            <br>↓
            <br>📻 AM Modulator (DSB-TC)
            <br>↓
            <br>📶 Noisy Channel (AWGN)
            <br>↓
            <br>🔍 Envelope Detector
            <br>↓
            <br>🔊 Recovered Signal
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============================================================================
# SIDEBAR – USER INPUTS
# ============================================================================

st.sidebar.markdown(
    "<h2 style='color:#1565C0;'>⚙️ Simulation Parameters</h2>",
    unsafe_allow_html=True,
)

st.sidebar.markdown("### 🎵 Message Signal")
Am = st.sidebar.slider("Message Amplitude  Aₘ  (V)", 0.1, 5.0, 1.0, 0.1)
fm = st.sidebar.slider("Message Frequency  fₘ  (Hz)", 1, 50, 5, 1)

st.sidebar.markdown("### 📡 Carrier Signal")
Ac = st.sidebar.slider("Carrier Amplitude  A꜀  (V)", 0.5, 10.0, 2.0, 0.1)
fc = st.sidebar.slider("Carrier Frequency  f꜀  (Hz)", 10, 500, 50, 5)

st.sidebar.markdown("### ⚡ Load Resistance")
R = st.sidebar.slider("Load Resistance  R  (Ω)", 1, 1000, 50, 1)

st.sidebar.markdown("### 📶 Channel Noise")
noise_level = st.sidebar.slider("Noise Level  σ", 0.0, 2.0, 0.1, 0.05)
noise_seed   = st.sidebar.number_input("Random Seed (for reproducibility)", 0, 9999, 42, 1)

st.sidebar.markdown("### ⏱️ Simulation Settings")
duration = st.sidebar.slider("Duration  (s)", 0.1, 5.0, 1.0, 0.1)
fs       = st.sidebar.slider("Sampling Frequency  fₛ  (Hz)", 1000, 20000, 5000, 500)

st.sidebar.markdown("---")
st.sidebar.info(
    "**MAKAUT EC401 – Analog Communication**\n\n"
    "Adjust sliders to observe real-time changes in signals, "
    "power, bandwidth, and detection quality."
)

# ============================================================================
# SIGNAL COMPUTATION
# ============================================================================

t         = generate_time_vector(duration, fs)
message   = generate_message_signal(t, Am, fm)
carrier   = generate_carrier_signal(t, Ac, fc)
s_t, mu   = am_modulate(t, Am, Ac, fm, fc)
r_t, noise = add_awgn(s_t, noise_level, seed=int(noise_seed))
snr_db    = compute_snr_db(s_t, noise)

# Envelope detection
detected  = envelope_detect(r_t, fs, fc, fm)
recovered = normalize_to_amplitude(detected, Am)

# All calculations
results = compute_all(Am, Ac, fm, R)
cond    = get_modulation_condition(mu)

# ============================================================================
# WARNING / INFO BANNERS
# ============================================================================

st.subheader("⚠️ System Warnings & Status")

warn_col1, warn_col2 = st.columns(2)

with warn_col1:
    if abs(mu - 1.0) <= 0.02:
        st.success(
            f"**Critical Modulation** (μ = {mu:.3f})  \n"
            "This gives maximum undistorted modulation. Envelope detection works optimally."
        )
    elif mu < 1.0:
        st.info(
            f"**Under Modulation** (μ = {mu:.3f})  \n"
            "Envelope detection is generally possible without signal distortion."
        )
    else:
        st.error(
            f"**Over Modulation Detected** (μ = {mu:.3f})  \n"
            "Envelope distortion will occur. The recovered signal may be clipped or distorted."
        )

with warn_col2:
    if fc <= 5 * fm:
        st.warning(
            f"**Carrier-to-Message Frequency Ratio is Low**  (f꜀/fₘ = {fc/fm:.1f})  \n"
            "Carrier frequency should be much greater than message frequency (ideally f꜀ ≥ 10 × fₘ) "
            "for proper AM simulation and clean envelope detection."
        )
    else:
        st.success(
            f"**Frequency Ratio OK**  (f꜀/fₘ = {fc/fm:.1f})  \n"
            "Carrier frequency is sufficiently higher than message frequency."
        )

    if fs < 10 * fc:
        st.warning(
            f"**Sampling Rate May Be Too Low**  (fₛ/f꜀ = {fs/fc:.1f})  \n"
            "Recommend fₛ ≥ 10 × f꜀ for accurate waveform representation."
        )
    else:
        st.success(
            f"**Sampling Rate Adequate**  (fₛ/f꜀ = {fs/fc:.1f})  \n"
            "Waveform sampling is sufficient for accurate display."
        )

st.markdown("---")

# ============================================================================
# RESULT CARDS
# ============================================================================

st.subheader("📊 Calculated Parameters")

c1, c2, c3, c4 = st.columns(4)
c5, c6, c7     = st.columns(3)

def metric_card(col, label, value, unit="", delta=None):
    col.metric(label=label, value=f"{value} {unit}".strip(), delta=delta)

metric_card(c1, "Modulation Index  μ", results["Modulation Index (μ)"])
metric_card(c2, "Bandwidth  BW", results["Bandwidth BW (Hz)"], "Hz")
metric_card(c3, "Carrier Power  Pc", results["Carrier Power Pc (W)"], "W")
metric_card(c4, "Total Power  Pt", results["Total Transmitted Power Pt (W)"], "W")
metric_card(c5, "Sideband Power  Psb", results["Sideband Power Psb (W)"], "W")
metric_card(c6, "Efficiency  η", results["Efficiency η (%)"], "%")
c7.metric(label="Modulation Condition", value=cond)

if noise_level > 0:
    st.caption(f"📶 Channel SNR: **{snr_db:.2f} dB**  (noise level σ = {noise_level})")

st.markdown("---")

# ============================================================================
# WAVEFORM VISUALISATION
# ============================================================================

st.subheader("📈 Signal Waveforms")
st.caption(
    "All five stages of the AM communication chain are shown below. "
    "Use the Plotly toolbar (top-right of each chart) to zoom, pan, or export."
)

tab1, tab2, tab3 = st.tabs([
    "🔀 Full Communication Chain",
    "🔎 Individual Signals",
    "⚖️ Message vs Recovered",
])

with tab1:
    st.plotly_chart(
        plot_all_signals(t, message, carrier, s_t, r_t, recovered),
        use_container_width=True,
    )

with tab2:
    sig_choice = st.selectbox(
        "Select signal to view",
        ["Message Signal  m(t)",
         "Carrier Signal  c(t)",
         "AM Modulated Signal  s(t)",
         "Noisy Received Signal  r(t)",
         "Recovered Signal"],
    )
    sig_map = {
        "Message Signal  m(t)":        (message,   COLOURS["message"],   "m(t)"),
        "Carrier Signal  c(t)":        (carrier,   COLOURS["carrier"],   "c(t)"),
        "AM Modulated Signal  s(t)":   (s_t,       COLOURS["am"],        "s(t)"),
        "Noisy Received Signal  r(t)": (r_t,       COLOURS["noisy"],     "r(t)"),
        "Recovered Signal":            (recovered, COLOURS["recovered"], "Recovered"),
    }
    sel_sig, sel_col, sel_name = sig_map[sig_choice]
    st.plotly_chart(
        plot_single_signal(t, sel_sig, sig_choice, colour=sel_col, name=sel_name, height=380),
        use_container_width=True,
    )

with tab3:
    st.plotly_chart(plot_comparison(t, message, recovered), use_container_width=True)
    st.plotly_chart(
        plot_power_distribution(
            results["Carrier Power Pc (W)"],
            results["Sideband Power Psb (W)"],
        ),
        use_container_width=True,
    )

st.markdown("---")

# ============================================================================
# RESULT ANALYSIS SECTION
# ============================================================================

st.subheader("🧠 Technical Analysis")

eta    = results["Efficiency η (%)"]
bw     = results["Bandwidth BW (Hz)"]
pc     = results["Carrier Power Pc (W)"]
pt     = results["Total Transmitted Power Pt (W)"]
psb    = results["Sideband Power Psb (W)"]
pc_pct = (pc / pt * 100) if pt > 0 else 0
sb_pct = (psb / pt * 100) if pt > 0 else 0

analysis_text = f"""
**Modulation Index  μ = {mu:.4f}  →  {cond}**

{"The signal is **under-modulated**. The message amplitude is smaller than the carrier amplitude, so the envelope never crosses zero. Envelope detection will work correctly — the diode RC circuit can track the envelope without distortion." if mu < 1.0 else ""}
{"The signal is at **critical modulation** (μ ≈ 1). The envelope just touches zero at its troughs. This is the boundary condition — envelope detection still works but any increase in modulation depth will cause distortion." if abs(mu - 1.0) <= 0.02 else ""}
{"The signal is **over-modulated** (μ > 1). The carrier is suppressed at the troughs — the envelope folds back on itself. A simple envelope detector cannot correctly recover the original message; the recovered signal will be distorted (phase reversal artifact). A synchronous or coherent detector would be required." if mu > 1.0 else ""}

---

**Bandwidth**

The AM DSB-TC signal occupies a bandwidth of **BW = 2fₘ = {bw:.1f} Hz**, centred around the carrier frequency f꜀ = {fc} Hz. Two sidebands are produced: an upper sideband at f꜀ + fₘ = {fc + fm} Hz and a lower sideband at f꜀ − fₘ = {fc - fm} Hz.

---

**Noise & Channel Effect**

{"The channel is **noiseless** (noise level = 0). The received signal is identical to the transmitted signal." if noise_level == 0 else f"With noise level σ = {noise_level}, the channel SNR is approximately **{snr_db:.2f} dB**. {'The noise is low and the envelope detector should recover the message with minimal distortion.' if snr_db > 20 else 'The noise level is moderate. Some distortion in the recovered signal is expected.' if snr_db > 10 else 'The noise level is high. Significant distortion in the recovered signal is expected. Reduce noise level for better recovery.'}"}

---

**Power Distribution**

| Component | Power | Percentage |
|-----------|-------|------------|
| Carrier | {pc:.6f} W | {pc_pct:.1f}% |
| Sidebands (both) | {psb:.6f} W | {sb_pct:.1f}% |
| **Total** | **{pt:.6f} W** | **100%** |

The carrier alone accounts for **{pc_pct:.1f}%** of the total transmitted power, while only **{sb_pct:.1f}%** carries the actual information. This is the fundamental inefficiency of AM DSB-TC.

---

**Transmission Efficiency  η = {eta:.2f}%**

{"The efficiency is very low (η < 25%). Most transmitted power is wasted on the carrier." if eta < 25 else "The efficiency is moderate. Increasing the modulation index (while keeping μ ≤ 1) would improve it." if eta < 33.4 else "The efficiency is at its theoretical maximum for AM DSB-TC (μ = 1, η = 33.33%). At critical modulation, one-third of total power carries the message signal."}

Maximum possible efficiency for AM DSB-TC occurs at μ = 1: η_max = 1/(2+1) = **33.33%**.
"""

st.markdown(analysis_text)
st.markdown("---")

# ============================================================================
# EXPORT SECTION
# ============================================================================

st.subheader("📥 Export Data")

exp_col1, exp_col2, exp_col3 = st.columns(3)

# --- CSV 1: Simulation Parameters ---
params_df = pd.DataFrame({
    "Parameter":  ["Am (V)", "Ac (V)", "fm (Hz)", "fc (Hz)", "R (Ω)",
                   "Noise Level σ", "Duration (s)", "Sampling Freq (Hz)"],
    "Value":      [Am, Ac, fm, fc, R, noise_level, duration, fs],
})
with exp_col1:
    st.download_button(
        label="⬇ Download Parameters CSV",
        data=params_df.to_csv(index=False),
        file_name="am_simulation_parameters.csv",
        mime="text/csv",
    )

# --- CSV 2: Calculation Results ---
calc_df = pd.DataFrame(
    list(results.items()), columns=["Parameter", "Value"]
)
with exp_col2:
    st.download_button(
        label="⬇ Download Results CSV",
        data=calc_df.to_csv(index=False),
        file_name="am_calculation_results.csv",
        mime="text/csv",
    )

# --- CSV 3: Waveform Data ---
# Limit to 5000 samples to keep file size manageable
max_export = min(5000, len(t))
step       = max(1, len(t) // max_export)
wave_df    = pd.DataFrame({
    "Time (s)":               t[::step],
    "Message m(t)":           message[::step],
    "Carrier c(t)":           carrier[::step],
    "AM Signal s(t)":         s_t[::step],
    "Noisy Received r(t)":    r_t[::step],
    "Recovered Signal":       recovered[::step],
})
with exp_col3:
    st.download_button(
        label="⬇ Download Waveform Data CSV",
        data=wave_df.to_csv(index=False),
        file_name="am_waveform_data.csv",
        mime="text/csv",
    )

st.markdown("---")

# ============================================================================
# ABOUT SECTION
# ============================================================================

st.subheader("ℹ️ About This Project")

about_col1, about_col2 = st.columns([1, 1])

with about_col1:
    st.markdown(
        """
        **Project Objective**

        This simulator provides an interactive, real-time analysis of the complete
        AM transmission system — from message signal generation through DSB-TC
        modulation, additive Gaussian noise, envelope detection, and signal recovery.
        It serves as a practical complement to the theoretical concepts of MAKAUT
        EC401 Analog Communication.

        **MAKAUT EC401 Syllabus Relevance**

        The tool directly covers Unit topics including:
        - Analog communication system block diagram
        - Need for modulation (bandwidth efficiency, antenna size)
        - Amplitude modulation: DSB-TC derivation and waveforms
        - Modulation index and modulation conditions
        - AM bandwidth calculation (BW = 2fₘ)
        - Power relations: Pc, Pt, Psb, and transmission efficiency η
        - Noise in communication channels (AWGN model)
        - Envelope detector operation and signal recovery

        **Technologies Used**

        | Tool | Purpose |
        |------|---------|
        | Python | Core language |
        | Streamlit | Web interface |
        | NumPy | Signal generation & math |
        | SciPy | Butterworth LPF for envelope detection |
        | Plotly | Interactive waveform visualisation |
        | Pandas | Data export (CSV) |
        """
    )

with about_col2:
    st.markdown("**System Block Diagram**")
    st.markdown(
        """
        <div style="
            background: #F8F9FA;
            border: 1px solid #DEE2E6;
            border-radius: 10px;
            padding: 20px;
            font-family: monospace;
            font-size: 13px;
            color: #212529;
            line-height: 2.0;
        ">
        ┌─────────────────┐<br>
        │  Message Source  │  m(t) = Aₘ sin(2π fₘ t)<br>
        └────────┬────────┘<br>
                 │<br>
        ┌────────▼────────┐<br>
        │  AM Modulator   │  s(t) = A꜀[1 + μ m(t)/Aₘ] sin(2π f꜀ t)<br>
        │    (DSB-TC)     │<br>
        └────────┬────────┘<br>
                 │<br>
        ┌────────▼────────┐<br>
        │  Noisy Channel  │  r(t) = s(t) + n(t)<br>
        │    (AWGN)       │  n(t) ~ N(0, σ²)<br>
        └────────┬────────┘<br>
                 │<br>
        ┌────────▼────────┐<br>
        │ Envelope Detector│  |r(t)| → LPF → DC remove<br>
        │ (Rectify + LPF) │<br>
        └────────┬────────┘<br>
                 │<br>
        ┌────────▼────────┐<br>
        │ Recovered Signal │  ≈ m(t)  (when μ ≤ 1, SNR high)<br>
        └─────────────────┘
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown(
        """
        **Future Scope**

        - Add DSB-SC (Suppressed Carrier) simulation
        - Add SSB (Single Sideband) simulation
        - Frequency spectrum visualisation via FFT
        - Real audio file as message signal input
        - AM vs FM comparison module
        - Advanced diode envelope detector circuit model
        - Automatic Gain Control (AGC) simulation
        """
    )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#78909C; font-size:13px; padding:10px;">
        📡 AM Transmitter & Receiver Simulator &nbsp;|&nbsp;
        MAKAUT EC401 Analog Communication &nbsp;|&nbsp;
        Built with Streamlit, NumPy, SciPy & Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
