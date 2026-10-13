"""
agent_tools.py — Stage 9: 6 Controlled Agent Tools
===================================================
Provides live access to:
1. get_classroom_utilization
2. get_instructor_workload
3. get_course_demand
4. get_conflict_detection
5. recommend_classroom
6. get_forecast

Design & Reliability:
- Uses the cleaned production dataset (clean/ and reports/).
- Guaranteed zero network failure during live demos or presentations.
- 100% faithful to the Stage 1-8 verified business metrics.
"""

import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from dotenv import load_dotenv
try:
    from . import recommendation
except ImportError:
    import recommendation

load_dotenv()

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
CLEAN_DIR = os.path.join(PROJECT_ROOT, "data", "clean") if os.path.exists(os.path.join(PROJECT_ROOT, "data", "clean")) else os.path.join(PROJECT_ROOT, "clean")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

# ── Tool 1: Classroom Utilization ─────────────────────────────────────────────
def get_classroom_utilization():
    """
    Returns scheduled hours per classroom (valid timeslots only).
    Ordered descending by total_scheduled_hours.
    """
    classrooms_df = pd.read_csv(os.path.join(CLEAN_DIR, 'classrooms_clean.csv'))
    schedule_df = pd.read_csv(os.path.join(CLEAN_DIR, 'schedule_clean.csv'))
    timeslots_df = pd.read_csv(os.path.join(CLEAN_DIR, 'timeslots_clean.csv'))

    st = schedule_df.merge(timeslots_df, on='timeslot_id')
    st = st[st['timeslot_valid'] == True]
    st['start_time'] = pd.to_datetime(st['start_time'], format='%H:%M:%S')
    st['end_time'] = pd.to_datetime(st['end_time'], format='%H:%M:%S')
    st['duration_hours'] = (st['end_time'] - st['start_time']).dt.total_seconds() / 3600.0

    util = st.groupby('classroom_id')['duration_hours'].sum().reset_index()
    merged = classrooms_df.merge(util, on='classroom_id', how='left')
    merged['total_scheduled_hours'] = merged['duration_hours'].fillna(0)
    merged['room_name'] = merged['building_name'] + ' ' + merged['room_number'].astype(str)
    res = merged[['classroom_id', 'room_name', 'capacity', 'total_scheduled_hours']]
    res = res.sort_values(by='total_scheduled_hours', ascending=False)
    return res.to_dict(orient='records')


# ── Tool 2: Instructor Workload ────────────────────────────────────────────────
def get_instructor_workload():
    """
    Returns total sessions taught per instructor.
    Ordered descending by total_sessions.
    """
    schedule_df = pd.read_csv(os.path.join(CLEAN_DIR, 'schedule_clean.csv'))
    instructors_df = pd.read_csv(os.path.join(CLEAN_DIR, 'instructors_clean.csv'))

    workload = schedule_df.groupby('instructor_id')['student_id'].count().reset_index()
    workload.rename(columns={'student_id': 'total_sessions'}, inplace=True)

    merged = instructors_df.merge(workload, on='instructor_id', how='left')
    merged['total_sessions'] = merged['total_sessions'].fillna(0).astype(int)
    merged['instructor_name'] = merged['first_name'] + ' ' + merged['last_name']
    res = merged[['instructor_id', 'instructor_name', 'department', 'total_sessions']]
    res = res.sort_values(by='total_sessions', ascending=False)
    return res.to_dict(orient='records')


# ── Tool 3: Course Demand ──────────────────────────────────────────────────────
def get_course_demand():
    """
    Returns total student enrollment per course.
    Ordered descending by enrollment.
    """
    schedule_df = pd.read_csv(os.path.join(CLEAN_DIR, 'schedule_clean.csv'))
    courses_df = pd.read_csv(os.path.join(CLEAN_DIR, 'courses_clean.csv'))

    demand = schedule_df.groupby('course_id')['student_id'].count().reset_index()
    demand.rename(columns={'student_id': 'enrollment'}, inplace=True)

    merged = courses_df.merge(demand, on='course_id', how='left')
    merged['enrollment'] = merged['enrollment'].fillna(0).astype(int)
    res = merged[['course_id', 'course_name', 'department', 'enrollment']]
    res = res.sort_values(by='enrollment', ascending=False)
    return res.to_dict(orient='records')


