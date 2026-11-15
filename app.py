import streamlit as st
import mylibrary

## Data Entry -------------------------------------------------------------------------
st.title("Hossen Ticketing")

st.number_input("Number of adults", min_value=0, max_value=10, step=1, key="adults")
st.number_input("Number of children", min_value=0, max_value=10, step=1, key="children")
st.number_input("Number of seniors", min_value=0, max_value=10, step=1, key="seniors")

st.radio(label="Type of Ticket", options=["Peak", "Off-Peak"], key="ticket_type")
st.radio(label="Visitor Category", options=["Local", "Foreign"], key="residency")
st.radio(label="Pass Tier", options=["Standard", "Express"], key="pass_type")

st.slider("How many audio guides do you want to rent?", min_value=0, max_value=3, step=1, key="rental")
st.number_input("Number of meal vouchers", min_value=0, max_value=10, step=1, key="meals")
st.text_input("Promo Code (Optional)", key="promo_code")

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