from typing import TypedDict
from langgraph.graph import StateGraph, END
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


class QuizState(TypedDict):
    topic: str
    quiz: list


def generate_quiz(state):

    topic = state["topic"]

    prompt = f"""
Generate exactly 10 multiple-choice questions (MCQs) on the programming topic: {topic}.

Difficulty Distribution:

Question 1-5:
- Easy level
- Beginner friendly
- Basic concepts
- Very simple questions

Question 6-8:
- Medium level
- Conceptual understanding
- Slightly tricky

Question 9-10:
- Hard level
- Advanced concepts
- Interview level

Rules:
- Questions must be strictly related to {topic}.
- Each question must have exactly 4 options.
- Only one correct answer.
- Keep questions short and clear.
- Avoid repeated questions.
- Return ONLY valid JSON.
- No markdown.
- No explanation.
- No text before or after JSON.

Format:

[
  {{
    "question": "What is an array?",
    "options": [
      "Collection of same type elements",
      "Loop",
      "Function",
      "Class"
    ],
    "answer": "Collection of same type elements"
  }}
]
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown if Gemini returns it
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        quiz = json.loads(text)
    except Exception:
        # Fallback quiz if JSON parsing fails
        quiz = [
            {
                "question": f"What is {topic}?",
                "options": [
                    "Programming Concept",
                    "Animal",
                    "Country",
                    "Movie"
                ],
                "answer": "Programming Concept"
            }
        ]

    return {"quiz": quiz}


builder = StateGraph(QuizState)

builder.add_node(
    "quiz_generator",
    generate_quiz
)

builder.set_entry_point(
    "quiz_generator"
)

builder.add_edge(
    "quiz_generator",
    END
)

graph = builder.compile()