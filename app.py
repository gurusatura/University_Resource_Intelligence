import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import uuid
import sys
import os

# Clean modular imports from src/ package
from src import agent_tools
from src import agent

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UniResource IQ — University Resource Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom Design System CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background palette */
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* Main Top Header */
.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 1.4rem;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    margin-bottom: 1.2rem;
}
.top-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f0f6fc;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.text-sql-badge {
    background: #1f6feb1a;
    border: 1px solid #1f6feb66;
    color: #58a6ff;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
}
.table-badge {
    font-family: 'Courier New', monospace;
    font-size: 0.75rem;
    color: #8b949e;
    background: #0d1117;
    border: 1px solid #21262d;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
}

/* KPI Cards */
.kpi-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
.kpi-label {
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.kpi-val {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f0f6fc;
    margin: 0.2rem 0;
}
.kpi-sub {
    font-size: 0.72rem;
    color: #58a6ff;
}

/* Chat Assistant Card */
.chat-response-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.chat-user-card {
    background: #1c2128;
    border: 1px solid #30363d;
    border-left: 3px solid #1f6feb;
    border-radius: 8px;
    padding: 0.8rem 1.1rem;
    margin: 0.8rem 0;
    color: #e6edf3;
    font-size: 0.92rem;
}

/* Status Pill */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #161b22;
    border: 1px solid #238636;
    color: #3fb950;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# ── Plotly Theme ──────────────────────────────────────────────────────────────
PLOT_THEME = dict(
    plot_bgcolor="#161b22",
    paper_bgcolor="#161b22",
    font_color="#8b949e",
    font_family="Inter",
    title_font_color="#e6edf3",
    title_font_size=13,
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickfont_color="#8b949e"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickfont_color="#8b949e"),
    margin=dict(l=20, r=20, t=35, b=20)
)

def make_chart_for_tool(tool_name, tool_result):
    """Dynamically generates an interactive Plotly chart based on tool output."""
    if not tool_result:
        return None

    try:
        if tool_name == "get_classroom_utilization" and isinstance(tool_result, list):
            df = pd.DataFrame(tool_result).head(6)
            fig = px.bar(
                df, x='room_name', y='total_scheduled_hours',
                labels={'room_name': 'Classroom', 'total_scheduled_hours': 'Scheduled Hours'},
                color='total_scheduled_hours',
                color_continuous_scale=['#1f6feb', '#58a6ff']
            )
            fig.update_layout(**PLOT_THEME, title="Top Classrooms by Scheduled Hours", showlegend=False)
            fig.update_coloraxes(showscale=False)
            return fig

        elif tool_name == "get_instructor_workload" and isinstance(tool_result, list):
            df = pd.DataFrame(tool_result).head(6)
            fig = px.bar(
                df, x='instructor_name', y='total_sessions',
                labels={'instructor_name': 'Faculty Member', 'total_sessions': 'Total Sessions'},
                color_discrete_sequence=['#238636']
            )
            fig.update_layout(**PLOT_THEME, title="Top Instructor Workload (Sessions)")
            return fig

        elif tool_name == "get_course_demand" and isinstance(tool_result, list):
            df = pd.DataFrame(tool_result).head(6)
            fig = px.bar(
                df, x='course_name', y='enrollment',
                labels={'course_name': 'Course', 'enrollment': 'Student Enrollment'},
                color_discrete_sequence=['#8957e5']
            )
            fig.update_layout(**PLOT_THEME, title="Course Enrollment Demand Rankings")
            return fig

        elif tool_name == "get_forecast" and isinstance(tool_result, list):
            df = pd.DataFrame(tool_result).head(6)
            colors = ['#238636' if t == 'Increasing' else '#1f6feb' if t == 'Stable' else '#da3633' 
                      for t in df['trend_direction']]
            fig = go.Figure(data=[
                go.Bar(
                    x=df['course_name'],
                    y=df['forecast_Fall_2026'],
                    marker_color=colors,
                    name='Fall 2026 Projection'
                )
            ])
            fig.update_layout(**PLOT_THEME, title="Demand Forecast Projection for Fall 2026")
            return fig

        elif tool_name == "get_conflict_detection" and isinstance(tool_result, dict):
            tot_rooms = tool_result.get("total_classroom_conflicts", 0)
            tot_inst = tool_result.get("total_instructor_conflicts", 0)
            fig = go.Figure(data=[
                go.Bar(x=['Room Double-Bookings', 'Instructor Conflicts'], y=[tot_rooms, tot_inst],
                       marker_color=['#da3633', '#d29922'])
            ])
            fig.update_layout(**PLOT_THEME, title="Total Detected Scheduling Conflicts")
            return fig

    except Exception:
        return None

    return None

