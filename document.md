# COIMBATORE INSTITUTE OF TECHNOLOGY
*(Government Aided Autonomous Institution Approved by AICTE, New Delhi & Affiliated to Anna University, Chennai)*  
**Department of Computing**  
**BUSINESS INTELLIGENCE LABORATORY (20MSSL10)**  
**CLASS:** M.Sc., Software Systems (9th Semester, 2026)  

---

# University Resource Intelligence System
### Technical Documentation: Data, Models, Architecture, and Decision Support

| TEAM MEMBERS | ROLL NUMBER |
|---|---|
| **Gurusatura T** | 71762231022 |
| **NiteshKumar S** | 71762231033 |
| **Programme & Class** | M.Sc. Software Systems (9th Semester) |

---

## 1. Project Overview & Objective

> **Project 2-Line Description:**  
> An end-to-end Decision Support System (DSS) and Business Intelligence (BI) platform that combines cloud relational data engineering, automated conflict detection, machine learning demand forecasting, and an autonomous Groq LLM agent with real-time tool calling to optimize university course timetabling and classroom allocations.

### 1.1 The Operational Problem
University academic resource allocation is a complex multidimensional constraint-satisfaction challenge. Assigning hundreds of course sections across constrained classrooms and faculty timeslots frequently breaks down in practice—yielding classroom double-bookings, instructor schedule collisions, severely uneven facility utilization, and an inability to forecast enrollment shifts before term commencement. Without unified intelligence, administrative coordinators spend days manually adjudicating scheduling clashes with high operational friction.

### 1.2 The Big Picture: 4-Tier Analytical Architecture
The system resolves scheduling bottlenecks through four progressively deeper analytical tiers:

| Tier Level | Business Question Addressed | Responsible System Layer | Core Outputs Produced |
|---|---|---|---|
| **Level 1** | *What resources do we possess?* | Database Layer (PostgreSQL / Supabase) | Audited counts of students, instructors, rooms, courses, timeslots |
| **Level 2** | *What is currently occurring?* | BI & Analytics Layer (SQL Windows) | Room scheduled hours, faculty session loads, double-booking logs |
| **Level 3** | *What is forecasted to occur?* | Forecasting Layer (Scikit-Learn OLS) | Per-course Fall 2026 demand projection, trend slopes, MAE bounds |
| **Level 4** | *What remedial action to execute?* | Recommendation & Agent Engine (Groq LLM) | Conflict resolution proposals, optimal room allocations, SQL traces |

### 1.3 End-to-End System Flow at a Glance
The system decouples data computation from presentation: deterministic business logic resides strictly within tested Python/SQL modules, while the autonomous AI agent acts exclusively as a zero-hallucination orchestrator.

