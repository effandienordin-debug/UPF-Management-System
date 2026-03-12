import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post, api_patch

st.set_page_config(page_title="Equipment Borrowing", layout="wide")

st.title("Equipment Borrowing (IT & Event Logistics)")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

# Fetch equipment list
equipment = api_get("/equipment")

tab1, tab2 = st.tabs(["Available Equipment", "My Borrowings"])

with tab1:
    st.subheader("Equipment Catalog")
    if equipment:
        available_equipment = [e for e in equipment if e["status"] == "Available"]
        if available_equipment:
            df = pd.DataFrame(available_equipment)
            st.dataframe(df[["name", "category", "serial_number", "condition"]])
            
            with st.form("borrow_form"):
                selected_eq_name = st.selectbox("Select Equipment to Borrow", options=[e["name"] for e in available_equipment])
                selected_eq_id = next(e["id"] for e in available_equipment if e["name"] == selected_eq_name)
                
                expected_return = st.date_input("Expected Return Date", min_value=datetime.today().date() + timedelta(days=1))
                purpose = st.text_area("Purpose")
                
                submit = st.form_submit_button("Borrow Equipment")
                if submit:
                    borrow_data = {
                        "equipment_id": selected_eq_id,
                        "expected_return_date": datetime.combine(expected_return, datetime.min.time()).isoformat(),
                        "purpose": purpose
                    }
                    
                    result = api_post("/equipment/borrow", borrow_data)
                    if result:
                        st.success(f"Equipment {selected_eq_name} borrowed successfully!")
                        st.rerun()
        else:
            st.info("No equipment currently available.")
    else:
        st.info("No equipment in inventory.")

with tab2:
    st.subheader("My Borrowed Items")
    borrowings = api_get("/equipment/borrowings")
    if borrowings:
        # Filter for current user's borrowings (mocking user_id comparison)
        my_borrowings = [b for b in borrowings if str(b["user_id"]) == str(st.session_state.user["id"])]
        if my_borrowings:
            df = pd.DataFrame(my_borrowings)
            st.dataframe(df[["equipment_id", "borrow_date", "expected_return_date", "status"]])
            
            with st.form("return_form"):
                borrowed_items = [b for b in my_borrowings if b["status"] == "Borrowed"]
                if borrowed_items:
                    # In a real app, you'd map equipment names here
                    selected_borrowing = st.selectbox("Select item to return", options=[b["id"] for b in borrowed_items])
                    if st.form_submit_button("Return Item"):
                        result = api_post(f"/equipment/return/{selected_borrowing}", {})
                        if result:
                            st.success("Equipment returned successfully!")
                            st.rerun()
                else:
                    st.info("No active borrowings to return.")
        else:
            st.info("You haven't borrowed any equipment.")
    else:
        st.info("No borrowing records found.")

with tab3:
    st.subheader("Equipment Management (Admin Only)")
    if st.session_state.user["role"] == "UPF Admin":
        with st.form("add_equipment_form"):
            name = st.text_input("Equipment Name")
            category = st.selectbox("Category", options=["IT", "Event & Logistic"])
            serial_number = st.text_input("Serial Number")
            condition = st.text_input("Condition (e.g. New, Good)")
            
            if st.form_submit_button("Add Equipment"):
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
