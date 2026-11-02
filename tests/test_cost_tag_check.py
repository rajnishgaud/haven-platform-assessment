import json
from pathlib import Path

from scripts.cost_tag_check import REQUIRED_TAG, evaluate_plan, check_plan


def test_plan_flags_all_resources_missing_billing_tag(capsys):
    plan_path = Path(__file__).parents[1] / "fixtures" / "plan.json"
    assert check_plan(str(plan_path)) == 1
    output = capsys.readouterr().out
    assert "aws_s3_bucket.listing_media" in output
    assert "aws_lambda_function.mls_feed_sync" in output
    assert "aws_s3_bucket.landlord_media[0]" not in output
    assert "aws_lambda_function.screening_report_export" not in output


def test_repeated_runs_are_identical_and_do_not_duplicate_findings(tmp_path, capsys):
    plan = {"resource_changes": [
        {"address": "aws_s3_bucket.example", "change": {
            "actions": ["create"], "after": {"tags": {"tenant_id": "ten-1"}}
        }}
    ]}
    path = tmp_path / "plan.json"
    path.write_text(json.dumps(plan), encoding="utf-8")

    first_code = check_plan(str(path))
    first_output = capsys.readouterr().out
    second_code = check_plan(str(path))
    second_output = capsys.readouterr().out

    assert first_code == second_code == 1
    assert first_output == second_output
    assert first_output.count("aws_s3_bucket.example") == 1


def test_noop_and_read_changes_are_skipped():
    plan = {"resource_changes": [
        {"address": "aws_x.noop", "change": {"actions": ["no-op"], "after": {}}},
        {"address": "aws_x.read", "change": {"actions": ["read"], "after": {}}},
    ]}
    assert evaluate_plan(plan) == []


def test_generic_resource_type_is_checked():
    plan = {"resource_changes": [
        {"address": "random_resource.example", "change": {
            "actions": ["update"], "after": {"tags": {REQUIRED_TAG: "la-9"}}
        }}
    ]}
    assert evaluate_plan(plan) == []
