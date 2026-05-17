# -*- coding: utf-8 -*-
"""
app.py
Offline Urdu Speech-to-Text System - Premium Enhanced UI
"""

import os
import time
import streamlit as st

st.set_page_config(
    page_title="Offline Urdu Speech-to-Text System",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    from session_controller import SessionController
    MODULES_OK = True
    MODULE_ERR = ""
except ImportError as e:
    MODULES_OK = False
    MODULE_ERR = str(e)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Nastaliq+Urdu:wght@400;600;700&display=swap');

:root {
  --bg:        #0e1a2e;
  --bg2:       #112240;
  --surface:   #162d4a;
  --card:      #1a3356;
  --card2:     #1f3a60;
  --accent:    #4f9eff;
  --accent2:   #38bdf8;
  --accent3:   #7dd3fc;
  --teal:      #2dd4bf;
  --purple:    #818cf8;
  --text:      #e8f0fe;
  --text2:     #93b4d8;
  --text3:     #5580a0;
  --stroke:    rgba(79,158,255,0.15);
  --stroke2:   rgba(79,158,255,0.08);
  --glow:      rgba(79,158,255,0.2);
  --glow2:     rgba(45,212,191,0.15);
}

/* ── Reset & Base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

.block-container {
  padding: 2rem 2.5rem !important;
  max-width: 100% !important;
}

/* ── Grid background ── */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(79,158,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(79,158,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none; z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: rgba(14,26,46,0.95) !important;
  border-right: 1px solid var(--stroke) !important;
}

[data-testid="stSidebar"] > div { padding: 2rem 1.4rem !important; }

/* ── HEADER ── */
.main-header {
  position: relative;
  background: linear-gradient(135deg, rgba(79,158,255,0.12) 0%, rgba(45,212,191,0.07) 100%);
  border: 1px solid var(--stroke);
  border-radius: 22px;
  padding: 2rem 2.8rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  overflow: hidden;
}

.main-header::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(79,158,255,0.5), rgba(45,212,191,0.3), transparent);
}

.main-header::after {
  content: '';
  position: absolute;
  top: -80px; right: -80px;
  width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(79,158,255,0.12) 0%, transparent 65%);
  pointer-events: none;
}

.header-icon {
  width: 72px; height: 72px;
  background: linear-gradient(135deg, rgba(79,158,255,0.25), rgba(45,212,191,0.15));
  border: 1px solid rgba(79,158,255,0.4);
  border-radius: 18px;
  display: flex; align-items: center; justify-content: center;
  font-size: 38px;
  flex-shrink: 0;
  box-shadow: 0 0 36px rgba(79,158,255,0.2);
  position: relative; z-index: 1;
}

.header-title {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text);
  margin: 0 0 10px 0;
  position: relative; z-index: 1;
}

.header-title span {
  background: linear-gradient(90deg, var(--accent2), var(--teal));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-badges {
  display: flex; gap: 8px; flex-wrap: wrap;
  position: relative; z-index: 1;
}

.hbadge {
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.hbadge-green {
  background: rgba(45,212,191,0.1);
  border: 1px solid rgba(45,212,191,0.25);
  color: #5eead4;
}

.hbadge-purple {
  background: rgba(79,158,255,0.15);
  border: 1px solid rgba(79,158,255,0.3);
  color: var(--accent3);
}

.hbadge-pink {
  background: rgba(129,140,248,0.1);
  border: 1px solid rgba(129,140,248,0.25);
  color: #a5b4fc;
}

/* ── Cards ── */
.card {
  background: linear-gradient(160deg, var(--card), var(--bg2));
  border: 1px solid var(--stroke);
  border-radius: 18px;
  padding: 1.6rem;
  margin-bottom: 1.2rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  position: relative; overflow: hidden;
}

.card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(79,158,255,0.3), transparent);
}

.card:hover {
  border-color: rgba(79,158,255,0.3);
  box-shadow: 0 8px 32px rgba(79,158,255,0.08);
}

