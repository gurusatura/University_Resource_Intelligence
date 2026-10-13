import os
import sys

# Add src/ to sys.path for clean modular imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import agent_tools

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def demo_utilization():
    print_header("Classroom Utilization (Top 5)")
    data = agent_tools.get_classroom_utilization()
    for row in data[:5]:
        print(f"  Room: {row['room_name']:10s} | Capacity: {row['capacity']:<4} | Scheduled Hours: {row['total_scheduled_hours']:.1f}")

def demo_workload():
    print_header("Instructor Workload (Top 5)")
    data = agent_tools.get_instructor_workload()
    for row in data[:5]:
        print(f"  Instructor: {row['instructor_name']:20s} | Dept: {row['department']:20s} | Sessions: {row['total_sessions']}")

def demo_demand():
    print_header("Course Demand (Top 5)")
    data = agent_tools.get_course_demand()
    for row in data[:5]:
        print(f"  Course: {row['course_name']:45s} | Enrollment: {row['enrollment']}")

def demo_conflicts():
    print_header("Conflict Detection (Summary)")
    data = agent_tools.get_conflict_detection()
    
    room_conflicts = data['classroom_conflicts']
    inst_conflicts = data['instructor_conflicts']
    
    print(f"  Total Classroom Conflicts:  {len(room_conflicts)}")
    print(f"  Total Instructor Conflicts: {len(inst_conflicts)}")
    
    if inst_conflicts:
        worst = inst_conflicts[0]
        print("\n  [WORST INSTRUCTOR CONFLICT]")
        print(f"  Instructor: {worst['instructor_name']}")
        print(f"  Timeslot:   ID {worst['timeslot_id']} ({worst['day']} {worst['start_time']} - {worst['end_time']})")
        print(f"  Overlapping Courses: {worst['overlapping_courses']}")
        print("  Courses:")
        for c in worst['course_names'].split(' | '):
            print(f"    - {c}")

def demo_recommendation():
    print_header("Recommend a Classroom")
    print("  Scenario: We need a room for 40 students during Timeslot 5.")
    print("  Searching...")
    result = agent_tools.recommend_classroom(course_id=1, timeslot_id=5, required_capacity=40)
    
    if result.get("status") == "SUCCESS":
        print(f"\n  [RECOMMENDATION] {result['recommendation']} (Capacity: {result['capacity']})")
        print(f"  Reason: {result['reason']}")
    else:
        print(f"\n  [FAILED] {result.get('reason')}")

def demo_forecast():
    print_header("Demand Forecast for Fall 2026 (Top 5)")
    data = agent_tools.get_forecast()
    for row in data[:5]:
        print(f"  Course: {row['course_name']:45s} | Trend: {row['trend_direction']:10s} | Est. Fall 2026: {row['forecast_Fall_2026']}")

def main_menu():
    while True:
        print("\n" + "*"*60)
        print("   UNIVERSITY SCHEDULING INTELLIGENCE - OFFLINE DEMO")
        print("*"*60)
        print("  1. View Classroom Utilization")
        print("  2. View Instructor Workload")
        print("  3. View Course Demand")
        print("  4. View Scheduling Conflicts")
        print("  5. Run Classroom Recommendation Engine")
        print("  6. View Fall 2026 Demand Forecast")
        print("  0. Exit")
        print("*"*60)
        
        choice = input("Select an option (0-6): ").strip()
        
        if choice == '1':
            demo_utilization()
        elif choice == '2':
            demo_workload()
        elif choice == '3':
            demo_demand()
        elif choice == '4':
            demo_conflicts()
        elif choice == '5':
            demo_recommendation()
        elif choice == '6':
            demo_forecast()
        elif choice == '0':
            print("Exiting demo...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    clear_screen()
    main_menu()
