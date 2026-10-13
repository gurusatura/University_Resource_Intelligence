import os
import pandas as pd

# Dynamic Data Paths
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
CLEAN_DIR = os.path.join(PROJECT_ROOT, "data", "clean") if os.path.exists(os.path.join(PROJECT_ROOT, "data", "clean")) else os.path.join(PROJECT_ROOT, "clean")

classrooms_df = pd.read_csv(os.path.join(CLEAN_DIR, 'classrooms_clean.csv'))
schedule_df = pd.read_csv(os.path.join(CLEAN_DIR, 'schedule_clean.csv'))
courses_df = pd.read_csv(os.path.join(CLEAN_DIR, 'courses_clean.csv'))
timeslots_df = pd.read_csv(os.path.join(CLEAN_DIR, 'timeslots_clean.csv'))

# Pre-calculate utilization (hours scheduled in valid timeslots)
# Join schedule and timeslots
sched_time = pd.merge(schedule_df, timeslots_df, on='timeslot_id')
sched_time = sched_time[sched_time['timeslot_valid'] == True]
# Calculate duration in hours
sched_time['start_time'] = pd.to_datetime(sched_time['start_time'], format='%H:%M:%S')
sched_time['end_time'] = pd.to_datetime(sched_time['end_time'], format='%H:%M:%S')
sched_time['duration_hours'] = (sched_time['end_time'] - sched_time['start_time']).dt.total_seconds() / 3600.0
# Sum utilization per classroom
utilization_series = sched_time.groupby('classroom_id')['duration_hours'].sum().reset_index()
utilization_series.rename(columns={'duration_hours': 'total_scheduled_hours'}, inplace=True)

classrooms_df = classrooms_df.merge(utilization_series, on='classroom_id', how='left')
classrooms_df['total_scheduled_hours'] = classrooms_df['total_scheduled_hours'].fillna(0)
classrooms_df['room_name'] = classrooms_df['building_name'] + ' ' + classrooms_df['room_number'].astype(str)


def recommend_classroom(course_id, timeslot_id, required_capacity):
    # 1. Get all classrooms matching capacity
    df_rooms = classrooms_df[classrooms_df['capacity'] >= required_capacity]
    
    if df_rooms.empty:
        return {
            "status": "FAILED", 
            "reason": f"No classrooms exist with capacity >= {required_capacity}.", 
            "recommendation": None
        }

    # 2. Check availability at timeslot
    booked_rooms = schedule_df[schedule_df['timeslot_id'] == timeslot_id]['classroom_id'].unique()
    available_rooms = df_rooms[~df_rooms['classroom_id'].isin(booked_rooms)].copy()
    
    if available_rooms.empty:
        return {
            "status": "FAILED", 
            "reason": f"Found {len(df_rooms)} room(s) fitting capacity {required_capacity}, but all are currently double-booked at timeslot {timeslot_id}.", 
            "recommendation": None
        }

    # 3. Rank by lowest existing utilization
    available_rooms = available_rooms.sort_values(by='total_scheduled_hours', ascending=True)
    best_room = available_rooms.iloc[0]
    
    return {
        "status": "SUCCESS",
        "recommendation": best_room['room_name'],
        "classroom_id": int(best_room['classroom_id']),
        "capacity": int(best_room['capacity']),
        "utilization_hours": round(float(best_room['total_scheduled_hours']), 1),
        "reason": f"Room meets capacity ({best_room['capacity']} >= {required_capacity}), is completely available at timeslot {timeslot_id}, and has the lowest existing utilization ({round(best_room['total_scheduled_hours'], 1)} hours) among available candidates."
    }

def suggest_conflict_resolution(classroom_id, timeslot_id):
    # Get courses in this specific room + timeslot
    conflicts = schedule_df[(schedule_df['classroom_id'] == classroom_id) & (schedule_df['timeslot_id'] == timeslot_id)]
    
    if len(conflicts) <= 1:
        return "No conflict detected for this room and timeslot."
    
    # Calculate enrollment FOR THIS SPECIFIC SESSION (the actual headcount in this room at this time)
    session_enrollments = conflicts.groupby('course_id').size().reset_index(name='session_enrollment')
    conflicts = pd.merge(session_enrollments, courses_df, on='course_id')
    
    # Sort by actual physical session headcount
    conflicts = conflicts.sort_values(by='session_enrollment', ascending=False)
    
    keep = conflicts.iloc[0]
    move = conflicts.iloc[1:]
    
    suggestion = f"Conflict found ({len(conflicts)} courses assigned to room {classroom_id} at timeslot {timeslot_id}).\n"
    suggestion += f"  -> ACTION: Keep '{keep['course_name']}' (highest session headcount: {keep['session_enrollment']}) in current room.\n"
    suggestion += f"  -> ACTION: Re-assign the following courses using the recommendation engine:\n"
    for _, row in move.iterrows():
        suggestion += f"     - '{row['course_name']}' (session headcount: {row['session_enrollment']})\n"
    return suggestion


if __name__ == "__main__":
    print("Starting Stage 8 Recommendation Engine Tests...\n")

    print("--- SCENARIO 1: Clean room found ---")
    res1 = recommend_classroom(course_id=1, timeslot_id=1, required_capacity=20)
    for k, v in res1.items(): print(f"{k}: {v}")
    
    print("\n--- SCENARIO 2: Obvious pick unavailable ---")
    res2 = recommend_classroom(course_id=1, timeslot_id=60, required_capacity=20)
    for k, v in res2.items(): print(f"{k}: {v}")

    print("\n--- SCENARIO 3: No valid option (Capacity Impossible) ---")
    res3 = recommend_classroom(course_id=1, timeslot_id=1, required_capacity=500)
    for k, v in res3.items(): print(f"{k}: {v}")

    print("\n--- CONFLICT RESOLUTION TEST ---")
    print(suggest_conflict_resolution(classroom_id=11, timeslot_id=60))
