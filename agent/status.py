from datetime import datetime, date
from typing import List

from models.schemas import Action


def parse_deadline(deadline: str):
    """
    Parse either:
    - YYYY-MM-DD
    - YYYY-MM-DD HH:MM
    """

    if not deadline:
        return None

    try:
        # Exact date + time
        return datetime.strptime(
            deadline,
            "%Y-%m-%d %H:%M"
        )

    except ValueError:
        try:
            # Date only
            return datetime.strptime(
                deadline,
                "%Y-%m-%d"
            )

        except ValueError:
            return None


def calculate_status(
    action: Action,
    simulation_datetime: str
) -> str:
    """
    Calculate action status using the simulated date/time.

    Completed and unclear-ownership actions retain their
    explicit status.
    """

    # These statuses should not be changed automatically.
    if action.status in [
        "completed",
        "unclear_ownership"
    ]:
        return action.status

    deadline = parse_deadline(action.deadline)

    if deadline is None:
        return action.status

    current_time = datetime.strptime(
        simulation_datetime,
        "%Y-%m-%d %H:%M"
    )

    # Exact deadline
    if " " in action.deadline:

        if deadline < current_time:
            return "overdue"

        if deadline.date() == current_time.date():
            return "due_today"

        return "upcoming"

    # Date-only deadline
    deadline_date = deadline.date()
    current_date = current_time.date()

    if deadline_date < current_date:
        return "overdue"

    if deadline_date == current_date:
        return "due_today"

    return "upcoming"


def update_statuses(
    actions: List[Action],
    simulation_datetime: str
) -> List[Action]:
    """
    Recalculate statuses for all actions.
    """

    updated_actions = []

    for action in actions:

        new_status = calculate_status(
            action,
            simulation_datetime
        )

        updated_action = action.model_copy(
            update={
                "status": new_status
            }
        )

        updated_actions.append(
            updated_action
        )

    return updated_actions


if __name__ == "__main__":

    from agent.resolver import resolve_actions

    actions = resolve_actions()

    simulation_time = "2026-09-23 12:00"

    updated_actions = update_statuses(
        actions,
        simulation_time
    )

    print(
        f"Simulation time: {simulation_time}"
    )

    print("\nACTION STATUS")
    print("-" * 60)

    for action in updated_actions:

        print(
            f"{action.id} | "
            f"{action.title} | "
            f"{action.status} | "
            f"Deadline: {action.deadline_text}"
        )