.card-recording {
  border-color: rgba(45,212,191,0.5) !important;
  box-shadow: 0 0 50px rgba(45,212,191,0.12), inset 0 0 30px rgba(45,212,191,0.04) !important;
  background: linear-gradient(135deg, #1a3356, #0f2a1f) !important;
}

/* ── Status Badge ── */
.status-badge {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 9px 18px;
  border-radius: 100px;
  font-size: 11px; font-weight: 700;
  letter-spacing: 0.08em;
  font-family: 'IBM Plex Mono', monospace;
  margin-bottom: 1rem;
}

.status-live {
  background: rgba(45,212,191,0.12);
  border: 1.5px solid rgba(45,212,191,0.5);
  color: var(--teal);
}

.status-idle {
  background: rgba(71,85,105,0.2);
  border: 1.5px solid rgba(71,85,105,0.4);
  color: var(--text3);
}

@keyframes pulse-ring {
  0% { box-shadow: 0 0 0 0 rgba(52,211,153,0.7); }
  70% { box-shadow: 0 0 0 10px rgba(52,211,153,0); }
  100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
}

.pulse-dot {
  width: 9px; height: 9px;
  border-radius: 50%;
  background: var(--teal);
  animation: pulse-ring 1.5s ease infinite;
}

/* ── Timer ── */
.timer-wrap {
  text-align: center;
  padding: 0.8rem 0 0.4rem;
}

.timer-display {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 64px;
  font-weight: 600;
  letter-spacing: -0.04em;
  line-height: 1;
  background: linear-gradient(135deg, var(--accent2), var(--teal));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.timer-label {
  font-size: 9px;
  color: var(--text3);
  letter-spacing: 0.22em;
  font-family: 'IBM Plex Mono', monospace;
  margin-top: 5px;
  text-transform: uppercase;
}

/* ── Audio visualizer bars ── */
.visualizer {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 4px;
  height: 42px;
  margin: 0.8rem 0 0.4rem;
}

.v-bar {
  width: 5px;
  border-radius: 3px;
  background: linear-gradient(180deg, var(--accent2), var(--teal));
  opacity: 0.65;
}

@keyframes bar1 { 0%,100%{height:6px} 50%{height:34px} }
@keyframes bar2 { 0%,100%{height:18px} 50%{height:8px} }
@keyframes bar3 { 0%,100%{height:10px} 50%{height:40px} }
@keyframes bar4 { 0%,100%{height:26px} 50%{height:6px} }
@keyframes bar5 { 0%,100%{height:4px} 50%{height:22px} }
@keyframes bar6 { 0%,100%{height:16px} 50%{height:38px} }
@keyframes bar7 { 0%,100%{height:8px} 50%{height:20px} }
@keyframes bar8 { 0%,100%{height:28px} 50%{height:10px} }

.v-bar.b1{animation:bar1 1.0s ease infinite;}
.v-bar.b2{animation:bar2 1.2s ease infinite 0.1s;}
.v-bar.b3{animation:bar3 0.9s ease infinite 0.2s;}
.v-bar.b4{animation:bar4 1.3s ease infinite 0.05s;}
.v-bar.b5{animation:bar5 1.0s ease infinite 0.3s;}
.v-bar.b6{animation:bar6 1.1s ease infinite 0.15s;}
.v-bar.b7{animation:bar7 0.85s ease infinite 0.25s;}
.v-bar.b8{animation:bar8 1.2s ease infinite 0.1s;}

.v-bar-idle { height: 4px !important; opacity: 0.15; animation: none !important; }

/* ── Buttons ── */
div[data-testid="stButton"] > button {
  width: 100%;
  padding: 14px 20px !important;
  border-radius: 12px;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 0.05em;
  transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
  border: 1px solid var(--stroke) !important;
  background: rgba(79,158,255,0.1) !important;
  color: var(--accent3) !important;
  box-shadow: 0 4px 16px rgba(79,158,255,0.08) !important;
  position: relative; overflow: hidden;
}

div[data-testid="stButton"] > button:not([disabled]):hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(79,158,255,0.2) !important;
  border-color: rgba(79,158,255,0.4) !important;
  background: rgba(79,158,255,0.18) !important;
}

div[data-testid="stButton"] > button:not([disabled]):active {
  transform: translateY(0);
}

div[data-testid="stButton"] > button:disabled {
  opacity: 0.3 !important;
  cursor: not-allowed !important;
  transform: none !important;
  background: rgba(26,51,86,0.4) !important;
  border-color: rgba(85,128,160,0.2) !important;
  color: var(--text3) !important;
  box-shadow: none !important;
}

/* START button — teal tint */
div[data-testid="stButton"]:has(button:not([disabled])[kind="secondary"]):first-child > button,
div[data-testid="stButton"] > button[data-testid*="start"] {
  border-color: rgba(45,212,191,0.35) !important;
  background: rgba(45,212,191,0.1) !important;
  color: #5eead4 !important;
}

/* ── Live Transcription Box ── */
.live-box {
  background: linear-gradient(135deg, rgba(79,158,255,0.07), rgba(45,212,191,0.04));
  border: 1.5px solid var(--stroke);
  border-radius: 18px;
  padding: 2.2rem 2.6rem;
  min-height: 300px;
  direction: rtl;
  text-align: right;
  font-size: 24px;
  line-height: 2.4;
  color: var(--text);
  font-family: 'Noto Nastaliq Urdu', Georgia, serif;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: all 0.4s ease;
  position: relative;
}

.live-box::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(79,158,255,0.25), transparent);
}

