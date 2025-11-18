import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import re

st.set_page_config(page_title="Stock Entry", page_icon="📝")

# -----------------------------
# Google Sheets Secure Connect
# -----------------------------
@st.cache_resource
def connect_sheet():
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
    creds = Credentials.from_service_account_file(
        "dagad-478622-030fe5514acb.json",
        scopes=scopes
    )
    client = gspread.authorize(creds)
    sheet = client.open("dagadget_stock_data").worksheet("stock_data")  
    return sheet

sheet = connect_sheet()

# -----------------------------
# Sanitize Inputs
# -----------------------------
def clean(x: str):
    if not x:
        return ""
    return re.sub(r"[<>/{}$|]", "", x.strip())

# -----------------------------
# UI Form
# -----------------------------
st.title("📝 Stock Rate Entry")

vendor_list = ["B Shopee", "C Shopee", "D Shopee"]

with st.form("entry_form"):
    vendor = st.selectbox("Vendor Shop *", vendor_list)
    brand = st.text_input("Brand *")
    model = st.text_input("Model Name *")
    color = st.text_input("Color *")
    variant = st.text_input("Variant (Storage / RAM) *")
    price = st.text_input("Price in ₹ *")
    notes = st.text_area("Remarks (optional)")

    submitted = st.form_submit_button("Submit Entry")

if submitted:

    # Validation
    if not all([brand, model, color, variant, price]):
        st.error("All mandatory fields (*) are required.")
        st.stop()

    if not price.isdigit():
        st.error("Price must be a numeric value.")
        st.stop()

    # Clean
    vendor = clean(vendor)
    brand = clean(brand)
    model = clean(model)
    color = clean(color)
    variant = clean(variant)
    price = clean(price)
    notes = clean(notes)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [timestamp, vendor, brand, model, color, variant, price, notes]

    try:
        sheet.append_row(row)
        st.success("✅ Entry saved successfully.")
        st.balloons()
    except Exception as e:
        st.error("❌ Failed to update Google Sheet. Contact admin.")
