import os
import pandas as pd
import plotly.express as px
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

def generate_reports():
    print("Starting Stage 5 BI / Reporting...\n")

    # 1. Classroom Utilization (valid timeslots only)
    print("1. Calculating Classroom Utilization...")
    query_util = """
        SELECT c.classroom_id, c.building_name || ' ' || c.room_number AS room_name,
               SUM(EXTRACT(EPOCH FROM (t.end_time - t.start_time))/3600) AS total_scheduled_hours
        FROM schedule s
        JOIN timeslots t ON s.timeslot_id = t.timeslot_id
        JOIN classrooms c ON s.classroom_id = c.classroom_id
        WHERE t.timeslot_valid = TRUE
        GROUP BY c.classroom_id, room_name
        ORDER BY total_scheduled_hours DESC
    """
    df_util = pd.read_sql(query_util, engine)
    print(f"Top 3 utilized classrooms:\n{df_util.head(3).to_string(index=False)}\n")
    
    fig_util = px.bar(df_util, x='room_name', y='total_scheduled_hours',
                      title="Classroom Utilization (Valid Hours)",
                      labels={'total_scheduled_hours': 'Scheduled Hours', 'room_name': 'Classroom'})
    fig_util.write_html(os.path.join(REPORTS_DIR, "classroom_utilization.html"))

    # 2. Instructor Workload (Session Count)
    print("2. Calculating Instructor Workload...")
    query_workload = """
        SELECT i.first_name || ' ' || i.last_name AS instructor_name, i.department,
               COUNT(s.student_id) AS total_sessions
        FROM schedule s
        JOIN instructors i ON s.instructor_id = i.instructor_id
        GROUP BY instructor_name, i.department
        ORDER BY total_sessions DESC
    """
    df_workload = pd.read_sql(query_workload, engine)
    print(f"Top 3 instructors by workload:\n{df_workload.head(3).to_string(index=False)}\n")
    
    fig_workload = px.box(df_workload, x='department', y='total_sessions',
                          title="Instructor Workload Distribution by Department",
                          labels={'total_sessions': 'Sessions Taught', 'department': 'Department'})
    fig_workload.write_html(os.path.join(REPORTS_DIR, "instructor_workload.html"))

    # 3. Course Enrollment
    print("3. Calculating Course Enrollment...")
    query_enrollment = """
        SELECT c.course_name, c.department, COUNT(s.student_id) AS enrollment
        FROM schedule s
        JOIN courses c ON s.course_id = c.course_id
        GROUP BY c.course_name, c.department
        ORDER BY enrollment DESC
    """
    df_enroll = pd.read_sql(query_enrollment, engine)
    print(f"Top 3 enrolled courses:\n{df_enroll.head(3).to_string(index=False)}\n")
    print(f"Bottom 3 enrolled courses:\n{df_enroll.tail(3).to_string(index=False)}\n")
    
    fig_enroll = px.bar(df_enroll, x='course_name', y='enrollment', color='department',
                        title="Course Enrollment (Schedule Row Count)",
                        labels={'enrollment': 'Students Enrolled', 'course_name': 'Course'})
    fig_enroll.write_html(os.path.join(REPORTS_DIR, "course_enrollment.html"))

    # 4. Student Counts by Program and Year
    print("4. Calculating Student Demographics...")
    query_students = """
        SELECT program_name, year, COUNT(student_id) AS student_count
        FROM students
        GROUP BY program_name, year
        ORDER BY program_name, year
    """
    df_students = pd.read_sql(query_students, engine)
    
    # Pivot for summary print
    pivot = df_students.pivot(index='program_name', columns='year', values='student_count').fillna(0)
    print(f"Sample Student Counts by Program (first 5):\n{pivot.head(5).to_string()}\n")
    
    fig_students = px.bar(df_students, x='program_name', y='student_count', color='year',
                          title="Student Demographics by Program and Year",
                          labels={'student_count': 'Number of Students', 'program_name': 'Program', 'year': 'Year'},
                          barmode='stack')
    fig_students.write_html(os.path.join(REPORTS_DIR, "student_demographics.html"))

    print(f"All BI reports successfully generated and saved to {REPORTS_DIR}")

if __name__ == "__main__":
    generate_reports()
