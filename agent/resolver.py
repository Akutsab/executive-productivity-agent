from typing import List

from models.schemas import Action


EXECUTIVE = "Arjun Malhotra"


def create_base_actions() -> List[Action]:
    """
    Create normalized executive actions from the supplied
    AIONOS dataset.

    Only information supported by the provided source data
    is included. Original deadline wording is preserved in
    deadline_text when the source does not provide an exact time.
    """

    actions = [

        # -------------------------------------------------
        # ACT-001: Vendor List
        # -------------------------------------------------

        Action(
            id="ACT-001",
            title="Send updated vendor list",
            owner=EXECUTIVE,
            owner_type="executive",
            stakeholder="Raghav Sethi",

            # Source says "Wednesday morning", not an exact time.
            deadline="2026-09-23",
            deadline_text="Wednesday morning",

            status="overdue",
            priority="high",

            description=(
                "Send the updated vendor list to Raghav."
            ),

            sources=[
                "Leadership Sync",
                "Vendor List Email Thread",
                "Voice Note 1"
            ],

            evidence=[
                "I told Raghav I'd send him the updated vendor list.",
                "will send by tomorrow (Wednesday) morning for sure.",
                "need to get Raghav that vendor list"
            ],

            confidence=1.0
        ),


        # -------------------------------------------------
        # ACT-002: Q3 Campaign Deck
        # -------------------------------------------------

        Action(
            id="ACT-002",
            title="Review Q3 campaign deck",
            owner=EXECUTIVE,
            owner_type="executive",
            stakeholder="Neha Kapoor",

            # Exact time is explicitly confirmed in the email.
            deadline="2026-09-24 09:30",
            deadline_text="Thursday 9:30 AM",

            status="upcoming",
            priority="high",

            description=(
                "Review the Q3 campaign deck prepared by Neha."
            ),

            sources=[
                "Leadership Sync",
                "Q3 Campaign Deck Email Thread",
                "Arjun Calendar",
                "Neha Calendar"
            ],

            evidence=[
                "I'll send it to Arjun for review by Wednesday.",
                "shifting the review to Thursday morning instead of Wednesday",
                "Thursday morning works.",
                "Let's say 9:30 AM Thursday.",
                "Deck Review with Arjun"
            ],

            confidence=1.0
        ),


        # -------------------------------------------------
        # ACT-003: Meridian Logistics Call
        # -------------------------------------------------

        Action(
            id="ACT-003",
            title="Confirm Meridian Logistics call",
            owner=EXECUTIVE,
            owner_type="executive",
            stakeholder="Priya Nair",

            # Exact time explicitly confirmed.
            deadline="2026-09-23 15:00",
            deadline_text="Wednesday 3:00 PM",

            status="completed",
            priority="high",

            description=(
                "Confirm the new meeting time with Priya "
                "from Meridian Logistics."
            ),

            sources=[
                "Leadership Sync",
                "Call Reschedule Email Thread",
                "Voice Note 2",
                "Arjun Calendar"
            ],

            evidence=[
                "I need to reconfirm the new time with their team myself.",
                "how about Wednesday 3:00 PM?",
                "Wednesday 3 PM works on our end, confirmed.",
                "Yes, confirmed, see you at 3."
            ],

            confidence=1.0
        ),


        # -------------------------------------------------
        # ACT-004: Expense Variance Report
        # -------------------------------------------------

        Action(
            id="ACT-004",
            title="Receive July expense variance report",
            owner="Divya Rao",
            owner_type="other",
            stakeholder=EXECUTIVE,

            # Source says "Wednesday evening", not an exact time.
            deadline="2026-09-23",
            deadline_text="Wednesday evening",

            status="completed",
            priority="medium",

            description=(
                "Receive the July expense variance report "
                "from Divya before board preparation."
            ),

            sources=[
                "Leadership Sync",
                "Expense Variance Report Email Thread",
                "Voice Note 2"
            ],

            evidence=[
                "Divya, can you also pull the July expense variance report",
                "I'll have it ready Wednesday evening.",
                "Wednesday evening is tight but doable, I'll prioritize it.",
                "Report attached, sent as promised."
            ],

            confidence=1.0
        ),


        # -------------------------------------------------
        # ACT-005: Mumbai Office Lease
        # -------------------------------------------------

        Action(
            id="ACT-005",
            title="Resolve Mumbai office lease ownership",
            owner=None,
            owner_type="unclear",
            stakeholder=None,

            # Source explicitly says Friday EOD.
            deadline="2026-09-25",
            deadline_text="Friday EOD",

            status="unclear_ownership",
            priority="high",

            description=(
                "Identify who is responsible for signing off "
                "the Mumbai office lease renewal."
            ),

            sources=[
                "Leadership Sync",
                "Mumbai Office Lease Renewal Email Thread",
                "Voice Note 1"
            ],

            evidence=[
                "Not sure whose desk that's on right now.",
                "I think that's supposed to be Facilities, but I haven't seen anyone pick it up.",
                "Okay, flag it, don't assume.",
                "Don't think it's been assigned.",
                "Not on my end - I believe this typically sits with Facilities directly, not us.",
                "still unowned - can you confirm who's handling it?"
            ],

            confidence=1.0
        )
    ]

    return actions


def resolve_actions() -> List[Action]:
    """
    Return the normalized executive action set.
    """

    return create_base_actions()


def print_actions(actions: List[Action]) -> None:
    """
    Display normalized actions in a readable format.
    """

    for action in actions:

        print("\n" + "=" * 60)

        print(f"ID:          {action.id}")
        print(f"Title:       {action.title}")
        print(f"Owner:       {action.owner}")
        print(f"Owner Type:  {action.owner_type}")
        print(f"Stakeholder: {action.stakeholder}")
        print(f"Deadline:    {action.deadline}")
        print(f"Deadline Text:{action.deadline_text}")
        print(f"Status:      {action.status}")
        print(f"Priority:    {action.priority}")
        print(f"Confidence:  {action.confidence}")

        print(
            f"Sources:     {', '.join(action.sources)}"
        )

        print("Evidence:")

        for evidence in action.evidence:
            print(f"  - {evidence}")


if __name__ == "__main__":

    actions = resolve_actions()

    print(
        f"\nResolved actions: {len(actions)}"
    )

    print_actions(actions)