# Terminal log

Captured from the assessment workspace after reading `README.md`. The original seed files were
left unchanged.

## Setup

```text
$ python -m pip install -r requirements.txt
Requirement already satisfied: pytest>=8.0 ... (9.0.2)
```

## First-draft review (intentional implementation mistake caught by test)

The first draft incorrectly compared a landlord account ID directly with a tenant ID. The
same-account test failed, exposing the mismatch:

```text
1 failed, 3 passed
AssertionError: assert False is True
```

After correcting the comparison to use the landlord account reached through the tenant's
property, the access-control tests passed:

```text
....                                                                     [100%]
4 passed in 0.11s
```

## Final B2 test run

```text
$ python --version
Python 3.13.5

$ pytest --version
pytest 9.0.2

$ pytest -q
........                                                                 [100%]
8 passed in 0.10s
```

## Cost-tag check run twice against the unchanged plan

```text
$ python scripts/cost_tag_check.py fixtures/plan.json
aws_lambda_function.mls_feed_sync: missing required tag 'landlord_account_id'
aws_s3_bucket.listing_media: missing required tag 'landlord_account_id'
exit=1

$ python scripts/cost_tag_check.py fixtures/plan.json
aws_lambda_function.mls_feed_sync: missing required tag 'landlord_account_id'
aws_s3_bucket.listing_media: missing required tag 'landlord_account_id'
exit=1
```

Both invocations produced byte-for-byte identical findings and the same exit code. The two
reported resources are expected failures in the supplied fixture; the resources already carrying
`landlord_account_id` are not reported.