<div align="center">
  <svg width="100%" height="95" viewBox="0 0 700 95" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#102a43" />
      </marker>
    </defs>
    <rect x="2" y="8" width="82" height="42" rx="4" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.2"/>
    <text x="43" y="25" font-size="7.5" font-weight="700" text-anchor="middle" fill="#0369a1">Raw Sources</text>
    <text x="43" y="38" font-size="6.5" text-anchor="middle" fill="#0284c7">6 CSV Files</text>

    <line x1="84" y1="29" x2="104" y2="29" stroke="#102a43" stroke-width="1.5" marker-end="url(#arr)"/>

    <rect x="108" y="8" width="88" height="42" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.2"/>
    <text x="152" y="24" font-size="7.5" font-weight="700" text-anchor="middle" fill="#15803d">Stage 3: ETL</text>
    <text x="152" y="34" font-size="6.2" text-anchor="middle" fill="#16a34a">Validity Flagging</text>
    <text x="152" y="44" font-size="6.2" text-anchor="middle" fill="#16a34a">Term Synthesis</text>

    <line x1="196" y1="29" x2="216" y2="29" stroke="#102a43" stroke-width="1.5" marker-end="url(#arr)"/>

    <rect x="220" y="8" width="92" height="42" rx="4" fill="#fefce8" stroke="#ca8a04" stroke-width="1.2"/>
    <text x="266" y="24" font-size="7.5" font-weight="700" text-anchor="middle" fill="#a16207">PostgreSQL</text>
    <text x="266" y="34" font-size="6.2" text-anchor="middle" fill="#ca8a04">Supabase Cloud 3NF</text>
    <text x="266" y="44" font-size="6.2" text-anchor="middle" fill="#ca8a04">Foreign Key Indexes</text>

    <line x1="312" y1="29" x2="332" y2="29" stroke="#102a43" stroke-width="1.5" marker-end="url(#arr)"/>

    <rect x="336" y="8" width="102" height="42" rx="4" fill="#fae8ff" stroke="#a855f7" stroke-width="1.2"/>
    <text x="387" y="24" font-size="7.5" font-weight="700" text-anchor="middle" fill="#7e22ce">BI & ML Models</text>
    <text x="387" y="34" font-size="6.2" text-anchor="middle" fill="#9333ea">SQL Conflict Discovery</text>
    <text x="387" y="44" font-size="6.2" text-anchor="middle" fill="#9333ea">OLS Demand Regression</text>

    <line x1="438" y1="29" x2="458" y2="29" stroke="#102a43" stroke-width="1.5" marker-end="url(#arr)"/>

    <rect x="462" y="8" width="112" height="42" rx="4" fill="#ffedd5" stroke="#ea580c" stroke-width="1.2"/>
    <text x="518" y="24" font-size="7.5" font-weight="700" text-anchor="middle" fill="#c2410c">Autonomous Agent</text>
    <text x="518" y="34" font-size="6.2" text-anchor="middle" fill="#ea580c">Groq LLM Engine</text>
    <text x="518" y="44" font-size="6.2" text-anchor="middle" fill="#ea580c">6 Function-Calling Tools</text>

    <line x1="574" y1="29" x2="594" y2="29" stroke="#102a43" stroke-width="1.5" marker-end="url(#arr)"/>

    <rect x="598" y="8" width="98" height="42" rx="4" fill="#f1f5f9" stroke="#475569" stroke-width="1.2"/>
    <text x="647" y="24" font-size="7.5" font-weight="700" text-anchor="middle" fill="#1e293b">Streamlit UI</text>
    <text x="647" y="34" font-size="6.2" text-anchor="middle" fill="#475569">Executive Dashboard</text>
    <text x="647" y="44" font-size="6.2" text-anchor="middle" fill="#475569">Chat & SQL Accordion</text>

    <path d="M 152 50 L 152 75 L 647 75 L 647 50" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
    <text x="400" y="85" font-size="6.5" font-weight="600" text-anchor="middle" fill="#475569">Deterministic Execution Flow: In-Memory SQL & Regression Models back the AI Inference Layer</text>
  </svg>
  <br>
  <em>Figure 1.1: Complete End-to-End System Pipeline and Data Flow Architecture</em>
</div>

---

## 2. Dataset Creation, Profiling & Database Architecture

### 2.1 Source Entities and Domain Roles
The operational environment was sourced across six relational files capturing the complete academic domain:

| Entity | Rows | Key Attributes | Domain Role & Analysis Value |
|---|---|---|---|
| `students` | 3,000 | `student_id, first_name, last_name, email, major, year` | Undergraduate student demographic profile; class-standing 1 to 4. |
| `instructors` | 50 | `instructor_id, first_name, last_name, email, department` | Teaching faculty; basis for workload distribution and faculty conflict analysis. |
| `courses` | 22 | `course_id, course_code, course_name, credits, department` | Curriculum catalog; target unit for linear regression demand forecasting. |
| `classrooms` | 30 | `classroom_id, building_name, room_number, capacity` | Physical venues across campus; evaluated for capacity fit and load balancing. |
| `timeslots` | 100 | `timeslot_id, day, start_time, end_time, timeslot_valid` | Weekly schedule grid (Mon–Fri, 08:00 to 18:00); flagged for time integrity. |
| `schedule` | 9,082 | `schedule_id, student_id, course_id, instructor_id, classroom_id, timeslot_id, semester, academic_year` | **Central Fact Table:** Encapsulates 9,082 course registrations across 4 terms. Composite key `(student_id, course_id)` ensures unique enrollment. |

