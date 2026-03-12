import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get

st.set_page_config(page_title="UPF Master Calendar", layout="wide")

st.title("UPF Integrated Master Calendar")

if 'token' not in st.session_state or st.session_state.token is None:
    st.switch_page("streamlit_app.py")
    st.stop()

# Fetch all types of bookings
room_bookings = api_get("/meeting-rooms/bookings")
vehicle_bookings = api_get("/vehicles/bookings")
maintenance_requests = api_get("/maintenance/")

events = []

if room_bookings:
    for b in room_bookings:
        events.append({
            "title": f"Room Booking: {b.get('purpose', 'Meeting')}",
            "start": b["start_time"],
            "end": b["end_time"],
            "color": "#3788d8" # Blue
        })

if vehicle_bookings:
    for b in vehicle_bookings:
        events.append({
            "title": f"Vehicle: {b.get('destination', 'Trip')}",
            "start": b["start_time"],
            "end": b["end_time"],
            "color": "#28a745" # Green
        })

if maintenance_requests:
    for r in maintenance_requests:
        # For maintenance, use created_at as start
        events.append({
            "title": f"Maintenance: {r['title']}",
            "start": r["created_at"],
            "end": r["created_at"],
            "color": "#dc3545" # Red
        })

calendar_options = {
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay",
    },
    "initialView": "dayGridMonth",
}

state = calendar(events=events, options=calendar_options)

st.write(state)
