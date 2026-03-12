import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post

st.set_page_config(page_title="Staff Parking Registry", layout="wide")

st.title("Staff Parking Registry")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Register Vehicle")
    with st.form("parking_form"):
        plate_number = st.text_input("Plate Number", placeholder="WAA 1234")
        vehicle_model = st.text_input("Vehicle Model", placeholder="e.g. Proton Saga")
        color = st.text_input("Color", placeholder="e.g. White")
        parking_lot = st.text_input("Parking Lot Number (if assigned)", placeholder="e.g. P1-05")
        
        submit = st.form_submit_button("Register Vehicle")
        if submit:
            vehicle_data = {
                "user_id": st.session_state.user["id"],
                "plate_number": plate_number,
                "vehicle_model": vehicle_model,
                "color": color,
                "parking_lot_number": parking_lot
            }
            
            result = api_post("/parking/", vehicle_data)
            if result:
                st.success("Vehicle registered successfully!")
                st.rerun()

with col2:
    st.subheader("Staff Parking Registry")
    vehicles = api_get("/parking/")
    if vehicles:
        df = pd.DataFrame(vehicles)
        st.dataframe(df[["plate_number", "vehicle_model", "color", "parking_lot_number", "created_at"]])
    else:
        st.info("No vehicles registered.")