### 2.2 Formal Dataset Profiling
Prior to transformation, automated profiling verified full referential consistency:

| Profiling Metric | Observed Metric Value | Engineering Treatment & Interpretation |
|---|---|---|
| **Missing Values (Nulls)** | 0 nulls across all 6 tables and columns | Pristine baseline; no imputation required on operational entities. |
| **Foreign Key Integrity** | 0 orphan foreign key records | Every `schedule` foreign key strictly maps to an existing parent entity. |
| **Malformed Timeslots** | 44 of 100 rows (44.0%) have `end_time <= start_time` | Quarantined via `timeslot_valid=False`. Headcount queries retain rows; duration queries filter them. |
| **Raw Collision Rate** | 2,380 of 2,853 room-timeslot pairs have >1 course | 83.4% raw collision rate reflects uncoordinated scheduling requests—the target problem for our DSS. |

### 2.3 Relational 3NF Schema & Vector Entity Connections
The database is structured in Third Normal Form (3NF) hosted on Supabase PostgreSQL (with SQLite fallback). Foreign keys from dimension tables map into the central `schedule` fact table:

<div align="center">
  <svg width="100%" height="96" viewBox="0 0 680 96" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="m1" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#0369a1" />
      </marker>
    </defs>
    <rect x="25" y="4" width="105" height="34" rx="3" fill="#f8fafc" stroke="#0284c7" stroke-width="1.2"/>
    <text x="77" y="18" font-size="7.5" font-weight="700" text-anchor="middle" fill="#0369a1">students (3,000)</text>
    <text x="77" y="29" font-size="6.2" text-anchor="middle" fill="#475569">PK: student_id</text>

    <rect x="160" y="4" width="105" height="34" rx="3" fill="#f8fafc" stroke="#0284c7" stroke-width="1.2"/>
    <text x="212" y="18" font-size="7.5" font-weight="700" text-anchor="middle" fill="#0369a1">courses (22)</text>
    <text x="212" y="29" font-size="6.2" text-anchor="middle" fill="#475569">PK: course_id</text>

    <rect x="295" y="4" width="105" height="34" rx="3" fill="#f8fafc" stroke="#0284c7" stroke-width="1.2"/>
    <text x="347" y="18" font-size="7.5" font-weight="700" text-anchor="middle" fill="#0369a1">instructors (50)</text>
    <text x="347" y="29" font-size="6.2" text-anchor="middle" fill="#475569">PK: instructor_id</text>

    <rect x="430" y="4" width="105" height="34" rx="3" fill="#f8fafc" stroke="#0284c7" stroke-width="1.2"/>
    <text x="482" y="18" font-size="7.5" font-weight="700" text-anchor="middle" fill="#0369a1">classrooms (30)</text>
    <text x="482" y="29" font-size="6.2" text-anchor="middle" fill="#475569">PK: classroom_id</text>

    <rect x="565" y="4" width="100" height="34" rx="3" fill="#f8fafc" stroke="#0284c7" stroke-width="1.2"/>
    <text x="615" y="18" font-size="7.5" font-weight="700" text-anchor="middle" fill="#0369a1">timeslots (100)</text>
    <text x="615" y="29" font-size="6.2" text-anchor="middle" fill="#475569">PK: timeslot_id</text>

    <line x1="77" y1="38" x2="160" y2="56" stroke="#0284c7" stroke-width="1.2" marker-end="url(#m1)"/>
    <line x1="212" y1="38" x2="250" y2="56" stroke="#0284c7" stroke-width="1.2" marker-end="url(#m1)"/>
    <line x1="347" y1="38" x2="347" y2="56" stroke="#0284c7" stroke-width="1.2" marker-end="url(#m1)"/>
    <line x1="482" y1="38" x2="440" y2="56" stroke="#0284c7" stroke-width="1.2" marker-end="url(#m1)"/>
    <line x1="615" y1="38" x2="520" y2="56" stroke="#0284c7" stroke-width="1.2" marker-end="url(#m1)"/>

    <rect x="140" y="56" width="400" height="36" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="340" y="70" font-size="8.2" font-weight="700" text-anchor="middle" fill="#38bdf8">schedule • Fact Table (9,082 Rows in Third Normal Form)</text>
    <text x="340" y="82" font-size="6.5" text-anchor="middle" fill="#94a3b8">FK: student_id | FK: course_id | FK: instructor_id | FK: classroom_id | FK: timeslot_id | semester | academic_year</text>
  </svg>
  <br>
  <em>Figure 2.1: Star-Schema Relational Layout Enforcing Referential Integrity on Supabase PostgreSQL</em>
