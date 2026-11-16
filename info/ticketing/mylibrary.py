## Pricing Configuration --------------------------------------------------------------
TICKET_PRICES = {
    "Off-Peak": {"Adult": 10.00, "Child": 6.00, "Senior": 6.00},
    "Peak":     {"Adult": 14.00, "Child": 8.00, "Senior": 8.00}
}

RESIDENCY_MULTIPLIER = {
    "Local": 1.0,
    "Foreign": 1.5
}

PASS_SURCHARGE = {
    "Standard": 0.00,
    "Express": 15.00 
}

FAMILY_BUNDLE = {
    "min_adults": 2,
    "min_children": 2,
    "discount_rate": 0.15  # 15% off base admission for bundled adult and child tickets
}

ADDON_PRICES = {
    "Audio Guide": 3.00,
    "Meal Voucher": 12.00
}

## Business Logic ---------------------------------------------------------------------

# Validation
def validate_booking(adults, children, seniors, rental):
    total_visitors = adults + children + seniors

    if total_visitors == 0:
        return False, "Please select at least one ticket before calculating."
    if children > 0 and (adults + seniors) == 0:
        return False, "Children must be accompanied by at least one Adult or Senior."
    if rental > total_visitors:
        return False, "Audio guides rented cannot exceed the total number of visitors."

    return True, ""

# Calculation
def calculate_total(adults, children, seniors, ticket_type, residency, pass_type):
    rates = TICKET_PRICES[ticket_type]
    multiplier = RESIDENCY_MULTIPLIER[residency]
    surcharge = PASS_SURCHARGE[pass_type]

    # Compute category subtotals via dictionary lookup
    quantities = {
        "Adult": adults, 
        "Child": children, 
        "Senior": seniors
    }
    subtotals = {}
    for category, count in quantities.items():
        unit_price = (rates[category] * multiplier) + surcharge
        subtotals[category] = round(count * unit_price, 2)
    

    # Calculate total number of complete family bundles eligible for discount, min() enforces limiting group
    adult_bundles = adults // FAMILY_BUNDLE["min_adults"]
    child_bundles = children // FAMILY_BUNDLE["min_children"]
    bundle_count = min(adult_bundles, child_bundles)

    if bundle_count > 0:
        # Family discount applies to base admission only, excludes Express surcharge
        single_bundle_value = (
            FAMILY_BUNDLE["min_adults"] * rates["Adult"]
            + FAMILY_BUNDLE["min_children"] * rates["Child"]
        ) * multiplier
        bundle_discount = round(
            bundle_count * single_bundle_value * FAMILY_BUNDLE["discount_rate"], 2
        )
    else:
        bundle_discount = 0.00

    return (
        subtotals["Adult"],
        subtotals["Child"],
        subtotals["Senior"],
        bundle_count,
        bundle_discount,
    )



def calculate_addons(addon_quantities):
    total_addons = 0.00
    for addon_name, quantity in addon_quantities.items():
        total_addons += quantity * ADDON_PRICES[addon_name]

    return round(total_addons, 2)