import pandas as pd
import numpy as np
import os
from datetime import datetime

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw") if os.path.exists(os.path.join(PROJECT_ROOT, "data", "raw")) else PROJECT_ROOT
OUT_DIR = os.path.join(PROJECT_ROOT, "data", "clean")
os.makedirs(OUT_DIR, exist_ok=True)

def to_time(s):
    s = str(s).strip()
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(s, fmt).time()
        except ValueError:
            pass
    return None

def run_etl():
    print("Starting ETL Process...")
    
    # 1. Load Data
    students = pd.read_csv(os.path.join(DATA_DIR, "students.csv"))
    instructors = pd.read_csv(os.path.join(DATA_DIR, "instructors.csv"))
    courses = pd.read_csv(os.path.join(DATA_DIR, "courses.csv"))
    classrooms = pd.read_csv(os.path.join(DATA_DIR, "classrooms.csv"))
    timeslots = pd.read_csv(os.path.join(DATA_DIR, "timeslots.csv"))
    schedule = pd.read_csv(os.path.join(DATA_DIR, "schedule.csv"))
    
    # 2. Transform Students: cast year to int
    year_map = {'Freshman': 1, 'Sophomore': 2, 'Junior': 3, 'Senior': 4}
    students['year'] = students['year'].map(year_map).astype(int)
    
    print(f"Students transformed: 'year' cast to {students['year'].dtype}")
    
    # 3. Transform Timeslots: parse time and add timeslot_valid
    timeslots['start_time'] = timeslots['start_time'].apply(to_time)
    timeslots['end_time'] = timeslots['end_time'].apply(to_time)
    
    # Determine validity: end_time > start_time
    timeslots['timeslot_valid'] = timeslots['end_time'] > timeslots['start_time']
    
    malformed_count = (~timeslots['timeslot_valid']).sum()
    print(f"Timeslots transformed: parsed times. Found {malformed_count} malformed timeslots.")
    
    # 4. Transform Schedule: inject synthetic semester/year
    # Let's assign them randomly across 4 semesters (e.g., Fall 2024, Spring 2025, Fall 2025, Spring 2026)
    # We use a fixed seed for reproducibility.
    np.random.seed(42)
    synthetic_terms = [
        {"semester": "Fall", "academic_year": 2024},
        {"semester": "Spring", "academic_year": 2025},
        {"semester": "Fall", "academic_year": 2025},
        {"semester": "Spring", "academic_year": 2026}
    ]
    
    # Assign terms to courses (so all schedules for a course in a term are consistent)
    # Or just random per row? The prompt says "course demand trend across the synthetic semester/year dimension"
    # To have a trend, it's better to assign at the schedule row level or student-course level (which schedule is).
    # We'll just randomly assign each schedule row to a term.
    term_indices = np.random.choice(len(synthetic_terms), size=len(schedule))
    
    schedule['semester'] = [synthetic_terms[i]['semester'] for i in term_indices]
    schedule['academic_year'] = [synthetic_terms[i]['academic_year'] for i in term_indices]
    
    print("Schedule transformed: injected synthetic 'semester' and 'academic_year'.")
    print(f"Total schedule rows kept: {len(schedule)}")
    
    # 5. Save Cleaned Data
    students.to_csv(os.path.join(OUT_DIR, "students_clean.csv"), index=False)
    instructors.to_csv(os.path.join(OUT_DIR, "instructors_clean.csv"), index=False)
    courses.to_csv(os.path.join(OUT_DIR, "courses_clean.csv"), index=False)
    classrooms.to_csv(os.path.join(OUT_DIR, "classrooms_clean.csv"), index=False)
    timeslots.to_csv(os.path.join(OUT_DIR, "timeslots_clean.csv"), index=False)
    schedule.to_csv(os.path.join(OUT_DIR, "schedule_clean.csv"), index=False)
    
    print(f"Clean data saved to {OUT_DIR}")

if __name__ == "__main__":
    run_etl()