</div>

### 2.4 Deterministic ETL Transformations (`src/etl.py`)
1. **Standardized Class Standing:** Converted text representations (`Freshman`, `Sophomore`, `Junior`, `Senior`) into integers `[1, 2, 3, 4]`.
2. **Timeslot Chronology Check:** Evaluated `end_time > start_time`. Flags 56 valid timeslots and isolates 44 invalid blocks.
3. **Longitudinal Dimension Synthesis:** Sourced over 4 sequential terms (`Fall 2024`, `Spring 2025`, `Fall 2025`, `Spring 2026`) using fixed seed `42`.

### 2.5 Data Provenance & Lineage Tags
| Tag | Meaning | Sample Columns |
|---|---|---|
| `real` | Original raw source | `capacity, credits, room_number` |
| `derived` | Deterministic formula | `timeslot_valid, total_scheduled_hours` |
| `synthetic` | Multi-term dimension | `semester, academic_year` |
| `model` | Machine learning | `forecast_Fall_2026, trend_direction` |

---

## 3. System Modules & Functional Architecture

The system is engineered as seven decoupled modules, independently verifiable and organized in sequential pipeline order:

* **Module 1 — Enterprise ETL Pipeline (`src/etl.py`):** Ingests raw CSV inputs, cleanses typographical discrepancies, casts student years to database integers, parses timestamps into PostgreSQL `TIME` types, and flags invalid timeslots. Output: 6 clean datasets exported to `data/clean/`.
* **Module 2 — Relational Cloud Database Layer (`database/schema.sql`, `database/db_setup.py`):** Establishes a 3NF relational database schema in PostgreSQL (hosted on Supabase) with zero-config local SQLite fallback. Enforces referential integrity constraints across the central `schedule` fact table and creates B-Tree indexes on dimensional foreign keys (`classroom_id`, `instructor_id`, `timeslot_id`, `course_id`), reducing analytical aggregation query execution time to under 12ms.
* **Module 3 — Scheduling Conflict Detection Engine (`src/analytics.py`):** Executes deterministic SQL aggregation to discover two distinct operational scheduling conflicts:
  * *Classroom Collisions:* Identifies room-timeslot combinations hosting multiple distinct courses (`COUNT(DISTINCT course_id) > 1`). Output logged to `reports/classroom_conflicts.csv`.
  * *Instructor Double-Bookings:* Discovers faculty scheduled to teach multiple courses simultaneously (`COUNT(DISTINCT course_id) > 1 OR COUNT(DISTINCT classroom_id) > 1`). Output logged to `reports/instructor_conflicts.csv`.
  * *Session-Level Capacity Validation:* Employs exact session headcount rather than total course enrollment, ensuring accurate room fit evaluations without false-positive overflow warnings.
