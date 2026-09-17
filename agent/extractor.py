import json
from pathlib import Path
from typing import List, Dict, Any


DATA_PATH = Path(__file__).parent.parent / "data" / "source_data.json"


def load_data() -> Dict[str, Any]:
    """Load the supplied assignment data."""

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_meeting_actions(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract statements from the meeting transcript that may
    represent commitments, delegated tasks, or ownership issues.
    """

    actions = []

    for meeting in data.get("meetings", []):

        for item in meeting.get("transcript", []):

            speaker = item["speaker"]
            text = item["text"]

            # Statements made by Arjun are especially important
            # because Arjun is the executive user.
            if speaker == "Arjun Malhotra":

                actions.append({
                    "source": "meeting",
                    "source_id": meeting["id"],
                    "date": meeting["date"],
                    "speaker": speaker,
                    "text": text
                })

    return actions


def extract_email_actions(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract all email messages as candidate action evidence."""

    actions = []

    for thread in data.get("emails", []):

        for message in thread.get("messages", []):

            actions.append({
                "source": "email",
                "source_id": thread["thread_id"],
                "subject": thread["subject"],
                "date": message["date"],
                "time": message["time"],
                "from": message["from"],
                "to": message["to"],
                "text": message["text"]
            })

    return actions


def extract_voice_actions(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract Arjun's personal voice notes."""

    actions = []

    for note in data.get("voice_notes", []):

        actions.append({
            "source": "voice_note",
            "source_id": note["id"],
            "date": note["date"],
            "time": note["time"],
            "speaker": note["speaker"],
            "text": note["text"]
        })

    return actions


def extract_calendar_events(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract Arjun's calendar events."""

    events = []

    calendars = data.get("calendars", {})

    for event in calendars.get("Arjun Malhotra", []):

        events.append({
            "source": "calendar",
            "date": event["date"],
            "start": event["start"],
            "end": event["end"],
            "event": event["event"]
        })

    return events


def extract_all_sources(data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Extract all source categories."""

    return {
        "meeting_actions": extract_meeting_actions(data),
        "email_actions": extract_email_actions(data),
        "voice_actions": extract_voice_actions(data),
        "calendar_events": extract_calendar_events(data)
    }


if __name__ == "__main__":

    data = load_data()

    extracted = extract_all_sources(data)

    for source, items in extracted.items():

        print(f"\n{'=' * 50}")
        print(f"{source.upper()}")
        print(f"{'=' * 50}")

        print(f"Items found: {len(items)}")

        for item in items[:3]:
            print(item)