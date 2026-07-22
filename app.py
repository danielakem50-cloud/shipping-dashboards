import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Superstore Front Frame", layout="wide")
st.title("Superstore Sales - Same-Day Shipping Front Frame")
st.markdown("**Data is loaded from CSV file**")

@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv")  
    return df

data = load_data()

# Assign column names 
data.columns = [
    "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID",
    "Segment", "Country", "City", "State", "Region", "Product ID",
    "Category", "Sub-Category", "Sales"
]

# Analysis
data["Order Date"] = pd.to_datetime(data["Order Date"], errors='coerce')
data["Ship Date"] = pd.to_datetime(data["Ship Date"], errors='coerce')
data["Shipping_Days"] = (data["Ship Date"] - data["Order Date"]).dt.days

houston = data[data["City"] == "Houston"]
same_day_count = (houston["Shipping_Days"] == 0).sum()
total_houston = len(houston)
percentage = round((same_day_count / total_houston) * 100, 1) if total_houston else 0

shipping_pattern = houston["Shipping_Days"].value_counts().sort_index().head(10)

# Front End
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders in Houston", total_houston)
col2.metric("Same-Day Orders", same_day_count)
col3.metric("Same-Day Percentage", f"{percentage}%")

st.subheader("Shipping Time Distribution in Houston")
fig, ax = plt.subplots(figsize=(10, 5))
shipping_pattern.plot(kind='bar', ax=ax, color='skyblue')
ax.set_xlabel("Number of Shipping Days")
ax.set_ylabel("Total Orders")
ax.set_title("Shipping Speed Analysis - Houston")
st.pyplot(fig)

st.subheader("Full Superstore Data (searchable)")
st.dataframe(data, use_container_width=True, height=450)

# Download
st.subheader("Download Report")
if st.button("Generate Excel Report"):
    summary = pd.DataFrame({
        "Metric": ["Total Orders in Houston", "Same-Day Orders", "Same-Day Percentage"],
        "Value": [total_houston, same_day_count, f"{percentage}%"]
    })
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        summary.to_excel(writer, sheet_name="Front Frame", index=False, startrow=1)
        shipping_pattern.to_excel(writer, sheet_name="Front Frame", startrow=8)
        data.to_excel(writer, sheet_name="Full Superstore Data", index=False)
    
    st.download_button(
        label="Click here to Download Excel File",
        data=output.getvalue(),
        file_name="Superstore_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.caption("Made with Streamlit • CSV Data")