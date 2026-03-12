import streamlit as st
import requests

API_URL = "http://localhost:8000"

def get_auth_header():
    if 'token' in st.session_state and st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def api_get(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}", headers=get_auth_header())
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.session_state.token = None
            st.rerun()
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to server: {e}")
        return None

def api_post(endpoint, data):
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data, headers=get_auth_header())
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 401:
            st.session_state.token = None
            st.rerun()
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to server: {e}")
        return None

def api_patch(endpoint, data=None):
    try:
        response = requests.patch(f"{API_URL}{endpoint}", json=data, headers=get_auth_header())
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.session_state.token = None
            st.rerun()
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to server: {e}")
        return None
