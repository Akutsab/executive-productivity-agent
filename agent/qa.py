import os
from typing import List

from dotenv import load_dotenv
from google import genai

from models.schemas import Action

load_dotenv()


def build_context(actions: List[Action]) -> str:
    """
    Convert normalized actions into compact context for Gemini.
    """

    context_parts = []

    for action in actions:

        sources_text = "\n".join(
            f"- {source}"
            for source in action.sources
        )

        evidence_text = "\n".join(
            f"- {evidence}"
            for evidence in action.evidence
        )

        context_parts.append(
            f"""
ACTION ID: {action.id}
TITLE: {action.title}
OWNER: {action.owner}
OWNER TYPE: {action.owner_type}
STAKEHOLDER: {action.stakeholder}
DEADLINE: {action.deadline}
STATUS: {action.status}
PRIORITY: {action.priority}
DESCRIPTION: {action.description}

SOURCES:
{sources_text}

EVIDENCE:
{evidence_text}
"""
        )

    return "\n".join(context_parts)


def local_answer(question: str, actions: List[Action]) -> str:
    """
    Simple deterministic fallback.
    Used when Gemini is unavailable.
    """

    q = question.lower()

    # Raghav / vendor list
    if "raghav" in q or "vendor" in q:
        for action in actions:
            if action.id == "ACT-001":
                return (
                    "You promised Raghav Sethi that you would send "
                    "the updated vendor list. Your latest commitment "
                    f"was {action.deadline}, and the action is currently "
                    f"{action.status}."
                )

    # Mumbai lease
    if "mumbai" in q or "lease" in q:
        for action in actions:
            if action.id == "ACT-005":
                return (
                    "Ownership of the Mumbai office lease is unclear. "
                    "The available evidence does not confirm an owner. "
                    "Divya believes it typically sits with Facilities, "
                    "but the source material does not establish that "
                    "Facilities has been assigned the task."
                )

    # Overdue
    if "overdue" in q or "late" in q:
        overdue = [
            action for action in actions
            if action.status == "overdue"
        ]

        if not overdue:
            return "There are currently no overdue actions."

        return (
            "Overdue action:\n"
            + "\n".join(
                f"- {action.title} "
                f"(deadline: {action.deadline})"
                for action in overdue
            )
        )

    # Waiting
    if "waiting" in q:
        waiting = [
            action for action in actions
            if action.status == "waiting_on_others"
            or (
                action.owner_type == "other"
                and action.status != "completed"
            )
        ]

        if not waiting:
            return "You are not currently waiting on any incomplete action."

        return (
            "You are waiting on:\n"
            + "\n".join(
                f"- {action.title} "
                f"(owner: {action.owner})"
                for action in waiting
            )
        )

    # Today's actions
    if "today" in q:
        today = [
            action for action in actions
            if action.status == "due_today"
            or action.status == "overdue"
        ]

        if not today:
            return "There are no actions due today."

        return (
            "Actions requiring attention today:\n"
            + "\n".join(
                f"- {action.title} "
                f"({action.status})"
                for action in today
            )
        )

    return (
        "I couldn't find a direct answer in the normalized action "
        "data. Please ask about commitments, deadlines, ownership, "
        "overdue items, or actions you're waiting on."
    )


def answer_question(
    question: str,
    actions: List[Action]
) -> str:

    api_key = os.getenv("GEMINI_API_KEY")

    # No API key → local fallback
    if not api_key:
        return (
            "Gemini API key is not configured.\n\n"
            + local_answer(question, actions)
        )

    try:

        client = genai.Client(
            api_key=api_key
        )

        context = build_context(actions)

        system_instruction = """
You are an Executive Productivity Agent.

Answer the user's question using ONLY the
provided normalized action context.

Rules:

1. Never invent facts.
2. Never assign ownership when ownership is unclear.
3. Clearly state when ownership is unclear.
4. Use the provided evidence to support answers.
5. Be concise and executive-friendly.
6. Mention relevant deadlines and statuses when useful.
7. If the context does not contain enough information,
   say that the information is not available.
8. Do not use outside knowledge.
"""

        user_prompt = f"""
NORMALIZED EXECUTIVE ACTIONS:

{context}

USER QUESTION:

{question}

Answer using only the information above.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config={
                "system_instruction": system_instruction,
                "temperature": 0,
            },
        )

        if response.text:
            return response.text

        return local_answer(question, actions)

    except Exception as error:

        print(
            "\nGemini is temporarily unavailable."
            " Using local fallback..."
        )

        return local_answer(question, actions)


if __name__ == "__main__":

    from agent.resolver import resolve_actions
    from agent.status import update_statuses

    simulation_time = "2026-09-23 12:00"

    actions = resolve_actions()

    actions = update_statuses(
        actions,
        simulation_time
    )

    question = input(
        "\nAsk your Executive Productivity Agent: "
    )

    answer = answer_question(
        question,
        actions
    )

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(answer)