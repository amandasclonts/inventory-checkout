import streamlit as st
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

# Path to your Excel file (where it logs checkouts)
excel_path = r"C:\Users\amandac\Western Building Group\FileShare - Documents\Lisa & Amanda\Amanda - AI\AZ Part List.xlsx"
sheet_name = "Checkout"

# --- UI: Title ---
st.title("Inventory Checkout Log")

# --- UI: Input Fields ---
name = st.text_input("Your Name")
item = st.selectbox("Select Item", [
    "DB-1/8", "DB-#30", "DB-3/16", "DB-1/4", "DB-3/16 SDS", "DB-1/4 SDS", "CSB-7 1/4", "CSB-6 1/2", "CSB-5 3/8",
    "CSB-7 1/4 AL", "CSB-6 1/2 AL", "CW-4 1/2", "CW-5", "RZBLD", "BSB-44 7/8", "RSB-6", "RSB-12", "JSB-24T", "JSB-TS",
    "ACM-RB", "BTH-3", "BTH-6", "PBT #2R", "PBT #3", "SBT #2", "SBT #3", "TBT-T25", "DCB", "ND-1/4 x6", "ND-5/16 x6",
    "ND-3/8 x6", "STLN", "RK-Jw/s", "RK-PT", "STPL-T-50", "#8-1 ST", "#8-3/4 ST", "#8-1 AP", "#8-3/4 AP", "#10-1 PN-T2",
    "1 HWH-WOOD", "2 HWH-WOOD", "1 PN-T3", "1 1/4 PN T-17", "1 1/4 PN T-3", "2PN-T3", "3 PN-T3", "1 HWH-T3",
    "1 1/2 HWH-T3", "2 HWH-T3", "2 1/2 HWH-T3", "3 HWH-T3", "1 1/4 T5", "1 1/2 T5", "3 T5", "1 1/4 T5 TORX",
    "RVT #44 AL", "RVT #46 AL", "RVT #44 SS", "RVT #46 SS", "3/16 NAILIN", "1 1/4 TAP HWH 1/4", "1 3/4 TAP HWH 1/4",
    "2 1/4 TAP HWH 1/4", "BKR-7/8 OPEN", "SG 795 WHT", "SG 795 CHR", "SG 795 GRY", "SG 795 BLK", "SG 795 SND",
    "SG 795 CHM", "SGT-YELLOW", "SGT-GREEN", "SGT-RNG", "SB 1/16", "SR 1/8", "SB 1/4"
])
quantity = st.number_input("Quantity", min_value=1, step=1)
unit_type = st.selectbox("Quantity Type", ["Individual piece(s)", "Bag", "Box"])

# --- UI: Hardcoded Job List ---
job_options = [
    "21041 - Beaver Valley Hospital",
    "21048 - TSMC Fab 21 - Phoenix, AZ",
    "21056 - Skyline High School - Academics",
    "21064 - Carvana Corporate Campus",
    "21066 - Maya Hotel",
    "22001 - MWR Hotel and Conference Center at Mayflower",
    "22004 - QTS PHX2 DC1",
    "22006 - Historic Post Office",
    "22010 - WSD New High School",
    "22015 - TCSD Deseret Peak High School",
    "22017 - Black Desert Resort",
    "22018 - Gilbert NWTP South Reservoir Improvements",
    "22025 - Caesars Republic Hotel",
    "22030 - Shoreline Middle School",
    "22034 - BYU Arts Building",
    "22043 - Dangerous Cargo Pad and CATM Facility",
    "22044 - Vantage Data Center AZ 12 & 13",
    "22049 - Tempe Municipal Operations Center - GMP 3",
    "22052 - The McKinley",
    "22056 - IHC Layton Ambulatory Surgical Center",
    "22060 - Prologis Loop 303 Goodyear Building 1",
    "22062 - Cache Valley Transit District Admin & Maint Facility",
    "23001 - 601 N Central",
    "23002 - Mesa Police Evidence Storage",
    "23003 - Ground Based Strategic Deterrent Software Sustainment Center",
    "23006 - NTT PH2-PH3",
    "23009 - Liberty Dogs Mock-Up Building",
    "23011 - Frank E Moss Courthouse Renovation",
    "23012 - OSD Pathways Facility",
    "23013 - Intermountain Washington Fields Clinic",
    "23014 - Stansbury Junior High School",
    "23015 - Sunset Junior High School Replacement",
    "23016 - Brix",
    "23017 - COE Flight Engineering Lab Complex Edwards AFB",
    "23018 - Delta Flight Operations Training Facility",
    "23019 - Elliot Mesa Commerce Center",
    "23020 - QTS PHX2 DC5",
    "23021 - Hopi HCC Outpatient and Emergency Expansion",
    "23022 - Cedar East Elementary School",
    "23023 - Fry's Store 655 - Gilbert",
    "23025 - Goodyear Civic Square Building 3B & 4",
    "23026 - Liberty Dogs Warehouse Building D1",
    "23027 - Tooele Tech College Expansion",
    "23028 - City of Mesa Northeast Public Safety Facility",
    "23032 - Primary Children's Wasatch Canyons Replacement Project",
    "23034 - Waterford School Student Commons",
    "23035 - Snowball WTP",
    "23037 - Park City HS Expansion & Remodel"
]
job_selected = st.selectbox("Select Job", job_options)

checkout_date = st.date_input("Checkout Date", value=datetime.today())
checkout_time = st.time_input("Checkout Time", value=datetime.now().time())

# --- Submission Logic ---
if st.button("Submit"):
    if name.strip() == "":
        st.warning("Please enter your name.")
    else:
        new_row = {
            "Timestamp": f"{checkout_date.strftime('%Y-%m-%d')} {checkout_time.strftime('%I:%M %p')}",
            "Name": name,
            "Job": job_selected,
            "Item": item,
            "Quantity": quantity,
            "Quantity Type": unit_type
        }

        # Write to Excel
        book = load_workbook(excel_path)
        sheet = book[sheet_name]
        next_row = sheet.max_row + 1

        writer = pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='overlay')
        writer.book = book
        writer.sheets = {ws.title: ws for ws in book.worksheets}

        df = pd.DataFrame([new_row])
        write_header = next_row == 1
        df.to_excel(writer, sheet_name=sheet_name, startrow=next_row, index=False, header=write_header)
        writer.close()

        st.success(f"{quantity} x {item} checked out by {name} on {checkout_date} at {checkout_time}")
        st.write("✅ Data written:", df)
