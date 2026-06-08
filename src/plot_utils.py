"""
plot_utils.py
-------------
Plotly-based interactive waveform visualisation utilities.

All charts follow a consistent style:
  - White background template
  - Labelled axes  (Time in seconds, Amplitude in Volts)
  - Grid lines enabled
  - Legend shown

MAKAUT EC401 Analog Communication – Visualisation Module
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Colour palette (colourblind-friendly-ish and visually distinct)
COLOURS = {
    "message":   "#2196F3",   # Blue
    "carrier":   "#FF9800",   # Orange
    "am":        "#4CAF50",   # Green
    "noisy":     "#F44336",   # Red
    "recovered": "#9C27B0",   # Purple
}

_LAYOUT_DEFAULTS = dict(
    template="plotly_white",
    font=dict(family="Arial, sans-serif", size=13),
    margin=dict(l=50, r=30, t=60, b=50),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)


def _add_grid(fig, rows=1):
    for r in range(1, rows + 1):
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#e0e0e0", row=r, col=1)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#e0e0e0", row=r, col=1)
    return fig


# ---------------------------------------------------------------------------
# Individual signal plot
# ---------------------------------------------------------------------------

def plot_single_signal(
    t: np.ndarray,
    signal: np.ndarray,
    title: str,
    colour: str = "#2196F3",
    name: str = "Signal",
    height: int = 300,
) -> go.Figure:
    """Plot a single signal waveform."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=signal,
        mode="lines",
        name=name,
        line=dict(color=colour, width=1.8),
    ))
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center"),
        xaxis_title="Time (s)",
        yaxis_title="Amplitude (V)",
        height=height,
        **_LAYOUT_DEFAULTS,
    )
    fig = _add_grid(fig)
    return fig


# ---------------------------------------------------------------------------
# All five signals stacked in subplots
# ---------------------------------------------------------------------------

def plot_all_signals(
    t: np.ndarray,
    message: np.ndarray,
    carrier: np.ndarray,
    am_signal: np.ndarray,
    noisy_signal: np.ndarray,
    recovered: np.ndarray,
) -> go.Figure:
    """
    Plot the full communication chain as 5 stacked subplots.

    Rows
    ----
    1. Message signal m(t)
    2. Carrier signal c(t)
    3. AM modulated signal s(t)
    4. Noisy received signal r(t)
    5. Recovered signal (envelope detected)
    """
    subplot_titles = [
        "① Message Signal  m(t) = Aₘ sin(2π fₘ t)",
        "② Carrier Signal  c(t) = A꜀ sin(2π f꜀ t)",
        "③ AM Modulated Signal  s(t) = A꜀ [1 + μ sin(2π fₘ t)] sin(2π f꜀ t)",
        "④ Noisy Received Signal  r(t) = s(t) + n(t)",
        "⑤ Recovered Signal  (After Envelope Detection)",
    ]

    fig = make_subplots(
        rows=5, cols=1,
        subplot_titles=subplot_titles,
        vertical_spacing=0.07,
        shared_xaxes=False,
    )

    traces = [
        (message,     "m(t)",      COLOURS["message"]),
        (carrier,     "c(t)",      COLOURS["carrier"]),
        (am_signal,   "s(t)",      COLOURS["am"]),
        (noisy_signal,"r(t)",      COLOURS["noisy"]),
        (recovered,   "Recovered", COLOURS["recovered"]),
    ]

    for i, (sig, name, colour) in enumerate(traces, start=1):
        fig.add_trace(
            go.Scatter(x=t, y=sig, mode="lines", name=name,
                       line=dict(color=colour, width=1.5)),
            row=i, col=1,
        )
        fig.update_xaxes(title_text="Time (s)", row=i, col=1,
                         showgrid=True, gridcolor="#e0e0e0")
        fig.update_yaxes(title_text="Amplitude (V)", row=i, col=1,
                         showgrid=True, gridcolor="#e0e0e0")

    fig.update_layout(
        height=1400,
        title=dict(
            text="AM Communication Chain — Signal Progression",
            x=0.5, xanchor="center", font=dict(size=16),
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1),
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12),
        margin=dict(l=50, r=30, t=80, b=50),
    )

    return fig


# ---------------------------------------------------------------------------
# Comparison plot: original message vs recovered signal
# ---------------------------------------------------------------------------

def plot_comparison(
    t: np.ndarray,
    message: np.ndarray,
    recovered: np.ndarray,
) -> go.Figure:
    """Compare original message signal with envelope-detected recovered signal."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=message,
        mode="lines",
        name="Original Message  m(t)",
        line=dict(color=COLOURS["message"], width=2.5),
    ))
    fig.add_trace(go.Scatter(
        x=t, y=recovered,
        mode="lines",
        name="Recovered Signal  (Envelope Detector Output)",
        line=dict(color=COLOURS["recovered"], width=2.0, dash="dash"),
    ))

    fig.update_layout(
        title=dict(
            text="Comparison: Original Message vs Recovered Signal",
            x=0.5, xanchor="center",
        ),
        xaxis_title="Time (s)",
        yaxis_title="Amplitude (V)",
        height=420,
        **_LAYOUT_DEFAULTS,
    )
    fig = _add_grid(fig)
    return fig


# ---------------------------------------------------------------------------
# Power distribution bar chart
# ---------------------------------------------------------------------------

def plot_power_distribution(Pc: float, Psb: float) -> go.Figure:
    """Bar chart showing carrier power vs sideband power."""
    fig = go.Figure(go.Bar(
        x=["Carrier Power  Pc", "Sideband Power  Psb"],
        y=[Pc, Psb],
        marker_color=[COLOURS["carrier"], COLOURS["am"]],
        text=[f"{Pc:.4f} W", f"{Psb:.4f} W"],
        textposition="outside",
    ))
    fig.update_layout(
        title=dict(text="Power Distribution: Carrier vs Sidebands", x=0.5, xanchor="center"),
        yaxis_title="Power (W)",
        height=350,
        **_LAYOUT_DEFAULTS,
    )
    fig.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    return fig
