import json

from graph.state import APProcessState
from graph.models import ComponentDetection
from utils.gemini_client import call_gemini_structured
from utils import roi_math


COMPONENT_SYSTEM_PROMPT = """You are an RPA Solution Architect. Your ONLY job is to CLASSIFY which technical
automation components a project needs — not to price them. Pricing is done deterministically in code.

For the given priority/scored steps, decide which of these components are required and how many of each:
- ui_automation: driving web/desktop apps through their UI (count = number of DISTINCT apps automated this way)
- api_integration: REST/SOAP/DB integrations (count = number of distinct integrations)
- structured_data: reading/writing Excel/CSV/structured files
- ocr_idp: OCR / Intelligent Document Processing for invoices, PDFs, scanned docs
- business_rules: a decision/rules engine (matching tolerances, approval thresholds, GL coding)
- exception_handling: exception detection, routing and escalation logic
- orchestration: scheduling/queue orchestration across bots
- hitl: human-in-the-loop review/approval steps

Also estimate num_bots: how many distinct production bots/automations will run.
Only include components that are genuinely justified by the steps. Provide a short rationale referencing the step(s) for each."""


def calculate_roi_node(state: APProcessState) -> dict:
    """Node: Deterministic, grounded ROI projection.

    The LLM only classifies the technical components (its strength). All money,
    time, FTE and payback math is computed in utils.roi_math so the same inputs
    always yield the same ROI — fully reproducible and defensible.
    """
    scored_steps = state.get("scored_steps", [])
    opportunities = state.get("opportunities", [])
    discovery_facts = state.get("discovery_facts", {}) or {}
    fallback_rate = state.get("hourly_rate")

    # ---- Step 1: LLM classifies technical components (no pricing) ------------
    prompt = f"""Classify the technical automation components required for these AP steps.

Priority / scored steps:
{json.dumps(scored_steps, indent=2)}

Return the components list (with counts + rationale) and num_bots. Do NOT estimate any costs — only classify."""

    try:
        detection = call_gemini_structured(
            prompt,
            system_prompt=COMPONENT_SYSTEM_PROMPT,
            response_schema=ComponentDetection,
        )
    except Exception:
        detection = {}

    components = (detection or {}).get("components") or []
    num_bots = (detection or {}).get("num_bots") or 1

    # Safety net: if the model returned nothing usable, infer a minimal footprint
    # from the systems present so cost is never zero.
    if not components:
        systems = set()
        for s in scored_steps:
            for sys_name in s.get("systems_used", []) or []:
                systems.add(sys_name)
        components = [
            {"component": "ui_automation", "count": max(1, len(systems)),
             "rationale": "Inferred from the systems used across the process steps."},
            {"component": "business_rules", "count": 1, "rationale": "Matching/approval logic."},
            {"component": "exception_handling", "count": 1, "rationale": "Exception routing."},
        ]

    # ---- Step 2: deterministic cost model -----------------------------------
    implementation_cost, annual_maintenance_cost, cost_breakdown = roi_math.compute_costs(
        components, num_bots
    )

    # ---- Step 3: deterministic, grounded ROI/FTE ----------------------------
    roi_estimate = roi_math.compute_roi(
        scored_steps=scored_steps,
        opportunities=opportunities,
        discovery_facts=discovery_facts,
        implementation_cost=implementation_cost,
        annual_maintenance_cost=annual_maintenance_cost,
        cost_breakdown=cost_breakdown,
        fallback_hourly_rate=fallback_rate,
    )
    roi_estimate["rpa_platform_detected"] = (detection or {}).get("rpa_platform_detected")
    roi_estimate["num_bots"] = num_bots
    roi_estimate["detected_components"] = components

    return {"roi_estimate": roi_estimate}
