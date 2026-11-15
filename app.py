import streamlit as st
import mylibrary

## Data Entry -------------------------------------------------------------------------
st.title("Tales of Lanfang Ticketing")

st.number_input("Number of adults", min_value=0, max_value=10, step=1, key="adults")
st.number_input("Number of children", min_value=0, max_value=10, step=1, key="children")
st.number_input("Number of seniors", min_value=0, max_value=10, step=1, key="seniors")

st.radio(label="Type of Ticket", options=["Peak", "Off-Peak"], key="ticket_type")
st.radio(label="Visitor Category", options=["Local", "Foreign"], key="residency")
st.radio(label="Pass Tier", options=["Standard", "Express"], key="pass_type")

st.slider("How many audio guides do you want to rent?", min_value=0, max_value=3, step=1, key="rental")
st.number_input("Number of meal vouchers", min_value=0, max_value=10, step=1, key="meals")

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

    # Validate inputs before running price calculations
    is_valid, error_msg = mylibrary.validate_booking(adults, children, seniors, rental)

    if not is_valid:
        st.error(error_msg)

    else:
        # Unpacks subtotal breakdown and bundle savings from business logic
        adult_price, children_price, senior_price, bundle_count, bundle_discount = (
            mylibrary.calculate_total(adults, children, seniors, ticket_type, residency, pass_type)
        )

        # Bundle add-on quantities into a dict so calculate_addons() loops over
        addon_quantities = {
            "Audio Guide": rental,
            "Meal Voucher": meals
        }
        addons_cost = mylibrary.calculate_addons(addon_quantities)

        total_price = round(
            adult_price + children_price + senior_price - bundle_discount + addons_cost, 2
        )

        if bundle_count > 0:
            st.success(f"Family Bundle Applied ({bundle_count}x): You saved ${bundle_discount:.2f}!")

        receipt = {
            "Ticket Tier": ticket_type,
            "Visitor Category": residency,
            "Pass Tier": pass_type,
            "Adults Subtotal": f"${adult_price:.2f}",
            "Children Subtotal": f"${children_price:.2f}",
            "Seniors Subtotal": f"${senior_price:.2f}",
            "Family Bundle Discount": f"-${bundle_discount:.2f}",
            "Add-ons Cost (Audio Guides & Meals)": f"${addons_cost:.2f}",
            "Total Payable": f"${total_price:.2f}"
        }

        st.table(receipt)
else:
    st.info("Select your ticket quantities above.")