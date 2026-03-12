import streamlit as st
import requests
import pandas as pd
from datetime import datetime

from api_client import api_get

# Page configuration
st.set_page_config(
    page_title="UPF Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API base URL
API_URL = "http://localhost:8000"

def get_metrics():
    # Placeholder for dynamic metric fetching
    # In a real environment, we would fetch these from the API
    return {
        "pending_bookings": 5,
        "vehicles_in_use": 3,
        "open_tickets": 12,
        "visitors_today": 8,
        "stationery_stock": 150,
        "low_stock_alerts": 2,
        "pos_transactions": 4,
        "equipment_borrowed": 3
    }

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

def login():
    st.title("UPF Management System Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            try:
                response = requests.post(
                    f"{API_URL}/auth/login",
                    data={"username": email, "password": password}
                )
                if response.status_code == 200:
                    st.session_state.token = response.json()["access_token"]
                    # Get user info
                    user_response = requests.get(
                        f"{API_URL}/auth/me",
                        headers={"Authorization": f"Bearer {st.session_state.token}"}
                    )
                    st.session_state.user = user_response.json()
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            except Exception as e:
                st.error(f"Error connecting to server: {e}")

def main():
    if not st.session_state.token:
        # Hide the sidebar and the hamburger menu completely when not logged in
        st.markdown(
            """
            <style>
                [data-testid="stSidebar"] {
                    display: none;
                }
                [data-testid="collapsedControl"] {
                    display: none;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        login()
    else:
        st.sidebar.title(f"Welcome, {st.session_state.user['full_name']}")
        st.sidebar.write(f"Role: {st.session_state.user['role']}")
        
        if st.sidebar.button("Logout"):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()

        st.title("UPF Dashboard")
        
        metrics = get_metrics()
        
        # Dashboard Analytics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pending Room Bookings", str(metrics["pending_bookings"]))
            st.metric("Stationery Items In Stock", str(metrics["stationery_stock"]))
        with col2:
            st.metric("Vehicles In Use", str(metrics["vehicles_in_use"]))
            st.metric("Low Stock Alerts", str(metrics["low_stock_alerts"]))
        with col3:
            st.metric("Open Maintenance Tickets", str(metrics["open_tickets"]))
            st.metric("Daily POS Transactions", str(metrics["pos_transactions"]))
        with col4:
            st.metric("Visitors Today", str(metrics["visitors_today"]))
            st.metric("Equipment Borrowed", str(metrics["equipment_borrowed"]))
            
        st.divider()
        
        st.subheader("Module Navigation")
        st.info("Access modules via the sidebar on the left.")
        
        # Display icons/cards for modules
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.info("🏢 Meeting Rooms")
            st.info("📝 Visitors")
            st.info("📦 Stationery POS")
        with m_col2:
            st.info("🚗 Vehicles")
            st.info("🔧 Maintenance")
            st.info("📥 Stationery Inventory")
        with m_col3:
            st.info("🛠️ Equipment Borrowing")
            st.info("📦 Equipment Inventory")
            st.info("📈 Reports & Analytics")
            st.info("🅿️ Parking Registry")
            
if __name__ == "__main__":
    main()
