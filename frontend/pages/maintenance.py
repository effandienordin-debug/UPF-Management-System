import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post

st.set_page_config(page_title="Maintenance Management", layout="wide")

st.title("Maintenance & Repair System")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Report an Issue")
    with st.form("maintenance_form"):
        title = st.text_input("Title", placeholder="e.g. Aircon leaking")
        description = st.text_area("Description")
        location = st.text_input("Location", placeholder="e.g. Level 2, Block B")
        priority = st.selectbox("Priority", options=["Low", "Medium", "High", "Emergency"])
        
        submit = st.form_submit_button("Submit Ticket")
        if submit:
            request_data = {
                "title": title,
                "description": description,
                "location": location,
                "priority": priority
            }
            
            result = api_post("/maintenance", request_data)
            if result:
                st.success("Maintenance ticket created!")
                st.rerun()

with col2:
    st.subheader("My Maintenance Tickets")
    requests = api_get("/maintenance")
    if requests:
        df = pd.DataFrame(requests)
        st.dataframe(df[["title", "location", "priority", "status", "created_at"]])
    else:
        st.info("No maintenance requests found.")
