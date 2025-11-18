import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analytics", page_icon="📊")

# -----------------------------
# Secure Sheet Connect
# -----------------------------
@st.cache_resource
def load_sheet():
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
    creds = Credentials.from_service_account_file(
        "dagad-478622-030fe5514acb.json",
        scopes=scopes
    )
    client = gspread.authorize(creds)
    sh = client.open("dagadget_stock_data").worksheet("stock_data")
    data = sh.get_all_records()
    return pd.DataFrame(data)

df = load_sheet()

st.title("📊 Stock Analytics Dashboard")

if df.empty:
    st.warning("No data available yet.")
    st.stop()

# -----------------------------
# Filters
# -----------------------------
with st.expander("🔍 Filters"):
    col1, col2, col3 = st.columns(3)

    vendor_filter = col1.selectbox("Vendor", ["All"] + sorted(df["Vendor"].unique()))
    brand_filter = col2.selectbox("Brand", ["All"] + sorted(df["Brand"].unique()))
    model_filter = col3.selectbox("Model", ["All"] + sorted(df["Model"].unique()))

filtered_df = df.copy()

if vendor_filter != "All":
    filtered_df = filtered_df[filtered_df["Vendor"] == vendor_filter]
if brand_filter != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand_filter]
if model_filter != "All":
    filtered_df = filtered_df[filtered_df["Model"] == model_filter]

st.dataframe(filtered_df, use_container_width=True)

# -----------------------------
# Charts
# -----------------------------
st.subheader("📌 Brand Availability")
brand_count = filtered_df["Brand"].value_counts()
fig1 = px.bar(brand_count, title="Brand-wise Count")
st.plotly_chart(fig1)

st.subheader("📌 Vendor Stock Distribution")
vendor_count = filtered_df["Vendor"].value_counts()
fig2 = px.pie(values=vendor_count.values, names=vendor_count.index, title="Vendor Distribution")
st.plotly_chart(fig2)

st.subheader("📌 Price Trends (Model-wise)")
if "Price" in filtered_df.columns:
    filtered_df["Price"] = pd.to_numeric(filtered_df["Price"], errors="coerce")
    fig3 = px.scatter(filtered_df, x="Model", y="Price", color="Brand", title="Price Trend")
    st.plotly_chart(fig3)

# -----------------------------
# Download Button
# -----------------------------
st.download_button(
    label="⬇ Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="Stock_Data_Export.csv",
    mime="text/csv"
)
