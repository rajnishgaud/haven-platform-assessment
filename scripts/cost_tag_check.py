"""
B2, part 2 — deterministic Terraform plan cost-tag policy check.

Every changed resource with a proposed after-state must carry the billing-unit
tag `landlord_account_id`. Findings are keyed by (resource address, required tag),
deduplicated, and emitted in sorted order so identical plans produce identical
exit codes and output.
"""
import json
import sys

REQUIRED_TAG = "landlord_account_id"


def evaluate_plan(plan: dict) -> list[str]:
    findings = set()
    for resource in plan.get("resource_changes", []):
        change = resource.get("change") or {}
        actions = change.get("actions") or []
        # A no-op/read has no infrastructure mutation to validate. A pure delete
        # has no after-state; create/update/replacement after-states are checked.
        if not actions or all(action in {"no-op", "read", "delete"} for action in actions):
            continue
        after = change.get("after")
        if after is None:
            continue
        tags = after.get("tags") if isinstance(after, dict) else None
        if not isinstance(tags, dict) or not tags.get(REQUIRED_TAG):
            address = resource.get("address", "<unknown-address>")
            findings.add((address, REQUIRED_TAG))
    return [f"{address}: missing required tag '{tag}'"
            for address, tag in sorted(findings)]


def check_plan(plan_path: str) -> int:
    try:
        with open(plan_path, encoding="utf-8") as plan_file:
            plan = json.load(plan_file)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Unable to read Terraform plan '{plan_path}': {exc}", file=sys.stderr)
        return 2

    findings = evaluate_plan(plan)
    if findings:
        for finding in findings:
            print(finding)
        return 1
    print(f"All changed resources have the required '{REQUIRED_TAG}' tag.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <terraform-plan.json>", file=sys.stderr)
        sys.exit(2)
    sys.exit(check_plan(sys.argv[1]))
