from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED_FILES = [
    "R223N_cross_sample_selection_note.md",
    "R223N_paper_print_reasoning_chain_product.md",
    "R223N_classroom_event_expansion_chain.json",
    "R223N_teacher_default_reading_draft.md",
    "R223N_teacher_default_reading_draft.html",
    "R223N_review_ledger_sample.json",
    "R223N_component_screen_evidence_trigger_map.md",
    "R223N_rubric_score.md",
    "R223N_cross_sample_validation_report.md",
    "validate_1013R_R223N_cross_sample_classroom_event_expansion.py",
    "PACKAGE_MANIFEST.json",
    "README_FOR_GPT_REVIEW.md",
]

REQUIRED_EVENT_FIELDS = [
    "event_id",
    "event_name",
    "section",
    "source_anchor",
    "teaching_responsibility",
    "student_problem",
    "task_release",
    "expected_student_responses",
    "likely_misconceptions_or_failures",
    "teacher_follow_up_questions",
    "teacher_scaffolding_moves",
    "teacher_rescue_strategy",
    "screen_trigger",
    "component_trigger",
    "learning_sheet_trigger",
    "evidence_trigger",
    "assessment_alignment",
    "transition_chain",
    "teacher_visible_note",
    "control_points",
]

CONTROL_FIELDS = ["observe", "ask_when", "rescue_when", "screen_when", "component_when", "evidence_when", "proceed_when"]
BANNED_PREVIOUS_SAMPLE_TERMS = ["文具", "智造", "代言", "赠笔礼", "毛笔", "铅笔"]


def check(condition, message, failures):
    if not condition:
        failures.append(message)


def main():
    failures = []
    check_count = 0

    for file_name in REQUIRED_FILES:
        check_count += 1
        check((ROOT / file_name).exists(), f"missing required file: {file_name}", failures)

    chain_path = ROOT / "R223N_classroom_event_expansion_chain.json"
    ledger_path = ROOT / "R223N_review_ledger_sample.json"
    teacher_path = ROOT / "R223N_teacher_default_reading_draft.md"
    rubric_path = ROOT / "R223N_rubric_score.md"
    report_path = ROOT / "R223N_cross_sample_validation_report.md"

    chain = json.loads(chain_path.read_text(encoding="utf-8"))
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    teacher = teacher_path.read_text(encoding="utf-8")
    rubric = rubric_path.read_text(encoding="utf-8")
    report = report_path.read_text(encoding="utf-8")

    check_count += 1
    check(chain.get("stage_id") == "1013R_R223N_CROSS_SAMPLE_CLASSROOM_EVENT_EXPANSION_VALIDATION", "wrong stage_id", failures)
    check_count += 1
    check(chain.get("standard_id") == "GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE", "wrong standard_id", failures)
    check_count += 1
    check(len(chain.get("events", [])) >= 7, "event count must be >= 7", failures)

    for event in chain.get("events", []):
        for field in REQUIRED_EVENT_FIELDS:
            check_count += 1
            check(field in event and event[field] not in (None, "", []), f"{event.get('event_id')} missing {field}", failures)
        for field in CONTROL_FIELDS:
            check_count += 1
            check(field in event.get("control_points", {}), f"{event.get('event_id')} missing control point {field}", failures)
        check_count += 1
        check(event["source_anchor"].get("source_status") in {"source_evidence", "system_inference_from_source"}, f"{event.get('event_id')} bad source_status", failures)
        check_count += 1
        check("trigger_condition" in event["component_trigger"], f"{event.get('event_id')} component trigger lacks condition", failures)
        check_count += 1
        check("minimum_evidence" in event["evidence_trigger"], f"{event.get('event_id')} evidence lacks minimum", failures)

    check_count += 1
    check(len(ledger.get("entries", [])) == len(chain.get("events", [])), "ledger entries must match events", failures)
    for entry in ledger.get("entries", []):
        rv = entry.get("review_view_only", {})
        for field in ["xiaojiao_judgement_full", "control_points_full", "screen_trigger", "component_trigger", "learning_sheet_trigger", "evidence_trigger"]:
            check_count += 1
            check(field in rv, f"ledger {entry.get('event_id')} missing {field}", failures)

    check_count += 1
    check(teacher.count("【本环节在做什么】") >= 7, "teacher draft lacks event purpose notes", failures)
    check_count += 1
    check(teacher.count("【教师关注】") >= 7, "teacher draft lacks teacher focus notes", failures)
    check_count += 1
    check(teacher.count("【下游影响】") >= 7, "teacher draft lacks downstream notes", failures)
    check_count += 1
    check("【小教判断】" not in teacher, "teacher default should not expose full xiaojiao judgement", failures)
    check_count += 1
    check("完整控制点" not in teacher, "teacher default should not expose full control ledger", failures)

    scanned = teacher + "\n" + json.dumps(chain, ensure_ascii=False)
    for term in BANNED_PREVIOUS_SAMPLE_TERMS:
        check_count += 1
        check(term not in scanned, f"previous sample term leaked into teacher/event product: {term}", failures)

    check_count += 1
    score_match = re.search(r"score=(\d+)/25", rubric)
    check(score_match is not None, "rubric score missing", failures)
    score = int(score_match.group(1)) if score_match else 0
    check_count += 1
    check(score >= 20, "rubric score below pass line", failures)
    check_count += 1
    check("23/25" in rubric and "23/25" in report, "expected 23/25 migration score not recorded", failures)

    boundary = chain.get("boundary", {})
    for key in ["r97b_modified", "ui_modified", "runtime_connected", "provider_model_connected", "database_written", "formal_apply_allowed"]:
        check_count += 1
        check(boundary.get(key) is False, f"boundary must keep {key}=false", failures)

    result = {
        "passed": not failures,
        "check_count": check_count,
        "failed": len(failures),
        "failures": failures,
        "event_count": len(chain.get("events", [])),
        "rubric_score": score,
    }
    (ROOT / "validate_1013R_R223N_cross_sample_classroom_event_expansion_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
