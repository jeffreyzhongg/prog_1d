import streamlit as st
import mylibrary

# 1. User Input Widgets
st.title("Tales of Lanfang Ticketing")

st.number_input("Number of adults", min_value=0, max_value=10, step=1, key="adults")
st.number_input("Number of children", min_value=0, max_value=10, step=1, key="children")
st.number_input("Number of seniors", min_value=0, max_value=10, step=1, key="seniors")
st.slider("Audio guides to rent", min_value=0, max_value=3, step=1, key="rental")

st.radio("Type of Ticket", options=["Peak", "Off-Peak"], key="ticket_type")
st.radio("Visitor Category", options=["Local", "Foreign"], key="status")

# 2. Calculation & Receipt Display
if st.button("Get Total"):
    adults = st.session_state.adults
    children = st.session_state.children
    seniors = st.session_state.seniors
    rental = st.session_state.rental
    ticket_type = st.session_state.ticket_type
    status = st.session_state.status

    adult_price, children_price, senior_price, bundle_count, bundle_discount = (
        mylibrary.calculate_total(adults, children, seniors, ticket_type, status)
    )
    guides_cost = mylibrary.audio_guides(rental)

    grand_total = round(
        adult_price + children_price + senior_price - bundle_discount + guides_cost, 2
    )

    if bundle_count > 0:
        st.success(f"Family Bundle Applied ({bundle_count}x): You saved ${bundle_discount:.2f}!")

    receipt = {
        "Ticket Tier": ticket_type,
        "Visitor Category": status,
        "Adults Subtotal": f"${adult_price:.2f}",
        "Children Subtotal": f"${children_price:.2f}",
        "Seniors Subtotal": f"${senior_price:.2f}",
        "Family Bundle Discount": f"-${bundle_discount:.2f}",
        "Audio Guides Cost": f"${guides_cost:.2f}",
        "Total Payable": f"${grand_total:.2f}"
    }

    st.table(receipt)
else:
    st.info("Select your ticket quantities above and click 'Get Total'.")