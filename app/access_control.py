"""
B2, part 1 — landlord-account-scoped screening-report authorization.

A report belongs to a tenant, the tenant belongs to a property, and the property
belongs to a landlord account. The PropertyManager's landlord account is the
authorization boundary. Missing or ambiguous relationships fail closed.
"""
from app.models import PropertyManager, ScreeningReport, Property, Tenant


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    matching_tenants = [tenant for tenant in tenants if tenant.id == report.tenant_id]
    if len(matching_tenants) != 1:
        return False

    tenant = matching_tenants[0]
    matching_properties = [prop for prop in properties if prop.id == tenant.property_id]
    if len(matching_properties) != 1:
        return False

    prop = matching_properties[0]
    return bool(
        actor.landlord_account_id
        and prop.landlord_account_id
        and actor.landlord_account_id == prop.landlord_account_id
    )
