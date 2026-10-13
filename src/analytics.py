import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load DB credentials
load_dotenv()
db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(db_url)
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_analytics():
    print("Starting Stage 6 Analytics...\n")

    # 1. Classroom Conflict Detection
    print("1. Classroom Double-Booking Conflicts...")
    query_room_conflicts = """
        SELECT c.classroom_id, c.building_name || ' ' || c.room_number AS room_name,
               t.timeslot_id, t.day, t.start_time, t.end_time,
               COUNT(DISTINCT s.course_id) AS overlapping_courses,
               STRING_AGG(DISTINCT cr.course_name, ' | ') AS course_names
        FROM schedule s
        JOIN classrooms c ON s.classroom_id = c.classroom_id
        JOIN timeslots t ON s.timeslot_id = t.timeslot_id
        JOIN courses cr ON s.course_id = cr.course_id
        GROUP BY c.classroom_id, room_name, t.timeslot_id, t.day, t.start_time, t.end_time
        HAVING COUNT(DISTINCT s.course_id) > 1
        ORDER BY overlapping_courses DESC
    """
    df_room_conflicts = pd.read_sql(query_room_conflicts, engine)
    csv_path = os.path.join(REPORTS_DIR, "classroom_conflicts.csv")
    df_room_conflicts.to_csv(csv_path, index=False)
    print(f"Total Classroom Conflicts Found: {len(df_room_conflicts)}")
    print(f"Top 3 Worst Classroom Collisions:\n{df_room_conflicts[['room_name', 'timeslot_id', 'overlapping_courses', 'course_names']].head(3).to_string(index=False)}\n")

    # 2. Instructor Conflict Detection
    print("2. Instructor Double-Booking Conflicts...")
    query_inst_conflicts = """
        SELECT i.instructor_id, i.first_name || ' ' || i.last_name AS instructor_name,
               t.timeslot_id, t.day, t.start_time, t.end_time,
               COUNT(DISTINCT s.course_id) AS overlapping_courses,
               STRING_AGG(DISTINCT cr.course_name, ' | ') AS course_names,
               STRING_AGG(DISTINCT c.building_name || ' ' || c.room_number, ' | ') AS room_names
        FROM schedule s
        JOIN instructors i ON s.instructor_id = i.instructor_id
        JOIN timeslots t ON s.timeslot_id = t.timeslot_id
        JOIN courses cr ON s.course_id = cr.course_id
        JOIN classrooms c ON s.classroom_id = c.classroom_id
        GROUP BY i.instructor_id, instructor_name, t.timeslot_id, t.day, t.start_time, t.end_time
        HAVING COUNT(DISTINCT s.course_id) > 1 OR COUNT(DISTINCT s.classroom_id) > 1
        ORDER BY overlapping_courses DESC
    """
    df_inst_conflicts = pd.read_sql(query_inst_conflicts, engine)
    csv_path = os.path.join(REPORTS_DIR, "instructor_conflicts.csv")
    df_inst_conflicts.to_csv(csv_path, index=False)
    print(f"Total Instructor Conflicts Found: {len(df_inst_conflicts)}")
    print(f"Top 3 Worst Instructor Collisions:\n{df_inst_conflicts[['instructor_name', 'timeslot_id', 'overlapping_courses', 'room_names']].head(3).to_string(index=False)}\n")

    # 3. Capacity Mismatch
    print("3. Classroom Capacity Mismatch...")
    query_capacity = """
        SELECT s.course_id, cr.course_name, s.classroom_id, 
               c.building_name || ' ' || c.room_number AS room_name,
               s.timeslot_id, c.capacity, 
               COUNT(s.student_id) AS session_enrollment,
               (COUNT(s.student_id) - c.capacity) AS overflow
        FROM schedule s
        JOIN classrooms c ON s.classroom_id = c.classroom_id
        JOIN courses cr ON s.course_id = cr.course_id
        GROUP BY s.course_id, cr.course_name, s.classroom_id, room_name, s.timeslot_id, c.capacity
        HAVING COUNT(s.student_id) > c.capacity
        ORDER BY overflow DESC
    """
    df_capacity = pd.read_sql(query_capacity, engine)
    csv_path = os.path.join(REPORTS_DIR, "capacity_mismatches.csv")
    df_capacity.to_csv(csv_path, index=False)
    print(f"Total Capacity Mismatches Found: {len(df_capacity)}")
    print(f"Top 3 Worst Capacity Overflows:\n{df_capacity[['course_name', 'room_name', 'timeslot_id', 'capacity', 'session_enrollment', 'overflow']].head(3).to_string(index=False)}\n")

    print(f"All Analytics reports successfully generated and saved to {REPORTS_DIR}")

if __name__ == "__main__":
    run_analytics()
