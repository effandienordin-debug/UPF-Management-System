import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post

st.set_page_config(page_title="Equipment Inventory", layout="wide")

st.title("Equipment Inventory Management")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

# Fetch all equipment
equipment = api_get("/equipment/")

tab1, tab2 = st.tabs(["Inventory View", "Add New Equipment"])

with tab1:
    if equipment:
        df = pd.DataFrame(equipment)
        st.subheader("Current Equipment List")
        
        # Filter by status
        status_filter = st.selectbox("Filter by Status", options=["All", "Available", "Borrowed", "Maintenance", "Lost"])
        if status_filter != "All":
            df = df[df['status'] == status_filter]
            
        st.dataframe(df[["name", "category", "serial_number", "status", "condition"]])
    else:
        st.info("No equipment in inventory.")

with tab2:
    if st.session_state.user["role"] == "UPF Admin":
        st.subheader("Add New Equipment")
        with st.form("add_equipment_form"):
            name = st.text_input("Equipment Name")
            category = st.selectbox("Category", options=["IT", "Event & Logistic"])
            serial_number = st.text_input("Serial Number")
            condition = st.text_input("Condition (e.g. New, Good)")
            
            submit = st.form_submit_button("Add Equipment")
            if submit:
                eq_data = {
                    "name": name,
                    "category": category,
                    "serial_number": serial_number,
                    "condition": condition
                }
                result = api_post("/equipment/", eq_data)
                if result:
                    st.success(f"Equipment {name} added successfully!")
                    st.rerun()
    else:
        st.warning("Only UPF Admin can manage equipment inventory.")
