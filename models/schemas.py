from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class Action(BaseModel):
    """
    Represents one normalized executive action.
    """

    id: str
    title: str

    owner: Optional[str] = None

    owner_type: Literal[
        "executive",
        "other",
        "unclear"
    ]

    stakeholder: Optional[str] = None

    # Normalized date/time when known.
    deadline: Optional[str] = None

    # Original wording from the source.
    deadline_text: Optional[str] = None

    status: Literal[
        "upcoming",
        "due_today",
        "overdue",
        "completed",
        "waiting_on_others",
        "unclear_ownership"
    ]

    priority: Literal[
        "high",
        "medium",
        "low"
    ] = "medium"

    description: str = ""

    sources: List[str] = Field(
        default_factory=list
    )

    evidence: List[str] = Field(
        default_factory=list
    )

    confidence: float = 1.0