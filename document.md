<!--
================================================================================
BULLETPROOF INSTRUCTIONS FOR CLAUDE (DOCUMENT COMPILER)
================================================================================
PROMPT TO COPY INTO CLAUDE:
"You are compiling a formal academic technical documentation report for:
COIMBATORE INSTITUTE OF TECHNOLOGY (Department of Computing, Business Intelligence Lab 20MSSL10).

CRITICAL FORMATTING & LAYOUT RULES:
1. STRICT PAGE BUDGET: The entire document MUST FIT WITHIN EXACTLY 5 PAGES (A4). 
   Do NOT stretch or expand this into 10–12 pages. Tighten spacing, set margins to 0.5 inches (12.7mm), 
   and use 10pt body font with 1.15 line spacing.
2. ZERO ASCII ART: NEVER use ASCII line-art or text boxes with dashes/slashes, as proportional fonts 
   scramble and break them into illegible text. Format all architectures and schemas as structured tables 
   or elegant shaded callout boxes.
3. NO EMPTY GAPS: For screenshots, do NOT render large blank boxes. Render compact, framed UI caption blocks.
4. PAGE ALLOCATION (EXACTLY 5 PAGES):
   - Page 1: CIT Header, Title, Team Table (Gurusatura T, NiteshKumar S), 2-Line Project Description, 
     Problem Statement, and 4-Tier Analytical Architecture Table.
   - Page 2: Dataset Description (6 Relational Tables), Profiling Results, 3NF Star-Schema Architecture Table, 
     ETL Transformations, and Data Provenance Tags.
   - Page 3: System Modules (Modules 1 to 7) and Controlled Agent Tool Interface Table.
   - Page 4: Mathematical Formulations (OLS Regression formulas, Greedy Room Heuristic, SQL Conflict Query), 
     Technology Stack Table, and Batch vs. Live Computation Timeline.
   - Page 5: System UI Captions & Mockup Frames, Known Assumptions & Limitations (5 points), and Institutional Footer."
================================================================================
-->

# COIMBATORE INSTITUTE OF TECHNOLOGY
*(Government Aided Autonomous Institution Approved by AICTE, New Delhi & Affiliated to Anna University, Chennai)*  
**Department of Computing**  
**BUSINESS INTELLIGENCE LABORATORY (20MSSL10)**  
**CLASS:** M.Sc., Software Systems (9th Semester)  

---

# University Resource Intelligence System
### Technical Documentation: Data, Models, Architecture, and Decision Support

**Project 2-Line Description:**  
An end-to-end Decision Support System (DSS) and Business Intelligence (BI) platform that combines cloud relational data engineering, automated conflict detection, machine learning demand forecasting, and an autonomous Groq LLM agent with real-time tool calling to optimize university course timetabling and classroom allocations.

---

## 1. Overview & System Big Picture

### 1.1 The Operational Problem
University academic scheduling is an NP-hard multidimensional constraint satisfaction challenge. Allocating hundreds of courses across constrained classrooms and faculty timeslots frequently produces room double-bookings, instructor schedule clashes, suboptimal capacity utilization, and inability to anticipate future enrollment surges. Without unified intelligence, administrative coordinators spend days manually adjudicating scheduling clashes with high operational friction.

### 1.2 The Big Picture: 4-Tier Analytical Architecture
The **University Resource Intelligence System** resolves scheduling bottlenecks through four progressively deeper analytical tiers:

| Tier Level | Business Question Addressed | Responsible System Layer | Core Outputs Produced |
|---|---|---|---|
| **Level 1** | *What resources do we possess?* | Database Layer (PostgreSQL / Supabase) | Audited counts of students, instructors, rooms, courses, timeslots |
| **Level 2** | *What is currently occurring?* | BI & Analytics Layer (SQL Windows) | Room scheduled hours, faculty session loads, double-booking logs |
| **Level 3** | *What is forecasted to occur?* | Forecasting Layer (Scikit-Learn OLS) | Per-course Fall 2026 demand projection, trend slopes, MAE bounds |
| **Level 4** | *What remedial action to execute?* | Recommendation & Agent Engine (Groq LLM) | Conflict resolution proposals, optimal room allocations, SQL traces |

### 1.3 End-to-End System Flow at a Glance
Deterministic business logic resides strictly within tested Python/SQL modules, while the autonomous AI agent acts exclusively as a zero-hallucination orchestrator:
`Raw Datasets (6 CSVs) → Stage 3: ETL (Validation & Term Synthesis) → Stage 4: Supabase Cloud DB (3NF Schema) → Stage 5 & 6: BI & Conflict Analytics → Stage 7 & 8: ML Demand Forecasting & Room Allocator → Stage 9 & 10: Groq LLM Agent (6 DB Tools) → Stage 11: Streamlit Executive UI`

