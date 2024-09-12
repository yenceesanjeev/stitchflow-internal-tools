import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Helper functions
def calculate_license_savings(employees, idp, saml_percentage, automation_percentage):
    base_savings = employees * 50  # Assumption: $50 savings per employee
    instant_savings = base_savings * (saml_percentage / 100)
    
    # Higher potential savings when automation is low
    potential_savings = base_savings * ((100 - automation_percentage) / 100)
    
    total_savings = instant_savings + potential_savings
    return instant_savings, potential_savings, total_savings

def calculate_compliance_gaps(employees):
    return employees // 10  # Assumption: 1 gap per 10 employees

def calculate_operational_efficiency(employees, automation_percentage):
    access_checks = employees * 2  # Assumption: 2 checks per employee
    time_freed = employees * (automation_percentage / 100) * 0.5  # Assumption: 0.5 hours freed per automated employee
    return access_checks, time_freed

def calculate_additional_opportunities(employees):
    instant_savings = employees * 25  # Assumption: $25 additional instant savings per employee
    annual_savings = employees * 30  # Assumption: $30 additional annual savings per employee
    compliance_gaps = employees // 20  # Assumption: 1 additional gap per 20 employees
    return instant_savings, annual_savings, compliance_gaps

def calculate_integration_coverage(employees):
    current = min(employees // 50, 100)  # Assumption: 1 integration per 50 employees, max 100
    future = min(current + 20, 100)  # Assumption: 20 more integrations by Sep 2024, max 100
    return current, future

# Sidebar inputs
st.sidebar.title("Input Parameters")
employees = st.sidebar.number_input("Number of Employees", min_value=1, value=100)
idp = st.sidebar.selectbox("Identity Provider", ["Okta", "OneLogin"])
saml_percentage = st.sidebar.slider("SAML Percentage", 0, 100, 50)
automation_percentage = st.sidebar.slider("Automation Percentage", 0, 100, 50)

# Reset button
if st.sidebar.button("Reset"):
    st.rerun()

# Main content
st.title("ROI Calculator")

st.write("Use the sidebar to adjust input parameters and see the ROI calculations update in real-time.")

st.subheader("ROI Report")

# Calculate values
instant_savings, potential_savings, total_savings = calculate_license_savings(employees, idp, saml_percentage, automation_percentage)
compliance_gaps = calculate_compliance_gaps(employees)
access_checks, time_freed = calculate_operational_efficiency(employees, automation_percentage)
add_instant_savings, add_annual_savings, add_compliance_gaps = calculate_additional_opportunities(employees)
current_coverage, future_coverage = calculate_integration_coverage(employees)

# Create DataFrame for output table
data = {
    "Category": [
        "License savings realized",
        "",
        "",
        "Security and compliance gaps closed",
        "IT operational efficiency unlocked",
        "",
        "Identified additional opportunities",
        "",
        "",
        "Acme's integrations coverage",
        ""
    ],
    "Metric": [
        "Instant license savings, $",
        "Potential annual savings*, $",
        "Total potential savings, $",
        "Compliance gaps closed, #",
        "Access & license checks running, #",
        "IT team time freed up, hrs",
        "Instant license savings, $",
        "Annual license savings, $",
        "Compliance gaps, #",
        f"Today: {current_coverage}% ({current_coverage}/100)",
        f"By Sep 2024: {future_coverage}% ({future_coverage}/100+)"
    ],
    "Value": [
        f"{instant_savings:,.2f}",
        f"{potential_savings:,.2f}",
        f"{total_savings:,.2f}",
        str(compliance_gaps),
        f"{access_checks:,}",
        f"{time_freed:.2f}",
        f"{add_instant_savings:,.2f}",
        f"{add_annual_savings:,.2f}",
        str(add_compliance_gaps),
        "",
        ""
    ]
}

df = pd.DataFrame(data)

# Apply alternating row colors
def highlight_rows(row):
    if row.name % 2 == 0:
        return ['background-color: #f0f2f6'] * len(row)
    return [''] * len(row)

styled_df = df.style.apply(highlight_rows, axis=1).set_properties(**{
    'color': 'black',
    'font-weight': 'bold',
    'background-color': 'white'
})

# Display the table with improved visibility
st.table(styled_df)

