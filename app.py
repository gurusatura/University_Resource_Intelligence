import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Clean modular imports from src/ package
from src import agent_tools
from src import agent

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="University Resource Intelligence System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Premium CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* Header bar */
.header-container {
    background: linear-gradient(135deg, #1c2a3a 0%, #0d1117 100%);
    border-bottom: 1px solid #21262d;
    padding: 2rem 3rem 1.5rem 3rem;
    margin: -4rem -4rem 2rem -4rem;
}
.header-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #e6edf3;
    letter-spacing: -0.5px;
    margin: 0;
}
.header-subtitle {
    font-size: 0.88rem;
    color: #8b949e;
    margin-top: 0.3rem;
    font-weight: 400;
}
.header-badge {
    display: inline-block;
    background: #1f6feb22;
    border: 1px solid #1f6feb55;
    color: #58a6ff;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.18rem 0.65rem;
    border-radius: 20px;
    margin-top: 0.5rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Metric cards */
.metric-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    transition: border-color 0.2s;
}
.metric-card:hover {
    border-color: #30363d;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #e6edf3;
    line-height: 1;
}
.metric-label {
    font-size: 0.78rem;
    color: #8b949e;
    font-weight: 500;
    margin-top: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.metric-pill {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.15rem 0.55rem;
    border-radius: 12px;
    margin-top: 0.6rem;
}
.pill-danger { background: #da3633aa; color: #ff7b72; border: 1px solid #da363360; }
.pill-info   { background: #1f6feb33; color: #79c0ff; border: 1px solid #1f6feb60; }
.pill-warn   { background: #9e6a0333; color: #e3b341; border: 1px solid #9e6a0360; }

/* Section headers */
.section-header {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #8b949e;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #21262d;
}

/* Conflict banner */
.conflict-banner {
    background: #1a0a0a;
    border: 1px solid #da363360;
    border-left: 4px solid #da3633;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin: 1rem 0;
}
.conflict-banner-title {
    color: #ff7b72;
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.conflict-banner-body {
    color: #e6edf3;
    font-size: 0.9rem;
    margin-top: 0.3rem;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-radius: 8px;
    padding: 4px;
    gap: 2px;
    border: 1px solid #21262d;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px;
    color: #8b949e;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.5rem 1.5rem;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: #1f6feb !important;
    color: #ffffff !important;
}

/* Chat messages */
.stChatMessage {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
}

/* Chat input */
.stChatInputContainer {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
}

/* Plotly chart container */
.js-plotly-plot {
    border-radius: 8px;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; }

/* Divider */
hr { border-color: #21262d !important; }
</style>
""", unsafe_allow_html=True)

# ── Plotly Theme Helper ───────────────────────────────────────────────────────
CHART_THEME = dict(
    plot_bgcolor="#161b22",
    paper_bgcolor="#161b22",
    font_color="#8b949e",
    font_family="Inter",
    title_font_color="#e6edf3",
    title_font_size=13,
    colorway=["#1f6feb", "#388bfd", "#58a6ff", "#79c0ff", "#a5d6ff",
              "#cae8ff", "#3fb950", "#56d364", "#7ee787"],
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickfont_color="#8b949e"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickfont_color="#8b949e"),
)

def apply_theme(fig, title=""):
    fig.update_layout(
        **CHART_THEME,
        title=dict(text=title, font_size=13, font_color="#e6edf3"),
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(
            bgcolor="#21262d",
            bordercolor="#30363d",
            borderwidth=1,
            font_color="#8b949e"
        ),
        hoverlabel=dict(bgcolor="#21262d", bordercolor="#30363d", font_color="#e6edf3")
    )
    fig.update_xaxes(**CHART_THEME["xaxis"])
    fig.update_yaxes(**CHART_THEME["yaxis"])
    return fig

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-container">
    <div class="header-title">University Resource Intelligence System</div>
    <div class="header-subtitle">Scheduling analytics, conflict detection, demand forecasting, and AI-assisted recommendations</div>
    <span class="header-badge">Live Data</span>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Dashboard", "Intelligence Agent"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
with tab1:

    # Load all data upfront
    util_data     = agent_tools.get_classroom_utilization()
    workload_data = agent_tools.get_instructor_workload()
    demand_data   = agent_tools.get_course_demand()
    forecast_data = agent_tools.get_forecast()
    conflicts     = agent_tools.get_conflict_detection()
    c_rooms       = conflicts.get("classroom_conflicts", [])
    c_inst        = conflicts.get("instructor_conflicts", [])

    df_util     = pd.DataFrame(util_data)
    df_workload = pd.DataFrame(workload_data)
    df_demand   = pd.DataFrame(demand_data)
    df_forecast = pd.DataFrame(forecast_data)

    # ── KPI Row ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)

    top_room = df_util.iloc[0] if not df_util.empty else {}
    top_inst = df_workload.iloc[0] if not df_workload.empty else {}
    top_fc   = df_forecast.iloc[0] if not df_forecast.empty else {}

    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{int(top_room.get('total_scheduled_hours', 0))}</div>
            <div class="metric-label">Peak Room Hours</div>
            <span class="metric-pill pill-info">{top_room.get('room_name', '—')}</span>
        </div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(c_inst):,}</div>
            <div class="metric-label">Instructor Conflicts</div>
            <span class="metric-pill pill-danger">Requires Review</span>
        </div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(c_rooms):,}</div>
            <div class="metric-label">Room Double-Bookings</div>
            <span class="metric-pill pill-danger">Requires Review</span>
        </div>""", unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{int(top_fc.get('forecast_Fall_2026', 0))}</div>
            <div class="metric-label">Highest Fall 2026 Forecast</div>
            <span class="metric-pill pill-warn">{top_fc.get('trend_direction', '—')}</span>
        </div>""", unsafe_allow_html=True)

    # ── Conflict Alert ────────────────────────────────────────────────────────
    if c_inst:
        worst = c_inst[0]
        st.markdown(f"""
        <div class="conflict-banner">
            <div class="conflict-banner-title">Critical Conflict Detected</div>
            <div class="conflict-banner-body">
                <strong>{worst['instructor_name']}</strong> is assigned to
                <strong>{worst['overlapping_courses']} overlapping courses</strong>
                simultaneously on <strong>{worst['day']}</strong>
                (Timeslot {worst['timeslot_id']}, {worst['start_time']} – {worst['end_time']}).
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ── Charts Row 1 ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Utilization & Workload</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if not df_util.empty:
            fig = px.bar(
                df_util, x="room_name", y="total_scheduled_hours",
                labels={"total_scheduled_hours": "Scheduled Hours", "room_name": "Classroom"},
            )
            apply_theme(fig, "Classroom Utilization — Scheduled Hours per Room")
            fig.update_traces(marker_color="#1f6feb", marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if not df_workload.empty:
            fig = px.box(
                df_workload, x="department", y="total_sessions",
                labels={"total_sessions": "Sessions Taught", "department": "Department"},
                color="department", color_discrete_sequence=CHART_THEME["colorway"]
            )
            apply_theme(fig, "Instructor Workload Distribution by Department")
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    # ── Charts Row 2 ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Enrollment & Forecasting</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        if not df_demand.empty:
            fig = px.bar(
                df_demand, x="course_name", y="enrollment", color="department",
                labels={"enrollment": "Students Enrolled", "course_name": "Course"},
                color_discrete_sequence=CHART_THEME["colorway"]
            )
            apply_theme(fig, "Course Enrollment — Student Count per Course")
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        if not df_forecast.empty:
            top10 = df_forecast.head(10).copy()
            color_map = {"Increasing": "#3fb950", "Stable": "#1f6feb", "Decreasing": "#da3633"}
            fig = px.bar(
                top10, x="course_name", y="forecast_Fall_2026",
                color="trend_direction",
                labels={"forecast_Fall_2026": "Forecasted Students", "course_name": "Course", "trend_direction": "Trend"},
                color_discrete_map=color_map
            )
            apply_theme(fig, "Fall 2026 Demand Forecast — Top 10 Courses")
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    # ── Conflict Detail Tables ────────────────────────────────────────────────
    st.markdown('<div class="section-header">Conflict Detail</div>', unsafe_allow_html=True)
    ct1, ct2 = st.columns(2)

    with ct1:
        if c_inst:
            df_ci = pd.DataFrame(c_inst[:10])[
                ["instructor_name", "day", "timeslot_id", "overlapping_courses"]
            ].rename(columns={
                "instructor_name": "Instructor",
                "day": "Day",
                "timeslot_id": "Timeslot ID",
                "overlapping_courses": "Overlapping Courses"
            })
            st.caption("Top 10 Instructor Conflicts")
            st.dataframe(df_ci, use_container_width=True, hide_index=True)

    with ct2:
        if c_rooms:
            df_cr = pd.DataFrame(c_rooms[:10])[
                ["room_name", "day", "timeslot_id", "overlapping_courses"]
            ].rename(columns={
                "room_name": "Room",
                "day": "Day",
                "timeslot_id": "Timeslot ID",
                "overlapping_courses": "Overlapping Courses"
            })
            st.caption("Top 10 Classroom Double-Bookings")
            st.dataframe(df_cr, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: AGENT CHAT — WhatsApp Layout
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    import datetime

    st.markdown("""
    <style>
    .wa-header {
        background: #075E54;
        border-radius: 12px 12px 0 0;
        padding: 0.85rem 1.4rem;
        display: flex;
        align-items: center;
        gap: 0.9rem;
    }
    .wa-avatar {
        width: 40px; height: 40px;
        background: #128C7E;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.9rem; font-weight: 700; color: #fff;
        flex-shrink: 0;
    }
    .wa-header-name  { font-size: 0.97rem; font-weight: 600; color: #fff; line-height: 1.2; }
    .wa-header-sub   { font-size: 0.73rem; color: rgba(255,255,255,0.72); }

    .wa-body {
        background-color: #0b141a;
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23182229' fill-opacity='0.9'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        min-height: 440px;
        max-height: 520px;
        overflow-y: auto;
        padding: 1rem 1.2rem;
        border-left: 1px solid #1f2c33;
        border-right: 1px solid #1f2c33;
    }

    .wa-row-user { display:flex; justify-content:flex-end; margin:0.45rem 0; }
    .wa-row-bot  { display:flex; justify-content:flex-start; margin:0.45rem 0; }

    .wa-bubble-user {
        background: #005c4b;
        color: #e9edef;
        border-radius: 10px 2px 10px 10px;
        padding: 0.5rem 0.85rem 0.35rem 0.85rem;
        max-width: 68%;
        font-size: 0.875rem;
        line-height: 1.55;
        box-shadow: 0 1px 2px rgba(0,0,0,0.4);
        word-wrap: break-word;
    }
    .wa-bubble-bot {
        background: #1f2c33;
        color: #e9edef;
        border-radius: 2px 10px 10px 10px;
        padding: 0.5rem 0.85rem 0.35rem 0.85rem;
        max-width: 72%;
        font-size: 0.875rem;
        line-height: 1.55;
        box-shadow: 0 1px 2px rgba(0,0,0,0.4);
        word-wrap: break-word;
    }
    .wa-ts {
        font-size: 0.64rem;
        color: rgba(233,237,239,0.45);
        text-align: right;
        margin-top: 3px;
    }
    .ticks { color: #53bdeb; }

    .wa-date-divider {
        text-align: center;
        margin: 1rem 0 0.8rem 0;
    }
    .wa-date-chip {
        background: #182229;
        color: #8696a0;
        font-size: 0.7rem;
        padding: 0.28rem 0.9rem;
        border-radius: 20px;
        border: 1px solid #2a373f;
    }

    .wa-inputbar {
        background: #1f2c33;
        border-radius: 0 0 12px 12px;
        border-top: 1px solid #2a373f;
        padding: 0.6rem 1rem;
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    .wa-send-btn {
        background: #00a884;
        border-radius: 50%;
        width: 38px; height: 38px;
        display: inline-flex; align-items: center; justify-content: center;
        color: #fff; font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    def ts_now():
        return datetime.datetime.now().strftime("%I:%M %p")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Header
    st.markdown("""
    <div class="wa-header">
        <div class="wa-avatar">UA</div>
        <div>
            <div class="wa-header-name">University Scheduling Assistant</div>
            <div class="wa-header-sub">6 live data tools &bull; Online</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Build bubble HTML
    body = '<div class="wa-body">'
    body += '<div class="wa-date-divider"><span class="wa-date-chip">Today</span></div>'
    body += """
    <div class="wa-row-bot">
        <div class="wa-bubble-bot">
            Hello! I am your University Scheduling Assistant.<br>
            Ask me anything about rooms, instructors, conflicts, or forecasts.
            <div class="wa-ts">Just now</div>
        </div>
    </div>"""

    for msg in st.session_state.messages:
        txt = msg["content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        t = msg.get("ts", "")
        if msg["role"] == "user":
            body += f"""
            <div class="wa-row-user">
                <div class="wa-bubble-user">{txt}
                    <div class="wa-ts">{t} <span class="ticks">&#10003;&#10003;</span></div>
                </div>
            </div>"""
        else:
            body += f"""
            <div class="wa-row-bot">
                <div class="wa-bubble-bot">{txt}
                    <div class="wa-ts">{t}</div>
                </div>
            </div>"""

    body += "</div>"
    st.markdown(body, unsafe_allow_html=True)

    # Decorative input bar
    st.markdown("""
    <div class="wa-inputbar">
        <span style="font-size:1.3rem; color:#8696a0;">&#128247;</span>
        <span style="flex:1; font-size:0.82rem; color:#8696a0;">Type a message</span>
        <span class="wa-send-btn">&#9658;</span>
    </div>
    <div style="height:0.5rem"></div>
    """, unsafe_allow_html=True)

    # Actual functional input
    if prompt := st.chat_input("Message University Assistant..."):
        now = ts_now()
        st.session_state.messages.append({"role": "user", "content": prompt, "ts": now})
        with st.spinner(""):
            try:
                response = agent.ask(prompt)
            except Exception as e:
                response = f"Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": response, "ts": ts_now()})
        st.rerun()