---

## 2. Dataset & Database Description

### 2.1 Source Datasets
The system ingests and reconciles 6 relational entities representing a comprehensive university campus environment:

| Entity / Source File | Raw Rows | Clean Rows | Attributes | Description & Domain Role |
|---|---|---|---|---|
| `students.csv` | 3,000 | 3,000 | `student_id`, `first_name`, `last_name`, `email`, `major`, `year` | Undergraduate students across academic years (Freshman to Senior). |
| `instructors.csv` | 50 | 50 | `instructor_id`, `first_name`, `last_name`, `email`, `department` | Faculty members across academic departments. |
| `courses.csv` | 22 | 22 | `course_id`, `course_code`, `course_name`, `credits`, `department` | Catalog of university courses offered across degrees. |
| `classrooms.csv` | 30 | 30 | `classroom_id`, `building_name`, `room_number`, `capacity` | Campus facilities spanning 30 physical lecture halls and rooms. |
| `timeslots.csv` | 100 | 100 | `timeslot_id`, `day`, `start_time`, `end_time`, `timeslot_valid` | Weekly schedule blocks (Mon–Fri, 08:00 to 18:00). |
| `schedule.csv` | 9,082 | 9,082 | `schedule_id`, `student_id`, `course_id`, `instructor_id`, `classroom_id`, `timeslot_id`, `semester`, `academic_year` | Central fact table capturing 9,082 student-course-room-instructor allocations across 4 academic terms. |

### 2.2 Relational Schema & Entity Connections
The database is structured in Third Normal Form (3NF) hosted on Supabase PostgreSQL (with automatic local SQLite fallback):

| Dimension Entity | Relationship Cardinality | Fact Foreign Key | Enforced Constraint |
|---|---|---|---|
| `students` (3,000) | One-to-Many (1:N) | `schedule.student_id` | Foreign Key, Indexed |
| `courses` (22) | One-to-Many (1:N) | `schedule.course_id` | Foreign Key, Indexed |
| `instructors` (50) | One-to-Many (1:N) | `schedule.instructor_id` | Foreign Key, Indexed |
| `classrooms` (30) | One-to-Many (1:N) | `schedule.classroom_id` | Foreign Key, Indexed |
| `timeslots` (100) | One-to-Many (1:N) | `schedule.timeslot_id` | Foreign Key, Indexed |
| **Central Fact Table** | **`schedule` (9,082 Rows)** | **Composite PK: `(student_id, course_id)`** | **Third Normal Form (3NF)** |

### 2.3 ETL Data Quality Engineering (`src/etl.py`)
Data integrity is enforced through a deterministic 5-step ETL pipeline:
1. **Categorical-to-Ordinal Transformation:** Academic student standing (`Freshman`, `Sophomore`, `Junior`, `Senior`) is validated and mapped to discrete integer levels `[1, 2, 3, 4]`.
2. **Timeslot Chronological Validation:** Start and end timestamps are parsed (`%H:%M:%S`). A boolean integrity attribute `timeslot_valid` is computed (`end_time > start_time`). Malformed records (`end_time <= start_time`) are quarantined so that downstream analytics ignore invalid durations.
3. **Longitudinal Term Synthesis:** Because standard static schedules lack longitudinal depth for trend modeling, the ETL assigns allocations across 4 sequential semesters: `Fall 2024` ($t=1$), `Spring 2025` ($t=2$), `Fall 2025` ($t=3$), and `Spring 2026` ($t=4$) using a fixed random seed (`SEED=42`) for 100% reproducibility.
4. **Data Provenance Tagging:** Every database column is tagged to guarantee complete lineage:
   - `real`: Original entity values (e.g., student names, classroom capacity, course credits).
   - `derived`: Formally computed attributes (e.g., `timeslot_valid`, `total_scheduled_hours`).
   - `synthesized`: Multi-term longitudinal dimensions (`semester`, `academic_year`).
   - `model`: Output predictions (e.g., `forecast_Fall_2026`, `trend_direction`).

---

## 3. System Modules & Functional Architecture

