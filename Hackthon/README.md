---
title: Smart Customer Support
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "latest"
dockerfile: Dockerfile
pinned: false
---
# Customer Support OpenEnv

## Environment Overview & Motivation
This environment provides a real-world simulation of a customer support agent. Agents are required to triage incoming customer tickets, classify them into appropriate semantic categories, draft a helpful conversational response, and successfully close the tickets.

This fulfills real-world, non-gaming constraints required by the Meta OpenEnv Hackathon.

## Observation Space
The observation space is defined cleanly as a Pydantic Model (`Observation`) which contains:
- `open_tickets`: A list of currently open `Ticket` objects (containing ID, message, category, response, and status).
- `last_action_result`: Textual feedback on the last action taken by the agent.

## Action Space
The action space is a strongly typed Pydantic Model (`Action`) which specifies:
- `action_type`: One of `"classify"`, `"respond"`, `"close"`, or `"wait"`.
- `ticket_id`: The target ticket ID.
- `text_content`: Text representing either the category name or the response content, depending on the `action_type`.

## Reward Function
Rewards are given for incremental progress to prevent sparse rewards and to encourage optimal stepwise behavior:
- Correct classification: `+0.2`
- Meaningful response drafted: `+0.3`
- Successfully closing a handled ticket: `+0.5`
- Penalties (`-0.1` to `-0.2`) are given for destructive actions, out-of-order steps (e.g., responding before categorizing), and infinite loops. This pushes agents towards effective planning.

## Tasks
1. **Easy Task**: 1 ticket focused on simple login issues.
2. **Medium Task**: 2 tickets focused on billing and account management.
3. **Hard Task**: 3 tickets spanning technical, billing, and complex sales inquiries.

Each uses an isolated Agent Grader `evaluate(env)` producing a deterministic score mapped between 0.0 and 1.0.

## Setup & Usage Instructions
1. Install requirements:
   ```bash
   pip install -r requirements.txt