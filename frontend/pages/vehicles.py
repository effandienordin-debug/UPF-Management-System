import streamlit as st
import pandas as pd
from datetime import datetime, time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post

st.set_page_config(page_title="Vehicle Booking", layout="wide")

st.title("Official Vehicle Booking")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

# Get vehicles
vehicles = api_get("/vehicles")
if vehicles:
    vehicle_names = {v["id"]: f"{v['model']} ({v['plate_number']})" for v in vehicles}
    vehicle_options = {f"{v['model']} ({v['plate_number']})": v["id"] for v in vehicles}
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("New Booking")
        with st.form("vehicle_booking_form"):
            vehicle_name = st.selectbox("Select Vehicle", options=list(vehicle_options.keys()))
            booking_date = st.date_input("Date", min_value=datetime.today())
            start_time = st.time_input("Start Time", value=time(9, 0))
            end_time = st.time_input("End Time", value=time(17, 0))
            destination = st.text_input("Destination")
            purpose = st.text_area("Purpose")
            
            submit = st.form_submit_button("Book Vehicle")
            if submit:
                start_dt = datetime.combine(booking_date, start_time)
                end_dt = datetime.combine(booking_date, end_time)
                
                booking_data = {
                    "vehicle_id": vehicle_options[vehicle_name],
                    "start_time": start_dt.isoformat(),
                    "end_time": end_dt.isoformat(),
                    "destination": destination,
                    "purpose": purpose
                }
                
                result = api_post("/vehicles/bookings", booking_data)
                if result:
                    st.success("Vehicle booking request submitted!")
                    st.rerun()

    with col2:
        st.subheader("Current Bookings")
        bookings = api_get("/vehicles/bookings")
        if bookings:
            df = pd.DataFrame(bookings)
            df["Vehicle"] = df["vehicle_id"].map(vehicle_names)
            df["Start"] = pd.to_datetime(df["start_time"]).dt.strftime('%Y-%m-%d %H:%M')
            df["End"] = pd.to_datetime(df["end_time"]).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df[["Vehicle", "Start", "End", "destination", "purpose", "status"]])
        else:
            st.info("No bookings found.")
else:
    st.warning("No vehicles available.")
