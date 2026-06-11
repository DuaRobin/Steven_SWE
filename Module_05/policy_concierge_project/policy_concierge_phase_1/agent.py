from .tools import get_policy_status, search_policy_docs, request_renewal_quote
from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent

# Stage 1. Gather raw facts. This is your Phase 0 agent, now writing to state.
researcher = LlmAgent(
    name="researcher",
    model="gemini-2.5-flash",
    instruction=(
        "You gather facts to answer a Hartford policy question. Use your tools to "
        "look up a policy status, search the policy documents, or quote a renewal. "
        "Reply with a short bullet list of the facts you found, not prose."
    ),
    tools=[get_policy_status, search_policy_docs, request_renewal_quote],
    output_key="research_findings",
)

# Stage 2 inner loop, two agents that pass work back and forth.
drafter = LlmAgent(
    name="drafter",
    model="gemini-2.5-flash",
    instruction=(
        "Write a clear customer answer from the research findings below.\n"
        "Research findings:\n{research_findings?}\n\n"
        "If feedback on a previous draft is present, revise using it.\n"
        "Previous draft: {draft?}\n"
        "Feedback: {feedback?}"
    ),
    output_key="draft",
)

critic = LlmAgent(
    name="critic",
    model="gemini-2.5-flash",
    instruction=(
        "Review the draft below for accuracy, tone, and completeness, and reply "
        "with one or two concrete improvements.\n"
        "Draft:\n{draft?}"
    ),
    output_key="feedback",
)

# Runs the drafter and critic pair a fixed number of times, then stops. No
# early exit, so the parent pipeline always continues on to the polisher.
refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[drafter, critic],
    max_iterations=2,
)

# Stage 3. Final wording pass.
polisher = LlmAgent(
    name="polisher",
    model="gemini-2.5-flash",
    instruction=(
        "Polish the draft below into a friendly, professional final reply.\n"
        "Draft:\n{draft?}"
    ),
    output_key="final",
)

# The root agent runs the three stages in order.
root_agent = SequentialAgent(
    name="policy_concierge_phase_1",
    sub_agents=[researcher, refinement_loop, polisher],
)
