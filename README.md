# 🎯 Executive Productivity Agent

An AI-powered executive productivity agent that identifies commitments, tracks deadlines, detects ownership gaps, removes duplicate actions, generates daily executive briefs, and answers natural-language questions using grounded evidence.

## 📌 Assignment

**AIONOS Internship Selection — Assignment 1: Executive Productivity Agent**

The agent is designed to help an executive stay on top of commitments across meetings, emails, voice notes, and calendar information.

---

## 🚀 Features

- 📌 **Commitment Extraction**
  - Identifies executive actions from supplied communication data.
  - Tracks who owns each action.

- ⏰ **Deadline Tracking**
  - Identifies upcoming, due-today, overdue, and completed actions.
  - Preserves the original deadline wording when an exact time is not available.

- 👤 **Ownership Detection**
  - Separates executive-owned actions from actions owned by others.
  - Flags unclear ownership instead of making assumptions.

- ♻️ **Deduplication**
  - Combines repeated references to the same executive action across different sources.

- 📝 **Daily Executive Brief**
  - Summarizes:
    - Overdue actions
    - Actions due today
    - Waiting on others
    - Unclear ownership
    - Upcoming actions

- 🤖 **Natural-Language Q&A**
  - Ask questions such as:
    - "What did I promise Raghav?"
    - "What needs action today?"
    - "What is waiting on others?"
    - "Who owns the Mumbai lease?"

- 🔎 **Evidence & Source Traceability**
  - Each action maintains its supporting sources and evidence.

- 🕐 **Simulation Mode**
  - The assignment's simulated dates can be selected through the Streamlit interface to demonstrate how action status changes over time.

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │   Supplied Data Pack │
                    │                      │
                    │ • Meetings           │
                    │ • Emails             │
                    │ • Voice Notes        │
                    │ • Calendar           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Extractor       │
                    │                      │
                    │ Extract structured   │
                    │ source information   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Resolver       │
                    │                      │
                    │ Normalize executive │
                    │ actions & ownership  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Deduplicator      │
                    │                      │
                    │ Merge repeated       │
                    │ actions and evidence │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Status Engine     │
                    │                      │
                    │ Upcoming / Due Today │
                    │ Overdue / Completed  │
                    │ Ownership flags      │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
        ┌──────────────────┐       ┌──────────────────┐
        │ Daily Brief      │       │ Q&A Agent        │
        │                  │       │                  │
        │ Executive        │       │ Grounded natural │
        │ summary          │       │ language answers │
        └────────┬─────────┘       └────────┬─────────┘
                 │                          │
                 └────────────┬─────────────┘
                              ▼
                    ┌──────────────────────┐
                    │   Streamlit UI       │
                    │                      │
                    │ Dashboard + Q&A      │
                    └──────────────────────┘