import streamlit as st
import pandas as pd
from datetime import date
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post

st.set_page_config(page_title="Inventory Management", layout="wide")

st.title("Logistics & Inventory Management")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

tab1, tab2 = st.tabs(["Inventory", "Event Logistics Request"])

with tab1:
    st.subheader("Inventory Levels")
    items = api_get("/inventory/items")
    if items:
        df = pd.DataFrame(items)
        st.dataframe(df[["name", "category", "quantity"]])
    else:
        st.info("No items found.")

with tab2:
    st.subheader("Request Logistics for Event")
    if items:
        item_options = {i["name"]: i["id"] for i in items}
        with st.form("event_form"):
            title = st.text_input("Event Title")
            event_date = st.date_input("Event Date", min_value=date.today())
            location = st.text_input("Event Location")
            
            st.divider()
            st.write("Catering Details")
            catering_needed = st.checkbox("Catering Needed")
            catering_details = st.text_area("Catering Details (if needed)")
            
            st.divider()
            st.write("Logistics Items")
            selected_item = st.selectbox("Add Item", options=list(item_options.keys()))
            quantity = st.number_input("Quantity", min_value=1, value=1)
            
            submit = st.form_submit_button("Submit Request")
            if submit:
                request_data = {
                    "title": title,
                    "date": event_date.isoformat(),
                    "location": location,
                    "catering_needed": catering_needed,
                    "catering_details": catering_details,
                    "items": [{"item_id": item_options[selected_item], "quantity": quantity}]
                }
                
                result = api_post("/inventory/events", request_data)
                if result:
                    st.success("Event logistics request submitted!")
                    st.rerun()
    else:
        st.warning("No items available in inventory.")
