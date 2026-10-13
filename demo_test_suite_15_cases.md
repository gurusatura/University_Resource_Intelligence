# UniResource IQ — 15 Demonstration Test Cases

A complete reference guide for testing and demonstrating the **University Resource Intelligence System**. Includes the exact prompt, the triggered tool, the expected grounded numbers, and the visual UI components rendered.

---

## 1. Classroom Utilization Tests

### Test 1: Busiest Classroom (Single Metric)
- **Prompt:** `Which classroom has the highest scheduled hours?`
- **Tool Triggered:** `get_classroom_utilization`
- **Expected Answer:** Classroom **D 773** (ID: 25) with **828.0 scheduled hours** (capacity: 29).
- **UI Visuals:** Text answer + Interactive Plotly Bar Chart + `<> Executed SQL` accordion + `📋 View Data` table.

### Test 2: Top 5 Classroom Utilization Ranking
- **Prompt:** `Show me the top 5 most used classrooms and their hours.`
- **Tool Triggered:** `get_classroom_utilization`
- **Expected Answer:**
  1. **D 773** — 828.0 hrs
  2. **A 541** — 811.0 hrs
  3. **B 544** — 785.0 hrs
  4. **J 651** — 783.5 hrs
  5. **F 886** — 774.0 hrs
- **UI Visuals:** Horizontal/vertical Plotly Bar Chart + SQL query + Data table.

### Test 3: Least Utilized Classroom
- **Prompt:** `Which classroom is used the least, and how many hours was it scheduled?`
- **Tool Triggered:** `get_classroom_utilization`
- **Expected Answer:** Classroom **F 493** (ID: 15) with the lowest scheduled hours (**621.5 hours**).
- **UI Visuals:** Text answer + SQL accordion + Data table.

---

## 2. Instructor Workload Tests

### Test 4: Peak Instructor Workload
- **Prompt:** `Which instructor taught the highest number of sessions?`
- **Tool Triggered:** `get_instructor_workload`
- **Expected Answer:** **Heather Molina** (Department: Management) with **209 total sessions**.
- **UI Visuals:** Green Plotly Bar Chart of Top Faculty + Executed SQL accordion + Data table.

### Test 5: Top 5 Instructors by Sessions
- **Prompt:** `Who are the top 5 faculty members with the heaviest teaching load?`
- **Tool Triggered:** `get_instructor_workload`
- **Expected Answer:**
  1. **Heather Molina** (Management) — 209 sessions
  2. **David Morales** (Biology) — 198 sessions
  3. **Michael Vance** (History) — 196 sessions
  4. **Kathryn Perez** (Economics) — 195 sessions
  5. **Lisa Thomas** (Sociology) — 194 sessions
- **UI Visuals:** Interactive Plotly Workload Chart + SQL query + Data table.

---

## 3. Course Demand & Enrollment Tests

### Test 6: Most Enrolled Course
- **Prompt:** `Which course has the highest student enrollment?`
- **Tool Triggered:** `get_course_demand`
- **Expected Answer:** **"De-engineered systematic pricing structure"** (Course ID: 16, Computer Science) with **457 students enrolled**.
- **UI Visuals:** Purple Plotly Bar Chart + Executed SQL accordion + Data table.

### Test 7: Top Enrolled Courses
- **Prompt:** `List the top courses by student demand.`
- **Tool Triggered:** `get_course_demand`
- **Expected Answer:** Ranks top courses led by Course 16 (457), followed by other high-demand offerings.
- **UI Visuals:** Plotly Demand Chart + SQL query + 10-row Data table.

---

## 4. Scheduling Conflict Detection Tests

### Test 8: Total Scheduling Conflicts Summary
- **Prompt:** `Are there any scheduling conflicts in the university schedule?`
- **Tool Triggered:** `get_conflict_detection`
- **Expected Answer:** **2,380 classroom double-bookings** and **2,684 instructor multi-booking conflicts** detected in the schedule.
- **UI Visuals:** Bar Chart comparing Room vs Instructor collisions + SQL query + Data table.

### Test 9: Instructor Scheduling Overlaps
- **Prompt:** `Are any instructors scheduled to teach two courses at the same time?`
- **Tool Triggered:** `get_conflict_detection`
- **Expected Answer:** Confirms that 2,684 instructor overlap instances exist and quotes the worst cases.
- **UI Visuals:** Executed SQL accordion (`HAVING COUNT(DISTINCT s.course_id) > 1`) + Data table.

### Test 10: Classroom Double-Bookings
- **Prompt:** `Which classrooms have double-booking conflicts?`
- **Tool Triggered:** `get_conflict_detection`
- **Expected Answer:** Identifies top classroom collisions where multiple courses share the same room at the same timeslot.
- **UI Visuals:** Plotly conflict comparison + Executed SQL accordion + Data table.

---

## 5. Classroom Recommendation Tests

### Test 11: Successful Recommendation (Standard Case)
- **Prompt:** `Recommend an available classroom for 20 students during timeslot 10.`
- **Tool Triggered:** `recommend_classroom` (args: `required_capacity=20`, `timeslot_id=10`)
- **Expected Answer:** Recommends **K 793** (Capacity: 46, lowest utilization: 665.0 hrs).
- **UI Visuals:** Text recommendation explaining room capacity and utilization optimality.

### Test 12: Successful Recommendation (Large Capacity)
- **Prompt:** `I need an available room for 40 students at timeslot 2. What do you recommend?`
- **Tool Triggered:** `recommend_classroom` (args: `required_capacity=40`, `timeslot_id=2`)
- **Expected Answer:** Recommends the available candidate meeting `>= 40` seats with minimum prior scheduled hours.
- **UI Visuals:** Recommendation card + candidate details.

### Test 13: Graceful Failure (No Room Large Enough)
- **Prompt:** `Can you recommend a classroom for 500 students at timeslot 5?`
- **Tool Triggered:** `recommend_classroom` (args: `required_capacity=500`, `timeslot_id=5`)
- **Expected Answer:** Graceful refusal: *"No classrooms exist with capacity >= 500."*
- **UI Visuals:** Clear explanatory card showing why the allocation is impossible.

---

## 6. Machine Learning Demand Forecast Tests

### Test 14: Fall 2026 Top Growth Course
- **Prompt:** `Which course is forecasted to have the highest demand in Fall 2026?`
- **Tool Triggered:** `get_forecast`
- **Expected Answer:** **"User-centric maximized firmware"** (Course ID: 19) with a forecasted enrollment of **128 students** (historical mean: 107.5, trend: Increasing, coefficient: +8.2, MAE: 4.5).
- **UI Visuals:** Plotly Forecast Chart with color-coded trend bars + Executed Model query + Data table.

---

## 7. Out-of-Scope & Grounding Test

### Test 15: Out-of-Scope Strict Refusal
- **Prompt:** `Who is the dean of the university and what is their email address?`
- **Tool Triggered:** None (LLM identifies out-of-scope question).
- **Expected Answer:** Strict refusal: *"I don't have access to that information through my available tools."*
- **UI Visuals:** Safe text message with zero hallucination and zero invented names.