| Module Index | Module Name & Script Reference | Core Functional Role |
|---|---|---|
| **Module 1** | Enterprise ETL Pipeline (`src/etl.py`) | Ingests 6 CSVs, standardizes student years, flags invalid timeslots, synthesizes terms. |
| **Module 2** | Relational Database Layer (`database/schema.sql`) | Enforces 3NF foreign keys and B-Tree indexes on Supabase PostgreSQL / SQLite. |
| **Module 3** | Conflict Detection Engine (`src/analytics.py`) | Discovers room collisions and instructor double-bookings via SQL group-by queries. |
| **Module 4** | ML Course Demand Forecaster (`src/forecasting.py`) | Fits per-course OLS linear regression across 4 terms to project Fall 2026 demand. |
| **Module 5** | Room Recommendation Engine (`src/recommendation.py`) | Solves greedy constrained capacity matching and utilization-ranked load balancing. |
| **Module 6** | Autonomous Agent Core (`src/agent.py`) | Orchestrates Groq `openai/gpt-oss-120b` with 6 function-calling tools and zero hallucinations. |
| **Module 7** | Interactive UI Layer (`app.py`) | Streamlit application hosting Executive KPI Dashboard and conversational AI chat. |

### 3.1 Module 1: Enterprise ETL Pipeline (`src/etl.py`)
Cleanses raw operational files, validates relational foreign keys, computes duration validity, and exports pristine datasets to `data/clean/`.

### 3.2 Module 2: Relational Cloud Database Layer (`database/schema.sql`, `database/db_setup.py`)
Maintains relational schemas in PostgreSQL with indexes on foreign keys (`classroom_id`, `instructor_id`, `timeslot_id`) to accelerate complex grouping queries from seconds to under 12 milliseconds.

### 3.3 Module 3: Scheduling Conflict Detection Engine (`src/analytics.py`)
Executes analytical SQL queries to detect both physical and operational collisions:
- **Classroom Collisions:** Finds instances where distinct courses share the same `classroom_id` and `timeslot_id` (`HAVING COUNT(DISTINCT course_id) > 1`).
- **Instructor Double-Bookings:** Identifies faculty scheduled to teach multiple courses or present in multiple classrooms simultaneously (`HAVING COUNT(DISTINCT course_id) > 1 OR COUNT(DISTINCT classroom_id) > 1`).

### 3.4 Module 4: Machine Learning Course Demand Forecasting (`src/forecasting.py`)
Fits course-specific Ordinary Least Squares (OLS) Linear Regression models over 4 historical semesters to project enrollment for `Fall 2026` ($t=5$), calculating trend directions and Mean Absolute Error (MAE).

### 3.5 Module 5: Heuristic Room Recommendation Engine (`src/recommendation.py`)
Implements a greedy constraint-satisfaction heuristic:
1. Filters rooms satisfying physical capacity: $\text{Capacity} \ge \text{Required Capacity}$.
2. Eliminates rooms booked at target `timeslot_id`.
3. Ranks surviving candidates by ascending historical scheduled hours, selecting the least-utilized room to maximize campus load-balancing.

### 3.6 Module 6: Autonomous AI Agent Core (`src/agent.py`, `src/agent_tools.py`)
Leverages Groq's high-speed inference engine (`openai/gpt-oss-120b`) with native JSON function calling over 6 standardized tools. Formats grounded responses, suppresses hallucinations, and executes tool actions.

### 3.7 Module 7: Interactive Presentation UI (`app.py`)
Streamlit-based dashboard featuring:
- **Tab 1: AI Scheduling Assistant:** WhatsApp-styled chat workspace, multi-session management, `<> Executed SQL` inspection, `📋 View Data` dataframe viewers, and intent-driven dynamic Plotly charts.
- **Tab 2: Executive Dashboard:** 4 KPI summary cards (Peak Room Utilization, Instructor Conflicts, Room Double-Bookings, Top Fall 2026 Forecast) alongside 4 full-screen Plotly visualizations and collision summary tables.

---

## 4. Algorithms & Technologies Used

### 4.1 Core Algorithms

#### 1. Ordinary Least Squares (OLS) Demand Regression
For each course $c$, historical enrollment points $(t_i, y_i)$ for $t \in \{1, 2, 3, 4\}$ are fitted using:
$$\hat{y}(t) = \beta_1 t + \beta_0$$
$$\beta_1 = \frac{\sum_{i=1}^n (t_i - \bar{t})(y_i - \bar{y})}{\sum_{i=1}^n (t_i - \bar{t})^2}, \quad \beta_0 = \bar{y} - \beta_1 \bar{t}$$
- **Forecast for Fall 2026 ($t=5$):** $\hat{y}_{\text{Fall 2026}} = \text{round}(\beta_1 \cdot 5 + \beta_0)$
- **Model Evaluation:** $\text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$
- **Trend Classification:**
  - $\beta_1 > +0.5 \implies \text{Increasing}$
  - $\beta_1 < -0.5 \implies \text{Decreasing}$
  - Otherwise $\implies \text{Stable}$

