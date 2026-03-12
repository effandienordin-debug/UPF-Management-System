import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post

st.set_page_config(page_title="Stationery Inventory", layout="wide")

st.title("Stationery Inventory Management")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

# Get stationery items
items = api_get("/stationery/items")

tab1, tab2 = st.tabs(["Inventory View", "Add New Item"])

with tab1:
    if items:
        df = pd.DataFrame(items)
        st.subheader("Current Stock Levels")
        
        # Highlight low stock
        df['low_stock'] = df['stock_quantity'] < df['minimum_stock_level']
        
        def highlight_low_stock(row):
            return ['background-color: #ffcccc' if row.low_stock else '' for _ in row]
            
        # Display selected columns and apply styling
        display_cols = ["item_name", "category", "unit", "stock_quantity", "minimum_stock_level", "storage_location"]
        st.dataframe(df[display_cols].style.apply(highlight_low_stock, axis=1))
        
        if df['low_stock'].any():
            st.warning("Warning: Some items are below minimum stock level!")
    else:
        st.info("No items in inventory.")

with tab2:
    st.subheader("Add New Stationery Item")
    with st.form("add_item_form"):
        item_name = st.text_input("Item Name")
        category = st.text_input("Category")
        unit = st.text_input("Unit (e.g. Box, Ream, Unit)")
        stock_quantity = st.number_input("Current Stock", min_value=0, value=0)
        minimum_stock_level = st.number_input("Minimum Stock Level", min_value=0, value=0)
        storage_location = st.text_input("Storage Location")
        
        submit = st.form_submit_button("Add Item")
        if submit:
            item_data = {
                "item_name": item_name,
                "category": category,
                "unit": unit,
                "stock_quantity": stock_quantity,
                "minimum_stock_level": minimum_stock_level,
                "storage_location": storage_location
            }
            
            result = api_post("/stationery/items", item_data)
            if result:
                st.success(f"Item {item_name} added successfully!")
                st.rerun()
