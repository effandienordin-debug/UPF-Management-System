import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_get
import sys
import os
# We will use pandas for Excel and reportlab for PDF in a real environment
# Here we'll just implement the UI for it.
import pandas as pd
from io import BytesIO
# For PDF export
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Reports & Analytics", layout="wide")

st.title("Reports & Analytics")

if 'token' not in st.session_state or not st.session_state.token:
    st.error("Please login from the Dashboard first.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Stationery Usage", "Equipment Usage", "Maintenance Stats"])

with tab1:
    st.subheader("Stationery Consumption Reports")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Usage by Department")
        transactions = api_get("/stationery/transactions")
        if transactions:
            df = pd.DataFrame(transactions)
            dept_usage = df.groupby('department')['total_items'].sum().reset_index()
            st.bar_chart(dept_usage.set_index('department'))
            st.dataframe(dept_usage)
            
            # Monthly Usage Chart
            st.divider()
            st.write("Monthly Usage")
            df['month'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y-%m')
            monthly_usage = df.groupby('month')['total_items'].sum().reset_index()
            st.line_chart(monthly_usage.set_index('month'))
        else:
            st.info("No transaction data available.")
            
    with col2:
        st.write("Low Stock Report")
        items = api_get("/stationery/items")
        if items:
            df_items = pd.DataFrame(items)
            low_stock = df_items[df_items['stock_quantity'] < df_items['minimum_stock_level']]
            if not low_stock.empty:
                st.warning(f"Found {len(low_stock)} items below minimum stock level!")
                st.dataframe(low_stock[["item_name", "stock_quantity", "minimum_stock_level", "unit"]])
            else:
                st.success("All items are above minimum stock level.")
        else:
            st.info("No inventory data available.")

    st.divider()
    if transactions:
        df = pd.DataFrame(transactions)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        st.download_button(
            label="Download Stationery Usage (Excel)",
            data=output.getvalue(),
            file_name="stationery_usage.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # PDF Export
        pdf_output = BytesIO()
        c = canvas.Canvas(pdf_output, pagesize=letter)
        c.drawString(100, 750, "UPF Stationery Usage Report")
        y = 700
        for index, row in df.iterrows():
            c.drawString(100, y, f"{row['department']} - {row['total_items']} items - {row['transaction_date']}")
            y -= 20
        c.save()
        st.download_button(
            label="Download Stationery Usage (PDF)",
            data=pdf_output.getvalue(),
            file_name="stationery_usage.pdf",
            mime="application/pdf"
        )

with tab2:
    st.subheader("Equipment Borrowing Statistics")
    borrowings = api_get("/equipment/borrowings")
    if borrowings:
        df_b = pd.DataFrame(borrowings)
        st.write("Borrowing Status Summary")
        status_counts = df_b['status'].value_counts()
        st.bar_chart(status_counts)
        st.dataframe(df_b[["equipment_id", "borrow_date", "expected_return_date", "status"]])
    else:
        st.info("No borrowing data available.")

with tab3:
    st.subheader("Maintenance Ticket Statistics")
    m_requests = api_get("/maintenance/")
    if m_requests:
        df_m = pd.DataFrame(m_requests)
        st.write("Tickets by Priority")
        p_counts = df_m['priority'].value_counts()
        st.bar_chart(p_counts)
        st.write("Tickets by Status")
        s_counts = df_m['status'].value_counts()
        st.bar_chart(s_counts)
    else:
        st.info("No maintenance data available.")
