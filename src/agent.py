"""
agent.py — Stage 10/11: LLM Agent with Tool-Calling powered by Groq
===================================================================
Provider: Groq (via groq SDK / OpenAI-compatible function calling)
Model:    llama-3.3-70b-versatile
Tools:    6 live DB-backed tools from agent_tools.py
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq
try:
    from . import agent_tools
except ImportError:
    import agent_tools

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")

# ── Initialize Groq Client ────────────────────────────────────────────────────
client = Groq(api_key=GROQ_API_KEY)
MODEL = "openai/gpt-oss-120b"

# ── Tool Declarations (OpenAI / Groq standard JSON schema) ────────────────────
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_classroom_utilization",
            "description": (
                "Returns a ranked list of all classrooms with their total scheduled hours "
                "(valid timeslots only). Use this to answer questions about which rooms are "
                "most/least used, busiest buildings, or overall utilization."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_instructor_workload",
            "description": (
                "Returns a ranked list of all instructors with their total session counts "
                "and departments. Use this to answer questions about instructor workload, "
                "who teaches the most/least, or workload distribution by department."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_course_demand",
            "description": (
                "Returns all courses ranked by student enrollment count. Use this to answer "
                "questions about which courses are most/least popular, enrollment numbers, "
                "or course demand by department."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_conflict_detection",
            "description": (
                "Detects and returns all classroom double-bookings and instructor "
                "scheduling conflicts from the live database. Use this to answer questions "
                "about scheduling conflicts, double-booked rooms, or instructors assigned "
                "to multiple courses at the same time."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_classroom",
            "description": (
                "Recommends the best available classroom for a specific timeslot and "
                "minimum required capacity. Ranks candidates by lowest existing utilization. "
                "Use when asked to suggest a room for a course or session."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "The course ID needing a room. Default is 1 if unknown."
                    },
                    "timeslot_id": {
                        "type": "integer",
                        "description": "The timeslot ID for which to find a room."
                    },
                    "required_capacity": {
                        "type": "integer",
                        "description": "Minimum number of seats required in the room."
                    }
                },
                "required": ["timeslot_id", "required_capacity"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": (
                "Returns a per-course linear regression demand forecast for Fall 2026, "
                "including historical mean, trend direction, regression coefficient, and MAE. "
                "Use this to answer questions about future enrollment projections, which "
                "courses are growing or shrinking, or forecasted demand."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

SYSTEM_PROMPT = """You are the University Resource Intelligence Assistant for this university's scheduling system.

You have access to exactly 6 data tools:
1. get_classroom_utilization — classroom scheduled hours
2. get_instructor_workload — instructor session counts
3. get_course_demand — course enrollment figures
4. get_conflict_detection — scheduling conflicts (rooms & instructors)
5. recommend_classroom — room recommendation for a given timeslot and capacity
6. get_forecast — course demand forecast for Fall 2026

STRICT RULES:
- Language: ALWAYS answer in clear, professional English. If the user asks in another language (like Tamil, Hindi, etc.) or asks you to speak in another language, politely state in English: "I only support English. Please ask your questions about university scheduling in English."
- Grounding: For scheduling, classroom, instructor, and course data queries, you MUST ONLY answer using data returned by a tool call. Never invent or estimate numbers.
- Out of scope: If a question is outside the scope of your 6 tools (e.g. student grades, dean information, staff personal contacts, university fees), state clearly: "I don't have access to that information through my available tools."
- Conciseness: Be direct, clean, and concise. Never repeat words or loop.
"""

# ── Tool Dispatcher ────────────────────────────────────────────────────────────
def sanitize_for_json(obj):
    import uuid, decimal, datetime
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(i) for i in obj]
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
        return str(obj)
    elif isinstance(obj, datetime.timedelta):
        return obj.total_seconds()
    else:
        return obj

def dispatch_tool(name: str, args: dict):
    if name == "get_classroom_utilization":
        return sanitize_for_json(agent_tools.get_classroom_utilization())
    elif name == "get_instructor_workload":
        return sanitize_for_json(agent_tools.get_instructor_workload())
    elif name == "get_course_demand":
        return sanitize_for_json(agent_tools.get_course_demand())
    elif name == "get_conflict_detection":
        return sanitize_for_json(agent_tools.get_conflict_detection())
    elif name == "recommend_classroom":
        course_id = args.get("course_id", 1)
        timeslot_id = args.get("timeslot_id")
        required_capacity = args.get("required_capacity")
        return sanitize_for_json(agent_tools.recommend_classroom(course_id, timeslot_id, required_capacity))
    elif name == "get_forecast":
        return sanitize_for_json(agent_tools.get_forecast())
    else:
        return {"error": f"Unknown tool: {name}"}

# ── Agentic Ask Function ───────────────────────────────────────────────────────
def ask(question: str) -> str:
    """
    Send a natural-language question to the Groq agent.
    Performs tool calling automatically and returns a grounded answer.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.1,
            max_tokens=600,
            frequency_penalty=0.3
        )

        response_message = response.choices[0].message

        # If the model does not call any tool, return its final text answer
        if not response_message.tool_calls:
            raw_text = response_message.content or ""
            return raw_text.replace('\u202f', ' ').replace('\xa0', ' ')

        # Model decided to call one or more tools
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            fn_name = tool_call.function.name
            try:
                fn_args = json.loads(tool_call.function.arguments)
            except Exception:
                fn_args = {}

            print(f"  [tool call] {fn_name}({fn_args})")
            tool_result = dispatch_tool(fn_name, fn_args)

            # Format results concisely to stay well within token limits
            if fn_name == "get_conflict_detection" and isinstance(tool_result, dict):
                rc = tool_result.get("classroom_conflicts", [])
                ic = tool_result.get("instructor_conflicts", [])
                truncated_result = {
                    "total_classroom_conflicts": len(rc),
                    "total_instructor_conflicts": len(ic),
                    "worst_instructor_conflict": ic[0] if ic else None,
                    "top_instructor_conflicts": ic[:5] if ic else [],
                    "top_classroom_conflicts": rc[:5] if rc else []
                }
            elif isinstance(tool_result, list) and len(tool_result) > 10:
                truncated_result = tool_result[:10] + [{"_note": f"... {len(tool_result) - 10} more items omitted"}]
            else:
                truncated_result = tool_result

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": fn_name,
                "content": json.dumps(truncated_result)
            })

# ── Test Suite ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    separator = "-" * 70

    QUESTIONS = [
        ("Q1 [Utilization]",
         "Which classroom is used the most, and how many hours has it been scheduled?"),

        ("Q2 [Conflicts]",
         "Are there any instructor scheduling conflicts in the current schedule? "
         "Give me a summary of how many there are and the worst case."),

        ("Q3 [Recommendation]",
         "I need a room for 40 students during timeslot 5. What room do you recommend?"),

        ("Q4 [Forecast]",
         "Which course is forecasted to have the highest demand next semester (Fall 2026), "
         "and what is the forecast number?"),

        ("Q5 [Out-of-scope]",
         "Who is the dean of the university, and what is their email address?"),
    ]

    for label, question in QUESTIONS:
        print(f"\n{'=' * 70}")
        print(f"{label}")
        print(f"Q: {question}")
        print(separator)
        answer = ask(question)
        print(f"A: {answer}")

    print(f"\n{'=' * 70}")
    print("Stage 10 (Groq) testing complete.")
