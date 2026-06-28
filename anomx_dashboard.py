import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AnomX — Aviation Asset Monitoring",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #080c12 !important;
    color: #c8d6e5 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: #080c12 !important;
}

.main .block-container {
    padding: 0.5rem 1.2rem 2rem 1.2rem !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #0a0f1a 100%) !important;
    border-right: 1px solid rgba(0, 240, 255, 0.12) !important;
    width: 72px !important;
    min-width: 72px !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}

[data-testid="stSidebar"] .stMarkdown { padding: 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #ff2a5f44; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #ff2a5f; }

/* ── Plotly transparent bg ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Remove Streamlit default chrome ── */
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Metric overrides ── */
[data-testid="metric-container"] {
    background: transparent !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar HTML ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { width: 72px !important; min-width: 72px !important; }
    </style>

    <div style="
        display: flex; flex-direction: column; align-items: center;
        padding: 16px 0; gap: 6px; height: 100vh;
        background: linear-gradient(180deg, #0d1117 0%, #0a0e18 100%);
    ">
        <!-- Logo / Compass -->
        <div style="
            width: 44px; height: 44px; border-radius: 10px; margin-bottom: 12px;
            background: linear-gradient(135deg, #ff2a5f22, #00f0ff22);
            border: 1.5px solid #00f0ff66;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 18px #00f0ff44, inset 0 0 12px #00f0ff11;
        ">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="9" stroke="#00f0ff" stroke-width="1.2" stroke-dasharray="2 1"/>
                <line x1="12" y1="3" x2="12" y2="21" stroke="#ff2a5f" stroke-width="1.5"/>
                <line x1="3" y1="12" x2="21" y2="12" stroke="#ff2a5f" stroke-width="1.5"/>
                <circle cx="12" cy="12" r="2.5" fill="#ff2a5f" opacity="0.9"/>
                <polygon points="12,5 13.2,9 12,8 10.8,9" fill="#00f0ff"/>
            </svg>
        </div>

        <!-- Nav Icons -->
        <div class="nav-icon active-nav" style="
            width: 44px; height: 44px; border-radius: 10px; cursor: pointer;
            background: linear-gradient(135deg, #ff2a5f33, #c0205544);
            border: 1.5px solid #ff2a5f88;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 14px #ff2a5f55;
        ">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff2a5f" stroke-width="1.8">
                <rect x="3" y="3" width="7" height="7" rx="1"/>
                <rect x="14" y="3" width="7" height="7" rx="1"/>
                <rect x="3" y="14" width="7" height="7" rx="1"/>
                <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
        </div>

        <div style="
            width: 44px; height: 44px; border-radius: 10px; cursor: pointer; margin-top: 4px;
            background: rgba(255,255,255,0.03); border: 1.5px solid rgba(0,240,255,0.15);
            display: flex; align-items: center; justify-content: center;
        ">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6b7fa3" stroke-width="1.8">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 2v2M12 20v2M2 12h2M20 12h2"/>
                <path d="M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M17.66 6.34l-1.41 1.41M6.34 17.66l-1.41 1.41"/>
            </svg>
        </div>

        <div style="
            width: 44px; height: 44px; border-radius: 10px; cursor: pointer;
            background: rgba(255,255,255,0.03); border: 1.5px solid rgba(0,240,255,0.15);
            display: flex; align-items: center; justify-content: center;
        ">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6b7fa3" stroke-width="1.8">
                <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
            </svg>
        </div>

        <div style="
            width: 44px; height: 44px; border-radius: 10px; cursor: pointer;
            background: rgba(255,255,255,0.03); border: 1.5px solid rgba(0,240,255,0.15);
            display: flex; align-items: center; justify-content: center;
        ">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6b7fa3" stroke-width="1.8">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                <path d="M2 17l10 5 10-5"/>
                <path d="M2 12l10 5 10-5"/>
            </svg>
        </div>

        <div style="
            width: 44px; height: 44px; border-radius: 10px; cursor: pointer;
            background: rgba(255,255,255,0.03); border: 1.5px solid rgba(0,240,255,0.15);
            display: flex; align-items: center; justify-content: center;
        ">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6b7fa3" stroke-width="1.8">
                <path d="M18 20V10M12 20V4M6 20v-6"/>
            </svg>
        </div>

        <div style="margin-top: auto;
            width: 44px; height: 44px; border-radius: 10px; cursor: pointer;
            background: rgba(255,255,255,0.03); border: 1.5px solid rgba(0,240,255,0.15);
            display: flex; align-items: center; justify-content: center;
        ">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6b7fa3" stroke-width="1.8">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Simulated Data ──────────────────────────────────────────────────────────────
np.random.seed(42)
time_labels = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
rul_values  = [285, 260, 240, 210, 185, 165, 140, 112, 85, 60, 35, 12]
noise       = np.random.normal(0, 4, 12)
rul_noisy   = [max(0, v + n) for v, n in zip(rul_values, noise)]

components  = ["Turbine Blades", "Compressor Valves", "Bearings", "Shaft Assembly"]
months      = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
wear_data   = {c: [round(random.uniform(30,95)) for _ in months] for c in components}

radar_labels = ["T2","T24","T30","T50","P30","Ps30","phi","NRf","T2"]
baseline_vals= [0.85, 0.72, 0.90, 0.68, 0.95, 0.80, 0.60, 0.78, 0.85]
anomaly_vals = [0.55, 0.88, 0.62, 0.91, 0.70, 0.55, 0.82, 0.95, 0.55]

# ─── Header & Engine Selector ─────────────────────────────────────────────────────
selected_engine = st.session_state.get("engine", "Engine #1")

st.markdown(f"""
<div style="
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 8px 10px 8px;
    border-bottom: 1px solid rgba(0,240,255,0.1);
    margin-bottom: 16px;
">
    <!-- Left: Title block -->
    <div style="display: flex; align-items: center; gap: 16px;">
        <div style="
            background: linear-gradient(135deg, #0d1825, #0d2030);
            border: 1.5px solid rgba(0,240,255,0.25);
            border-radius: 10px;
            padding: 8px 18px;
            box-shadow: 0 0 20px rgba(0,240,255,0.12), inset 0 0 10px rgba(0,240,255,0.05);
        ">
            <div style="font-family:'Orbitron',monospace; font-size:11px; color:#00f0ff88; letter-spacing:3px; text-transform:uppercase; margin-bottom:2px;">ANOMX</div>
            <div style="font-family:'Orbitron',monospace; font-size:15px; font-weight:700; color:#e8f4ff; letter-spacing:2px; text-shadow: 0 0 20px #00f0ff66;">AVIATION ASSET MONITORING</div>
        </div>

        <!-- Engine toggles -->
        <div style="display:flex; gap:8px;">
            {"".join([
                f'''<div style="
                    padding: 7px 16px; border-radius: 8px; cursor: pointer;
                    font-family: 'Orbitron', monospace; font-size: 11px; font-weight: 600;
                    letter-spacing: 1.5px;
                    background: {'linear-gradient(135deg, #ff2a5f33, #cc204488)' if e == selected_engine else 'rgba(255,255,255,0.04)'};
                    border: 1.5px solid {'#ff2a5f' if e == selected_engine else 'rgba(255,255,255,0.1)'};
                    color: {'#ff6080' if e == selected_engine else '#4a5568'};
                    box-shadow: {'0 0 14px #ff2a5f44' if e == selected_engine else 'none'};
                    transition: all 0.2s;
                ">{e}</div>'''
                for e in ["Engine #1","Engine #2","Engine #3","Engine #4"]
            ])}
        </div>
    </div>

    <!-- Right: timestamp & status pill -->
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#4a5a6e;">
            LIVE  {datetime.now().strftime("%H:%M:%S")}
        </div>
        <div style="
            display:flex; align-items:center; gap:6px;
            padding: 5px 14px; border-radius: 20px;
            background: rgba(0,240,255,0.08); border: 1px solid rgba(0,240,255,0.3);
        ">
            <div style="width:6px;height:6px;border-radius:50%;background:#00f0ff;box-shadow:0 0 8px #00f0ff;animation: pulse 1.5s infinite;"></div>
            <span style="font-family:'Orbitron',monospace;font-size:10px;color:#00f0ff;letter-spacing:2px;">STREAMING</span>
        </div>
    </div>
</div>

<style>
@keyframes pulse {{
    0%,100% {{ opacity:1; transform:scale(1); }}
    50%      {{ opacity:0.4; transform:scale(0.8); }}
}}
</style>
""", unsafe_allow_html=True)

# ─── KPI Cards Row ───────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([1.1, 1.1, 1.1])

with c1:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0d1525cc, #0a1020cc);
        border: 1.5px solid rgba(0,240,255,0.18);
        border-radius: 14px; padding: 18px 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 1px rgba(0,240,255,0.2);
        height: 130px;
    ">
        <div style="font-family:'Orbitron',monospace; font-size:9px; letter-spacing:3px; color:#00f0ff99; margin-bottom:12px;">OPERATIONAL STATUS</div>
        <div style="display:flex; flex-direction:column; gap:6px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; color:#6b7fa3;">Active Sensors</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#00f0ff; font-weight:600;">21 Channels</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; color:#6b7fa3;">Uptime</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#a0ffa0; font-weight:600;">98.4%</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; color:#6b7fa3;">Kafka Ingestion</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#00f0ff; font-weight:600;">1.2 MB/s</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2a0a1888, #1a0520cc);
        border: 2px solid rgba(255,42,95,0.55);
        border-radius: 14px; padding: 18px 20px;
        backdrop-filter: blur(16px);
        box-shadow: 0 0 40px rgba(255,42,95,0.2), 0 4px 24px rgba(0,0,0,0.5), inset 0 0 20px rgba(255,42,95,0.06);
        height: 130px; position: relative; overflow: hidden;
    ">
        <div style="position:absolute;top:-20px;right:-20px;width:120px;height:120px;
            border-radius:50%;background:radial-gradient(circle, rgba(255,42,95,0.15) 0%, transparent 70%);
            pointer-events:none;"></div>
        <div style="font-family:'Orbitron',monospace; font-size:9px; letter-spacing:3px; color:#ff2a5f; margin-bottom:12px;">ASSET HEALTH SCORE</div>
        <div style="display:flex; gap:16px; align-items:center;">
            <div style="font-family:'Orbitron',monospace; font-size:36px; font-weight:900; color:#ff4060; 
                text-shadow: 0 0 30px #ff2a5f, 0 0 60px rgba(255,42,95,0.4); line-height:1;">86%</div>
            <div style="display:flex; flex-direction:column; gap:5px;">
                <div style="font-size:11px; color:#ff6080;">Pred. RUL: <span style="color:#ffaa00;font-weight:600;">12 Days</span></div>
                <div style="font-size:11px; color:#ff6080;">Risk: <span style="color:#ff2a5f;font-weight:700;">HIGH</span></div>
                <div style="font-size:10px; color:#ff408044;">7–14 day window</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0d1525cc, #0a1020cc);
        border: 1.5px solid rgba(160,100,255,0.25);
        border-radius: 14px; padding: 18px 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 1px rgba(160,100,255,0.3);
        height: 130px;
    ">
        <div style="font-family:'Orbitron',monospace; font-size:9px; letter-spacing:3px; color:#aa66ff99; margin-bottom:12px;">ALERT LOGS & HISTORY</div>
        <div style="display:flex; flex-direction:column; gap:6px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; color:#6b7fa3;">Active Alerts</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#ffaa00; font-weight:600;">3 Pending</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; color:#6b7fa3;">Critical Anomalies</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#ff2a5f; font-weight:600;">1 Detected</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; color:#6b7fa3;">MTTR</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#aa66ff; font-weight:600;">4.2 Hours</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
        with left_mid:
    fig_rul = go.Figure()

    # Shaded danger zone — بدون annotation
    fig_rul.add_hrect(y0=0, y1=30, fillcolor="rgba(255,42,95,0.07)", line_width=0)

    # Annotations
    annotations = [
        dict(x="MAR", y=240, text="Degradation Start", showarrow=True,
             arrowhead=2, arrowcolor="#00f0ff66", font=dict(color="#00f0ff", size=9, family="JetBrains Mono"),
             ax=40, ay=-30, bgcolor="rgba(0,20,30,0.7)", bordercolor="#00f0ff44", borderpad=3),
        dict(x="JUL", y=140, text="Anomaly Detected", showarrow=True,
             arrowhead=2, arrowcolor="#ffaa0088", font=dict(color="#ffaa00", size=9, family="JetBrains Mono"),
             ax=40, ay=-30, bgcolor="rgba(30,20,0,0.7)", bordercolor="#ffaa0044", borderpad=3),
        dict(x="NOV", y=35, text="Critical Threshold", showarrow=True,
             arrowhead=2, arrowcolor="#ff2a5f88", font=dict(color="#ff2a5f", size=9, family="JetBrains Mono"),
             ax=40, ay=-30, bgcolor="rgba(30,0,10,0.7)", bordercolor="#ff2a5f44", borderpad=3),
        dict(x="JAN", y=28, text="CRITICAL ZONE", showarrow=False,
             font=dict(color="#ff2a5f", size=8, family="JetBrains Mono"),
             xanchor="left", yanchor="top"),
    ]

    # Gradient fill under line
    fig_rul.add_trace(go.Scatter(
        x=time_labels, y=[0]*12, fill=None, mode="lines", line=dict(width=0), showlegend=False
    ))السطر الجديد ده
        dict(x="JAN", y=28, text="CRITICAL ZONE", showarrow=False,
             font=dict(color="#ff2a5f", size=8, family="JetBrains Mono"),
             xanchor="left", yanchor="top"),
    ]

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# ─── Middle Row: RUL Trend + Gauge Rings ─────────────────────────────────────────
left_mid, right_mid = st.columns([2.2, 1])

with left_mid:
    # RUL trend line chart
    annotations = [
        dict(x="MAR", y=240, text="Degradation Start", showarrow=True,
             arrowhead=2, arrowcolor="#00f0ff66", font=dict(color="#00f0ff", size=9, family="JetBrains Mono"),
             ax=40, ay=-30, bgcolor="rgba(0,20,30,0.7)", bordercolor="#00f0ff44", borderpad=3),
        dict(x="JUL", y=140, text="Anomaly Detected", showarrow=True,
             arrowhead=2, arrowcolor="#ffaa0088", font=dict(color="#ffaa00", size=9, family="JetBrains Mono"),
             ax=40, ay=-30, bgcolor="rgba(30,20,0,0.7)", bordercolor="#ffaa0044", borderpad=3),
        dict(x="NOV", y=35, text="Critical Threshold", showarrow=True,
             arrowhead=2, arrowcolor="#ff2a5f88", font=dict(color="#ff2a5f", size=9, family="JetBrains Mono"),
             ax=40, ay=-30, bgcolor="rgba(30,0,10,0.7)", bordercolor="#ff2a5f44", borderpad=3),
    ]

    fig_rul = go.Figure()
    # Shaded danger zone
    fig_rul.add_hrect(y0=0, y1=30, fillcolor="rgba(255,42,95,0.07)", line_width=0)
    # Gradient fill under line (fake via scatter fill)
    fig_rul.add_trace(go.Scatter(
        x=time_labels, y=[0]*12, fill=None, mode="lines", line=dict(width=0), showlegend=False
    ))
    fig_rul.add_trace(go.Scatter(
        x=time_labels, y=rul_noisy,
        fill="tonexty",
        fillcolor="rgba(0,240,255,0.06)",
        mode="lines+markers",
        line=dict(color="#00f0ff", width=2.5, shape="spline"),
        marker=dict(color="#00f0ff", size=6, line=dict(color="#080c12", width=1.5),
                    symbol="circle"),
        name="RUL",
        showlegend=False,
    ))

    # Anomaly highlight scatter
    fig_rul.add_trace(go.Scatter(
        x=["JUL"], y=[140],
        mode="markers",
        marker=dict(color="#ffaa00", size=12, symbol="diamond",
                    line=dict(color="#ff6600", width=2),
                    ),
        showlegend=False,
    ))
    fig_rul.add_trace(go.Scatter(
        x=["NOV"], y=[35],
        mode="markers",
        marker=dict(color="#ff2a5f", size=12, symbol="x",
                    line=dict(color="#ff0040", width=2.5)),
        showlegend=False,
    ))

    fig_rul.update_layout(
        title=dict(
            text="<b>Predicted Remaining Useful Life (RUL) Trend</b>",
            font=dict(family="Orbitron", size=12, color="#c8d6e5"),
            x=0, xanchor="left", pad=dict(l=0, b=6)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=270,
        xaxis=dict(
            showgrid=False, tickfont=dict(family="JetBrains Mono", size=9, color="#4a5a6e"),
            tickcolor="#1a2535", linecolor="#1a2535",
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(0,240,255,0.06)", gridwidth=1,
            tickfont=dict(family="JetBrains Mono", size=9, color="#4a5a6e"),
            tickcolor="#1a2535", linecolor="#1a2535",
            title=dict(text="Cycles Remaining", font=dict(size=9, color="#4a5a6e", family="JetBrains Mono")),
            zeroline=False,
        ),
        annotations=annotations,
        hovermode="x unified",
    )

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0d1525cc, #0a1020cc);
        border: 1.5px solid rgba(0,240,255,0.15);
        border-radius: 14px; padding: 16px 16px 8px 16px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    ">
    """, unsafe_allow_html=True)
    st.plotly_chart(fig_rul, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with right_mid:
    # Three glowing gauge rings using Plotly indicators
    def make_gauge(value, label, color, bg_color):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number=dict(suffix="%", font=dict(family="Orbitron", size=26, color=color)),
            gauge=dict(
                axis=dict(range=[0, 100], visible=False),
                bar=dict(color=color, thickness=0.22),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                steps=[dict(range=[0, 100], color=bg_color)],
                threshold=dict(line=dict(color=color, width=2), thickness=0.8, value=value),
            ),
            domain=dict(x=[0,1], y=[0,1]),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=0),
            height=82,
            annotations=[dict(
                text=label, x=0.5, y=-0.05, showarrow=False,
                font=dict(family="JetBrains Mono", size=8, color="#6b7fa3"),
                xanchor="center",
            )]
        )
        return fig

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0d1525cc, #0a1020cc);
        border: 1.5px solid rgba(0,240,255,0.15);
        border-radius: 14px; padding: 14px 12px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
        height: 100%;
    ">
        <div style="font-family:'Orbitron',monospace; font-size:9px; letter-spacing:2px; color:#00f0ff66; margin-bottom:10px; text-align:center;">SENSOR GAUGES</div>
    """, unsafe_allow_html=True)

    gauges = [
        (65, "Vibration Criticality",    "#00c8ff", "rgba(0,200,255,0.08)"),
        (86, "Core Temp Deviation",      "#ff2a5f", "rgba(255,42,95,0.08)"),
        (69, "Exhaust Pressure",         "#aa66ff", "rgba(170,102,255,0.08)"),
    ]
    for val, lbl, col, bg in gauges:
        st.plotly_chart(make_gauge(val, lbl, col, bg), use_container_width=True, config={"displayModeBar": False})

    # Bottom mini KPI row
    st.markdown("""
        <div style="display:flex; justify-content:space-between; margin-top:4px; padding:0 4px;">
            <div style="text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#4a5a6e;">Thrust Output</div>
                <div style="font-family:'Orbitron',monospace;font-size:9px;color:#00c8ff;">NOM</div>
            </div>
            <div style="text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#4a5a6e;">Fuel Flow</div>
                <div style="font-family:'Orbitron',monospace;font-size:9px;color:#ff2a5f;">+8.2%</div>
            </div>
            <div style="text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#4a5a6e;">Oil Contam.</div>
                <div style="font-family:'Orbitron',monospace;font-size:9px;color:#aa66ff;">0.7 ppm</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# ─── Bottom Row: Horizontal Bar Chart + Radar ─────────────────────────────────────
b_left, b_right = st.columns([1.6, 1])

with b_left:
    # Component wear horizontal bar
    fig_bar = go.Figure()
    colors_bar = ["#00f0ff", "#7b61ff", "#ff2a5f", "#ffaa00"]

    for i, comp in enumerate(components):
        fig_bar.add_trace(go.Bar(
            y=months,
            x=wear_data[comp],
            name=comp,
            orientation="h",
            marker=dict(
                color=colors_bar[i],
                opacity=0.75,
                line=dict(width=0),
            ),
            width=0.18,
            offset=(i - 1.5) * 0.18,
        ))

    # Critical threshold line
    fig_bar.add_vline(x=80, line_width=1, line_dash="dot", line_color="#ff2a5f55",
                      annotation_text="⚠ Critical", annotation_font_color="#ff2a5f88",
                      annotation_font_size=8, annotation_font_family="JetBrains Mono")

    fig_bar.update_layout(
        title=dict(
            text="<b>Equipment Running Hours & Duty Cycles</b>",
            font=dict(family="Orbitron", size=11, color="#c8d6e5"),
            x=0, xanchor="left",
        ),
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=280,
        xaxis=dict(
            showgrid=True, gridcolor="rgba(0,240,255,0.05)", gridwidth=1,
            tickfont=dict(family="JetBrains Mono", size=8, color="#4a5a6e"),
            range=[0, 105],
            title=dict(text="Wear Index (%)", font=dict(size=9, color="#4a5a6e", family="JetBrains Mono")),
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(family="JetBrains Mono", size=9, color="#4a5a6e"),
            categoryorder="array", categoryarray=list(reversed(months)),
        ),
        legend=dict(
            orientation="h", x=0, y=1.12,
            font=dict(family="JetBrains Mono", size=8, color="#6b7fa3"),
            bgcolor="rgba(0,0,0,0)",
        ),
        hovermode="y unified",
    )

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0d1525cc, #0a1020cc);
        border: 1.5px solid rgba(0,240,255,0.15);
        border-radius: 14px; padding: 16px 16px 8px 16px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    ">
    """, unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with b_right:
    # Radar / polar chart
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=baseline_vals,
        theta=radar_labels,
        fill="toself",
        fillcolor="rgba(0,240,255,0.1)",
        line=dict(color="#00f0ff", width=1.5, dash="dot"),
        name="Optimal Baseline",
        marker=dict(color="#00f0ff", size=5),
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=anomaly_vals,
        theta=radar_labels,
        fill="toself",
        fillcolor="rgba(255,42,95,0.12)",
        line=dict(color="#ff2a5f", width=2),
        name="Current Anomaly",
        marker=dict(color="#ff2a5f", size=6),
    ))

    fig_radar.update_layout(
        title=dict(
            text="<b>Sensor Multi-Dimensional Profile</b>",
            font=dict(family="Orbitron", size=11, color="#c8d6e5"),
            x=0, xanchor="left",
        ),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            gridshape="circular",
            angularaxis=dict(
                tickfont=dict(family="JetBrains Mono", size=8, color="#6b7fa3"),
                linecolor="rgba(0,240,255,0.12)",
                gridcolor="rgba(0,240,255,0.08)",
            ),
            radialaxis=dict(
                visible=True, range=[0, 1],
                gridcolor="rgba(0,240,255,0.08)",
                tickfont=dict(family="JetBrains Mono", size=7, color="#2a3a4e"),
                linecolor="rgba(0,240,255,0.1)",
                showticklabels=False,
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=280,
        legend=dict(
            x=0.5, y=-0.08, xanchor="center",
            orientation="h",
            font=dict(family="JetBrains Mono", size=8, color="#6b7fa3"),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
    )

    # Deviation badge
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0d1525cc, #0a1020cc);
        border: 1.5px solid rgba(170,102,255,0.2);
        border-radius: 14px; padding: 16px 16px 8px 16px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
        position: relative;
    ">
        <div style="
            position:absolute; top:14px; right:16px;
            background: rgba(255,42,95,0.15); border: 1px solid rgba(255,42,95,0.4);
            border-radius: 20px; padding: 3px 10px;
            font-family:'JetBrains Mono',monospace; font-size:8px; color:#ff6080;
        ">+50% Signal Deviation</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ─── Footer status bar ────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="
    display:flex; align-items:center; justify-content:space-between;
    margin-top: 10px;
    padding: 10px 12px;
    background: rgba(13,17,23,0.9);
    border: 1px solid rgba(0,240,255,0.08);
    border-radius: 10px;
    font-family:'JetBrains Mono',monospace; font-size:9px; color:#2a3a4e;
">
    <div style="display:flex; gap:24px;">
        <span>PIPELINE: <span style="color:#00f0ff88;">KAFKA ✓</span></span>
        <span>SPARK: <span style="color:#00f0ff88;">ACTIVE</span></span>
        <span>DBT: <span style="color:#00f0ff88;">SYNCED</span></span>
        <span>ML MODEL: <span style="color:#ffaa0088;">INFERENCE</span></span>
        <span>AZURE DL: <span style="color:#00f0ff88;">CONNECTED</span></span>
    </div>
    <div style="color:#2a3a4e;">
        AnomX v1.0 · NASA C-MAPSS · {datetime.now().strftime("%d %b %Y")}
    </div>
</div>
""", unsafe_allow_html=True)
