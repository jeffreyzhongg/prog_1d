# Pricing Configuration (edit all rates and bundle rules here)
TICKET_PRICES = {
    "Off-Peak": {"Adult": 10.00, "Child": 6.00, "Senior": 6.00},
    "Peak":     {"Adult": 14.00, "Child": 8.00, "Senior": 8.00}
}

STATUS_MULTIPLIER = {
    "Local": 1.0,
    "Foreign": 1.5
}

FAMILY_BUNDLE = {
    "min_adults": 2,
    "min_children": 2,
    "discount_rate": 0.15  # 15% discount on bundled adult and child tickets
}

ADDON_PRICES = {
    "Audio Guide": 3.00
}


# Business Logic
def calculate_total(adults, children, seniors, ticket_type, status):
    """Returns (adult_price, children_price, senior_price, bundle_count, bundle_discount)."""
    rates = TICKET_PRICES[ticket_type]
    multiplier = STATUS_MULTIPLIER[status]

    adult_rate = rates["Adult"] * multiplier
    child_rate = rates["Child"] * multiplier
    senior_rate = rates["Senior"] * multiplier

    adult_price = round(adults * adult_rate, 2)
    children_price = round(children * child_rate, 2)
    senior_price = round(seniors * senior_rate, 2)

    # Determine how many complete family bundles qualify using floor division (//)
    adult_bundles = adults // FAMILY_BUNDLE["min_adults"]
    child_bundles = children // FAMILY_BUNDLE["min_children"]
    bundle_count = min(adult_bundles, child_bundles)

    if bundle_count > 0:
        bundled_adults_cost = bundle_count * FAMILY_BUNDLE["min_adults"] * adult_rate
        bundled_children_cost = bundle_count * FAMILY_BUNDLE["min_children"] * child_rate
        bundle_discount = round(
            (bundled_adults_cost + bundled_children_cost) * FAMILY_BUNDLE["discount_rate"], 2
        )
    else:
        bundle_discount = 0.00

    return adult_price, children_price, senior_price, bundle_count, bundle_discount


def audio_guides(guide_count):
    """Returns total rental cost for audio guides."""
    return round(guide_count * ADDON_PRICES["Audio Guide"], 2)