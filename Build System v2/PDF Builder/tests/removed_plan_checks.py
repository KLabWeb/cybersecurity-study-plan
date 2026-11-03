"""The plan-content checks removed from the tests, with their helpers and their data tables."""

REMOVED_TESTS = (
    "test_claim_dates", "test_claim_durations", "test_claim_languages", "test_claim_references",
    "test_claim_resources", "test_claim_summary", "test_claim_writeups", "test_concept_order",
    "test_no_mentor", "test_phase_material", "test_phase_timeline", "test_phase_weeks",
    "test_plan_mechanics", "test_plan_months", "test_plan_steps", "test_plan_structure",
    "test_resource_lists", "test_step_duplicates", "test_step_setups", "test_timeline_prose",
    "test_tool_prerequisites", "test_uniformity",
)
REMOVED_HELPERS = ("plan_data", "plan_sections")
REMOVED_DATA = ("step_actions", "tool_prerequisites", "resource_topics")
