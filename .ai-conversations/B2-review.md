# B2 AI-assisted work log

This file records the actual implementation prompt and a concrete first-draft error caught by
running the supplied tests. The seed data and models were not edited.

## Prompt/context supplied

> Implement B2: a Property Manager may view screening reports only for tenants under their own
> landlord account; prove cross-account denial and same-account allowance. Implement a generic
> cost-tag check requiring `landlord_account_id`, not `tenant_id`, and make repeated checks on an
> unchanged plan deterministic. Read the README first and do not modify seed data.

## README finding used before implementation

The README says `LandlordAccount` is the billing unit and that a PropertyManager is scoped to
exactly one LandlordAccount. The report hierarchy is report -> tenant -> property -> landlord
account. Therefore authorization must resolve that hierarchy and compare landlord account IDs;
the billing-tag policy must require `landlord_account_id`, not `tenant_id`.

## First-draft error and correction

The first authorization draft made an incorrect comparison between
`actor.landlord_account_id` and `tenant.id`. That mixes identifiers from different domain
entities and incorrectly denies a legitimate same-account request.

The supplied same-account test caught it:

```text
1 failed, 3 passed
AssertionError: assert False is True
```

The implementation was corrected to resolve the tenant's property and compare
`actor.landlord_account_id == property.landlord_account_id`. Missing or duplicate relationship
records fail closed. The access-control test file then reported:

```text
4 passed
```

## Final implementation decisions

- Authorization follows the model hierarchy and uses the landlord account as the boundary.
- Cost-tag validation checks all changed resources with a proposed after-state; it does not
  hardcode S3 or Lambda resource types.
- Findings are deduplicated by `(resource address, required tag key)` and sorted before output.
  No state is written, so repeated runs against the same plan are deterministic.
