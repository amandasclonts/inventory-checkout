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
item = st.selectbox("Select Item", ["Hammer", "Drill", "Screwdriver", "Wrench", "Tape Measure"])  # Customize list
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
