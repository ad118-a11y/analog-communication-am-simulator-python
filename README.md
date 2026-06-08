# 📡 AM Transmitter & Receiver Simulator

### Simulation of AM Transmitter and Envelope Detector Receiver under Noisy Channel

> **MAKAUT EC401 – Analog Communication Project**  
> An interactive simulation and analysis tool for AM DSB-TC modulation, noisy channel transmission, and envelope detection.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://touzpz7pnoq8qdalasm45s.streamlit.app/)

🔗 **Live App:** [https://touzpz7pnoq8qdalasm45s.streamlit.app/](https://touzpz7pnoq8qdalasm45s.streamlit.app/)

---

## 🎯 Objective

This project provides a complete, real-time simulation of the Amplitude Modulation (AM DSB-TC) communication chain:

```
Message Signal → AM Modulator (DSB-TC) → Noisy Channel (AWGN) → Envelope Detector → Recovered Signal
```

Users can adjust all parameters interactively and observe their effect on signal waveforms, power calculations, bandwidth, and detection quality — directly aligned with the MAKAUT EC401 Analog Communication syllabus.

---

## 📚 MAKAUT EC401 Syllabus Relevance

| Syllabus Topic | Covered |
|---|---|
| Analog communication system | ✅ |
| Need for modulation | ✅ |
| Amplitude Modulation (AM DSB-TC) | ✅ |
| Modulation index μ | ✅ |
| Under / Critical / Over modulation | ✅ |
| AM bandwidth (BW = 2fₘ) | ✅ |
| Carrier power Pc | ✅ |
| Total transmitted power Pt | ✅ |
| Transmission efficiency η | ✅ |
| Channel noise (AWGN model) | ✅ |
| Envelope detection | ✅ |
| Signal recovery | ✅ |

---

## ✨ Features

- **Real-time interactive simulation** with adjustable sliders for all parameters
- **Complete signal chain** display: message → carrier → AM → noisy → recovered
- **Automatic modulation condition detection**: Under / Critical / Over modulation
- **System warnings** for poor carrier-to-message frequency ratio and low sampling rate
- **All AM formulas computed and displayed**: μ, BW, Pc, Pt, Psb, η
- **SNR calculation** for the noisy channel
- **Power distribution chart**: Carrier power vs Sideband power
- **Comparison plot**: Original message vs Recovered signal
- **CSV export**: Parameters, calculation results, and full waveform data
- **Technical analysis section** that dynamically explains the current simulation state

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| NumPy | Signal generation and numerical computation |
| SciPy | Butterworth low-pass filter for envelope detection |
| Plotly | Interactive waveform visualisation |
| Pandas | Data tables and CSV export |

---

## 🖼️ System Block Diagram

```
┌─────────────────┐
│  Message Source  │   m(t) = Aₘ sin(2π fₘ t)
└────────┬────────┘
         │
┌────────▼────────┐
│   AM Modulator  │   s(t) = Aꜝ [1 + μ sin(2π fₘ t)] sin(2π fꜝ t)
│    (DSB-TC)     │   μ = Aₘ / Aꜝ
└────────┬────────┘
         │
┌────────▼────────┐
│  Noisy Channel  │   r(t) = s(t) + n(t)
│    (AWGN)       │   n(t) ~ N(0, σ²)
└────────┬────────┘
         │
┌────────▼────────┐
│ Envelope Detector│  |r(t)| → LPF → DC remove → normalise
│ (Rectify + LPF) │
└────────┬────────┘
         │
┌────────▼────────┐
│ Recovered Signal │  ≈ m(t)   (when μ ≤ 1, high SNR)
└─────────────────┘
```

---

## 📐 Formula Reference

| Parameter | Formula |
|---|---|
| Modulation Index | μ = Aₘ / Aꜝ |
| AM Signal | s(t) = Aꜝ [1 + μ sin(2π fₘ t)] sin(2π fꜝ t) |
| Bandwidth | BW = 2fₘ |
| Carrier Power | Pc = Aꜝ² / (2R) |
| Total Transmitted Power | Pt = Pc (1 + μ²/2) |
| Sideband Power | Psb = Pt − Pc |
| Transmission Efficiency | η = μ² / (2 + μ²) |
| Efficiency (%) | η% = η × 100 |

---

## 📁 Project Structure

```
analog-communication-am-simulator-python/
│
├── app.py                     ← Main Streamlit application
├── requirements.txt           ← Python dependencies
├── README.md                  ← Project documentation
├── .gitignore                 ← Git ignore rules
│
├── src/
│   ├── __init__.py
│   ├── signal_generator.py    ← Time vector, message & carrier generation
│   ├── am_modulation.py       ← AM DSB-TC modulation logic
│   ├── noise_channel.py       ← AWGN channel model
│   ├── envelope_detector.py   ← Rectify + LPF envelope detection
│   ├── calculations.py        ← All AM formulas (μ, BW, Pc, Pt, η …)
│   └── plot_utils.py          ← Plotly chart functions
│
├── docs/
│   └── project_explanation.md ← Detailed technical explanation
│
└── assets/
    └── screenshots/           ← App screenshots (add after running)
```

---

## 🚀 Installation & Setup

> Python is assumed to be already installed on your system.

**Step 1 — Clone the repository**

```bash
git clone https://github.com/<your-username>/analog-communication-am-simulator-python.git
```

**Step 2 — Open the project folder**

```bash
cd analog-communication-am-simulator-python
```

**Step 3 — Create a virtual environment**

```bash
python -m venv venv
```

**Step 4 — Activate the virtual environment**

Windows:
```bash
venv\Scripts\activate
```

macOS / Linux:
```bash
source venv/bin/activate
```

**Step 5 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 6 — Run the application**

```bash
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8501`.

---

## 📸 Screenshots

> Add screenshots to `assets/screenshots/` after running the application.

| Dashboard | Waveform Chain | Comparison |
|---|---|---|
| *(screenshot)* | *(screenshot)* | *(screenshot)* |

---

## 🔭 Future Scope

- DSB-SC (Double Sideband Suppressed Carrier) simulation module
- SSB (Single Sideband) simulation and comparison
- Frequency spectrum analysis using FFT
- Real audio file (.wav) as message signal input
- AM vs FM side-by-side comparison
- Advanced diode envelope detector circuit model with RC time constant control
- Automatic Gain Control (AGC) simulation
- BER vs SNR analysis (extension to digital comparison)

---

## 👥 Team Members

| Name | Roll Number | Institution |
|---|---|---|
| *(Team Member 1)* | *(Roll No.)* | MAKAUT |
| *(Team Member 2)* | *(Roll No.)* | MAKAUT |
| *(Team Member 3)* | *(Roll No.)* | MAKAUT |

---

## 📄 License

This project is intended for educational purposes under the MAKAUT EC401 Analog Communication course.

---

*Built with ❤️ using Python, Streamlit, NumPy, SciPy, and Plotly.*
