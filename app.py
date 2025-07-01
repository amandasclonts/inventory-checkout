import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Path to Excel file
excel_file = "tool_inventory_log.xlsx"

# Create file if it doesn't exist
if not os.path.exists(excel_file):
    df_init = pd.DataFrame(columns=["Timestamp", "Name", "Item", "Quantity"])
    df_init.to_excel(excel_file, index=False)

# Streamlit UI
st.title("Tool Checkout Log")

name = st.text_input("Your Name")
item = st.selectbox("Select Item", ["DB-1/8"", "DB-30", "DB-3/16"", "DB-1/4"", "DB-3/16" SDS", "DB-1/4" SDS", "CSB-7 1/4"", "CSB-6 1/2"", CSB-5 3/8"", "CSB-7 1/4" AL", 
"CSB-6 1/2"AL", "CW-4 1/2"", "CW-5"", "RZBLD", "BSB-44 7/8"", "RSB-6"", "RSB-12"", "JSB-24T", "JSB-TS", "ACM-RB", "BTH-3"", "BTH-6"", "PBT 2R", "PBT 3", 
"SBT 2", "SBT 3", "TBT-T25", "DCB", "ND-1/4"x6"", "ND-5/16" x6"", "ND-3/8"x6"", "STLN", "RK-Jw/s", "RK-PT", "STPL-T-50", "8-1" ST", "8-3/4" ST"])  # Customize list
quantity = st.number_input("Quantity", min_value=1, step=1)

if st.button("Submit"):
    if name.strip() == "":
        st.warning("Please enter your name.")
    else:
        new_entry = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Item": item,
            "Quantity": quantity
        }])

        # Append to Excel
        existing_df = pd.read_excel(excel_file)
        updated_df = pd.concat([existing_df, new_entry], ignore_index=True)
        updated_df.to_excel(excel_file, index=False)

        st.success(f"{quantity} x {item} checked out by {name}")
