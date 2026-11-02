# Design Notes

## B2 — idempotency key

The cost-tag check is deliberately stateless: it does not persist a "processed plan" marker or
modify the plan. Its deterministic finding identity (the idempotency key) is the tuple
`(resource_changes[].address, "landlord_account_id")`. Findings are held in a set and emitted
in sorted order. Thus the same unchanged plan produces the same findings, output, and exit
code on every run, with duplicate findings for the same resource/tag pair collapsed.

The plan file path, wall-clock time, run ID, and tenant ID are not used as the idempotency key.
The landlord account ID is the tag value being validated, not the identity of the finding.

## Any other decision with a non-obvious alternative

- **Authorization boundary:** resolve `report -> tenant -> property -> landlord_account_id`
  and compare that account ID with the manager's account ID. I chose this over comparing
  `tenant_id` or trusting a report-supplied account field because the README defines the
  landlord account as the ownership boundary and the report has no landlord field. Missing or
  ambiguous tenant/property relationships fail closed.
- **Plan validation scope:** validate every resource change with a non-null proposed
  after-state, regardless of Terraform resource type. This avoids a brittle allowlist of
  resource types. Pure no-op/read and pure-delete actions are skipped; replacement changes
  are checked because they include a create and proposed after-state. This assumes resources
  in this policy's managed scope are expected to support tags. If the platform later includes
  intentionally untaggable resources, add an explicit, reviewed exemption policy rather than
  silently skipping missing `tags`.
- **Terraform identity:** use `for_each` keyed by landlord account ID rather than `count` so
  removal of one account does not shift the addresses of other accounts. Existing count-based
  state requires explicit address migration.
- **Glacier policy:** do not archive objects while they are still in the deletion-request
  eligibility window. A later transition reduces early-delete exposure but cannot eliminate
  it if requests may arrive at any later time.
