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
    "discount_rate": 0.15  # 15% discount on bundled adult and child tickets
}

ADDON_PRICES = {
    "Audio Guide": 3.00,
    "Meal Voucher": 12.00
}

PROMO_CODES = {
    "YAY10": 0.10,  # 10% off total cost
    "SUTD20": 0.20  # 20% off total cost
}

## Business Logic ---------------------------------------------------------------------
# Validation
def validate_booking(adults, children, seniors, rental, promo_code):
    total_visitors = adults + children + seniors
    clean_code = promo_code.strip().upper()

    if total_visitors == 0:
        return False, "Please select at least one ticket before calculating."
    if children > 0 and (adults + seniors) == 0:
        return False, "Children must be accompanied by at least one Adult or Senior."
    if rental > total_visitors:
        return False, "Audio guides rented cannot exceed the total number of visitors."
    if clean_code != "" and clean_code not in PROMO_CODES:
        return False, f"Invalid promo code'{clean_code}'. Enter a valid code."

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

    # Determine total number of complete family bundles eligible for discount, min() enforces limiting group
    adult_bundles = adults // FAMILY_BUNDLE["min_adults"]
    child_bundles = children // FAMILY_BUNDLE["min_children"]
    bundle_count = min(adult_bundles, child_bundles)

    if bundle_count > 0:
        # Family discount applies to base admissions only, excludes Express surcharge
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

def calculate_promo(promo_code, ticket_subtotal):
    clean_code = promo_code.strip().upper()

    if clean_code == "":
        return 0.00, "none", ""
    if clean_code in PROMO_CODES:
        discount = round(ticket_subtotal * PROMO_CODES[clean_code], 2)
        return discount, "valid", clean_code
    
    return 0.00, "invalid", clean_code


def calculate_addons(addon_quantities):
    addon_subtotals = {}
    total_addons = 0.00

    for addon_name, quantity in addon_quantities.items():
        cost = round(quantity * ADDON_PRICES[addon_name], 2)
        addon_subtotals[addon_name] = cost
        total_addons += cost

    return addon_subtotals, round(total_addons, 2)