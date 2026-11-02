# Haven — Platform Infrastructure Assessment

Haven is a multi-tenant real estate platform.

## Domain model

```
LandlordAccount  (the billing unit)
  └── Property
        └── Tenant
              └── ScreeningReport  (SSN, credit score)

PropertyManager  (scoped to exactly one LandlordAccount)
```

A `LandlordAccount` is the billing unit — every property, every tenant, every report underneath
it rolls up to exactly one. A `PropertyManager` is scoped to exactly one `LandlordAccount` and
everything under it.

This codebase currently tags and checks access using whatever ID happened to be on hand when
each piece was written — that reflects how it was built, not a spec to replicate.

## What not to modify

`app/seed_data.py`, `app/models.py`, `fixtures/plan.json`, `terraform/terraform.tfstate` — the
assignment's checks assume this data is unchanged.

`terraform/terraform.tfstate` is checked in deliberately, not an accident — it's a seeded state
representing 4 already-provisioned landlord media buckets, standing in for a real AWS account so
B0 can be reproduced with `terraform plan` instead of just reasoned about. See `terraform/main.tf`
for how to use it.

## Where things are

| Path | Task |
|---|---|
| `terraform/main.tf` | B0 |
| `terraform/lifecycle.tf` | B1 |
| `app/access_control.py`, `scripts/cost_tag_check.py` | B2 — stubs to implement |

## Assessment evidence

- `B0.md` and `B1.md` contain the written analysis.
- `DESIGN_NOTES.md` documents the B2 idempotency key and implementation decisions.
- `TERMINAL_LOG.md` records the setup and test evidence captured during implementation.
- `.ai-conversations/` contains the captured AI-assisted implementation/review notes.

### Screen recording

**Recording link: TODO — add the URL of the required continuous, unedited recording before submission.**

The recording must begin before opening this repository and continue without cuts through
setup, README review, implementation, tests, and final Git history review. Keep the terminal
visible and narrate the README billing-unit finding before writing B2 code.
