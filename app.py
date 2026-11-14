import streamlit as st
import mylibrary

# --- 1. User Input Widgets ---
st.title("Tales of Lanfang Ticketing")

st.number_input("Number of adults", min_value=0, max_value=10, step=1, key="adults")
st.number_input("Number of children", min_value=0, max_value=10, step=1, key="children")
st.number_input("Number of seniors", min_value=0, max_value=10, step=1, key="seniors")
st.slider("Audio guides to rent", min_value=0, max_value=3, step=1, key="rental")

st.radio("Type of Ticket", options=["Peak", "Off-Peak"], key="ticket_type")
st.radio("Visitor Category", options=["Local", "Foreign"], key="residency")

# --- 2. Calculation & Receipt Display ---
if st.button("Get Total"):
    # Retrieve all widget values consistently from session_state
    adults = st.session_state.adults
    children = st.session_state.children
    seniors = st.session_state.seniors
    rental = st.session_state.rental
    ticket_type = st.session_state.ticket_type
    residency = st.session_state.residency

    # Delegate business logic to mylibrary.py
    adults_cost, children_cost, seniors_cost = mylibrary.calculate_ticket_costs(
        adults, children, seniors, ticket_type, residency
    )
    guides_cost = mylibrary.calculate_guide_cost(rental)
    grand_total = round(adults_cost + children_cost + seniors_cost + guides_cost, 2)

    # Format output dictionary for clean table rendering
    receipt_summary = {
        "Ticket Tier": ticket_type,
        "Visitor Category": residency,
        "Adults Subtotal": f"${adults_cost:.2f}",
        "Children Subtotal": f"${children_cost:.2f}",
        "Seniors Subtotal": f"${seniors_cost:.2f}",
        "Audio Guides Cost": f"${guides_cost:.2f}",
        "Total Payable": f"${grand_total:.2f}"
    }

    st.table(receipt_summary)
else:
    st.info("Select your ticket quantities above and click 'Get Total'.")