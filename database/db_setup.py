import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(DB_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "clean") if os.path.exists(os.path.join(PROJECT_ROOT, "data", "clean")) else os.path.join(PROJECT_ROOT, "clean")
SCHEMA_FILE = os.path.join(DB_DIR, "schema.sql")

def get_engine():
    # Expecting DATABASE_URL in .env, e.g., postgresql://user:password@localhost:5432/university
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in .env file. Please set it to your PostgreSQL connection string.")
    
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    return create_engine(db_url)

def run_db_setup():
    print("Starting Stage 4 Database Setup & Load...")
    engine = get_engine()
    
    # 1. Execute schema creation
    print("Creating schema...")
    with open(SCHEMA_FILE, 'r') as f:
        schema_sql = f.read()
    
    with engine.begin() as conn:
        for statement in schema_sql.split(';'):
            if statement.strip():
                conn.execute(text(statement))
    print("Schema created successfully.")
    
    # 2. Load data from clean CSVs
    print("Loading data into PostgreSQL...")
    tables = ['students', 'instructors', 'courses', 'classrooms', 'timeslots', 'schedule']
    
    for table in tables:
        csv_path = os.path.join(DATA_DIR, f"{table}_clean.csv")
        df = pd.read_csv(csv_path)
        
        # We use if_exists='append' since the tables are already created with proper types and PKs
        df.to_sql(table, engine, if_exists='append', index=False)
        print(f"Loaded {len(df)} rows into '{table}'.")

    # 3. Post-load verification
    print("\nRunning Verification Queries...")
    with engine.connect() as conn:
        # Row counts
        for table in tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"Verification - {table} row count: {result}")
        
        # FK Integrity Check for Schedule
        print("\nChecking FK Integrity for 'schedule' table...")
        fk_checks = {
            'student_id': 'students',
            'course_id': 'courses',
            'instructor_id': 'instructors',
            'classroom_id': 'classrooms',
            'timeslot_id': 'timeslots'
        }
        for fk_col, parent_table in fk_checks.items():
            query = f"""
            SELECT COUNT(*) 
            FROM schedule s 
            LEFT JOIN {parent_table} p ON s.{fk_col} = p.{fk_col}
            WHERE p.{fk_col} IS NULL
            """
            orphans = conn.execute(text(query)).scalar()
            print(f"Orphan rows for {fk_col} -> {parent_table}: {orphans}")
            assert orphans == 0, f"FK Violation: {orphans} orphans found for {fk_col}!"
        
        print("\nAll verifications passed. Database load is complete.")

if __name__ == "__main__":
    run_db_setup()
