import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post

st.set_page_config(page_title="Visitor Management", layout="wide")

st.title("Visitor Management")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

tab1, tab2 = st.tabs(["Register Visitor", "Visitor Log"])

with tab1:
    st.subheader("New Visitor Registration")
    with st.form("visitor_form"):
        full_name = st.text_input("Full Name")
        ic_number = st.text_input("IC/Passport Number")
        phone_number = st.text_input("Phone Number")
        company = st.text_input("Company")
        purpose = st.text_area("Purpose of Visit")
        visit_date = st.date_input("Visit Date", min_value=date.today())
        
        submit = st.form_submit_button("Register")
        if submit:
            visitor_data = {
                "full_name": full_name,
                "ic_number": ic_number,
                "phone_number": phone_number,
                "company": company,
                "purpose": purpose,
                "visit_date": visit_date.isoformat()
            }
            
            result = api_post("/visitors", visitor_data)
            if result:
                st.success(f"Visitor {full_name} registered successfully!")
                # In a real app, the QR path would be served via an API endpoint
                # or from a shared static folder.
                st.info(f"Visitor ID: {result['id']}")

with tab2:
    st.subheader("Visitor Logs")
    visitors = api_get("/visitors")
    if visitors:
        df = pd.DataFrame(visitors)
        st.dataframe(df[["full_name", "company", "purpose", "visit_date", "status"]])
    else:
        st.info("No visitors found.")