.live-box-active {
  border-color: rgba(45,212,191,0.4);
  background: linear-gradient(135deg, rgba(79,158,255,0.1), rgba(45,212,191,0.07));
  box-shadow: 0 0 50px rgba(45,212,191,0.08), inset 0 0 30px rgba(79,158,255,0.04);
}

.live-placeholder {
  direction: ltr;
  text-align: center;
  font-size: 13px;
  color: var(--text3);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 500;
}

@keyframes blink {
  0%,100% { opacity: 1; }
  50% { opacity: 0; }
}

.cursor {
  display: inline-block;
  width: 2px; height: 24px;
  background: var(--teal);
  margin-left: 8px;
  animation: blink 1s step-end infinite;
  border-radius: 2px;
  vertical-align: middle;
}

/* ── Results Panel ── */
.sentences-container {
  max-height: 520px;
  overflow-y: auto;
  display: flex;
  flex-direction: column-reverse;
  gap: 9px;
  padding-right: 4px;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(16px); }
  to   { opacity: 1; transform: translateX(0); }
}

.sentence-card {
  background: var(--card2);
  border: 1px solid var(--stroke);
  border-radius: 13px;
  padding: 1.1rem 1.3rem;
  animation: slideIn 0.35s ease;
  transition: all 0.25s ease;
}

.sentence-card:hover {
  border-color: rgba(79,158,255,0.3);
  transform: translateX(-4px);
  box-shadow: 0 4px 16px rgba(79,158,255,0.08);
}

.sentence-card.latest {
  border-color: rgba(45,212,191,0.4);
  background: linear-gradient(135deg, rgba(45,212,191,0.08), rgba(79,158,255,0.05));
  box-shadow: 0 0 24px rgba(45,212,191,0.1);
}

.sentence-time {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  color: var(--teal);
  margin-bottom: 8px;
  font-weight: 600;
  letter-spacing: 0.12em;
}

.sentence-text {
  direction: rtl;
  text-align: right;
  font-size: 17px;
  line-height: 2;
  color: var(--text);
  font-family: 'Noto Nastaliq Urdu', Georgia, serif;
  word-break: break-word;
}

/* ── Empty State ── */
.empty-state {
  text-align: center;
  padding: 50px 20px;
  color: var(--text3);
}

