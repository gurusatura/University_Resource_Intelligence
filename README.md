# University Resource Intelligence System

An end-to-end Decision Support System (DSS) and Business Intelligence (BI) platform for university exam and course scheduling. Combines cloud relational database architecture, automated ETL pipelines, SQL conflict detection, machine learning demand forecasting, heuristic room recommendations, and an autonomous AI agent with tool-calling capabilities.

---

## Architecture Overview

```
                      [ Raw Data Sources ]
                  (Students, Courses, Rooms,
                   Instructors, Timeslots, Sched)
                               │
                               ▼
                    [ Stage 3: ETL Pipeline ]
                       (Validation & Clean)
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
 [ Stage 4: PostgreSQL ]                  [ Clean Datasets ]
   (Supabase Cloud DB)                     (Local Parquet/CSV)
            │                                     │
   ┌────────┴────────┐                            │
   ▼                 ▼                            │
[ Stage 5: BI ]  [ Stage 6: Analytics ]           │
  (Reporting)      (Conflict Detection)           │
   │                 │                            │
   └────────┬────────┘                            │
            ▼                                     ▼
     [ Reports / Marts ]                 [ Stage 7 & 8: ML & Optimization ]
   (HTML Charts, Conflict CSVs)            (Demand Forecast, Room Recommender)
            │                                     │
            └──────────────────┬──────────────────┘
                               ▼
                   [ Stage 9 & 10: AI Agent ]
                    (Groq Tool-Calling Engine)
                               │
                               ▼
                   [ Stage 11: Streamlit UI ]
               (Executive KPI Dashboard & Chat)
```

---

## Key Features

1. **Enterprise Data Pipeline (ETL):** Validates timeslots (`end_time > start_time`), casts types, and validates referential integrity.
2. **PostgreSQL Relational Core:** Hosted on Supabase with strict primary keys, foreign key constraints, and normalized schema.
3. **Automated Conflict Detection:** SQL-driven identification of classroom double-bookings and instructor multi-course overlaps.
4. **Machine Learning Demand Forecasting:** Per-course Linear Regression with Trend Direction, Coefficients, and Mean Absolute Error (MAE) forecasting demand for Fall 2026.
5. **Classroom Recommendation Engine:** Capacity matching and utilization minimization heuristics for optimal room allocations.
6. **Autonomous Intelligence Agent:** Powered by Groq's low-latency inference engine with native function-calling over 6 live database and analytical tools.
7. **Interactive Streamlit Interface:** Modern dark-themed dashboard featuring executive KPI cards, Plotly charts, and a WhatsApp-themed chat workspace.

---

## Project Structure

```
University_Resource_Intelligence/
│
├── data/
│   ├── raw/                 # Original 6 source datasets
│   └── clean/               # Validated and transformed datasets from ETL
│
├── database/
│   ├── schema.sql           # PostgreSQL DDL table definitions and constraints
│   └── db_setup.py          # Migration and database ingestion script
│
├── src/
│   ├── __init__.py          # Package initialization
│   ├── etl.py               # Stage 3: Data cleaning and transformation pipeline
│   ├── bi_reporting.py      # Stage 5: SQL-driven BI visualizations
│   ├── analytics.py         # Stage 6: Scheduling conflict detection
│   ├── forecasting.py       # Stage 7: ML linear regression demand forecasting
│   ├── recommendation.py    # Stage 8: Heuristic classroom recommendation engine
│   ├── agent_tools.py       # Stage 9: 6 controlled agent tools
│   └── agent.py             # Stage 10: Groq LLM tool-calling agent
│
├── reports/                 # Generated visualizations, HTML charts, and CSV summaries
├── app.py                   # Stage 11: Streamlit Dashboard & Chat Application
├── demo_cli.py              # Interactive terminal CLI demo
├── requirements.txt         # Production Python dependencies
├── .env.example             # Template for environment configuration
├── .gitignore               # Excludes secrets, virtual environments, and caches
└── README.md                # Project documentation
```

---

## 11-Stage Implementation Walkthrough

| Stage | Name | Description | Key Artifact |
|---|---|---|---|
| **Stage 1** | Problem Definition | Scope, KPIs, constraints, and objective functions | Documentation |
| **Stage 2** | Schema Design | 3NF Relational schema with foreign keys and indexes | `database/schema.sql` |
| **Stage 3** | ETL Pipeline | Timeslot validation, data casting, and clean export | `src/etl.py` |
| **Stage 4** | Cloud Database Setup | Automated table creation and ingestion into PostgreSQL | `database/db_setup.py` |
| **Stage 5** | BI Visualizations | Interactive Plotly charts for utilization and workload | `src/bi_reporting.py` |
| **Stage 6** | Conflict Analytics | Advanced SQL aggregation detecting double-bookings | `src/analytics.py` |
| **Stage 7** | Demand Forecasting | Scikit-learn Linear Regression model for Fall 2026 | `src/forecasting.py` |
| **Stage 8** | Recommendation Engine | Constraint satisfaction and utilization-ranked room allocation | `src/recommendation.py` |
| **Stage 9** | Controlled Tools | 6 standardized tool interfaces with zero-failure fallbacks | `src/agent_tools.py` |
| **Stage 10** | Agent Intelligence | Groq-powered autonomous LLM with function calling | `src/agent.py` |
| **Stage 11** | Interactive UI | Streamlit dashboard with KPI cards and WhatsApp-style chat | `app.py` |

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/gurusatura/University_Resource_Intelligence.git
cd University_Resource_Intelligence
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```
Inside `.env`:
```env
DATABASE_URL=postgresql://user:password@host:5432/postgres
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

## Running the Application

### Launch Streamlit Dashboard & Chat UI
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### Run Interactive Terminal CLI
```bash
python demo_cli.py
```

### Run Autonomous Agent in Terminal
```bash
python src/agent.py
```

---

## Database & Analytical Queries

The PostgreSQL database enforces relational integrity across 6 core entities:
- `students`: Student demographics and academic standing
- `instructors`: Faculty profiles and department affiliations
- `courses`: Course registry with assigned academic departments
- `classrooms`: Physical facilities with room capacity and building locations
- `timeslots`: Days, start times, end times, and validity flags
- `schedule`: Central fact table linking courses, rooms, instructors, and timeslots

---

## Tech Stack

- **Language:** Python 3.10+
- **Database:** PostgreSQL (Supabase Cloud)
- **Data Engineering:** Pandas, NumPy, SQLAlchemy, Psycopg2
- **Machine Learning:** Scikit-Learn (Linear Regression)
- **Data Visualization:** Plotly Express & Plotly Graph Objects
- **AI Agent & LLM:** Groq API (`openai/gpt-oss-120b` via Groq LPU)
- **Web UI:** Streamlit with custom CSS architecture