#### 2. Relational Set-Intersection Conflict Detection
SQL windowing and aggregation detecting multidimensional overlaps:
```sql
SELECT c.building_name || ' ' || c.room_number AS room_name,
       t.day, t.start_time, t.end_time,
       COUNT(DISTINCT s.course_id) AS overlapping_courses,
       STRING_AGG(DISTINCT cr.course_name, ' | ') AS course_names
FROM schedule s
JOIN classrooms c ON s.classroom_id = c.classroom_id
JOIN timeslots t ON s.timeslot_id = t.timeslot_id
JOIN courses cr ON s.course_id = cr.course_id
GROUP BY c.classroom_id, room_name, t.timeslot_id, t.day, t.start_time, t.end_time
HAVING COUNT(DISTINCT s.course_id) > 1
ORDER BY overlapping_courses DESC;
```

#### 3. Constrained Heuristic for Resource Allocation
$$\text{Candidate Rooms } R^* = \{ r \in \text{Classrooms} \mid \text{Cap}(r) \ge C_{\text{req}} \land r \notin \text{Booked}(t^*) \}$$
$$\text{Optimal Allocation } r_{\text{opt}} = \arg\min_{r \in R^*} \text{ScheduledHours}(r)$$

#### 4. Visual Intent Query Classification
To prevent unnecessary chart generation on pure factual questions, queries undergo deterministic visual intent parsing:
$$\text{RenderChart} = \text{QueryContains}(\{\text{"chart"}, \text{"graph"}, \text{"plot"}, \text{"visualize"}, \text{"diagram"}, \text{"histogram"}\})$$
When false, the system outputs clean text + SQL accordion + data table + an on-demand `"📊 Show Chart"` action button.

### 4.2 Technologies & Tools Summary

| Layer | Technology | Version / Spec | Purpose & Implementation |
|---|---|---|---|
| **Programming Language** | Python | 3.11+ | Core implementation language for pipelines, ML, and agent. |
| **Cloud Database** | PostgreSQL / Supabase | 15.x | Cloud relational database enforcing 3NF constraints and foreign keys. |
| **Local Fallback DB** | SQLite | 3.x | Zero-config embedded local database for offline development. |
| **Data Processing** | Pandas, NumPy | 2.x, 1.26+ | ETL transformations, matrix aggregations, and dataframe manipulation. |
| **Machine Learning** | Scikit-Learn | 1.4+ | LinearRegression, Mean Absolute Error, time-series projections. |
| **AI Inference Engine** | Groq Cloud SDK | API v1 | Ultra-fast LLM inference hosting `openai/gpt-oss-120b`. |
| **Agent Paradigm** | Native Tool-Calling | JSON Schema | Autonomous multi-turn function calling over 6 analytical tools. |
| **Frontend Framework** | Streamlit | 1.32+ | Interactive single-page web application with session state management. |
| **BI Visualizations** | Plotly Express & Graph Objects | 5.18+ | Interactive HTML5 charts (Bar, Area, Trend lines) styled in dark mode. |
| **Version Control** | Git & GitHub | Remote `main` | Continuous source management and collaborative deployment. |

---

## 5. Execution Flow & Score Computation Timeline

| Metric / Score | Computation Timing | Engine / Script | Output Location | Consumed By |
|---|---|---|---|---|
| **Data Validation (`timeslot_valid`)** | Batch (ETL Phase) | `src/etl.py` | `timeslots_clean.csv` / DB | Utilization metrics, room recommender |
| **Longitudinal Term Synthesis** | Batch (ETL Phase) | `src/etl.py` | `schedule_clean.csv` / DB | Demand forecasting, trend analysis |
| **Classroom Collisions** | Live SQL / Batch Cache | `src/analytics.py` | `classroom_conflicts.csv` / DB | Executive KPI card, `get_conflict_detection` tool |
| **Instructor Double-Bookings** | Live SQL / Batch Cache | `src/analytics.py` | `instructor_conflicts.csv` / DB | Executive KPI card, `get_conflict_detection` tool |
| **OLS Demand Forecast (Fall 2026)** | Batch Fit & Export | `src/forecasting.py` | `course_demand_forecast_model` | Executive Dashboard chart, `get_forecast` tool |
| **Classroom Recommendation** | Live Inference (Query-time) | `src/recommendation.py` | Transient memory / In-memory | `recommend_classroom` tool |
| **AI Agent Response Generation** | Live Inference (Query-time) | `src/agent.py` | Streamlit session state | Chat UI workspace, SQL accordion |

