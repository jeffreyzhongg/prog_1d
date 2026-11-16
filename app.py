import streamlit as st
import mylibrary

## Data Entry -------------------------------------------------------------------------
st.title("Hossen Ticketing")
st.caption("Configure your park tickets, pass tier, and optional add-ons below.")

# Dynamic Rate Card
with st.expander("View Ticket Rates & Discount Rules"):
    off_peak = mylibrary.TICKET_PRICES["Off-Peak"]
    peak = mylibrary.TICKET_PRICES["Peak"]
    bundle = mylibrary.FAMILY_BUNDLE
    addons = mylibrary.ADDON_PRICES

    st.markdown(
        f"**Local Base Admission (Off-Peak / Peak):** \n\n"
        f"Adult `${off_peak['Adult']:.2f}` / `${peak['Adult']:.2f}`\n\n"
        f"Child `${off_peak['Child']:.2f}` / `${peak['Child']:.2f}`\n\n"
        f"Senior `${off_peak['Senior']:.2f}` / `${peak['Senior']:.2f}`\n\n "
        f"**Modifiers & Upgrades:** \n\n Foreign visitors `{mylibrary.RESIDENCY_MULTIPLIER['Foreign']}x` base rate \n\n"
        f"Express Pass `+${mylibrary.PASS_SURCHARGE['Express']:.2f}` per ticket\n\n"

        f"**Add-Ons:** \n\n Audio Guide `${addons['Audio Guide']:.2f}` \n\n "
        f"Meal Voucher `${addons['Meal Voucher']:.2f}`\n\n"

        f"**Discounts (Non-Stacking):** \n\n `{int(bundle['discount_rate'] * 100)}%` off base admission per "
        f"`{bundle['min_adults']}` Adults + `{bundle['min_children']}` Children bundle, or apply a valid promo code."
    )

st.divider()

# Grouped Data Entry
st.subheader("1. Select Visitors")
v_col1, v_col2, v_col3 = st.columns(3)
with v_col1:
    st.number_input("Adults", min_value=0, max_value=10, step=1, key="adults")
with v_col2:
    st.number_input("Children", min_value=0, max_value=10, step=1, key="children")
with v_col3:
    st.number_input("Seniors", min_value=0, max_value=10, step=1, key="seniors")

st.subheader("2. Ticket & Pass Options")
o_col1, o_col2, o_col3 = st.columns(3)
with o_col1:
    st.radio("Ticket Tier", options=["Peak", "Off-Peak"], horizontal=True, key="ticket_type")
with o_col2:
    st.radio("Visitor Category", options=["Local", "Foreign"], horizontal=True, key="residency")
with o_col3:
    st.radio("Pass Tier", options=["Standard", "Express"], horizontal=True, key="pass_type")

st.subheader("3. Add-Ons & Promo Code")
a_col1, a_col2, a_col3 = st.columns(3)
with a_col1:
    st.slider("Audio Guides", min_value=0, max_value=3, step=1, key="rental")
with a_col2:
    st.number_input("Meal Vouchers", min_value=0, max_value=10, step=1, key="meals")
with a_col3:
    st.text_input("Promo Code (Optional)", placeholder="e.g. LANFANG10", key="promo_code")

st.divider()

## Calculation & Receipt Display ------------------------------------------------------
if st.button("Get Total"):

    adults = st.session_state.adults
    children = st.session_state.children
    seniors = st.session_state.seniors
    ticket_type = st.session_state.ticket_type
    residency = st.session_state.residency
    pass_type = st.session_state.pass_type
    rental = st.session_state.rental
    meals = st.session_state.meals
    promo_code = st.session_state.promo_code

    # Validate inputs before running price calculations
    is_valid, error_msg = mylibrary.validate_booking(
        adults, children, seniors, rental, promo_code
        )

    if not is_valid:
        st.error(error_msg)

    else:
        # Unpacks subtotal breakdown and bundle savings from business logic
        adult_price, children_price, senior_price, bundle_count, bundle_discount = (
            mylibrary.calculate_total(adults, children, seniors, ticket_type, residency, pass_type)
        )

        ticket_subtotal = round(adult_price + children_price + senior_price, 2)

        promo_discount, promo_status, clean_code = mylibrary.calculate_promo(
            promo_code, ticket_subtotal
        )

        # Bundle add-on quantities into a dict so calculate_addons() loops over
        addon_quantities = {
            "Audio Guide": rental,
            "Meal Voucher": meals
        }
        addon_subtotals, addons_cost = mylibrary.calculate_addons(addon_quantities)

        total_price = round(
            adult_price + children_price + senior_price - bundle_discount + addons_cost, 2
        )

        # Display booking selections and itemised receipt table
        st.subheader("Booking Receipt")
        st.write(
            f"**Ticket Tier:** {ticket_type} | "
            f"**Visitor Category:** {residency} | "
            f"**Pass Tier:** {pass_type}"
        )

        # Apply whichever single discount saves the visitor more money (no stacking)
        if clean_code != "" and promo_discount > bundle_discount:
            final_discount = promo_discount
            st.success(f"Promo Code '{clean_code}' Applied: You saved ${promo_discount:.2f}!")
        elif bundle_count > 0:
            final_discount = bundle_discount
            if clean_code != "":
                st.info(
                    f"Family Bundle Applied ({bundle_count}x): You saved ${bundle_discount:.2f} "
                    f"(higher than promo code '{clean_code}')."
                )
            else:
                st.success(f"Family Bundle Applied ({bundle_count}x): You saved ${bundle_discount:.2f}!")
        else:
            final_discount = 0.00

        total_price = round(ticket_subtotal - final_discount + addons_cost, 2)
    
        # Build table rows dynamically so only selected items (qty > 0) appear
        line_items = [
            ("Adult Ticket", adults, adult_price),
            ("Child Ticket", children, children_price),
            ("Senior Ticket", seniors, senior_price),
            ("Audio Guide", rental, addon_subtotals["Audio Guide"]),
            ("Meal Voucher", meals, addon_subtotals["Meal Voucher"]),
        ]

        receipt_rows = []
        for item_name, qty, cost in line_items:
            if qty > 0:
                receipt_rows.append({
                    "Item": item_name,
                    "Quantity": qty,
                    "Subtotal": f"${cost:.2f}"
                })


        st.table(receipt_rows)
        st.metric(label="Total Payable", value=f"${total_price:.2f}")
else:
    st.info("Select your ticket quantities above.")