import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Path to your Excel file
excel_path = r"U:\AI\Shop (Chris)\Inventory-Checkout\AZ Part List.xlsx"
sheet_name = "Checkout"

# Streamlit UI
st.title("Inventory Checkout Log")

name = st.text_input("Your Name")
item = st.selectbox("Select Item", ["DB-1/8", "DB-#30", "DB-3/16", "DB-1/4", "DB-3/16 SDS", "DB-1/4 SDS", "CSB-7 1/4", "CSB-6 1/2", "CSB-5 3/8", "CSB-7 1/4 AL", 
"CSB-6 1/2 AL", "CW-4 1/2", "CW-5", "RZBLD", "BSB-44 7/8", "RSB-6", "RSB-12", "JSB-24T", "JSB-TS", "ACM-RB", "BTH-3", "BTH-6", "PBT #2R", "PBT #3", 
"SBT #2", "SBT #3", "TBT-T25", "DCB", "ND-1/4 x6", "ND-5/16 x6", "ND-3/8 x6", "STLN", "RK-Jw/s", "RK-PT", "STPL-T-50", "#8-1 ST", "#8-3/4 ST", "#8-1 AP", "#8-3/4 AP", "#10-1 PN-T2",
"1 HWH-WOOD", "2 HWH-WOOD", "1 PN-T3", "1 1/4 PN T-17", "1 1/4 PN T-3", "2PN-T3", "3 PN-T3", "1 HWH-T3", "1 1/2 HWH-T3", "2 HWH-T3", "2 1/2 HWH-T3", "3 HWH-T3", "1 1/4 T5", "1 1/2 T5",
"3 T5", "1 1/4 T5 TORX", "RVT #44 AL", "RVT #46 AL", "RVT #44 SS", "RVT #46 SS", "3/16 NAILIN", "1 1/4 TAP HWH 1/4", "1 3/4 TAP HWH 1/4", "2 1/4 TAP HWH 1/4", "BKR-7/8 OPEN",
"SG 795 WHT", "SG 795 CHR", "SG 795 GRY", "SG 795 BLK", "SG 795 SND", "SG 795 CHM", "SGT-YELLOW", "SGT-GREEN", "SGT-RNG", "SB 1/16", "SR 1/8", "SB 1/4"])  # Customize list
quantity = st.number_input("Quantity", min_value=1, step=1)

checkout_date = st.date_input("Checkout Date", value=datetime.today())
checkout_time = st.time_input("Checkout Time", value=datetime.now().time())

if st.button("Submit"):
    if name.strip() == "":
        st.warning("Please enter your name.")
    else:
        new_row = {
            "Timestamp": f"{checkout_date} {checkout_time}",
            "Name": name,
            "Item": item,
            "Quantity": quantity
        }

        # Load existing Excel workbook
        book = load_workbook(excel_path)
        writer = pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='overlay')
        writer.book = book
        writer.sheets = {ws.title: ws for ws in book.worksheets}

        # Find the next empty row in the sheet
        sheet = book[sheet_name]
        next_row = sheet.max_row + 1

        # Write the new row
        df = pd.DataFrame([new_row])
        df.to_excel(writer, sheet_name=sheet_name, startrow=next_row, index=False, header=False)

        st.write(f"Writing to Excel at row {next_row}")
        writer.save()
        st.success(f"{quantity} x {item} checked out by {name}")