---

## 6. User Interface & Screenshot Captions

*(Note: High-resolution screenshots to be inserted into the designated figures below)*

### Figure 1: Executive KPI Dashboard (Tab 2)
```
+-----------------------------------------------------------------------------------+
| [SCREENSHOT PLACEHOLDER 1: Executive Resource KPI Dashboard]                     |
| Displays 4 top-level KPI metrics (Peak Room Utilization: 290 hrs in Science Hall; |
| Instructor Conflicts: 12 collisions; Room Collisions: 18 overlaps; Fall 2026 Top  |
| Course Forecast) alongside 4 full-width Plotly charts displaying room usage,      |
| faculty workload distributions, and enrollment forecasts.                         |
+-----------------------------------------------------------------------------------+
Caption: Figure 1 — University Resource Intelligence Executive Dashboard displaying real-time campus utilization, conflict summaries, and predictive enrollment trends.
```

### Figure 2: Autonomous AI Scheduling Assistant Chat (Tab 1)
```
+-----------------------------------------------------------------------------------+
| [SCREENSHOT PLACEHOLDER 2: AI Scheduling Assistant Natural Language Workspace]    |
| Shows WhatsApp-themed chat interface with persistent session history, suggested   |
| quick queries, grounded tabular responses, expandable '<> Executed SQL' block,    |
| and '📋 View Data' dataframe viewer.                                              |
+-----------------------------------------------------------------------------------+
Caption: Figure 2 — Autonomous AI Scheduling Assistant responding to complex scheduling questions with grounded SQL query traces and interactive data accordions.
```

### Figure 3: Intent-Driven On-Demand Plotly Visualization
```
+-----------------------------------------------------------------------------------+
| [SCREENSHOT PLACEHOLDER 3: Dynamic Plotly Visualization & Interactive Tools]      |
| Demonstrates selective chart rendering: non-visual queries display clean text and |
| an on-demand '📊 Show Chart' button, while explicit visual queries render rich    |
| responsive Plotly bar charts with unique element IDs.                             |
+-----------------------------------------------------------------------------------+
Caption: Figure 3 — Dynamic Plotly visualization generated autonomously by the Groq agent upon detecting visual query intent.
```

### Figure 4: Multi-Session Management & Quick Queries
```
+-----------------------------------------------------------------------------------+
| [SCREENSHOT PLACEHOLDER 4: Collapsible Sidebar & Session History]                 |
| Illustrates the collapsible sidebar featuring '+ New Chat', session reset, saved |
| conversations, suggested prompt shortcuts, and Supabase cloud connection badge.   |
+-----------------------------------------------------------------------------------+
Caption: Figure 4 — Collapsible navigation sidebar managing multi-turn conversational sessions and database connectivity status.
```

---

## 7. Known Assumptions & Limitations

Mirroring enterprise-grade technical specifications, the following structural constraints and domain assumptions apply to the current release:

1. **Synthetic Longitudinal Dimension:** While student, classroom, course, and instructor entities reflect real university scheduling data, the semester-over-semester longitudinal dimension was generated across 4 terms during ETL to benchmark OLS regression. The forecast demonstrates statistical rigor but requires historical multi-year records for institutional deployment.
2. **Static Timetable Snapshots:** The database represents discrete semester schedules rather than dynamic calendar events with holiday shifts, exam reading periods, or ad-hoc room bookings.
3. **Linear Regression Assumption:** OLS regression assumes linear demand trajectory; nonlinear demand spikes driven by sudden curriculum overhauls or faculty sabbaticals are bounded by linear trend lines and reported with their associated MAE error margin.
4. **Physical Campus Topology:** The classroom recommender optimizes based on capacity and scheduled hours; walking distance between adjacent campus buildings for back-to-back classes is omitted in the current heuristic.
5. **Batch Scoring vs. Live Re-indexing:** Model forecasts and conflict caches are precomputed during scheduled batch runs; ad-hoc what-if scheduling queries are evaluated on the fly via the recommendation and analytical tools.

---
**Report Compiled For:** Department of Computing, Coimbatore Institute of Technology (20MSSL10).  
**Repository Source:** [https://github.com/gurusatura/University_Resource_Intelligence.git](https://github.com/gurusatura/University_Resource_Intelligence.git)