@keyframes float {
  0%,100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.empty-icon {
  font-size: 44px;
  margin-bottom: 12px;
  animation: float 3s ease-in-out infinite;
  opacity: 0.35;
}

/* ── Stat Metric ── */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(4,1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.stat-box {
  background: linear-gradient(135deg, var(--card), var(--bg2));
  border: 1px solid var(--stroke);
  border-radius: 14px;
  padding: 1.1rem;
  text-align: center;
  transition: all 0.25s ease;
  position: relative; overflow: hidden;
}

.stat-box::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(79,158,255,0.25), transparent);
}

.stat-box:hover {
  border-color: rgba(79,158,255,0.3);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(79,158,255,0.08);
}

.stat-icon { font-size: 20px; margin-bottom: 5px; }

.stat-val {
  font-size: 30px;
  font-weight: 800;
  font-family: 'IBM Plex Mono', monospace;
  background: linear-gradient(135deg, var(--accent2), var(--teal));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

.stat-lbl {
  font-size: 9px;
  color: var(--text3);
  letter-spacing: 0.18em;
  font-weight: 700;
  margin-top: 3px;
  text-transform: uppercase;
}

/* ── Sidebar Info ── */
.sidebar-logo {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text);
  margin-bottom: 3px;
}

.sidebar-sub {
  font-size: 10px;
  color: var(--text3);
  letter-spacing: 0.08em;
  margin-bottom: 1.4rem;
  font-family: 'IBM Plex Mono', monospace;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid var(--stroke2);
  font-size: 12px;
}

.info-key { color: var(--text2); font-weight: 500; }

.info-val {
  color: var(--accent2);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  font-weight: 600;
}

/* ── Section Heading ── */
.sec-heading {
  font-size: 13px;
  font-weight: 700;
  color: var(--text2);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.sec-heading::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--stroke);
}

/* ── Divider ── */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, rgba(79,158,255,0.2), transparent) !important;
  margin: 1.6rem 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(79,158,255,0.2);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(79,158,255,0.4); }

/* ── Streamlit metric override ── */
[data-testid="stMetric"] {
  background: linear-gradient(135deg, var(--card), var(--bg2)) !important;
  border: 1px solid var(--stroke) !important;
  border-radius: 14px !important;
  padding: 1rem 1.2rem !important;
}

