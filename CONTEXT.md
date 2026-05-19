# VigoTech ADK Workshop

A 75-minute hands-on introduction to Google ADK for the Python Vigo / VigoTech meetup, built around an assistant that answers questions about real local tech events.

## Language

**Workshop**:
The 75-minute session attendees join in person. Hands-on, follow-along format.

**Attendee**:
A workshop participant who runs the code on their own laptop. Expected count: 10-12, mixed Python experience, mostly new to ADK.
_Avoid_: User (ambiguous with "person asking the agent a question").

**End user**:
The person typing questions into the agent during the demo — in practice an **Attendee** wearing a different hat.
_Avoid_: User.

**Agent**:
An ADK `LlmAgent` — the unit of `model + instruction + tools`. The workshop's central mental model.

**VigoTech Events Assistant**:
The specific agent built across the three workshop steps. Themed instruction, one tool, multilingual (castellano / gallego / inglés).

**Step**:
One of three progressive examples (`01_basic_agent`, `02_tools`, `03_structured_output`). Each is its own directory containing an `agent.py` that exports `root_agent` for `adk web`.

**Tool**:
A Python function exposed to the agent — here, exactly one: `get_vigotech_events(topic, days_ahead)`.

**Event**:
An upcoming meetup hosted by a VigoTech alliance member. Pydantic shape: `title`, `date` (datetime), `location`, `url`, `group`.

**Group**:
A VigoTech alliance member organisation (e.g. "A Industriosa", "Agile Vigo"). Each group hosts at most one upcoming **Event** in the source data.

**Active group**:
A **Group** not marked `inactive: true` in the source JSON. Only active groups contribute events.

**EventRecommendation**:
The structured output schema returned by step 03 — one recommended **Event** with `reason` and `level` (`junior` | `senior` | `any`).

**Structurer agent**:
The second sub-agent in step 03's `SequentialAgent`. Reads events from state, outputs an **EventRecommendation**. Has no tools (ADK constraint: `output_schema` disables tool calling).

**Hallucination reveal**:
The rhetorical moment in step 01 where the toolless agent invents plausible-sounding events that don't exist, motivating the tool addition in step 02. The workshop's highest-leverage teaching moment.

## Relationships

- A **Group** hosts zero or one upcoming **Event**.
- An **Agent** uses zero or more **Tools** (step 01: zero, steps 02 and 03's fetcher: one).
- Step 03's pipeline is a `SequentialAgent` of two sub-**Agents**: fetcher (tool) → structurer (`output_schema`).
- The **Structurer agent** cannot have **Tools** — see [ADR-0001](./docs/adr/0001-sequential-agent-for-structured-output.md).

## Example dialogue

> **Speaker (step 01):** "OK, ask the agent what Python events are happening this week in Vigo."
> **Attendee:** "It just gave me three events that look real."
> **Speaker:** "Search for them. They don't exist. The **Agent** has no **Tool** — it's just guessing from training data. That's the **hallucination reveal**. In step 02 we give it a real **Tool** and the same question gets a real answer."

## Flagged ambiguities

- "user" was used to mean both **Attendee** (workshop participant) and **End user** (the person typing into the agent UI) — resolved: prefer **Attendee** for workshop logistics, **End user** only when distinguishing roles matters.
- The plan's "ideal event format" included a `description` field — the source JSON has no such field. Resolved: dropped `description`, added `group` as the synthesized context field instead.
- "multi-agent" appears in the plan's NO-list but step 03 uses a 2-agent `SequentialAgent`. Resolved: the constraint was about avoiding *enterprise* multi-agent complexity, not minimal composition. See [ADR-0001](./docs/adr/0001-sequential-agent-for-structured-output.md).
