import streamlit as st
from datetime import datetime

from agent.resolver import resolve_actions
from agent.status import update_statuses
from agent.deduplicator import deduplicate_actions
from agent.brief import generate_brief
from agent.qa import answer_question


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Executive Productivity Agent",
    page_icon="🎯",
    layout="wide"
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🎯 Executive Productivity Agent")

st.caption(
    "AI-powered commitment, deadline and ownership tracking "
    "for Arjun Malhotra — VP Sales"
)


# ---------------------------------------------------------
# SIMULATION CONTROL
# ---------------------------------------------------------

st.sidebar.header("⚙️ Simulation")

simulation_date = st.sidebar.date_input(
    "Simulation date",
    value=datetime(2026, 9, 23).date()
)

simulation_time = st.sidebar.time_input(
    "Simulation time",
    value=datetime(2026, 9, 23, 12, 0).time()
)

simulation_datetime = (
    f"{simulation_date} {simulation_time.strftime('%H:%M')}"
)


# ---------------------------------------------------------
# LOAD + PROCESS DATA
# ---------------------------------------------------------

actions = resolve_actions()

actions = deduplicate_actions(actions)

actions = update_statuses(
    actions,
    simulation_datetime
)


# ---------------------------------------------------------
# CALCULATE DASHBOARD METRICS
# ---------------------------------------------------------

overdue = [
    action for action in actions
    if action.status == "overdue"
]

due_today = [
    action for action in actions
    if action.status == "due_today"
]

waiting = [
    action for action in actions
    if action.status == "waiting_on_others"
    or (
        action.owner_type == "other"
        and action.status != "completed"
    )
]

unclear = [
    action for action in actions
    if action.status == "unclear_ownership"
]

upcoming = [
    action for action in actions
    if action.status == "upcoming"
]


# ---------------------------------------------------------
# METRIC CARDS
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔴 Overdue",
        len(overdue)
    )

with col2:
    st.metric(
        "🟡 Due Today",
        len(due_today)
    )

with col3:
    st.metric(
        "🔵 Waiting",
        len(waiting)
    )

with col4:
    st.metric(
        "⚠️ Unclear Ownership",
        len(unclear)
    )


st.divider()


# ---------------------------------------------------------
# DAILY BRIEF
# ---------------------------------------------------------

st.subheader("📋 Daily Executive Brief")

brief = generate_brief(actions)

st.code(
    brief,
    language="text"
)


# ---------------------------------------------------------
# ACTION TABLE
# ---------------------------------------------------------

st.subheader("📌 All Executive Actions")

for action in actions:

    if action.status == "overdue":
        icon = "🔴"

    elif action.status == "due_today":
        icon = "🟡"

    elif action.status == "unclear_ownership":
        icon = "⚠️"

    elif action.status == "completed":
        icon = "✅"

    else:
        icon = "🟢"

    with st.expander(
        f"{icon} {action.title}"
    ):

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Owner:** "
                f"{action.owner or 'Unclear'}"
            )

            st.write(
                f"**Stakeholder:** "
                f"{action.stakeholder or 'None'}"
            )

            st.write(
                f"**Deadline:** "
                f"{action.deadline or 'Not specified'}"
            )

        with col2:

            st.write(
                f"**Status:** "
                f"{action.status}"
            )

            st.write(
                f"**Priority:** "
                f"{action.priority}"
            )

            st.write(
                f"**Confidence:** "
                f"{action.confidence:.0%}"
            )

        st.write(
            f"**Description:** {action.description}"
        )

        st.write("**Sources:**")

        for source in action.sources:
            st.write(f"- {source}")

        st.write("**Evidence:**")

        for evidence in action.evidence:
            st.write(f"> {evidence}")


st.divider()


# ---------------------------------------------------------
# Q&A
# ---------------------------------------------------------

st.subheader("🤖 Ask Your Executive Agent")

question = st.text_input(
    "Ask a question about your commitments:",
    placeholder="e.g. What did I promise Raghav?"
)

if st.button("Ask Agent", type="primary"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Analyzing your executive commitments..."
        ):

            answer = answer_question(
                question,
                actions
            )

        st.markdown("### 💬 Answer")

        st.info(answer)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Data source: AIONOS Executive Productivity Agent "
    "Assignment 1 simulated data pack. "
    "No external data is used."
)