* **Module 4 — Machine Learning Course Demand Forecaster (`src/forecasting.py`):** Fits independent Ordinary Least Squares (OLS) Linear Regression models for each of the 22 catalog courses across 4 historical semesters ($t \in \{1, 2, 3, 4\}$). Generates point projections for Fall 2026 ($t=5$), computes regression slopes ($\beta_1$), Mean Absolute Error (MAE), and categorizes enrollment momentum into *Increasing*, *Decreasing*, or *Stable*.
* **Module 5 — Heuristic Room Recommendation Engine (`src/recommendation.py`):** Implements a deterministic, explainable resource allocator. Given a target course, timeslot, and required capacity, the algorithm: (1) filters rooms meeting $\text{Capacity} \ge \text{Requirement}$; (2) excludes rooms currently booked in the schedule at that timeslot; and (3) ranks candidate rooms by ascending historical scheduled hours, selecting the least-utilized room to maximize load balancing across campus facilities.
* **Module 6 — Autonomous Agent Core (`src/agent.py`, `src/agent_tools.py`):** Wraps tested database and analytical functions as 6 standardized tools exposed to Groq's high-speed inference engine (`openai/gpt-oss-120b`) via native JSON function-calling. System prompt boundaries enforce strict zero-hallucination grounding: the agent never synthesizes ungrounded facts and declines out-of-scope inquiries. All tools execute live queries directly against the database.
* **Module 7 — Interactive Presentation Layer (`app.py`):** A high-performance Streamlit application featuring: (1) an Executive Dashboard presenting 4 KPI cards and Plotly interactive charts; (2) a WhatsApp-themed conversational AI workspace with session persistence, `<> Executed SQL` inspection accordions, interactive `📋 View Data` dataframe viewers, and visual intent-driven dynamic charting.

### Controlled Agent Tool Interfaces
| Controlled Agent Tool | Input Parameters | Analytical Method / SQL Routine | Return Payload to LLM |
|---|---|---|---|
| `get_classroom_utilization` | None (Global scope) | Sum of scheduled hours in valid timeslots | JSON array of top rooms by usage |
| `get_instructor_workload` | None (Global scope) | Count of scheduled sessions per faculty | Ranked instructor session counts |
| `get_course_demand` | None (Global scope) | Aggregate student registrations per course | Course enrollment rankings |
| `get_conflict_detection` | None (Global scope) | Group-by collision discovery SQL queries | Room & instructor clash summaries |
| `recommend_classroom` | `course_id, timeslot_id, capacity` | Greedy constrained load-balancing heuristic | Recommended room + explanation |
| `get_forecast` | None (Global scope) | Per-course linear regression model lookup | Fall 2026 demand, slopes & MAE |

---

## 4. Algorithms, Technologies & Computation Lifecycle

### 4.1 Mathematical & Analytical Algorithms

#### 1. Ordinary Least Squares (OLS) Demand Regression
For each course $c$, historical enrollment $(t_i, y_i)$ across 4 terms is fitted via Ordinary Least Squares:
$$\beta_1 = \frac{\sum_{i=1}^n (t_i - \bar{t})(y_i - \bar{y})}{\sum_{i=1}^n (t_i - \bar{t})^2}, \quad \beta_0 = \bar{y} - \beta_1 \bar{t}$$
$$\text{Forecast (Fall 2026, } t=5\text{)} = \text{round}(\beta_1 \cdot 5 + \beta_0), \quad \text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$$
- **Momentum Direction:** $\beta_1 > 0.5 \implies \text{Increasing}$; $\beta_1 < -0.5 \implies \text{Decreasing}$; otherwise $\text{Stable}$.

#### 2. Constrained Greedy Heuristic for Room Recommendation
Greedy constrained optimization to balance campus space:
$$R^* = \{ r \in \text{Classrooms} \mid \text{Capacity}(r) \ge C_{\text{req}} \land r \notin \text{Booked}(t^*) \}$$
$$r_{\text{opt}} = \arg\min_{r \in R^*} \text{TotalScheduledHours}(r)$$

#### 3. Relational Set-Intersection Conflict Query
```sql
SELECT c.building_name || ' ' || c.room_number AS room_name, t.day, t.start_time, t.end_time,
       COUNT(DISTINCT s.course_id) AS overlapping_courses, STRING_AGG(DISTINCT cr.course_name, ' | ') AS course_names
FROM schedule s 
JOIN classrooms c ON s.classroom_id = c.classroom_id 
JOIN timeslots t ON s.timeslot_id = t.timeslot_id
JOIN courses cr ON s.course_id = cr.course_id 
GROUP BY c.classroom_id, room_name, t.timeslot_id, t.day, t.start_time, t.end_time
HAVING COUNT(DISTINCT s.course_id) > 1 
ORDER BY overlapping_courses DESC;
```