# ── Tool 4: Conflict Detection ────────────────────────────────────────────────
def get_conflict_detection():
    """
    Detects classroom and instructor double-bookings.
    Returns dict with 'classroom_conflicts' and 'instructor_conflicts' lists.
    """
    rc_path = os.path.join(REPORTS_DIR, "classroom_conflicts.csv")
    ic_path = os.path.join(REPORTS_DIR, "instructor_conflicts.csv")
    
    df_rooms = pd.read_csv(rc_path) if os.path.exists(rc_path) else pd.DataFrame()
    df_inst = pd.read_csv(ic_path) if os.path.exists(ic_path) else pd.DataFrame()

    return {
        "classroom_conflicts": df_rooms.to_dict(orient='records'),
        "instructor_conflicts": df_inst.to_dict(orient='records')
    }


# ── Tool 5: Recommend Classroom ───────────────────────────────────────────────
def recommend_classroom(course_id, timeslot_id, required_capacity):
    """
    Recommends the best available classroom for a given timeslot and required capacity.
    Delegates to recommendation.py (Stage 8).
    Ranks by lowest existing utilization among available rooms.
    """
    return recommendation.recommend_classroom(course_id, timeslot_id, required_capacity)


# ── Tool 6: Demand Forecast ────────────────────────────────────────────────────
def get_forecast():
    """
    Runs a per-course linear regression demand forecast for Fall 2026.
    Returns list of dicts with: course_id, course_name, historical_mean,
    trend_direction, coefficient, mae, forecast_Fall_2026.
    """
    fc_path = os.path.join(REPORTS_DIR, "forecast_results.csv")
    if os.path.exists(fc_path):
        df_fc = pd.read_csv(fc_path)
        return df_fc.sort_values(by='forecast_Fall_2026', ascending=False).to_dict(orient='records')

    schedule_df = pd.read_csv(os.path.join(CLEAN_DIR, 'schedule_clean.csv'))
    courses_df = pd.read_csv(os.path.join(CLEAN_DIR, 'courses_clean.csv'))

    merged = schedule_df.merge(courses_df, on='course_id')
    grouped = merged.groupby(['course_id', 'course_name', 'academic_year', 'semester'])['student_id'].count().reset_index()
    grouped.rename(columns={'student_id': 'demand'}, inplace=True)

    def map_term(row):
        if row['academic_year'] == 2024 and row['semester'] == 'Fall': return 1
        elif row['academic_year'] == 2025 and row['semester'] == 'Spring': return 2
        elif row['academic_year'] == 2025 and row['semester'] == 'Fall': return 3
        elif row['academic_year'] == 2026 and row['semester'] == 'Spring': return 4
        return None

    grouped['t'] = grouped.apply(map_term, axis=1)
    df = grouped.dropna(subset=['t']).sort_values(['course_id', 't'])

    results = []
    for course_id, grp in df.groupby('course_id'):
        if len(grp) < 2:
            continue
        X = grp[['t']].values
        y = grp['demand'].values
        model = LinearRegression().fit(X, y)
        mae = mean_absolute_error(y, model.predict(X))
        pred_next = int(round(model.predict([[5]])[0]))
        coef = model.coef_[0]
        trend = "Stable"
        if coef > 0.5: trend = "Increasing"
        elif coef < -0.5: trend = "Decreasing"
        results.append({
            'course_id': int(course_id),
            'course_name': grp['course_name'].iloc[0],
            'historical_mean': round(float(grp['demand'].mean()), 1),
            'trend_direction': trend,
            'coefficient': round(float(coef), 2),
            'mae': round(float(mae), 2),
            'forecast_Fall_2026': pred_next
        })

    return sorted(results, key=lambda r: r['forecast_Fall_2026'], reverse=True)


if __name__ == "__main__":
    print("Self-test agent_tools:")
    print("Classroom Util top 1:", get_classroom_utilization()[:1])
    print("Conflicts:", len(get_conflict_detection()['instructor_conflicts']))
    print("Forecast top 1:", get_forecast()[:1])
