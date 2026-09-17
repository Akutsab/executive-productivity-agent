from typing import List

from models.schemas import Action


def generate_brief(actions: List[Action]) -> str:
    """
    Generate a concise executive productivity brief
    from normalized actions.
    """

    overdue = [
        action
        for action in actions
        if action.status == "overdue"
    ]

    due_today = [
        action
        for action in actions
        if action.status == "due_today"
    ]

    waiting = [
        action
        for action in actions
        if action.status == "waiting_on_others"
        or (
            action.owner_type == "other"
            and action.status != "completed"
        )
    ]

    unclear = [
        action
        for action in actions
        if action.status == "unclear_ownership"
    ]

    upcoming = [
        action
        for action in actions
        if action.status == "upcoming"
    ]

    lines = []

    lines.append("DAILY EXECUTIVE BRIEF")
    lines.append("=" * 60)

    # Overdue
    lines.append("\n🔴 OVERDUE")

    if overdue:
        for action in overdue:
            stakeholder = (
                f" → {action.stakeholder}"
                if action.stakeholder
                else ""
            )

            deadline = (
                action.deadline_text
                or action.deadline
            )

            lines.append(
                f"- {action.title}"
                f"{stakeholder}"
                f" | Deadline: {deadline}"
            )
    else:
        lines.append("- None")

    # Due today
    lines.append("\n🟡 DUE TODAY")

    if due_today:
        for action in due_today:
            stakeholder = (
                f" → {action.stakeholder}"
                if action.stakeholder
                else ""
            )

            deadline = (
                action.deadline_text
                or action.deadline
            )

            lines.append(
                f"- {action.title}"
                f"{stakeholder}"
                f" | Deadline: {deadline}"
            )
    else:
        lines.append("- None")

    # Waiting on others
    lines.append("\n🔵 WAITING ON OTHERS")

    if waiting:
        for action in waiting:
            lines.append(
                f"- {action.title}"
                f" | Owner: {action.owner or 'Unknown'}"
            )
    else:
        lines.append("- None")

    # Unclear ownership
    lines.append("\n⚠️ UNCLEAR OWNERSHIP")

    if unclear:
        for action in unclear:
            deadline = (
                action.deadline_text
                or action.deadline
            )

            lines.append(
                f"- {action.title}"
                f" | Deadline: {deadline}"
            )
    else:
        lines.append("- None")

    # Upcoming
    lines.append("\n🟢 UPCOMING")

    if upcoming:
        for action in upcoming:
            deadline = (
                action.deadline_text
                or action.deadline
            )

            lines.append(
                f"- {action.title}"
                f" | Deadline: {deadline}"
            )
    else:
        lines.append("- None")

    return "\n".join(lines)


if __name__ == "__main__":

    from agent.resolver import resolve_actions
    from agent.status import update_statuses

    simulation_time = "2026-09-23 12:00"

    actions = resolve_actions()

    actions = update_statuses(
        actions,
        simulation_time
    )

    brief = generate_brief(actions)

    print(brief)