import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Hydrogen Calculator", layout="wide")

st.title("Hydrogen Calculator")

# Create tabs for the two calculators
tab1, tab2 = st.tabs(["ROI Calculator", "Payment Options Calculator"])

with tab1:
    st.header("ROI Calculator")

    # Inputs section with two columns
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        # Input for annual fuel cost
        annual_fuel_cost = st.number_input(
            "Annual diesel fuel cost for longest route ($)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            format="%.2f",
        )

    with input_col2:
        # Input for unit price in the ROI tab
        unit_price_roi = st.number_input(
            "Unit Price ($)",
            min_value=1000.0,
            value=10000.0,
            step=1000.0,
            format="%.2f",
            key="unit_price_roi",
        )

    # Calculate derived values
    potential_savings = annual_fuel_cost * 0.1  # 10% savings

    # Calculate breakeven in months
    breakeven_months = (
        (unit_price_roi / potential_savings) * 12
        if potential_savings > 0
        else float("inf")
    )

    # Calculate monthly values
    monthly_cost = annual_fuel_cost / 12
    monthly_savings = potential_savings / 12

    # Calculate 4-year savings
    four_year_savings = (potential_savings * 4) - unit_price_roi

    # Display calculated values
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Potential annual savings (10%)", f"${potential_savings:,.2f}")
        st.metric("Unit price", f"${unit_price_roi:,.2f}")

    with col2:
        if breakeven_months != float("inf"):
            st.metric("Break-even time", f"{breakeven_months:.1f} months")
        else:
            st.metric("Break-even time", "∞")

    # Results section
    st.subheader("Monthly Cost vs. Savings")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Current monthly cost", f"${monthly_cost:,.2f}")

    with col2:
        st.metric("Monthly savings with unit", f"${monthly_savings:,.2f}")

    # Four year savings
    savings_color = "green" if four_year_savings >= 0 else "red"
    st.markdown("---")
    st.markdown(f"### Potential net savings over next 4 years")
    st.markdown(
        f"<h2 style='color:{savings_color}'>${four_year_savings:,.2f}</h2>",
        unsafe_allow_html=True,
    )

with tab2:
    st.header("Payment Options Calculator")

    # Unit configuration
    st.subheader("Unit Configuration")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        unit_count = st.number_input("Number of Units", min_value=1, value=1, step=1)

    with col2:
        # Input for unit price in the Payment Options tab
        unit_price_payment = st.number_input(
            "Unit Price ($)",
            min_value=1000.0,
            value=10000.0,
            step=1000.0,
            format="%.2f",
            key="unit_price_payment",
        )

    total_cost = unit_price_payment * unit_count

    with col3:
        st.metric("Total Cost", f"${total_cost:,.2f}")

    # Calculate payment options
    st.subheader("Payment Options")

    # Function to calculate payment options
    def calculate_option(name, down_percent, total_amount):
        down_amount = total_amount * (down_percent / 100)
        remaining = total_amount - down_amount
        monthly_payment = remaining / 11

        return {
            "name": name,
            "down_percent": down_percent,
            "down_amount": down_amount,
            "monthly_payment": monthly_payment,
        }

    # Calculate the three options
    options = [
        calculate_option("Option 1", 50, total_cost),
        calculate_option("Option 2", 25, total_cost),
        calculate_option("Option 3", 15, total_cost),
    ]

    # Display options in columns
    cols = st.columns(3)

    for i, option in enumerate(options):
        with cols[i]:
            st.markdown(f"### {option['name']}")
            st.markdown(f"**{option['down_percent']}% Down**")
            st.markdown(f"Initial Down Payment: **${option['down_amount']:,.2f}**")
            st.markdown(f"11 Monthly Payments: **${option['monthly_payment']:,.2f}**")
            st.markdown("---")
            st.markdown(
                f"Total Payment: ${option['down_amount']:,.2f} + (11 × ${option['monthly_payment']:,.2f}) = ${total_cost:,.2f}"
            )
