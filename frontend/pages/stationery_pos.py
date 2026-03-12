import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get, api_post

st.set_page_config(page_title="Stationery POS", layout="wide")

st.title("Stationery POS")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

# Cart management
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Fetch stationery items
items = api_get("/stationery/items")
if items:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Add to Cart")
        item_names = {i["id"]: f"{i['item_name']} ({i['stock_quantity']} {i['unit']} left)" for i in items}
        item_options = {f"{i['item_name']} ({i['stock_quantity']} {i['unit']} left)": i["id"] for i in items}
        
        selected_item_name = st.selectbox("Select Item", options=list(item_options.keys()))
        quantity = st.number_input("Quantity", min_value=1, value=1)
        
        if st.button("Add to Cart"):
            item_id = item_options[selected_item_name]
            # Check if item already in cart
            existing_item = next((item for item in st.session_state.cart if item["item_id"] == item_id), None)
            if existing_item:
                existing_item["quantity"] += quantity
            else:
                st.session_state.cart.append({
                    "item_id": item_id,
                    "item_name": selected_item_name.split(' (')[0],
                    "quantity": quantity
                })
            st.success(f"Added {quantity} x {selected_item_name.split(' (')[0]} to cart")

    with col2:
        st.subheader("Transaction Cart")
        if st.session_state.cart:
            cart_df = pd.DataFrame(st.session_state.cart)
            st.table(cart_df[["item_name", "quantity"]])
            
            if st.button("Clear Cart"):
                st.session_state.cart = []
                st.rerun()
            
            st.divider()
            
            # Finalize transaction
            department = st.text_input("Department")
            # In a real app, you'd fetch staff list
            staff_id = st.text_input("Staff ID (UUID)", value=st.session_state.user["id"])
            
            if st.button("Complete Transaction"):
                if not department:
                    st.error("Please enter department")
                else:
                    transaction_data = {
                        "staff_id": staff_id,
                        "department": department,
                        "items": [{"item_id": item["item_id"], "quantity": item["quantity"]} for item in st.session_state.cart]
                    }
                    
                    result = api_post("/stationery/transactions", transaction_data)
                    if result:
                        st.success("Transaction completed successfully!")
                        st.session_state.cart = []
                        st.rerun()
        else:
            st.info("Cart is empty")

    st.divider()
    st.subheader("Recent Transactions")
    transactions = api_get("/stationery/transactions")
    if transactions:
        tx_df = pd.DataFrame(transactions)
        st.dataframe(tx_df[["department", "total_items", "transaction_date"]])
else:
    st.warning("No stationery items found.")