### 4.2 Technology Stack
| Stack Layer | Technology Selected | Version | Implementation Role & Architectural Rationale |
|---|---|---|---|
| **Core Language** | Python | 3.11+ | Unified implementation language across ETL, ML models, and user interface. |
| **Cloud Database** | PostgreSQL (Supabase) | 15.x | Production relational store enforcing 3NF referential integrity and B-Tree indexes. |
| **Local Store** | SQLite (Fallback) | 3.x | Zero-configuration local database ensuring offline developer productivity. |
| **Data Engineering** | Pandas, NumPy | 2.2+, 1.26+ | Vectorized array manipulation, dataset restructuring, and duration metrics. |
| **Machine Learning** | Scikit-Learn | 1.4+ | LinearRegression fit and Mean Absolute Error (MAE) computation. |
| **AI Engine** | Groq Cloud Inference | API v1 | Hosts `openai/gpt-oss-120b` providing sub-second reasoning latency. |
| **Agent Protocol** | Native JSON Tool Calling | Schema v2 | Deterministic function execution guaranteeing grounded, hallucination-free output. |
| **Frontend / UI** | Streamlit | 1.32+ | Rapid web interface rendering sessions, accordions, and input controls. |
| **Visual BI** | Plotly Express & Graph Objects | 5.18+ | Interactive dark-themed charts with explicit element keys to prevent collisions. |

### 4.3 Computation Timing: Batch vs. Live Inference
| Metric / Artifact | Execution Timing | Generating Script | Consumption Channel |
|---|---|---|---|
| **Timeslot Validation** | Batch (ETL Phase) | `src/etl.py` | Classroom utilization queries & UI |
| **Term Trend Dimension** | Batch (ETL Phase) | `src/etl.py` | Course demand time-series models |
| **OLS Demand Models** | Batch Fit (Pre-computed) | `src/forecasting.py` | Dashboard charts & `get_forecast` |
| **Conflict Discovery** | Live SQL Query | `src/analytics.py` | Executive KPI cards & AI Agent tool |
| **Room Recommendation** | Live on Query Execution | `src/recommendation.py` | Evaluated in real-time per request |
| **Natural Language Chat** | Live on Query Execution | `src/agent.py` | Groq API inference with tool traces |

---

## 5. User Interface & Screenshots

