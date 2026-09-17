from typing import List, Dict

from models.schemas import Action


def deduplicate_actions(actions: List[Action]) -> List[Action]:
    """
    Merge duplicate actions that refer to the same underlying commitment.
    """

    groups: Dict[str, Action] = {}

    for action in actions:

        # For our current dataset, these are the normalized commitment keys.
        key = action.title.lower().strip()

        if key not in groups:
            groups[key] = action
            continue

        existing = groups[key]

        # Merge sources
        merged_sources = list(
            dict.fromkeys(
                existing.sources + action.sources
            )
        )

        # Merge evidence
        merged_evidence = list(
            dict.fromkeys(
                existing.evidence + action.evidence
            )
        )

        # Keep the more specific deadline if available
        deadline = existing.deadline or action.deadline

        # Keep executive ownership if one action identifies it
        owner = existing.owner or action.owner

        owner_type = existing.owner_type

        if owner_type == "unclear" and action.owner_type != "unclear":
            owner_type = action.owner_type

        # Keep stakeholder information
        stakeholder = (
            existing.stakeholder
            or action.stakeholder
        )

        groups[key] = existing.model_copy(
            update={
                "deadline": deadline,
                "owner": owner,
                "owner_type": owner_type,
                "stakeholder": stakeholder,
                "sources": merged_sources,
                "evidence": merged_evidence,
                "confidence": max(
                    existing.confidence,
                    action.confidence
                )
            }
        )

    return list(groups.values())


if __name__ == "__main__":

    from agent.resolver import resolve_actions

    actions = resolve_actions()

    print(f"Actions before deduplication: {len(actions)}")

    deduplicated = deduplicate_actions(actions)

    print(
        f"Actions after deduplication: "
        f"{len(deduplicated)}"
    )

    print("\nActions:")
    for action in deduplicated:
        print(
            f"{action.id} | "
            f"{action.title} | "
            f"{len(action.sources)} sources"
        )