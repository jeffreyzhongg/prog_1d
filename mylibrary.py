# --- Pricing Configuration (Edit all rates in this single section) ---
TICKET_PRICES = {
    "Off-Peak": {"Adult": 10.00, "Child": 6.00, "Senior": 6.00},
    "Peak":     {"Adult": 14.00, "Child": 8.00, "Senior": 8.00}
}

RESIDENCY_MULTIPLIERS = {
    "Local": 1.0,
    "Foreign": 1.5
}

ADDON_PRICES = {
    "Audio Guide": 3.00
}


# --- Calculation Functions ---
def calculate_ticket_costs(adults, children, seniors, ticket_type, residency):
    tier_rates = TICKET_PRICES[ticket_type]
    multiplier = RESIDENCY_MULTIPLIERS[residency]

    adults_cost = round(adults * tier_rates["Adult"] * multiplier, 2)
    children_cost = round(children * tier_rates["Child"] * multiplier, 2)
    seniors_cost = round(seniors * tier_rates["Senior"] * multiplier, 2)

    return adults_cost, children_cost, seniors_cost


def calculate_guide_cost(guide_count):
    return round(guide_count * ADDON_PRICES["Audio Guide"], 2)