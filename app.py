import streamlit as st

st.set_page_config(
    page_title="Dagadget Mart System",
    page_icon="📱",
    layout="centered"
)

st.title("📱 Dagadget Mart Internal System")
st.subheader("Welcome to your secure stock management platform.")

st.markdown("""
### 👈 Use the left sidebar to navigate:
- 📝 **Data Entry**
- 📊 **Analytics Dashboard**
""")

st.info("Only authorized personnel should use this system.")
