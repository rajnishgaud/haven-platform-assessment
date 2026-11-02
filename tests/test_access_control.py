from app.access_control import can_access_screening_report


def test_property_manager_cannot_access_other_landlords_report(
    property_managers, properties, tenants, screening_reports
):
    assert can_access_screening_report(
        property_managers[0], screening_reports[1],
        properties=properties, tenants=tenants
    ) is False


def test_property_manager_can_access_same_landlords_report(
    property_managers, properties, tenants, screening_reports
):
    assert can_access_screening_report(
        property_managers[0], screening_reports[0],
        properties=properties, tenants=tenants
    ) is True


def test_missing_tenant_fails_closed(property_managers, properties, tenants, screening_reports):
    assert can_access_screening_report(
        property_managers[0], screening_reports[0],
        properties=properties, tenants=[]
    ) is False


def test_duplicate_tenant_mapping_fails_closed(
    property_managers, properties, tenants, screening_reports
):
    assert can_access_screening_report(
        property_managers[0], screening_reports[0],
        properties=properties, tenants=tenants + [tenants[0]]
    ) is False
