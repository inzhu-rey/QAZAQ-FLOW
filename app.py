
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="QAZAQ FLOW",
    page_icon="🚛",
    layout="wide"
)

st.title("🌍 QAZAQ FLOW")
st.subheader("International Smart Logistics Platform")
st.caption("Developed by SONDERS Team")

st.write(
    "QAZAQ FLOW — халықаралық жүк тасымалындағы "
    "бос көліктерді азайтуға және жүк иелері мен "
    "тасымалдаушыларды байланыстыруға арналған платформа."
)

# DEMO DATA
data = [
    [1, "Kazakhstan", "Uzbekistan", "Food products", 5, "Available"],
    [2, "Germany", "Poland", "Electronics", 8, "Available"],
    [3, "Turkey", "Kazakhstan", "Textiles", 12, "Available"],
    [4, "Uzbekistan", "Kyrgyzstan", "Fruits", 4, "Available"],
    [5, "China", "Kazakhstan", "Equipment", 10, "Available"],
    [6, "Poland", "Germany", "Furniture", 7, "Available"],
    [7, "Kazakhstan", "China", "Metals", 15, "Available"],
    [8, "Kyrgyzstan", "Uzbekistan", "Agricultural goods", 3, "Available"]
]

df = pd.DataFrame(
    data,
    columns=[
        "ID", "Origin", "Destination",
        "Cargo", "Weight (tons)", "Status"
    ]
)

# SIDEBAR
st.sidebar.title("🔎 Cargo Search")

countries = sorted(
    set(df["Origin"].tolist() + df["Destination"].tolist())
)

origin = st.sidebar.selectbox(
    "Origin country",
    ["All"] + countries
)

destination = st.sidebar.selectbox(
    "Destination country",
    ["All"] + countries
)

max_weight = st.sidebar.slider(
    "Maximum cargo weight (tons)",
    1, 30, 20
)

# FILTER
filtered = df.copy()

if origin != "All":
    filtered = filtered[filtered["Origin"] == origin]

if destination != "All":
    filtered = filtered[
        filtered["Destination"] == destination
    ]

filtered = filtered[
    filtered["Weight (tons)"] <= max_weight
]

# DASHBOARD
st.header("📦 Available Cargo")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# STATISTICS
st.header("📊 Platform Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total shipments", len(df))
col2.metric("Total cargo", f"{df['Weight (tons)'].sum()} tons")
col3.metric("Available shipments", len(df[df["Status"] == "Available"]))

# RETURN LOAD MATCHING
st.header("🔄 Return Load Matching")

st.write(
    "The system searches for cargo moving in the opposite direction."
)

if origin != "All" and destination != "All":
    reverse = df[
        (df["Origin"] == destination) &
        (df["Destination"] == origin)
    ]

    if not reverse.empty:
        st.success("Potential return-load matches found!")
        st.dataframe(reverse, use_container_width=True)
    else:
        st.info("No matching return cargo in the demo dataset.")
else:
    st.info(
        "Select both origin and destination countries "
        "to search for reverse-direction cargo."
    )

# ADD NEW SHIPMENT
st.header("➕ Add a Shipment")

with st.form("shipment_form"):
    new_origin = st.selectbox(
        "Origin",
        countries,
        key="new_origin"
    )

    new_destination = st.selectbox(
        "Destination",
        countries,
        key="new_destination"
    )

    cargo = st.text_input("Cargo type")

    weight = st.number_input(
        "Cargo weight (tons)",
        min_value=0.1,
        max_value=100.0,
        value=1.0
    )

    submitted = st.form_submit_button("Add shipment")

    if submitted:
        if new_origin == new_destination:
            st.error("Origin and destination must be different.")
        elif not cargo.strip():
            st.error("Enter cargo type.")
        else:
            st.success(
                f"Demo shipment created: {new_origin} → "
                f"{new_destination}, {cargo}, {weight} tons."
            )

st.divider()

st.header("💡 Why QAZAQ FLOW?")
st.write("""
- International cargo matching
- Return-load opportunities
- Cargo search and filtering
- Shipment statistics
- Digital connection between carriers and cargo owners
""")

st.caption("QAZAQ FLOW | SONDERS Team | MVP 2026")