# ── Session State Management (Sessions & Message IDs) ─────────────────────────
if "sessions" not in st.session_state:
    initial_id = "session_1"
    st.session_state.sessions = {
        initial_id: {
            "title": "Which classroom is used the most...",
            "created_at": datetime.datetime.now().strftime("%I:%M %p"),
            "messages": []
        }
    }
    st.session_state.current_session_id = initial_id

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

current_session = st.session_state.sessions[st.session_state.current_session_id]

# ── Left Sidebar (RetailIQ Style) ─────────────────────────────────────────────
with st.sidebar:
    # 1. Branding Header
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:1.2rem;">
        <div style="background:#0e4429; border:1px solid #238636; border-radius:8px; width:36px; height:36px; display:flex; align-items:center; justify-content:center; font-size:1.15rem;">🏛️</div>
        <div>
            <div style="font-weight:700; font-size:1.02rem; color:#f0f6fc; display:flex; align-items:center; gap:6px;">
                UniResource <span style="font-size:0.65rem; background:#1f6feb22; border:1px solid #1f6feb55; color:#58a6ff; padding:2px 6px; border-radius:12px; font-weight:600;">Agent</span>
            </div>
            <div style="font-size:0.72rem; color:#8b949e;">Resource Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. + New Chat Button
    if st.button("＋ New Chat", use_container_width=True):
        new_id = f"session_{len(st.session_state.sessions) + 1}"
        st.session_state.sessions[new_id] = {
            "title": "New Conversation",
            "created_at": datetime.datetime.now().strftime("%I:%M %p"),
            "messages": []
        }
        st.session_state.current_session_id = new_id
        st.rerun()

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # 3. SAVED CHATS Section
    st.markdown("<div style='font-size:0.72rem; color:#8b949e; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.4rem;'>Saved Chats</div>", unsafe_allow_html=True)
    for sid, sdata in list(st.session_state.sessions.items())[::-1]:
        is_active = (sid == st.session_state.current_session_id)
        btn_label = f"💬 {sdata['title'][:28]}..." if len(sdata['title']) > 28 else f"💬 {sdata['title']}"
        if st.button(btn_label, key=f"session_btn_{sid}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.current_session_id = sid
            st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # 4. SUGGESTED QUERIES Section
    st.markdown("<div style='font-size:0.72rem; color:#8b949e; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.4rem;'>Suggested Queries</div>", unsafe_allow_html=True)
    suggested = [
        "Which 5 classrooms have the highest usage?",
        "Are there any instructor scheduling conflicts?",
        "What is the demand forecast for Fall 2026?",
        "Recommend a room for 40 students at timeslot 5"
    ]
    for q in suggested:
        if st.button(q, key=f"sq_{hash(q)}", use_container_width=True):
            st.session_state.pending_query = q
            st.rerun()

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # 5. Connection Status Badge (Supabase Connected)
    st.markdown("""
    <div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:0.75rem 0.9rem; margin-top:auto;">
        <div style="display:flex; align-items:center; gap:8px; font-size:0.8rem; font-weight:600; color:#3fb950;">
            <span style="display:inline-block; width:8px; height:8px; background:#3fb950; border-radius:50%; box-shadow:0 0 6px #3fb950;"></span>
            Supabase Connected
        </div>
        <div style="font-size:0.73rem; color:#8b949e; margin-top:2px;">5,420 schedule records</div>
        <div style="font-size:0.68rem; color:#6e7681; margin-top:6px; border-top:1px solid #21262d; padding-top:4px;">
            Powered by Groq • v1.0
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Main Tabs (Assistant & Dashboard) ─────────────────────────────────────────
tab_assistant, tab_dashboard = st.tabs(["AI Analytics Assistant", "Executive Dashboard"])

# =============================================================================
# TAB 1: AI ANALYTICS ASSISTANT (RetailIQ Style)
# =============================================================================
with tab_assistant:
    # Top Header
    st.markdown("""
    <div class="top-header">
        <div class="top-title">
            University Resource Analytics Assistant
            <span class="text-sql-badge">✦ PostgreSQL & AI Agent</span>
        </div>
        <div class="table-badge">Table: public.schedule | public.classrooms</div>
    </div>
    """, unsafe_allow_html=True)

    # Display Chat History for Current Session
    if not current_session["messages"]:
        st.markdown("""
        <div style="background:#161b22; border:1px solid #21262d; border-radius:10px; padding:1.5rem; margin-bottom:1.5rem; text-align:center;">
            <div style="font-size:1.8rem; margin-bottom:0.5rem;">🏛️</div>
            <div style="font-weight:600; font-size:1.05rem; color:#f0f6fc;">How can I assist your university scheduling today?</div>
            <div style="font-size:0.83rem; color:#8b949e; margin-top:0.3rem;">
                Ask questions about classroom utilization, instructor workload, double-bookings, recommendations, or Fall 2026 forecasts.
            </div>
        </div>
        """, unsafe_allow_html=True)

    for msg in current_session["messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-user-card">
                <b>You:</b> {msg["content"]}
                <div style="font-size:0.68rem; color:#8b949e; text-align:right; margin-top:4px;">{msg.get('ts', '')} • ID: {msg.get('id', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown(f"""
                <div class="chat-response-card">
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:0.6rem;">
                        <span style="font-size:1.1rem;">🏛️</span>
                        <span style="font-weight:600; font-size:0.92rem; color:#58a6ff;">Assistant</span>
                        <span style="font-size:0.7rem; color:#8b949e;">• {msg.get('ts', '')} • ID: {msg.get('id', '')}</span>
                    </div>
                    <div style="font-size:0.92rem; line-height:1.6; color:#e6edf3;">
                        {msg["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Render dynamic chart if present
                if msg.get("chart_obj"):
                    st.plotly_chart(msg["chart_obj"], use_container_width=True)

                # Render <> Executed SQL Accordion
                if msg.get("sql_query"):
                    with st.expander("<> Executed SQL / Tool Query Logic", expanded=False):
                        st.code(msg["sql_query"], language="sql")
                        if msg.get("tool_name"):
                            st.caption(f"Tool: `{msg['tool_name']}` | Parameters: `{msg.get('tool_args', {})}`")

                # Render View Data Accordion
                if msg.get("data_records"):
                    data_len = len(msg["data_records"])
                    with st.expander(f"📋 View Data ({data_len} rows)", expanded=False):
                        df_view = pd.DataFrame(msg["data_records"])
                        st.dataframe(df_view, use_container_width=True, hide_index=True)

    # Handle Pending Query or Chat Input
    query_to_run = None
    if st.session_state.pending_query:
        query_to_run = st.session_state.pending_query
        st.session_state.pending_query = None
    else:
        chat_val = st.chat_input("Ask about university resources (e.g. room utilization, conflicts, instructor workloads)...")
        if chat_val:
            query_to_run = chat_val

    if query_to_run:
        now_ts = datetime.datetime.now().strftime("%I:%M %p")
        user_msg_id = f"msg_{uuid.uuid4().hex[:6]}"
        bot_msg_id = f"msg_{uuid.uuid4().hex[:6]}"

        # Append User Message
        current_session["messages"].append({
            "id": user_msg_id,
            "role": "user",
            "content": query_to_run,
            "ts": now_ts
        })

        # Update Session Title if First Query
        if len(current_session["messages"]) <= 1 or current_session["title"] == "New Conversation":
            current_session["title"] = query_to_run[:32] + ("..." if len(query_to_run) > 32 else "")

        # Execute AI Agent Analysis
        with st.spinner("Analyzing university data & executing query..."):
            try:
                res = agent.ask_detailed(query_to_run)
                answer_text = res.get("answer", "")
                tool_name = res.get("tool_name")
                tool_args = res.get("tool_args", {})
                tool_result = res.get("tool_result")
                sql_query = res.get("sql_query")

                # Prepare structured data records for view
                data_records = None
                if isinstance(tool_result, list):
                    data_records = tool_result
                elif isinstance(tool_result, dict):
                    if "classroom_conflicts" in tool_result:
                        data_records = tool_result.get("classroom_conflicts", [])
                    elif "candidate_classrooms" in tool_result:
                        data_records = tool_result.get("candidate_classrooms", [])

                chart_fig = make_chart_for_tool(tool_name, tool_result)

            except Exception as e:
                answer_text = f"An error occurred while executing the query: {str(e)}"
                tool_name = None
                tool_args = {}
                sql_query = None
                data_records = None
                chart_fig = None

        # Append Bot Message
        current_session["messages"].append({
            "id": bot_msg_id,
            "role": "assistant",
            "content": answer_text,
            "tool_name": tool_name,
            "tool_args": tool_args,
            "sql_query": sql_query,
            "data_records": data_records,
            "chart_obj": chart_fig,
            "ts": datetime.datetime.now().strftime("%I:%M %p")
        })

        st.rerun()


# =============================================================================
# TAB 2: EXECUTIVE DASHBOARD (Full-Screen Visualizations & KPI Cards)
# =============================================================================
with tab_dashboard:
    # Load all data upfront for dashboard
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

    # 4 KPI Metrics
    st.markdown("<div style='font-size:0.85rem; color:#8b949e; font-weight:600; text-transform:uppercase; margin-bottom:0.8rem;'>Executive Resource Metrics</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        peak_room = df_util.iloc[0]["room_name"] if not df_util.empty else "N/A"
        peak_hrs = df_util.iloc[0]["total_scheduled_hours"] if not df_util.empty else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Peak Room Utilization</div>
            <div class="kpi-val">{peak_hrs:.0f} hrs</div>
            <div class="kpi-sub">{peak_room} (Highest Scheduled)</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Instructor Conflicts</div>
            <div class="kpi-val">{len(c_inst)}</div>
            <div class="kpi-sub" style="color:#d29922;">Simultaneous Bookings</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Room Double-Bookings</div>
            <div class="kpi-val">{len(c_rooms)}</div>
            <div class="kpi-sub" style="color:#da3633;">Collisions Detected</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        top_fc_course = df_forecast.iloc[0]["course_name"] if not df_forecast.empty else "N/A"
        top_fc_val = df_forecast.iloc[0]["forecast_Fall_2026"] if not df_forecast.empty else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Fall 2026 Top Forecast</div>
            <div class="kpi-val">{top_fc_val}</div>
            <div class="kpi-sub" style="color:#3fb950;">{top_fc_course[:22]}...</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # 4 BI Charts
    r1_c1, r1_c2 = st.columns(2)
    with r1_c1:
        fig_u = px.bar(
            df_util.head(10), x='room_name', y='total_scheduled_hours',
            color='total_scheduled_hours', color_continuous_scale=['#1f6feb', '#58a6ff'],
            title="Classroom Utilization — Top 10 Rooms (Valid Hours)"
        )
        fig_u.update_layout(**PLOT_THEME, showlegend=False)
        fig_u.update_coloraxes(showscale=False)
        st.plotly_chart(fig_u, use_container_width=True)

    with r1_c2:
        fig_w = px.bar(
            df_workload.head(10), x='instructor_name', y='total_sessions',
            color_discrete_sequence=['#238636'],
            title="Instructor Workload — Top 10 Faculty (Total Sessions)"
        )
        fig_w.update_layout(**PLOT_THEME)
        st.plotly_chart(fig_w, use_container_width=True)

    r2_c1, r2_c2 = st.columns(2)
    with r2_c1:
        fig_d = px.bar(
            df_demand.head(10), x='course_name', y='enrollment',
            color_discrete_sequence=['#8957e5'],
            title="Course Demand — Top 10 Enrolled Courses"
        )
        fig_d.update_layout(**PLOT_THEME)
        st.plotly_chart(fig_d, use_container_width=True)

    with r2_c2:
        colors_fc = ['#238636' if t == 'Increasing' else '#1f6feb' if t == 'Stable' else '#da3633' 
                     for t in df_forecast.head(10)['trend_direction']]
        fig_f = go.Figure(data=[
            go.Bar(
                x=df_forecast.head(10)['course_name'],
                y=df_forecast.head(10)['forecast_Fall_2026'],
                marker_color=colors_fc
            )
        ])
        fig_f.update_layout(**PLOT_THEME, title="Fall 2026 Demand Projections (Linear Regression)")
        st.plotly_chart(fig_f, use_container_width=True)

    # Data Tables
    t1, t2 = st.columns(2)
    with t1:
        st.caption("Top 10 Instructor Schedule Conflicts")
        if c_inst:
            df_ci = pd.DataFrame(c_inst[:10])[["instructor_name", "day", "timeslot_id", "overlapping_courses"]]
            st.dataframe(df_ci, use_container_width=True, hide_index=True)
    with t2:
        st.caption("Top 10 Classroom Collisions")
        if c_rooms:
            df_cr = pd.DataFrame(c_rooms[:10])[["room_name", "day", "timeslot_id", "overlapping_courses"]]
            st.dataframe(df_cr, use_container_width=True, hide_index=True)