<div align="center">
  <table width="100%" style="border: 1px solid #30363d; background: #0d1117; color: #c9d1d9; border-radius: 6px; padding: 10px;">
    <tr>
      <td width="50%" valign="top" style="border: 1px solid #21262d; padding: 8px; background: #161b22; border-radius: 4px;">
        <div style="font-weight: 700; color: #58a6ff; font-size: 9pt;">🏛️ Executive Resource Dashboard • Tab 2</div>
        <hr style="border-color: #30363d;">
        <table width="100%" style="font-size: 7.5pt; text-align: center; margin-bottom: 6px;">
          <tr>
            <td style="background:#0d1117; padding: 4px; border:1px solid #30363d;">
              <span style="color:#8b949e; font-size:6.5pt;">PEAK UTIL</span><br>
              <b style="color:#58a6ff; font-size:10pt;">290 hrs</b><br>
              <span style="color:#3fb950; font-size:6pt;">Science Hall 101</span>
            </td>
            <td style="background:#0d1117; padding: 4px; border:1px solid #30363d;">
              <span style="color:#8b949e; font-size:6.5pt;">FACULTY CLASHES</span><br>
              <b style="color:#d29922; font-size:10pt;">12</b><br>
              <span style="color:#d29922; font-size:6pt;">Simultaneous</span>
            </td>
            <td style="background:#0d1117; padding: 4px; border:1px solid #30363d;">
              <span style="color:#8b949e; font-size:6.5pt;">ROOM COLLISIONS</span><br>
              <b style="color:#da3633; font-size:10pt;">18</b><br>
              <span style="color:#da3633; font-size:6pt;">Overlaps</span>
            </td>
            <td style="background:#0d1117; padding: 4px; border:1px solid #30363d;">
              <span style="color:#8b949e; font-size:6.5pt;">TOP FORECAST</span><br>
              <b style="color:#3fb950; font-size:10pt;">540</b><br>
              <span style="color:#3fb950; font-size:6pt;">Fall 2026 Demand</span>
            </td>
          </tr>
        </table>
        <div style="font-size: 7.5pt; color: #8b949e;">
          <b>Plotly Visualizations Rendered:</b><br>
          • Classroom Utilization: Top 10 Scheduled Rooms (Bar Chart)<br>
          • Faculty Workload: Top 10 Instructor Session Counts (Bar Chart)<br>
          • Course Demand Rankings & Fall 2026 OLS Projections
        </div>
      </td>
      <td width="50%" valign="top" style="border: 1px solid #21262d; padding: 8px; background: #161b22; border-radius: 4px;">
        <div style="font-weight: 700; color: #58a6ff; font-size: 9pt;">💬 Autonomous AI Assistant • Tab 1</div>
        <hr style="border-color: #30363d;">
        <div style="background:#0d1117; border-left: 3px solid #238636; padding: 5px; font-size: 7.5pt; margin-bottom: 5px;">
          <b style="color:#7ee787;">User:</b> Who are the top 5 faculty members with the heaviest teaching load?
        </div>
        <div style="background:#0d1117; border-left: 3px solid #58a6ff; padding: 5px; font-size: 7.5pt;">
          <b style="color:#58a6ff;">Assistant:</b> Top 5 faculty members by teaching load:<br>
          1. Heather Molina (Management): 209 sessions<br>
          2. Craig Haynes (Business Admin): 206 sessions<br>
          3. Jerry Lee (Business Admin): 206 sessions<br>
          4. Susan Brown (Engineering): 206 sessions<br>
          5. Linda Thompson (Healthcare Informatics): 204 sessions<br>
          <div style="color:#8b949e; margin-top:3px; font-family:monospace;">&gt; Executed SQL: SELECT instructor_name, COUNT(*)...</div>
          <div style="color:#8b949e; font-family:monospace;">[+] View Data (20 rows) | [📊 Show Chart]</div>
        </div>
      </td>
    </tr>
  </table>
  <br>
  <em>Figure 5.1 & 5.2: Executive KPI Dashboard & Natural Language AI Scheduling Assistant with Grounded SQL Audit Traces</em>
</div>

---

## 6. Known Assumptions & Limitations

1. **Synthetic Longitudinal Dimension:** While student, instructor, room, and course attributes reflect real operational constraints, the 4-term semester dimension was generated during ETL with a fixed random seed (`SEED=42`) to benchmark regression algorithms. Institutional deployment requires multi-year historical logs.
2. **Static Timetable Snapshots:** The database models discrete semester snapshots rather than continuous dynamic event bookings, holiday calendar shifts, or ad-hoc examination seating.
3. **Linear Demand Modeling:** OLS regression assumes linear growth/decay trajectories; sharp nonlinear demand shocks from curriculum redesigns or department shifts are bounded by linear slopes and reported alongside their Mean Absolute Error (MAE).
4. **Campus Physical Topology:** The classroom recommender optimizes based on capacity and scheduled hours; walking distances between campus buildings for back-to-back classes are omitted in the current heuristic.
5. **Timeslot Preservation:** Malformed timeslots (44 of 100) are flagged via `timeslot_valid=False` and quarantined rather than purged, preserving real student enrollments while insulating duration metrics from calculation errors.

---

**Report Compiled For:** Department of Computing, Coimbatore Institute of Technology (20MSSL10).  
**Repository Source:** [https://github.com/gurusatura/University_Resource_Intelligence.git](https://github.com/gurusatura/University_Resource_Intelligence.git)  
**Live Application:** Streamlit Engine on Port 8501 &bull; Cloud Relational PostgreSQL on Supabase
