import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sqlalchemy import create_engine
import plotly.express as px
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

def map_term_to_time(row):
    # Mapping the 4 synthetic terms to chronological time steps (t)
    if row['academic_year'] == 2024 and row['semester'] == 'Fall': return 1
    elif row['academic_year'] == 2025 and row['semester'] == 'Spring': return 2
    elif row['academic_year'] == 2025 and row['semester'] == 'Fall': return 3
    elif row['academic_year'] == 2026 and row['semester'] == 'Spring': return 4
    else: return None

def term_name(t):
    mapping = {1: 'Fall 2024', 2: 'Spring 2025', 3: 'Fall 2025', 4: 'Spring 2026', 5: 'Fall 2026'}
    return mapping.get(t, f"t={t}")

def run_forecasting():
    print("Starting Stage 7 Forecasting...\n")
    print("NOTE: The forecast is performed strictly at the course level.")
    print("Because the semester/year dimension is synthetic and randomly assigned per row,")
    print("this forecast represents a mathematically sound demonstration of linear regression,")
    print("but has no real predictive validity for the university.\n")

    # 1. Fetch time series demand data from clean CSVs (bypassing DB connection issues)
    schedule_csv = r"d:\BI\university\University Exam Scheduling\clean\schedule_clean.csv"
    courses_csv = r"d:\BI\university\University Exam Scheduling\clean\courses_clean.csv"
    
    schedule_df = pd.read_csv(schedule_csv)
    courses_df = pd.read_csv(courses_csv)
    
    merged = schedule_df.merge(courses_df, on="course_id")
    df = merged.groupby(['course_id', 'course_name', 'academic_year', 'semester'])['student_id'].count().reset_index()
    df.rename(columns={'student_id': 'demand'}, inplace=True)
    df['t'] = df.apply(map_term_to_time, axis=1)
    df = df.sort_values(by=['course_id', 't'])

    results = []
    plot_data = []

    # 2. Build Linear Regression model for each course
    for course_id, group in df.groupby('course_id'):
        course_name = group['course_name'].iloc[0]
        
        # We need at least 2 points to fit a line
        if len(group) < 2:
            continue
            
        X = group[['t']].values
        y = group['demand'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate fit MAE
        y_pred = model.predict(X)
        mae = mean_absolute_error(y, y_pred)
        
        # Predict next term (t=5 -> Fall 2026)
        next_t = 5
        pred_next = int(round(model.predict([[next_t]])[0]))
        
        # Determine trend direction
        trend = "Stable"
        if model.coef_[0] > 0.5: trend = "Increasing"
        elif model.coef_[0] < -0.5: trend = "Decreasing"

        results.append({
            'course_id': course_id,
            'course_name': course_name,
            'historical_mean': round(group['demand'].mean(), 1),
            'trend_direction': trend,
            'coefficient': round(model.coef_[0], 2),
            'mae': round(mae, 2),
            'forecast_Fall_2026': pred_next
        })
        
        # Save plot data for the top few courses (for plotting)
        for _, row in group.iterrows():
            plot_data.append({'course_name': course_name, 'Term': term_name(row['t']), 'Demand': row['demand'], 'Type': 'Actual'})
        plot_data.append({'course_name': course_name, 'Term': term_name(next_t), 'Demand': pred_next, 'Type': 'Forecast'})

    # 3. Output Results
    df_results = pd.DataFrame(results).sort_values(by='forecast_Fall_2026', ascending=False)
    csv_path = os.path.join(REPORTS_DIR, "forecast_results.csv")
    df_results.to_csv(csv_path, index=False)
    
    print(f"Total courses forecasted: {len(df_results)}")
    print("Top 5 Courses by Forecasted Demand (Fall 2026):")
    print(df_results[['course_name', 'trend_direction', 'forecast_Fall_2026', 'mae']].head(5).to_string(index=False))
    
    print("\nOverall Model Performance:")
    print(f"Average MAE across all courses: {df_results['mae'].mean():.2f} students")

    # Plotting top 5 courses for visualization
    top_5_courses = df_results['course_name'].head(5).tolist()
    df_plot = pd.DataFrame(plot_data)
    df_plot_top5 = df_plot[df_plot['course_name'].isin(top_5_courses)]
    
    fig = px.line(df_plot_top5, x='Term', y='Demand', color='course_name', symbol='Type',
                  title='Course Demand Forecast (Linear Regression)',
                  markers=True)
    fig.write_html(os.path.join(REPORTS_DIR, "demand_forecast.html"))
    print(f"\nForecast visualization saved to {REPORTS_DIR}\\demand_forecast.html")

if __name__ == "__main__":
    run_forecasting()
