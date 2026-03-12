import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post

st.set_page_config(page_title="Meeting Room Booking", layout="wide")

st.title("Meeting Room Booking")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

# Get rooms
rooms = api_get("/meeting-rooms/rooms")
if rooms:
    room_names = {r["id"]: r["name"] for r in rooms}
    room_options = {r["name"]: r["id"] for r in rooms}
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("New Booking")
        with st.form("booking_form"):
            room_name = st.selectbox("Select Room", options=list(room_options.keys()))
            booking_date = st.date_input("Date", min_value=datetime.today())
            start_time = st.time_input("Start Time", value=time(9, 0))
            end_time = st.time_input("End Time", value=time(10, 0))
            purpose = st.text_area("Purpose")
            
            submit = st.form_submit_button("Book Room")
            if submit:
                start_dt = datetime.combine(booking_date, start_time)
                end_dt = datetime.combine(booking_date, end_time)
                
                booking_data = {
                    "room_id": room_options[room_name],
                    "start_time": start_dt.isoformat(),
                    "end_time": end_dt.isoformat(),
                    "purpose": purpose
                }
                
                result = api_post("/meeting-rooms/bookings", booking_data)
                if result:
                    st.success("Booking request submitted!")
                    st.rerun()

    with col2:
        st.subheader("Current Bookings")
        bookings = api_get("/meeting-rooms/bookings")
        if bookings:
            df = pd.DataFrame(bookings)
            df["Room"] = df["room_id"].map(room_names)
            df["Start"] = pd.to_datetime(df["start_time"]).dt.strftime('%Y-%m-%d %H:%M')
            df["End"] = pd.to_datetime(df["end_time"]).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df[["Room", "Start", "End", "purpose", "status"]])
        else:
            st.info("No bookings found.")
else:
    st.warning("No rooms available.")