[data-testid="stMetricLabel"] { color: var(--text3) !important; font-size: 11px !important; }
[data-testid="stMetricValue"] {
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 20px !important;
  color: var(--accent2) !important;
}
</style>
"""

# ═══════════════════════════════════════════════════════════
# Utility
# ═══════════════════════════════════════════════════════════

def fmt_time(secs: float) -> str:
    s = int(secs)
    return f"{s // 60:02d}:{s % 60:02d}"


def initialize_session_state():
    if "controller" not in st.session_state:
        if MODULES_OK:
            try:
                st.session_state.controller = SessionController()
                st.session_state.init_error = ""
            except SystemExit:
                st.session_state.controller = None
                st.session_state.init_error = "Model failed to load"
            except Exception as e:
                st.session_state.controller = None
                st.session_state.init_error = str(e)
        else:
            st.session_state.controller = None
            st.session_state.init_error = f"Import error: {MODULE_ERR}"

    st.session_state.setdefault("is_recording", False)
    st.session_state.setdefault("log_path", "")
    st.session_state.setdefault("show_cleared", False)


# ═══════════════════════════════════════════════════════════
# Sidebar
# ═══════════════════════════════════════════════════════════

def render_sidebar():
    ctrl = st.session_state.get("controller")
    is_recording = st.session_state.get("is_recording", False)

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-logo">🎤 Speech·to·Text</div>'
            '<div class="sidebar-sub">OFFLINE URDU TRANSCRIPTION</div>',
            unsafe_allow_html=True,
        )

        if is_recording:
            st.markdown(
                '<div class="status-badge status-live"><span class="pulse-dot"></span>LIVE · RECORDING</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="status-badge status-idle">◎ &nbsp; STANDBY</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        if ctrl:
            info = ctrl.get_model_info()
            st.markdown(
                '<div style="font-size:10px;font-weight:700;letter-spacing:0.18em;'
                'color:var(--text3);text-transform:uppercase;margin-bottom:0.8rem;">System Info</div>',
                unsafe_allow_html=True,
            )
            rows = [
                ("Model",   info.get("name", "whisper-tiny")),
                ("Engine",  info.get("engine", "OpenAI Whisper")),
                ("Language","🇵🇰 اردو"),
                ("Rate",    "16 kHz"),
                ("Mode",    "🔒 Offline"),
            ]
            for k, v in rows:
                st.markdown(
                    f'<div class="info-row">'
                    f'<span class="info-key">{k}</span>'
                    f'<span class="info-val">{v}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


# ═══════════════════════════════════════════════════════════
# Main Content
# ═══════════════════════════════════════════════════════════

def render_main_content():
    ctrl = st.session_state.get("controller")
    is_recording = st.session_state.get("is_recording", False)
    init_error = st.session_state.get("init_error", "")

    if init_error:
        st.error(f"❌ Initialization Error: {init_error}")
        st.stop()
    if not ctrl:
        st.error("❌ System not initialized")
        st.stop()

    # Sync state
    actual = ctrl.get_status()
    if actual != is_recording:
        st.session_state.is_recording = actual
        is_recording = actual

    # ── Header ──────────────────────────────────────────────
    st.markdown(
        '<div class="main-header">'
        '<div class="header-icon">🎙️</div>'
        '<div class="header-content">'
        '<div class="header-title">Offline Real-Time <span>Urdu Speech-to-Text</span></div>'
        '<div class="header-badges">'
        '<span class="hbadge hbadge-green">✓ 100% Offline</span>'
        '<span class="hbadge hbadge-purple">OpenAI Whisper</span>'
        '<span class="hbadge hbadge-pink">اردو · Urdu</span>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── 3-column layout ──────────────────────────────────────
    col1, col2, col3 = st.columns([0.95, 2.1, 1.3], gap="large")

    # ── Col 1 : Controls ─────────────────────────────────────
    with col1:
        card_cls = "card card-recording" if is_recording else "card"

        # Visualizer bars
        bar_cls = "" if is_recording else "v-bar-idle"
        bars = "".join(
            f'<div class="v-bar b{i} {bar_cls}"></div>' for i in range(1, 9)
        )

        st.markdown(
            f'<div class="{card_cls}">'
            f'<div class="status-badge {"status-live" if is_recording else "status-idle"}">'
            f'{"<span class=pulse-dot></span>" if is_recording else "◎ &nbsp;"}'
            f'{"RECORDING" if is_recording else "READY"}'
            f'</div>'
            f'<div class="visualizer">{bars}</div>'
            f'<div class="timer-wrap">'
            f'<div class="timer-display">{fmt_time(ctrl.get_session_duration() if is_recording else 0.0)}</div>'
            f'<div class="timer-label">{"ELAPSED TIME" if is_recording else "DURATION"}</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            def on_start():
                if not st.session_state.is_recording:
                    try:
                        st.session_state.show_cleared = False  # ✅ ALWAYS reset when starting
                        if ctrl.start_session():
                            st.session_state.is_recording = True
                    except Exception as e:
                        st.error(f"❌ {str(e)[:60]}")
            st.button("▶  START", key="btn_start", disabled=is_recording,
                      use_container_width=True, on_click=on_start)

        with c2:
            def on_stop():
                if st.session_state.is_recording:
                    try:
                        print("[App] STOP clicked")
                        # ✅ Get final text directly from stop_session
                        final_text = ctrl.stop_session()
                        st.session_state.is_recording = False  # ✅ This triggers Streamlit rerun
                        st.session_state.show_cleared = False
                        print(f"[App] STOP done. Final text: '{final_text}'")
                    except Exception as e:
                        print(f"[App] STOP error: {str(e)}")
                        st.error(f"❌ {str(e)[:60]}")
            st.button("⏹  STOP", key="btn_stop", disabled=not is_recording,
                      use_container_width=True, on_click=on_stop)

        st.divider()

        # Sentence counter card removed (duplicate with bottom stats)

    # ── Col 2 : Live Transcription ───────────────────────────
    with col2:
        st.markdown('<div class="sec-heading">🎤 Live Transcription</div>', unsafe_allow_html=True)

        partial = ctrl.get_partial_text() if is_recording else ""

        if is_recording:
            if partial:
                display = f"{partial}<span class='cursor'></span>"
            else:
                display = '<span class="live-placeholder">👂 &nbsp; Listening for speech…</span><span class="cursor"></span>'
            box_cls = "live-box live-box-active"
        else:
            display = '<span class="live-placeholder">👈 &nbsp; Click START to begin transcription</span>'
            box_cls = "live-box"

        st.markdown(f'<div class="{box_cls}">{display}</div>', unsafe_allow_html=True)

    # ── Col 3 : Results ──────────────────────────────────────
    with col3:
        st.markdown('<div class="sec-heading">💬 Results</div>', unsafe_allow_html=True)

        show_cleared = st.session_state.get("show_cleared", False)
        transcriptions = (
            ctrl.get_all_transcriptions()
            if not show_cleared
            else []
        )
        
        # DEBUG: Show what's happening
        print(f"[UI Results] show_cleared={show_cleared}, count={len(transcriptions)}")
        if transcriptions:
            for item in transcriptions:
                print(f"  → Displaying: {item}")

        if transcriptions:
            st.markdown('<div class="sentences-container">', unsafe_allow_html=True)
            for idx, item in enumerate(reversed(transcriptions)):
                cls = "sentence-card latest" if idx == 0 else "sentence-card"
                st.markdown(
                    f'<div class="{cls}">'
                    f'<div class="sentence-time">⏱ {item["timestamp"]}  ✓</div>'
                    f'<div class="sentence-text">{item["text"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="empty-state">'
                '<div class="empty-icon">💬</div>'
                '<div style="font-size:13px;font-weight:600;">No sentences yet</div>'
                '<div style="font-size:11px;margin-top:6px;color:var(--text3);">Start recording to see results</div>'
                '</div>',
                unsafe_allow_html=True,
            )

    # ── Bottom Stats ─────────────────────────────────────────
    st.divider()

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4, gap="medium")

    with stat_col1:
        st.metric("📝 Sentences", ctrl.get_sentence_count())
    with stat_col2:
        dur = ctrl.get_session_duration() if is_recording else 0.0
        st.metric("⏱ Duration", fmt_time(dur))
    with stat_col3:
        log_name = st.session_state.get("log_path", "").split("\\")[-1] or "—"
        st.metric("📄 Log", log_name[:16] if log_name != "—" else "—")
    with stat_col4:
        st.metric("🔔 Status", "🔴 Recording" if is_recording else "✅ Ready")

    st.divider()

    # ── Action Buttons ───────────────────────────────────────
    a1, a2, a3 = st.columns(3)

    with a1:
        if st.button("📁  Open Logs", use_container_width=True):
            try:
                import subprocess, sys
                logs_path = os.path.abspath("logs")
                if sys.platform == "win32":
                    os.startfile(logs_path)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", logs_path])
                else:
                    subprocess.Popen(["xdg-open", logs_path])
                st.success("✅ Logs folder opened!")
            except Exception as e:
                st.error(f"❌ {str(e)[:40]}")

    with a2:
        if st.button("🗑️  Clear Display", use_container_width=True):
            st.session_state.show_cleared = not st.session_state.get("show_cleared", False)
            st.rerun()

    with a3:
        if st.button("🔄  Refresh", use_container_width=True):
            st.rerun()

    # Auto-refresh while recording
    if is_recording:
        time.sleep(1.0)
        st.rerun()


# ═══════════════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════════════

def main():
    st.markdown(CSS, unsafe_allow_html=True)
    initialize_session_state()
    render_sidebar()
    render_main_content()


if __name__ == "__main__":
    main()
