# import library
import pandas as pd #data manipulate
import streamlit as st #web abb (Dashboard (DB))
import numpy as np # function (math,arrays)
from datetime import datetime # handle with time
import datetime
import altair as alt # visualized (DB)
from openpyxl import load_workbook # excel
import matplotlib.pyplot as plt # visualized
import seaborn as sns # visualized
import plotly.express as px # ***visualized
import plotly.graph_objs as go # visualized
import re # set of strings that matches
import seaborn as sns # visualized
import warnings  
warnings.filterwarnings('ignore') # ignore warning
import calendar #datetime

# text layout
st.set_page_config(
    page_title="Siteminder OTA",
    layout = 'wide',
)
st.markdown('# AtMind Group')
st.title('Online Travel Agent')

# choose choose a property to get started
hotel_select = st.selectbox("Please choose a property to get started", ["THE GRASS", "ASTER",'Amber PTY','ALTERA','ARDEN','AMBER 85','ARBOUR'])
# Upload files 
st.markdown('**Please Upload CSV Files**')
uploaded_files = st.file_uploader("Choose a CSV file", type='CSV', accept_multiple_files=True)
if uploaded_files:
    all= [] # handle with multifiles
    for uploaded_file in uploaded_files:
        try:
            for uploaded_file in uploaded_files:
                df = pd.read_csv(uploaded_file, thousands=',') 
                all.append(df)
        except Exception as e:
            pass
    if all:
            all = pd.concat(all) # concat when multifiles

            def clean_room_type(room_type):
                if ' X '  in room_type:
                    room_type = 'MIXED ROOM' #' 1 X deluxe,1 X two bedrooms ' convert to 'MIXED ROOM'
                return room_type
            # mapping roomtypes
            if hotel_select == "THE GRASS":
                def convert_room_type(room_type):
                    # if string is 'CITY VIEW ONE BEDROOM SUITE NONREFUND convert to ONE GRASS SUITE CITY VIEW'
                    if re.search(r'\bCITY VIEW ONE BEDROOM SUITE\b|\bONE GRASS SUITE CITY VIEW ROOM\b', room_type):
                        return 'ONE GRASS SUITE CITY VIEW'
                    elif re.search(r'\bห้องสวีทแบบสองห้องนอน\b|\bTWO-BEDROOM SUITE\b|\bBEDROOM SUITE\b|\bTWO GRASS SUITE ROOM\b|\bTWO BEDROOM SUITE\b|\bTWO GRASS SUITE\b|TWO', room_type):
                        return 'TWO GRASS SUITE'
                    elif re.search(r'\bห้องสวีท\b|\bSUITE\b|\bONE GRASS SUITE ROOM\b|\bONE BEDROOM SUITE\b|\bSUITE ONE GRASS SERVICE SUITE\b|\bSUITE ONE\b', room_type):
                        return 'ONE GRASS SUITE'
                    elif re.search(r'\bMIXED ROOM\b', room_type):
                        return 'MIXED'
                    else:
                        return 'UNKNOWN ROOM TYPE'
                # discount adr
                def apply_discount(channel, adr):
                    if channel == 'Booking.com':
                        return adr * 0.82
                    elif channel == 'Expedia':
                        return adr * 0.83
                    else:
                        return adr
                # discount abf 
                def calculate_adr_per_rn_abf(row):
                    if row['RO/ABF'] == 'ABF':
                        return row['ADR'] - 260
                    else:
                        return row['ADR']
            elif hotel_select == "ASTER":
                def convert_room_type(room_type):
                    if re.search(r'\bGRAND CORNER SUITE\b|\bGRAND CORNER SUITE ROOM\b|\bCORNER SUITE\b', room_type):
                        return 'GRAND CORNER SUITE'
                    elif re.search(r'\bGRAND DELUXE KING\b|\bDOUBLE GRAND DELUXE KING\b|\bDELUXE ROOM, 1 KING BED\b', room_type):
                        return 'GRAND DELUXE KING'
                    elif re.search(r'\bNEW DELUXE\b|\bNEW DELUXE ROOM\b|\bDOUBLE NEW DELUXE ROOM\b', room_type):
                        return 'NEW DELUXE'
                    elif re.search(r'\bGRAND DELUXE TWIN ROOM\b|\bGRAND DELUXE TWIN ROOM\b|\bTWIN GRAND DELUXE TWIN\b', room_type):
                        return 'GRAND DELUXE TWIN'
                    elif re.search(r'\bGRAND DELUXE ROOM\b|\bDOUBLE GRAND DELUXE DOUBLE ROOM\b|\bGRAND DELUXE\b|\bGRAND DELUXE DOUBLE ROOM\b', room_type):
                        return 'GRAND DELUXE'
                    elif re.search(r'\bMIXED ROOM\b', room_type):
                        return 'MIXED'
                    else:
                        return 'UNKNOWN ROOM TYPE'
                def apply_discount(channel, adr):
                    if channel == 'Booking.com':
                        return adr * 0.82
                    elif channel == 'Expedia':
                        return adr * 0.83
                    else:
                        return adr
                def calculate_adr_per_rn_abf(row):
                    if row['RO/ABF'] == 'ABF':
                        return row['ADR'] - 260
                    else:
                        return row['ADR']
            elif hotel_select == "Amber PTY":
                def convert_room_type(room_type):
                    if re.search(r'\bGRAND CORNER SUITE\b|\bGRAND CORNER SUITE ROOM\b|\bCORNER SUITE\b', room_type):
                        return 'GRAND CORNER SUITE'
                    elif re.search(r'\bGRAND DELUXE KING\b|\bDOUBLE GRAND DELUXE KING\b|\bDELUXE ROOM, 1 KING BED\b', room_type):
                        return 'GRAND DELUXE KING'
                    elif re.search(r'\bNEW DELUXE\b|\bNEW DELUXE ROOM\b|\bDOUBLE NEW DELUXE ROOM\b', room_type):
                        return 'NEW DELUXE'
                    elif re.search(r'\bGRAND DELUXE TWIN ROOM\b|\bGRAND DELUXE TWIN ROOM\b|\bTWIN GRAND DELUXE TWIN\b', room_type):
                        return 'GRAND DELUXE TWIN'
                    elif re.search(r'\bGRAND DELUXE ROOM\b|\bDOUBLE GRAND DELUXE DOUBLE ROOM\b|\bGRAND DELUXE\b|\bGRAND DELUXE DOUBLE ROOM\b', room_type):
                        return 'GRAND DELUXE'
                    elif re.search(r'\bDELUXE DOUBLE OR TWIN ROOM WITH CITY VIEW\b|\bDELUXE CITY VIEW ROOM\b|\bDELUXE CITY VIEW\b', room_type):
                        return 'DELUXE CITY VIEW ROOM'
                    elif re.search(r'\bDELUXE DOUBLE ROOM WITH POOL VIEW\b|\bDELUXE POOL VIEW DOUBLE\b|\bDELUXE POOL VIEW-DOUBLE\b|\bDELUXE POOL VEIW DOUBLE ROOM\b|\bDELUXE POOL VIEW\b|\bDELUXE DOUBLE ROOM WITH  POOL VIEW\b', room_type):
                        return 'DELUXE POOL VIEW DOUBLE'
                    elif re.search(r'\bDELUXE POOL VIEW TWIN ROOM\b|\bDELUXE TWIN ROOM WITH POOL VIEW\b|\bDELUXE POOL VIEW-TWIN\b|\bDELUXE POOL VIEW TWIN\b|\bTWIN DELUXE TWIN ROOM WITH POOL VIEW\b', room_type):
                        return 'DELUXE POOL VIEW TWIN'
                    elif re.search(r'\bDELUXE ROOM\b|\bDOUBLE OR TWIN DELUXE DOUBLE\b|\bDELUXE DOUBLE OR TWIN ROOM\b', room_type):
                        return 'DELUXE'
                    elif re.search(r'\bMIXED ROOM\b', room_type):
                        return 'MIXED'
                    else:
                        return 'UNKNOWN ROOM TYPE'
                def apply_discount(channel, adr):
                    if channel == 'Booking.com':
                        return adr * 0.82
                    elif channel == 'Expedia':
                        return adr * 0.83
                    else:
                        return adr
                def calculate_adr_per_rn_abf(row):
                    if row['RO/ABF'] == 'ABF':
                        return row['ADR'] - 260
                    else:
                        return row['ADR']
            elif hotel_select == "ALTERA":
                def convert_room_type(room_type):
                    if re.search(r'\bBEDROOM FAMILY SUITE WITH KITCHENETTE\b',room_type):
                        return 'TWO BEDROOM SUITE'
                    elif re.search(r'\bDELUXE POOL VIEW ROOM\b|\bDOUBLE DELUXE POOL VIEW DOUBLE\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\b|\bDELUXE DOUBLE OR TWIN ROOM WITH POOL VIEW\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\(DOUBLE BED\)\b|\bDELUXE TWIN ROOM WITH POOL VIEW\b|\bDOUBLE DELUXE POOL VIEW DOUBLE\b|\bDELUXE POOL VIEW TWIN\b|\bDELUXE POOL VIEW ROOM TWIN BED WITH KITCHENETTE\b|\bTWIN DELUXE POOL VIEW TWIN\b|\bDELUXE POOL VIEW WITH KITCHENETTE\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE \(TWIN\)\b|\bDELUXE POOL VIEW ROOM DOUBLE BED WITH KITCHENETTE\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\(TWIN BED\)\b', room_type):
                        return 'DELUXE POOL VIEW'
                    elif re.search(r'\bDELUXE ROOM WITH KITCHENETTE\b|\bDELUXE DOUBLE ROOM\b|\bDELUXE DOUBLE BED ROOM WITH KITCHENETTE\b|\DOUBLE DELUXE\b', room_type):
                        return 'DELUXE'
                    elif re.search(r'\bGRAND SUITE WITH DOUBLE BED\b|\bSUITE GRAND SUITE\b|\bGRAND SUITES ROOM WITH KITCHENETTE\(DOUBLE BED\)\b|\bGRAND SUITE WITH KITCHENETTE\b|\bGRAND SUITE ROOM WITH KITCHENETTE\b|\bGRAND SUITE  WITH KITCHENETTE\b|\bGRAND SUITE ROOM DOUBLE BED WITH KITCHENETTE\b|\bGRAND SUITE KITCHENETTE\b|\bGRAND SUITES ROOM WITH KITCHENETTE\(TWIN BED\)\b|\bGRAND SUITE ROOM TWIN BED WITH KITCHENETTE\b', room_type):
                        return 'GRAND SUITE'
                    elif re.search(r'\bGRAND SUITE POOL VIEW ROOM\b|\bGRAND SUITE POOL VIEW ROOM WITH KITCHENETTE\b|\bGRAND POOL VIEW SUITE WITH KITCHENETTE\b|\bGRAND SUITE WITH POOL VIEW\b|\bSUITE GRAND POOL VIEW\b|\bGRAND SUITE POOL VIEW WITH KITCHENETTE\b|\bGRAND SUITES POOL VIEW ROOM WITH KITCHENETTE\b|\bGRAND SUITE POOL VIEW ROOM DOUBLE BED WITH KITCHENETTE\b', room_type):
                        return 'GRAND SUITE POOL VIEW'
                    elif re.search(r'\bTWO BEDROOM SUITE\b|\bBEDROOM FAMILY SUITE WITH KITCHENETTE\b|\bFAMILY SUITE TWO BEDROOM WITH KITCHENETTE\b|\bFAMILY TWO\b|\bFAMILY ROOM FAMILY TWO BEDROOMS\b|\bFAMILY SUITES TWO BEDROOM\b|\bTWO BEDROOM FAMILY SUITE WITH KITCHENETTE\b|TWO', room_type):
                        return 'TWO BEDROOM SUITE'
                    elif re.search(r'\bDELUXE CITY VIEW ROOM\b|\bDELUXE DOUBLE OR TWIN ROOM WITH CITY VIEW\b|\bDELUXE CITY VIEW ROOM\b|\bDELUXE CITY VIEW ROOM WITH KITCHENETTE\b|\bDELUXE CITY VIEW ROOM DOUBLE OR TWIN BED WITH KITCHENETTE\b|\bDOUBLE OR TWIN DELUXE CITY VIEW DOUBLE OR TWIN\b', room_type):
                        return 'DELUXE CITY VIEW'
                    elif re.search(r'\bDELUXE POOL VIEW ROOM\b|\bDOUBLE DELUXE POOL VIEW DOUBLE\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\b|\bDELUXE DOUBLE OR TWIN ROOM WITH POOL VIEW\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\(DOUBLE BED\)\b|\bDELUXE TWIN ROOM WITH POOL VIEW\b|\bDOUBLE DELUXE POOL VIEW DOUBLE\b|\bDELUXE POOL VIEW TWIN\b|\bDELUXE POOL VIEW ROOM TWIN BED WITH KITCHENETTE\b|\bTWIN DELUXE POOL VIEW TWIN\b|\bDELUXE POOL VIEW WITH KITCHENETTE\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE \(TWIN\)\b|\bDELUXE POOL VIEW ROOM DOUBLE BED WITH KITCHENETTE\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\(TWIN BED\)\b', room_type):
                        return 'DELUXE POOL VIEW'
                    elif re.search(r'\bGRAND SUITE TWIN ROOM\b|\bGRAND SUITE WITH TWIN BED\b|\bGRAND SUITE TWIN\b|\bGRAND SUITE WITH KITCHENETTE \(TWIN\)\b|\bTWIN GRAND TWIN\b', room_type):
                        return 'GRAND SUITE TWIN'
                    elif re.search(r'\bMIXED ROOM\b', room_type):
                        return 'MIXED'
                    else:
                        return 'UNKNOWN'
                def apply_discount(channel, adr):
                    if channel == 'Booking.com':
                        return adr * 0.82
                    elif channel == 'Expedia':
                        return adr * 0.83
                    else:
                        return adr
                def calculate_adr_per_rn_abf(row):
                    if row['RO/ABF'] == 'ABF':
                        return row['ADR'] - 260
                    else:
                        return row['ADR']
            elif hotel_select == "ARDEN":
                def convert_room_type(room_type):
                    if re.search(r'\bDELUXE CITY VIEW\b|\bห้องดีลักซ์เตียงใหญ่หรือเตียงแฝดพร้อมวิวเมือง\b|\bDELUXE ROOM, CITY VIEW\b|\bDOUBLE OR TWIN DELUXE CITY VIEW DOUBLE OR TWIN\b|\bDELUXE CITY VIEW\b|\bDELUXE CITY VIEW ROOM\b|\bDELUXE CITY VIEW  (DOUBLE OR TWIN)\b|\bDELUXE CITY VIEW ROOM ONLY (DOUBLE 0R TWIN)\b', room_type):
                        return 'DELUXE CITY VIEW'
                    elif re.search(r'\bDELUXE POOL VIEW TWIN\b|\bห้องดีลักซ์เตียงใหญ่หรือเตียงแฝดพร้อมทัศนียภาพของสระว่ายน้ำ\b|\bDELUXE POOL VIEW\(TWIN BED\)\b|\bDELUXE POOL VIEW ROOM \(TWIN\)\b|\bห้องดีลักซ์เตียงแฝดพร้อมวิวสระว่ายน้ำ\b|\bDELUXE POOL VIEW ROOM ONLY \(TWIN\)\b|\bDELUXE POOL VIEW TWIN\b|\bDELUXE POOL VIEW ROOM ONLY \(TWIN\)\b|\bTWIN DELUXE POOL VIEW TWIN ROOM\b|\bDELUXE POOL VIEW ROOM WITH TWIN BED\b', room_type):
                        return 'DELUXE POOL VIEW TWIN'
                    elif re.search(r'\bDELUXE POOL VIEW\b|\bDOUBLE DELUXE POOL VIEW DOUBLE ROOM\b|\bDELUXE ROOM, POOL VIEW\b|\bDELUXE POOL VIEW\b|\bDELUXE ROOM WITH POOL VIEW\b|\bDELUXE POOL VIEW ROOM ONLY (DOUBLE)\b|\bDELUXE POOL VIEW ROOM WITH DOUBLE BED\b|\bDELUXE POOL VIEW TWIN\b|\bDELUXE POOL VIEW  (DOUBLE)\b|\bDELUXE ROOM ONLY (DOUBLE)\b|\bDELUXE POOL VIEW(DOUBLE BED)\b', room_type):
                        return 'DELUXE POOL VIEW'
                    elif re.search(r'\bDOUBLE DELUXE DOUBLE ROOM\b|\bห้องดีลักซ์เตียงใหญ่\b|\bDELUXE\b|\DELUXE ROOM\b|\bDELUXE (RO)\b|\bDELUXE  (DOUBLE)\b|\bDELUXE DOUBLE ROOM (BALCONY)\b', room_type):
                        return 'DELUXE'
                    elif re.search(r'\bEXCLUSIVE FAMILY SUITES\b|\bห้องสวีทแบบสองห้องนอน\b|\bFAMILY ROOM\b|\bEXCLUSIVE FAMILY SUITE\b|\bFAMILY ROOM FAMILY TWO BEDROOMS\b|\bEXCLUSIVE FAMILY SUITES ROOM ONLY (DOUBLE)\b|\bEXCLUSIVE FAMILY SUITES  (DOUBLE)\b|\bEXECUTIVE FAMILY SUIT\b', room_type):
                        return 'EXCLUSIVE FAMILY SUITES'
                    elif re.search(r'\bEXCLUSIVE SUITES\b|\bห้องเอ็กเซ็กคูทีฟสวีท\b|\bEXCLUSIVE SUITE\b|\bEXCLUSIVE SUITES\b|\bEXCLUSIVE SUITES ROOM ONLY (DOUBLE)\b', room_type):
                        return 'EXCLUSIVE SUITES'
                    elif re.search(r'\bMIXED ROOM\b', room_type):
                        return 'MIXED'
                    else:
                        return 'UNKNOWN'
                def apply_discount(channel, adr):
                    if channel == 'Booking.com':
                        return adr * 0.82
                    elif channel == 'Expedia':
                        return adr * 0.83
                    else:
                        return adr
                def calculate_adr_per_rn_abf(row):
                    if row['RO/ABF'] == 'ABF':
                        return row['ADR'] - 260
                    else:
                        return row['ADR']
            elif hotel_select == "AMBER 85":
                def convert_room_type(room_type):
                    if re.search(r'\bGRAND DELUXE ROOM\b|\bGRAND DELUXE\b|\bGRAND DELUXE DOUBLE ROOM\b|\bGRAND DELUXE ROOM ONLY\b|\bGRAND DOUBLE OR TWIN ROOM\b|\bDOUBLE GRAND DELUXE DOUBLE ROOM\b', room_type):
                        return 'GRAND DELUXE'
                    if re.search(r'\bDELUXE DOUBLE ROOM\b|\bDELUXE DOUBLE OR TWIN ROOM WITH CITY VIEW\b|\bDELUXE ROOM CITY VIEW\b|\bDELUXE ROOM ONLY\b|\bDELUXE DOUBLE OR TWIN ROOM\b|\bNEW DELUXE DOUBLE\b|\bDELUXE ROOM\b', room_type):
                        return 'NEW DELUXE'
                    elif re.search(r'\bNEW DELUXE TWIN\b|\bDELUXE TWIN ROOM\b|\bDOUBLE OR TWIN NEW DELUXE DOUBLE OR TWIN\b|\bDELUXE TWIN ROOM ONLY\b|\bTWIN NEW DELUXE TWIN ROOM\b', room_type):
                        return 'NEW DELUXE TWIN'
                    elif re.search(r'\bGRAND CORNER SUITES\b|\bGRAND DELUXE\b|\bSUITE WITH BALCONY\b|\bGRAND CORNER SUITES ROOM ONLY\b|\bSUITE SUITE GRAND CORNER\b|\bGRAND STUDIO SUITE\b|\bGRAND CORNER SUITE\b', room_type):
                        return 'GRAND CORNER SUITES'
                    elif re.search(r'\bMIXED ROOM\b', room_type):
                        return 'MIXED'
                    else:
                        return 'UNKNOWN'
                def apply_discount(channel, adr):
                    if channel == 'Booking.com':
                        return adr * 0.82
                    elif channel == 'Expedia':
                        return adr * 0.80
                    else:
                        return adr
                def calculate_adr_per_rn_abf(row):
                    if row['RO/ABF'] == 'ABF':
                        return row['ADR'] - 260
                    else:
                        return row['ADR']
            elif hotel_select == 'ARBOUR':
                def convert_room_type(room_type):
                    if re.search(r'\bDELUXE KING ROOM\b|\bDELUXE KING\b|\bDELUXE CITY VIEW KING\b|\bROOM DELUXE KING BED\b|\bDELUXE  KING ROOM\b|\bDELUXE KING ROOM ONLY\b|\bห้องดีลักซ์เตียงคิงไซส์\b|ห้องดีลักซ์เตียงคิงไซส์', room_type):
                        return 'DELUXE KING'
                    elif re.search(r'ห้องพรีเมียร์เตียงใหญ่ชั้นสูงพร้อมวิวเมือง|\bPREMIER HIGH FLOOR CITY VIEW\b|\bPREMIER DOUBLE ROOM HIGH FLOOR  WITH CITY VIEW\b|\bROOM PREMIER CITY VIEW\b',room_type):
                        return 'PREMIER HIGH FLOOR'
                    elif re.search(r'\bDELUXE CITY VIEW\b|\bDELUXE DOUBLE ROOM, CITY VIEW\b|\bROOM DELUXE CITY VIEW DOUBLE ROOM\b|\bDELUXE CITY VIEW\b|\bDELUXE DOUBLE ROOM WITH CITY VIEW\b|\bDELUXE CITY VIEW ROOM ONLY\b|\bห้องดีลักซ์เตียงใหญ่พร้อมวิวเมือง\b', room_type):
                        return 'DELUXE CITY VIEW'
                    elif re.search(r'\bDELUXE OCEAN VIEW\b|\bDELUXE DOUBLE ROOM WITH OCEAN VIEW\b|\bROOM DELUXE OCEAN VIEW\b|\bDELUXE DOUBLE ROOM, OCEAN VIEW\b|\bDELUXE OCEAN VIEW KING\b|\bDELUXE OCEAN VIEW ROOM ONLY\b|\bห้องดีลักซ์เตียงใหญ่พร้อมวิวมหาสมุทร\b', room_type):
                        return 'DELUXE OCEAN VIEW'
                    elif re.search(r'\bDELUXE DOUBLE OR TWIN\b|\bDELUXE DOUBLE OR TWIN ROOM\b|\bDELUXE DOUBLE OR TWIN\b|\bDELUXE\b|\bDELUXE TWIN BED\b|\bTWIN DELUXE TWIN ROOM\b|\bDELUXE \(DOUBLE OR TWIN\) ROOM ONLY\b|\bDELUXE \(DOUBLE OR TWIN\)\b|\bห้องดีลักซ์เตียงใหญ่หรือเตียงแฝด\b', room_type):
                        return 'DELUXE DOUBLE OR TWIN'
                    elif re.search(r'\bDELUXE CITY VIEW\b|\bDELUXE DOUBLE ROOM, CITY VIEW\b|\bROOM DELUXE CITY VIEW DOUBLE ROOM\b|\bDELUXE CITY VIEW\b|\bDELUXE DOUBLE ROOM WITH CITY VIEW\b|\bDELUXE CITY VIEW ROOM ONLY\b|\bห้องดีลักซ์เตียงใหญ่พร้อมวิวเมือง\b', room_type):
                        return 'DELUXE CITY VIEW'
                    elif re.search(r'\bPREMIER CITY VIEW\b|\bPREMIER CITY VIEW\b|PREMIER CITY VIEW KING|\bPREMIER DOUBLE ROOM, CITY VIEW\b|\bPREMIER DOUBLE ROOM WITH CITY VIEW\b|\bPREMIER CITY VIEW\b|\bPREMIER CITY VIEW ROOM ONLY\b|ห้องพรีเมียร์เตียงใหญ่พร้อมวิวเมือง', room_type):
                        return 'PREMIER CITY VIEW'
                    elif re.search(r'\bPREMIER KING\b|PREMIER DOUBLE ROOM|ห้องพรีเมียร์เตียงใหญ่|\bPREMIER KING\b|\bPREMIER CITY VIEW KING\b|\bPREMIER CITY VIEW ROOM ONLY\b|PREMIER DOUBLE BED', room_type):
                        return 'PREMIER KING'
                    elif re.search(r'\bDELUXE OCEAN VIEW\b|\bDELUXE DOUBLE ROOM WITH OCEAN VIEW\b|\bROOM DELUXE OCEAN VIEW\b|\bDELUXE DOUBLE ROOM, OCEAN VIEW\b|\bDELUXE OCEAN VIEW KING\b|\bDELUXE OCEAN VIEW ROOM ONLY\b|\bห้องดีลักซ์เตียงใหญ่พร้อมวิวมหาสมุทร\b', room_type):
                        return 'DELUXE OCEAN VIEW'
                    elif re.search(r'\bPREMIER HIGH FLOOR\b|\bROOM PREMIER\b|\bPREMIER HIGH FLOOR ROOM WITH VIEW\b|\bPREMIER ROOM\b|\bPREMIER HIGH FLOOR CITY VIEW ROOM ONLY\b|\bPREMIER ROOM ONLY\b|\bPREMIER HIGH FLOOR CITY VIEW ROOM ONLY\b|\bROOM PREMIER HIGH FLOOR\b|ห้องพรีเมียร์เตียงใหญ่ชั้นสูงพร้อมวิวเมือง|\bห้องพรีเมียร์เตียงใหญ่ชั้นสูงพร้อมวิวเมือง\b', room_type):
                        return 'PREMIER HIGH FLOOR'
                    elif re.search(r'\bTWO BEDROOM SUITES\b|\bTWO\b|\bTWO BEDROOM SUITE\b|\bTWO BEDROOM SUITES\b|\bFAMILY SUITE, 2 BEDROOMS\b|\bTWO BEDROOM SUITE OCEAN VIEW\b|\bSUITE TWO BEDROOM SUITES\b|\bห้องสวีทแบบสองห้องนอนพร้อมวิวทะเล\b|TWO|\bTWO BEDROOM SUITE OCEAN VIEW ROOM ONLY\b', room_type):
                        return 'TWO BEDROOM SUITE'
                    elif re.search(r'\bPENTHOUSE SUITE WITH PRIVATE POOL\b|เพนต์เฮาส์สวีทพร้อมสระว่ายน้ำส่วนตัว|\bPENTHOUSE SUITE WITH PRIVATE POOL\b|\bSUITE PENTHOUSE SUITE WITH PRIVATE POOL\b', room_type):
                        return 'PENTHOUSE SUITE'
                    elif re.search(r'\bHONEYMOON SUITE WITH OCEAN VIEW\b|\bHONEYMOON SUITE WITH OCEAN VIEW\b|\bHONEYMOON SUITES\b|ห้องฮันนีมูนสวีทพร้อมวิวมหาสมุทร', room_type):
                        return 'HONEYMOON SUITE'
                    elif re.search(r'\bMIXED ROOM\b', room_type):
                        return 'MIXED'
                    else:
                        return 'UNKNOWN'
                def apply_discount(channel, adr):
                    if channel == 'Booking.com':
                        return adr * 0.82
                    elif channel == 'Expedia':
                        return adr * 0.83
                    else:
                        return adr
                def calculate_adr_per_rn_abf(row):
                    if row['RO/ABF'] == 'ABF':
                        return row['ADR'] - 300
                    else:
                        return row['ADR']
            # To find NRF or Flex
            def convert_RF(room_type):
                if re.search(r'\bNON REFUNDABLE\b|\bไม่สามารถคืนเงินจอง\b|\bNON REFUND\b|\bNON-REFUNDABLE\b|\bNRF\b', room_type):
                    return 'NRF'
                elif re.search(r'\bUNKNOWN ROOM\b', room_type):
                    return 'UNKNOWN'
                elif  room_type == "1 X " or room_type == "2 X " or room_type == "3 X " or room_type == "4 X ":
                    return 'UNKNOWN'
                else:
                    return 'Flexible'
            # To find RO or ABF
            def convert_ABF(room_type):
                if re.search(r'\bBREAKFAST\b|\bWITH BREAKFAST\b|\bBREAKFAST INCLUDED\b', room_type):
                    return 'ABF'
                elif re.search(r'\bUNKNOWN ROOM\b', room_type):
                    return 'UNKNOWN'
                elif  room_type == "1 X " or room_type == "2 X " or room_type == "3 X " or room_type == "4 X ":
                    return 'UNKNOWN'
                elif re.search(r'\bRO\b|\bROOM ONLY\b', room_type):
                    return 'RO'
                else:
                    return 'RO'
            # cleaning data
            def perform(all): 
                all1 = all[['Booking reference'
                            ,'Guest names'
                            ,'Check-in'
                            ,'Check-out'
                            ,'Channel'
                            ,'Room'
                            ,'Booked-on date'
                            ,'Total price']] # focus on columns (Col) that we choose
                all1 = all1.dropna()  # drop empty values

                all1["Check-in"] = pd.to_datetime(all1["Check-in"]) # astype to datetime
                all1['Booked-on date'] = pd.to_datetime(all1['Booked-on date']) 
                all1['Booked'] = all1['Booked-on date'].dt.strftime('%m/%d/%Y') # extract just mm/dd/yyyy ( sting (str) type)
                all1['Booked'] = pd.to_datetime(all1['Booked'])
                all1["Check-out"] = pd.to_datetime(all1["Check-out"])
                all1["Length of stay"] = (all1["Check-out"] - all1["Check-in"]).dt.days # cal LOS
                all1["Lead time"] = (all1["Check-in"] - all1["Booked"]).dt.days # cal LT
                LT1 = [-1, 0, 1, 2, 3, 4, 5, 6, 7,8, 14, 30, 90, 120] #grouping data
                LT2 = ['-one', 'zero', 'one', 'two', 'three', 'four', 'five', 'six','seven', '8-14', '14-30', '31-90', '90-120', '120+']
                LT11 = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,31,90, 120, float('inf')]
                LT22 = ['.-1.', '.0.', '.1.', '.2.', '.3.', '.4.', '.5.', '.6.', '.7.', '.8.', '.9.', '.10.', '.11.', '.12.', '.13.', '.14.', '.15.', '.16.', '.17.', '.18.', '.19.', '.20.', '.21.', '.22.', '23.', '.24.', '25.', '.26.', '.27.', '.28.', '.29.', '.30.', '31-90.', '91-120', '120.+']
                value_ranges1 = [1,2,3,4,5,6,7,8,9,10,14,30,45,60]
                labels1 = ['one', 'two', 'three', 'four', 'five', 'six','seven','eight', 'nine', 'ten', '14-30', '30-45','45-60', '60+']
                all1['Lead time range'] = pd.cut(all1['Lead time'], bins=LT1 + [float('inf')], labels=LT2, right=False)
                all1['Lead time range1'] = pd.cut(all1['Lead time'], bins=LT11, labels=LT22, right=False)
                all1['LOS range'] = pd.cut(all1['Length of stay'], bins=value_ranges1 + [float('inf')], labels=labels1, right=False)

                all1['Room'] = all1['Room'].str.upper() #convert to uppercase
                all1['Booking reference'] = all1['Booking reference'].astype('str') # astype (datatype)
                all1['Total price'] = all['Total price'].str.strip('THB') # 'THB 1500' to '1500'
                all1['Total price'] = all1['Total price'].astype('float64') # astype
                all1['Quantity'] = all1['Room'].str.extract('^(\d+)', expand=False).astype(int) # {'Room':'1 X deluxe'} to {'Room':'deluxe','Quantity':1}
                all1['Room Type'] = all1['Room'].str.replace('-.*', '', regex=True) # '3 X DElUXE-NRF' to '3 X DELUXE'
                all1['Room Type'] = all1['Room Type'].apply(lambda x: re.sub(r'^\d+\sX\s', '', x)) #'3 X DElUXE' to 'DELUXE'
                all1['Room Type'] = all1['Room Type'].apply(clean_room_type) #apply with func
                all1['Room Type'] = all1['Room Type'].apply(lambda x: convert_room_type(x))
                all1['F/NRF'] = all1['Room'].apply(lambda x: convert_RF(x))
                all1['RO/ABF'] = all1['Room'].apply(lambda x: convert_ABF(x))
                all1['ADR'] = (all1['Total price']/all1['Length of stay'])/all1['Quantity'] # cal ADR
                all1['ADR'] = all1.apply(lambda row: apply_discount(row['Channel'], row['ADR']), axis=1) #apply function by row
                all1['RN'] = all1['Length of stay']*all1['Quantity']
                all1['ADR'] = all1.apply(calculate_adr_per_rn_abf, axis=1)

                all2 = all1[['Booking reference'
                            ,'Guest names'
                            ,'Check-in'
                            ,'Check-out'
                            ,'Channel'
                            ,'Booked'
                            ,'Total price'
                            ,'ADR'
                            ,'Length of stay'
                            ,'Lead time'
                            ,'RN'
                            ,'Quantity'
                            ,'Room'
                            ,'Room Type'
                            ,'RO/ABF'
                            ,'F/NRF'
                            ,'Lead time range'
                            ,'Lead time range1'
                            ,'LOS range']]
                return all2
            
            all2 =  perform(all) # perform data
            channels = all2['Channel'].unique() # To find unique Channel
            room_type_options = all2['Room Type'].unique().tolist() # To find unique Roomtype
            
            # to count booking by Channel, Room type
            counts = all2[['Channel', 'Room Type']].groupby(['Channel', 'Room Type']).size().reset_index(name='Count')
            total_count = counts['Count'].sum()
            fig = px.treemap(counts, path=['Channel', 'Room Type'], values='Count', color='Count',color_continuous_scale='YlOrRd') # treemap


            channels = all2['Channel'].unique()
            room_type_options =   all2['Room Type'].unique().tolist()
            selected_channels = st.sidebar.multiselect('Select channels', channels, default=channels) # multi select (sidebar)
            selected_room_types = st.sidebar.multiselect('Select room types', room_type_options, default=room_type_options)  # multi select (sidebar)
            
            #tab
            tab1, tab_stay = st.tabs(['**Book on date**','**Stay on date**'])
            with tab1:
                #select channel and roomtype
                if selected_channels:
                    filtered_df = all2[all2['Channel'].isin(selected_channels)]
                    filtered_df1 = all2[all2['Channel'].isin(selected_channels)]
                    if selected_room_types:
                        if 'All' not in selected_room_types:
                            filtered_df= filtered_df[filtered_df['Room Type'].isin(selected_room_types)]
                            filtered_df1= filtered_df1[filtered_df1['Room Type'].isin(selected_room_types)]
                    else:
                        if selected_room_types:
                            if 'All' not in selected_room_types:
                                filtered_df = all2[all2['Room Type'].isin(selected_room_types)]
                                filtered_df1 = all2[all2['Room Type'].isin(selected_room_types)]
                else:
                    # if do not select , show all
                    filtered_df = all2
                    filtered_df1 = all2
                # filtered_df by date
                col1,col2 = st.columns(2)
                with col1:
                    start_date = st.date_input('Select a start date', value=filtered_df['Booked'].min())
                with col2:
                    end_date = st.date_input('Select an end date', value=filtered_df['Booked'].max())
                filtered_df = filtered_df[(filtered_df['Booked'] >= pd.Timestamp(start_date)) & (filtered_df['Booked'] <= pd.Timestamp(end_date))]
                filtered_df1 = filtered_df1[(filtered_df1['Booked'] >= pd.Timestamp(start_date)) & (filtered_df1['Booked'] <= pd.Timestamp(end_date))]
                
                # filtered_df by variable
                col1 , col2 ,col3 = st.columns(3)
                with col2:
                    filter_LT = st.checkbox('Filter by LT ')
                    if filter_LT:
                        min_val, max_val = int(filtered_df['Lead time'].min()), int(filtered_df['Lead time'].max())
                        LT_min, LT_max = st.slider('Select a range of LT', min_val, max_val, (min_val, max_val))
                        filtered_df = filtered_df[(filtered_df['Lead time'] >= LT_min) & (filtered_df['Lead time'] <= LT_max)]
                        filtered_df1 = filtered_df1[(filtered_df1['Lead time'] >= LT_min) & (filtered_df1['Lead time'] <= LT_max)]
                    else:
                        filtered_df = filtered_df.copy()
                        filtered_df1 = filtered_df1.copy()
                with col1:
                    filter_LOS = st.checkbox('Filter by LOS ')
                    if filter_LOS:
                        min_val, max_val = int(filtered_df['Length of stay'].min()), int(filtered_df['Length of stay'].max())
                        LOS_min, LOS_max = st.slider('Select a range of LOS', min_val, max_val, (min_val, max_val))
                        filtered_df = filtered_df[(filtered_df['Length of stay'] >= LOS_min) & (filtered_df['Length of stay'] <= LOS_max)]
                        filtered_df1 = filtered_df1[(filtered_df1['Length of stay'] >= LOS_min) & (filtered_df1['Length of stay'] <= LOS_max)]
                    else:   
                        filtered_df = filtered_df.copy()
                        filtered_df1 = filtered_df1.copy()
                with col3:
                    filter_rn = st.checkbox('Filter by Roomnight')
                    if filter_rn:
                        min_val, max_val = int(filtered_df['RN'].min()), int(filtered_df['RN'].max())
                        rn_min, rn_max = st.slider('Select a range of roomnights', min_val, max_val, (min_val, max_val))
                        filtered_df = filtered_df[(filtered_df['RN'] >= rn_min) & (filtered_df['RN'] <= rn_max)]
                        filtered_df1 = filtered_df1[(filtered_df['RN'] >= rn_min) & (filtered_df1['RN'] <= rn_max)]
                    else:
                        filtered_df1 = filtered_df1.copy()
                # booked (overview) 
                if st.button('Overview (Booked)'):
                    tab1, tab2, tab3 ,tab4, tab5 , tab6 ,tab7,tab0,tab8,tab9= st.tabs(["Average", "Median", "Statistic",'Data'
                                                                    ,'Bar Chart','Room roomnight by channel'
                                                                    ,'Room revenue by channel','Room type by channel','Flexible/NRF','RO/ABF'])
                    with tab1:
                        col0,col00,col1, col2, col4 = st.columns(5)
                        filtered_df['ADR discount'] = filtered_df["ADR"]*filtered_df["Length of stay"]*filtered_df["Quantity"]
                        col0.metric('**Revenue**',f'{round(filtered_df["ADR discount"].sum(),0)}') # total Rev
                        min_booked = filtered_df["Booked"].min()
                        max_booked = filtered_df["Booked"].max()
                        per_period = (max_booked - min_booked).days
                        col00.metric('**Revenue per number of period(Booked)**',f'{round((filtered_df["ADR discount"].sum()/per_period),1)}')
                        col4.metric('**ADR with discount commission and ABF**',f'{round(filtered_df["ADR"].mean(),1)}',)
                        col1.metric("**A.LT**", f'{round(filtered_df["Lead time"].mean(),1)}')
                        col2.metric("**A.LOS**", f'{round(filtered_df["Length of stay"].mean(),1)}')
                    with tab2:
                        col1, col2, col3 = st.columns(3)
                        col3.metric('ADR with discount commission',f'{round(filtered_df["ADR"].median(),1)}')
                        col1.metric("A.LT", f'{round(filtered_df["Lead time"].median(),1)}')
                        col2.metric("A.LOS", f'{round(filtered_df["Length of stay"].median(),1)}')
                    with tab3:
                        st.write(filtered_df.describe()) #stat
                    with tab4:
                        st.write(filtered_df)
                    with tab5:
                        tab11, tab12, tab13, tab14 = st.tabs(['A.LT','A.LOS','A.RN','ADR by month'])
                        # bar table
                        with tab14:
                            # adr by month
                            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Booked'].dt.month_name()])['ADR'].mean().reset_index()
                            mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)
    
                            bar_chart = px.bar(mean_adr_by_month, x='Booked', y='ADR', color='Room Type',category_orders={'Booked': month_order},
                                text='ADR')
                            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                            st.plotly_chart(bar_chart, use_container_width=True)
                        with tab11:
                            # LT by month
                            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Booked'].dt.month_name()])['Lead time'].mean().reset_index()
                            mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)
    
                            bar_chart = px.bar(mean_adr_by_month, x='Booked', y='Lead time', color='Room Type',category_orders={'Booked': month_order},
                                text='Lead time')
                            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                            st.plotly_chart(bar_chart, use_container_width=True)
                        with tab12:
                            # LOS by month
                            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Booked'].dt.month_name()])['Length of stay'].mean().reset_index()
                            mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)
    
                            bar_chart = px.bar(mean_adr_by_month, x='Booked', y='Length of stay', color='Room Type',category_orders={'Booked': month_order},
                                text='Length of stay')
                            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                            st.plotly_chart(bar_chart, use_container_width=True)
                        with tab13:
                            # RN by month
                            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Booked'].dt.month_name()])['RN'].mean().reset_index()
                            mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)
    
                            bar_chart = px.bar(mean_adr_by_month, x='Booked', y='RN', color='Room Type',category_orders={'Booked': month_order},
                                text='RN')
                            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                            st.plotly_chart(bar_chart, use_container_width=True)
                    with tab6:
                        # treemap RN by ch,rt
                        counts = filtered_df[['Channel', 'Room Type','RN']].groupby(['Channel', 'Room Type']).sum().reset_index()
                        fig = px.treemap(counts, path=['Channel', 'Room Type','RN'], values='RN', color='RN',color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig, use_container_width=True)
                    with tab7:
                         # treemap Rev by ch,rt
                        counts = filtered_df[['Channel', 'Room Type','ADR discount']].groupby(['Channel', 'Room Type']).sum().reset_index()
                        fig = px.treemap(counts, path=['Channel', 'Room Type','ADR discount'], values='ADR discount', color='ADR discount',color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig, use_container_width=True)
                    with tab0:
                        # treemap count ch by ch,rt
                        counts = all2[['Channel', 'Room Type']].groupby(['Channel', 'Room Type']).size().reset_index(name='Count')
                        total_count = counts['Count'].sum()
                        fig = px.treemap(counts, path=['Channel', 'Room Type'], values='Count', color='Count',color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig, use_container_width=True)
                    with tab8:
                        # treemap F/NRF by ch,rt
                        counts = all2[['Channel','F/NRF']].groupby(['Channel', 'F/NRF']).size().reset_index(name='Count')
                        total_count = counts['Count'].sum()
                        fig = px.treemap(counts, path=['Channel', 'F/NRF'], values='Count', color='Count',color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig, use_container_width=True)
                    with tab9:
                        # treemap RO/ABF by ch,rt
                        counts = all2[['Channel','RO/ABF']].groupby(['Channel', 'RO/ABF']).size().reset_index(name='Count')
                        total_count = counts['Count'].sum()
                        fig = px.treemap(counts, path=['Channel', 'RO/ABF'], values='Count', color='Count',color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig, use_container_width=True)
                    # ADR by Room type and channel (Booked), ADR by Room type and channel (Stay)
                    table = filtered_df.copy()
                    table['Stay'] = table.apply(lambda row: pd.date_range(row['Check-in'], row['Check-out']- pd.Timedelta(days=1)), axis=1)
                    table = table.explode('Stay').reset_index(drop=True)
                    bb,ss = st.tabs(['**ADR by Room type and channel (Booked)**','**ADR by Room type and channel (Stay)**'])
                    with ss :
                        ADR_S,LT_S,LOS_S = st.tabs(['**ADR by channel and room type**','**LT by channel and room type**','**LOS by channel and room type**'])
                        with ADR_S:
                            st.markdown('**avg ADR without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                            df_january = table[['Stay','Channel','Room Type','ADR']]
                            avg_adr = df_january.groupby(['Channel', 'Room Type'])['ADR'].mean()
                            result = avg_adr.reset_index().pivot_table(values='ADR', index='Channel', columns='Room Type', fill_value=np.nan)
                            result.loc['Grand Total'] = result.mean()
                            result.at['Grand Total', 'Channel'] = 'Grand Total'
                            avg_adr_all_room_type = df_january.groupby(['Channel'])['ADR'].mean()
                            result['ALL ROOM TYPE'] = avg_adr_all_room_type
                            result = result.drop(columns='Channel')
                            result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                            st.write(result, use_container_width=True)
                        with LOS_S:
                            st.markdown('**avg LOS without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                            df_january = table[['Stay','Channel','Room Type','Length of stay']]
                            avg_adr = df_january.groupby(['Channel', 'Room Type'])['Length of stay'].mean()
                            result = avg_adr.reset_index().pivot_table(values='Length of stay', index='Channel', columns='Room Type', fill_value=np.nan)
                            result.loc['Grand Total'] = result.mean()
                            result.at['Grand Total', 'Channel'] = 'Grand Total'
                            avg_adr_all_room_type = df_january.groupby(['Channel'])['Length of stay'].mean()
                            result['ALL ROOM TYPE'] = avg_adr_all_room_type
                            result = result.drop(columns='Channel')
                            result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                            st.write(result, use_container_width=True)
                        with LT_S:
                            st.markdown('**avg LT without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                            df_january = table[['Stay','Channel','Room Type','Lead time']]
                            avg_adr = df_january.groupby(['Channel', 'Room Type'])['Lead time'].mean()
                            result = avg_adr.reset_index().pivot_table(values='Lead time', index='Channel', columns='Room Type', fill_value=np.nan)
                            result.loc['Grand Total'] = result.mean()
                            result.at['Grand Total', 'Channel'] = 'Grand Total'
                            avg_adr_all_room_type = df_january.groupby(['Channel'])['Lead time'].mean()
                            result['ALL ROOM TYPE'] = avg_adr_all_room_type
                            result = result.drop(columns='Channel')
                            result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                            st.write(result, use_container_width=True)
                    with bb :
                        ADR_S,LT_S,LOS_S = st.tabs(['**ADR by channel and room type**','**LT by channel and room type**','**LOS by channel and room type**'])
                        with ADR_S:
                            st.markdown('**avg ADR without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                            df_january = filtered_df[['Booked','Channel','Room Type','ADR']]
                            avg_adr = df_january.groupby(['Channel', 'Room Type'])['ADR'].mean()
                            result = avg_adr.reset_index().pivot_table(values='ADR', index='Channel', columns='Room Type', fill_value=np.nan)
                            result.loc['Grand Total'] = result.mean()
                            result.at['Grand Total', 'Channel'] = 'Grand Total'
                            avg_adr_all_room_type = df_january.groupby(['Channel'])['ADR'].mean()
                            result['ALL ROOM TYPE'] = avg_adr_all_room_type
                            result = result.drop(columns='Channel')
                            result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                            st.write(result, use_container_width=True)
                        with LOS_S:
                            st.markdown('**avg LOS without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                            df_january = filtered_df[['Booked','Channel','Room Type','Length of stay']]
                            avg_adr = df_january.groupby(['Channel', 'Room Type'])['Length of stay'].mean()
                            result = avg_adr.reset_index().pivot_table(values='Length of stay', index='Channel', columns='Room Type', fill_value=np.nan)
                            result.loc['Grand Total'] = result.mean()
                            result.at['Grand Total', 'Channel'] = 'Grand Total'
                            avg_adr_all_room_type = df_january.groupby(['Channel'])['Length of stay'].mean()
                            result['ALL ROOM TYPE'] = avg_adr_all_room_type
                            result = result.drop(columns='Channel')
                            result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                            st.write(result, use_container_width=True)
                        with LT_S:
                            st.markdown('**avg LT without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                            df_january = filtered_df[['Booked','Channel','Room Type','Lead time']]
                            avg_adr = df_january.groupby(['Channel', 'Room Type'])['Lead time'].mean()
                            result = avg_adr.reset_index().pivot_table(values='Lead time', index='Channel', columns='Room Type', fill_value=np.nan)
                            result.loc['Grand Total'] = result.mean()
                            result.at['Grand Total', 'Channel'] = 'Grand Total'
                            avg_adr_all_room_type = df_january.groupby(['Channel'])['Lead time'].mean()
                            result['ALL ROOM TYPE'] = avg_adr_all_room_type
                            result = result.drop(columns='Channel')
                            result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                            st.write(result, use_container_width=True)
                    # generate color        
                    channels = filtered_df['Channel'].unique()
                    num_colors = len(channels)
                    existing_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#6392FF']
                    additional_colors = ['#FFD700', '#8B008B', '#00FF00']
                    combined_colors = existing_colors + additional_colors
                    colors = combined_colors
                    color_scale =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}
                    color_scale1 =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}
                    
                    ch,rt = st.tabs(['Count Booked by Channel','Count Booked by Room type'])
                    with ch:
                        st.markdown('**Count Booked by Channel**')
                        grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
                        fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                        st.plotly_chart(fig,use_container_width=True)
                    with rt:
                        st.markdown('**Count Booked by Room type**')
                        grouped = filtered_df.groupby(['Booked', 'Room Type']).size().reset_index(name='counts')
                        fig = px.bar(grouped, x='Booked', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                        st.plotly_chart(fig,use_container_width=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        ch,rt = st.tabs(['Count LOS by Channel','Count LoS by Room type'])
                        with ch:
                            st.markdown('**Count LOS by Channel**')
                            grouped = filtered_df.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                        with rt:
                            st.markdown('**Count LOS by Room type**')
                            grouped = filtered_df.groupby(['Length of stay', 'Room Type']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Length of stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                    with col2:
                        ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                        with ch:
                            l1,l2,l3 = st.tabs(['Lead time (0-7)','Lead time (0-30)','Lead time non grouping'])
                            with l1:
                                st.markdown('**Count LT by Channel**')
                                grouped = filtered_df.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with l2:
                                st.markdown('**Count LT by Channel**')
                                grouped = filtered_df.groupby(['Lead time range1', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Lead time range1', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with l3:
                                st.markdown('**Count LT by Channel**')
                                grouped = filtered_df.groupby(['Lead time', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Lead time', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                        with rt:
                            l1,l2,l3 = st.tabs(['Lead time (0-7)','Lead time (0-30)','Lead time non grouping'])
                            with l1:
                                st.markdown('**Count LT by Room type**')
                                grouped = filtered_df.groupby(['Lead time range', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Lead time range', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with l2:
                                st.markdown('**Count LT by Room type**')
                                grouped = filtered_df.groupby(['Lead time range1', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Lead time range1', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with l3:
                                st.markdown('**Count LT by Room type**')
                                grouped = filtered_df.groupby(['Lead time', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Lead time', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                        
    
                        
                    filtered_df['Booked'] = pd.to_datetime(filtered_df['Booked'])
                    filtered_df['Day Name'] = filtered_df['Booked'].dt.strftime('%A')
                    filtered_df['Week of Year'] = filtered_df['Booked'].dt.isocalendar().week
    
    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('**count Booking in week of Year (calendar)**')
                        pt = filtered_df.pivot_table(index='Week of Year', columns='Day Name', aggfunc='size', fill_value=0)
                        if set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).issubset(filtered_df['Day Name'].unique()):
                            pt = filtered_df.pivot_table(index='Week of Year', columns='Day Name', aggfunc='size', fill_value=0)
                            pt = pt[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
                            st.write(pt.style.background_gradient(cmap='coolwarm', axis=1))
                        else:
                            st.write('Not enough data to create a pivot table')
    
                    with col2:
                        filtered_df0 =filtered_df[['Booked','RN']]
                        df_grouped = filtered_df0.groupby('Booked').sum().reset_index()
                        pivot_df = df_grouped.pivot_table(values='RN'
                                                , index=df_grouped['Booked'].dt.isocalendar().week
                                                , columns=df_grouped['Booked'].dt.day_name(), aggfunc='sum', fill_value=0)
                        st.markdown('**count Roomnight in week of Year (calendar)**')
                        if set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).issubset(filtered_df['Day Name'].unique()):
                            pt = pivot_df[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
                            st.write(pt.style.background_gradient(cmap='coolwarm', axis=1))
                        else:
                            st.write('Not enough data to create a pivot table')
                else:
                    st.write('---')
                
                
                st.markdown('**Insight (Pivot)**')
                booked_t,LT_t,LOS_t = st.tabs(['pivot by Booked','pivot by LT','pivot by LOS'])
                with booked_t:
                    st.markdown('**Pivot table by Booked**')
                    channels = filtered_df1['Channel'].unique()
                    num_colors = len(channels)
                    
                    existing_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#6392FF']
                    additional_colors = ['#FFD700', '#8B008B', '#00FF00']
                    combined_colors = existing_colors + additional_colors
                    colors = combined_colors
                    color_scale =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}

                    if st.button('ADR_Booked'):
                            col1, col2 = st.columns(2)
                            col1.markdown('**Average ADR by booked and Room Type**')
                            adr_avg = filtered_df1.groupby(['Booked', 'Room Type'])['ADR'].mean().reset_index()
                            fig = px.bar(adr_avg, x='Booked', y='ADR', color='Room Type',text_auto=True)
                            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                            col1.plotly_chart(fig, use_container_width=True)
                            col2.markdown('**Average ADR by booked**')
                            adr_avg = filtered_df1.groupby(['Booked'])['ADR'].mean().reset_index()
                            fig = px.bar(adr_avg, x='Booked', y='ADR',text_auto=True)
                            col2.plotly_chart(fig, use_container_width=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('**Count ADR by booked**')
                                grouped = filtered_df1.groupby(['Booked', 'ADR']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Booked', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with col2:
                                ch,rt = st.tabs(['Count Booked by Channel','Count Booked by Room type'])
                                with ch:
                                    st.markdown('**Count Booked by Channel**')
                                    grouped = filtered_df1.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with rt:
                                    st.markdown('**Count Booked by Room type**')
                                    grouped = filtered_df1.groupby(['Booked', 'Room Type']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Booked', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                    else:
                            st.write('---')
                        
                    if st.button('LT_BOOKED'):
                            col1, col2 = st.columns(2)
                            col1.markdown('**Average LT by booked and Room Type**')
                            adr_avg = filtered_df1.groupby(['Booked', 'Room Type'])['Lead time'].mean().reset_index()
                            fig = px.bar(adr_avg, x='Booked', y='Lead time', color='Room Type',text_auto=True)
                            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                            col1.plotly_chart(fig, use_container_width=True)
                            col2.markdown('**Average LT by booked**')
                            adr_avg = filtered_df1.groupby(['Booked'])['Lead time'].mean().reset_index()
                            fig = px.bar(adr_avg, x='Booked', y='Lead time',text_auto=True)
                            col2.plotly_chart(fig, use_container_width=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('**Count LT by booked**')
                                grouped = filtered_df1.groupby(['Booked', 'Lead time range']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Booked', y='counts', color='Lead time range',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with col2:
                                ch,rt = st.tabs(['Count Booked by Channel','Count Booked by Room type'])
                                with ch:
                                    st.markdown('**Count Booked by Channel**')
                                    grouped = filtered_df1.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with rt:
                                    st.markdown('**Count Booked by Room type**')
                                    grouped = filtered_df1.groupby(['Booked', 'Room Type']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Booked', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                    else:
                            st.write('---')
                        

                    if st.button('LOS_BOOKED'):
                            col1, col2 = st.columns(2)
                            col1.markdown('**Average LOS by booked and Room Type**')
                            adr_avg = filtered_df1.groupby(['Booked', 'Room Type'])['Length of stay'].mean().reset_index()
                            fig = px.bar(adr_avg, x='Booked', y='Length of stay', color='Room Type',text_auto=True)
                            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                            col1.plotly_chart(fig, use_container_width=True)
                            col2.markdown('**Average LOS by booked**')
                            adr_avg = filtered_df1.groupby(['Booked'])['Length of stay'].mean().reset_index()
                            fig = px.bar(adr_avg, x='Booked', y='Length of stay',text_auto=True)
                            col2.plotly_chart(fig, use_container_width=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('**Count LOS by booked**')
                                grouped = filtered_df1.groupby(['Booked', 'Length of stay']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Booked', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with col2:
                                ch,rt = st.tabs(['Count Booked by Channel','Count Booked by Room type'])
                                with ch:
                                    st.markdown('**Count Booked by Channel**')
                                    grouped = filtered_df1.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with rt:
                                    st.markdown('**Count Booked by Room type**')
                                    grouped = filtered_df1.groupby(['Booked', 'Room Type']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Booked', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                    else:
                            st.write('---')

                    if st.button('RN_BOOKED'):
                            col1, col2 = st.columns(2)
                            col1.markdown('**Average RN by booked and Room Type**')
                            adr_avg = filtered_df1.groupby(['Booked', 'Room Type'])['RN'].mean().reset_index()
                            fig = px.bar(adr_avg, x='Booked', y='RN', color='Room Type',text_auto=True)
                            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                            col1.plotly_chart(fig, use_container_width=True)
                            col2.markdown('**Average RN by booked**')
                            adr_avg = filtered_df1.groupby(['Booked'])['RN'].mean().reset_index()
                            fig = px.bar(adr_avg, x='Booked', y='RN',text_auto=True)
                            col2.plotly_chart(fig, use_container_width=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown('**Count RN by booked**')
                                grouped = filtered_df1.groupby(['Booked', 'RN']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Booked', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with col2:
                                ch,rt = st.tabs(['Count Booked by Channel','Count Booked by Room type'])
                                with ch:
                                    st.markdown('**Count Booked by Channel**')
                                    grouped = filtered_df1.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with rt:
                                    st.markdown('**Count Booked by Room type**')
                                    grouped = filtered_df1.groupby(['Booked', 'Room Type']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Booked', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                    else:
                            st.write('---')
                
                with LT_t:
                    st.markdown('**Pivot table by LT**')
                    channels = filtered_df1['Channel'].unique()
                    num_colors = len(channels)
                    existing_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#6392FF']
                    additional_colors = ['#FFD700', '#8B008B', '#00FF00']
                    combined_colors = existing_colors + additional_colors
                    colors = combined_colors
                    color_scale =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}

                    if st.button('ADR_LT'):
                            l1,l2,l3 = st.tabs(['Lead time (0-7)','Lead time (0-30)','Lead time non grouping'])
                            with l1:
                                col1, col2 = st.columns(2)
                                col1.markdown('**Average ADR by LT and Room Type**')
                                adr_avg = filtered_df1.groupby(['Lead time range', 'Room Type'])['ADR'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range', y='ADR', color='Room Type',text_auto=True)
                                fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                                col1.plotly_chart(fig, use_container_width=True)
                                col2.markdown('**Average ADR by LT**')
                                adr_avg = filtered_df1.groupby(['Lead time range'])['ADR'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range', y='ADR',text_auto=True)
                                col2.plotly_chart(fig, use_container_width=True)
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown('**Count ADR by LT**')
                                    grouped = filtered_df1.groupby(['Lead time range', 'ADR']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Lead time range', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with col2:
                                    ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                                    with ch:
                                        st.markdown('**Count LT by Channel**')
                                        grouped = filtered_df1.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                                    with rt:
                                        st.markdown('**Count LT by Room type**')
                                        grouped = filtered_df1.groupby(['Lead time range', 'Room Type']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                            with l2:
                                col1, col2 = st.columns(2)
                                #filtered_df1_pi = pd.pivot_table(filtered_df1, index='Booked',values=['ADR'])
                                col1.markdown('**Average ADR by LT and Room Type**')
                                #st.bar_chart(filtered_df1_pi)
                                adr_avg = filtered_df1.groupby(['Lead time range1', 'Room Type'])['ADR'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range1', y='ADR', color='Room Type',text_auto=True)
                                fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                                col1.plotly_chart(fig, use_container_width=True)
                                #filtered_df1_pi = pd.pivot_table(filtered_df1, index='Booked',values=['ADR'])
                                col2.markdown('**Average ADR by LT**')
                                #st.bar_chart(filtered_df1_pi)
                                adr_avg = filtered_df1.groupby(['Lead time range1'])['ADR'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range1', y='ADR',text_auto=True)
                                col2.plotly_chart(fig, use_container_width=True)    
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown('**Count ADR by LT**')
                                    grouped = filtered_df1.groupby(['Lead time range1', 'ADR']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Lead time range1', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with col2:
                                    ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                                    with ch:
                                        st.markdown('**Count LT by Channel**')
                                        grouped = filtered_df1.groupby(['Lead time range1', 'Channel']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range1', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                                    with rt:
                                        st.markdown('**Count LT by Room type**')
                                        grouped = filtered_df1.groupby(['Lead time range1', 'Room Type']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range1', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)      
                            with l3:
                                col1, col2 = st.columns(2)
                                col1.markdown('**Average ADR by LT and Room Type**')
                                adr_avg = filtered_df1.groupby(['Lead time', 'Room Type'])['ADR'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time', y='ADR', color='Room Type',text_auto=True)
                                fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                                col1.plotly_chart(fig, use_container_width=True)
                                col2.markdown('**Average ADR by LT**')
                                adr_avg = filtered_df1.groupby(['Lead time'])['ADR'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time', y='ADR',text_auto=True)
                                col2.plotly_chart(fig, use_container_width=True)    
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown('**Count ADR by LT**')
                                    grouped = filtered_df1.groupby(['Lead time', 'ADR']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Lead time', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with col2:
                                    ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                                    with ch:
                                        st.markdown('**Count LT by Channel**')
                                        grouped = filtered_df1.groupby(['Lead time', 'Channel']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                                    with rt:
                                        st.markdown('**Count LT by Room type**')
                                        grouped = filtered_df1.groupby(['Lead time', 'Room Type']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)                                                     
                    else:
                            st.write('---')

                    if st.button('LOS_LT'):
                            l1,l2,l3 = st.tabs(['Lead time (0-7)','Lead time (0-30)','Lead time non grouping'])
                            with l1:
                                col1, col2 = st.columns(2)
                                col1.markdown('**Average LOS by LT and Room Type**')
                                _avg = filtered_df1.groupby(['Lead time range', 'Room Type'])['Length of stay'].mean().reset_index()
                                fig = px.bar(_avg, x='Lead time range', y='Length of stay', color='Room Type',text_auto=True)
                                fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                                col1.plotly_chart(fig, use_container_width=True)
                                col2.markdown('**Average LOS by LT**')
                                adr_avg = filtered_df1.groupby(['Lead time range'])['Length of stay'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range', y='Length of stay',text_auto=True)
                                col2.plotly_chart(fig, use_container_width=True)
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown('**Count LOS by LT**')
                                    grouped = filtered_df1.groupby(['Lead time range', 'Length of stay']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Lead time range', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with col2:
                                    ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                                    with ch:
                                        st.markdown('**Count LT by Channel**')
                                        grouped = filtered_df1.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                                    with rt:
                                        st.markdown('**Count LT by Room type**')
                                        grouped = filtered_df1.groupby(['Lead time range', 'Room Type']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                            with l2:
                                col1, col2 = st.columns(2)
                                col1.markdown('**Average LOS by LT and Room Type**')
                                adr_avg = filtered_df1.groupby(['Lead time range1', 'Room Type'])['Length of stay'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range1', y='Length of stay', color='Room Type',text_auto=True)
                                fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                                col1.plotly_chart(fig, use_container_width=True)
                                col2.markdown('**Average LOS by LT**')
                                adr_avg = filtered_df1.groupby(['Lead time range1'])['Length of stay'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range1', y='Length of stay',text_auto=True)
                                col2.plotly_chart(fig, use_container_width=True)    
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown('**Count LOS by LT**')
                                    grouped = filtered_df1.groupby(['Lead time range1', 'Length of stay']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Lead time range1', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with col2:
                                    ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                                    with ch:
                                        st.markdown('**Count LT by Channel**')
                                        grouped = filtered_df1.groupby(['Lead time range1', 'Channel']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range1', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                                    with rt:
                                        st.markdown('**Count LT by Room type**')
                                        grouped = filtered_df1.groupby(['Lead time range1', 'Room Type']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range1', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)      
                            with l3:
                                col1, col2 = st.columns(2)
                                col1.markdown('**Average Length of stay by LT and Room Type**')
                                adr_avg = filtered_df1.groupby(['Lead time', 'Room Type'])['Length of stay'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time', y='Length of stay', color='Room Type',text_auto=True)
                                fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                                col1.plotly_chart(fig, use_container_width=True)
                                col2.markdown('**Average Length of stay by LT**')
                                adr_avg = filtered_df1.groupby(['Lead time'])['Length of stay'].mean().reset_index()
                                fig = px.bar(adr_avg, x='Lead time', y='Length of stay',text_auto=True)
                                col2.plotly_chart(fig, use_container_width=True)    
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown('**Count Length of stay by LT**')
                                    grouped = filtered_df1.groupby(['Lead time', 'Length of stay']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Lead time', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with col2:
                                    ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                                    with ch:
                                        st.markdown('**Count LT by Channel**')
                                        grouped = filtered_df1.groupby(['Lead time', 'Channel']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                                    with rt:
                                        st.markdown('**Count LT by Room type**')
                                        grouped = filtered_df1.groupby(['Lead time', 'Room Type']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                    else:
                            st.write('---')

                    if st.button('RN_LT'):
                            l1,l2,l3 = st.tabs(['Lead time (0-7)','Lead time (0-30)','Lead time non grouping'])
                            with l1:
                                col1, col2 = st.columns(2)
                                col1.markdown('**Count RN by LT and Room Type**')
                                _avg = filtered_df1.groupby(['Lead time range', 'Room Type'])['RN'].size().reset_index()
                                fig = px.bar(_avg, x='Lead time range', y='RN', color='Room Type',text_auto=True)
                                fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                                col1.plotly_chart(fig, use_container_width=True)
                                col2.markdown('**Count RN by LT**')
                                adr_avg = filtered_df1.groupby(['Lead time range'])['RN'].size().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range', y='RN',text_auto=True)
                                col2.plotly_chart(fig, use_container_width=True)
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown('**Count RN by LT**')
                                    grouped = filtered_df1.groupby(['Lead time range', 'RN']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Lead time range', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with col2:
                                    ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                                    with ch:
                                        st.markdown('**Count LT by Channel**')
                                        grouped = filtered_df1.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                                    with rt:
                                        st.markdown('**Count LT by Room type**')
                                        grouped = filtered_df1.groupby(['Lead time range', 'Room Type']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                            with l2:
                                col1, col2 = st.columns(2)
                                col1.markdown('**Count RN by LT and Room Type**')
                                adr_avg = filtered_df1.groupby(['Lead time range1', 'Room Type'])['RN'].size().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range1', y='RN', color='Room Type',text_auto=True)
                                fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                                col1.plotly_chart(fig, use_container_width=True)
                                col2.markdown('**Count RN by LT**')
                                adr_avg = filtered_df1.groupby(['Lead time range1'])['RN'].size().reset_index()
                                fig = px.bar(adr_avg, x='Lead time range1', y='RN',text_auto=True)
                                col2.plotly_chart(fig, use_container_width=True)    
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown('**Count RN by LT**')
                                    grouped = filtered_df1.groupby(['Lead time range1', 'RN']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Lead time range1', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with col2:
                                    ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                                    with ch:
                                        st.markdown('**Count LT by Channel**')
                                        grouped = filtered_df1.groupby(['Lead time range1', 'Channel']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range1', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                                    with rt:
                                        st.markdown('**Count LT by Room type**')
                                        grouped = filtered_df1.groupby(['Lead time range1', 'Room Type']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time range1', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)      
                            with l3:
                                col1, col2 = st.columns(2)
                                col1.markdown('**Count RN by LT and Room Type**')
                                adr_avg = filtered_df1.groupby(['Lead time', 'Room Type'])['RN'].size().reset_index()
                                fig = px.bar(adr_avg, x='Lead time', y='RN', color='Room Type',text_auto=True)
                                fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                                col1.plotly_chart(fig, use_container_width=True)
                                col2.markdown('**Count RN by LT**')
                                adr_avg = filtered_df1.groupby(['Lead time'])['RN'].size().reset_index()
                                fig = px.bar(adr_avg, x='Lead time', y='RN',text_auto=True)
                                col2.plotly_chart(fig, use_container_width=True)    
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown('**Count RN by LT**')
                                    grouped = filtered_df1.groupby(['Lead time', 'RN']).size().reset_index(name='counts')
                                    fig = px.bar(grouped, x='Lead time', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
                                    st.plotly_chart(fig,use_container_width=True)
                                with col2:
                                    ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                                    with ch:
                                        st.markdown('**Count LT by Channel**')
                                        grouped = filtered_df1.groupby(['Lead time', 'Channel']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True)
                                    with rt:
                                        st.markdown('**Count LT by Room type**')
                                        grouped = filtered_df1.groupby(['Lead time', 'Room Type']).size().reset_index(name='counts')
                                        fig = px.bar(grouped, x='Lead time', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                        st.plotly_chart(fig,use_container_width=True) 
                    else:
                            st.write('---')

                    if st.button('Portion_LT'): # portion (bar)
                            los_counts = filtered_df1['Lead time range'].value_counts().reset_index()
                            custom_order = ['-one', 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', '8-14', '14-30', '31-90', '90-120', '120+']
                            los_counts['sorting_order'] = pd.Categorical(los_counts['Lead time range'], categories=custom_order, ordered=True)
                            df_sorted = los_counts.sort_values('sorting_order')
                            df_sorted = df_sorted.drop('sorting_order', axis=1).reset_index(drop=True)
                            total_count = df_sorted['count'].sum()
                            total_count1 = los_counts['count'].sum()
                            los_counts['Percentage'] = (los_counts['count'] / total_count1) * 100
                            df_sorted['Percentage'] = (df_sorted['count'] / total_count1) * 100
                            los_counts = los_counts[['Lead time range','Percentage']]
                            color_mapping = {
                                            '-one': '#99f3bd',
                                            'zero': '#fbaccc',
                                            'one': '#a8df65',
                                            'two': '#ff7b54',
                                            'three': '#FFC300',
                                            'four': '#7FB3D5',
                                            'five': '#C70039',
                                            'six': '#900C3F',
                                            'seven': '#581845',
                                            '8-14': '#9C640C',
                                            '14-30': '#154360',
                                            '31-90': '#512E5F',
                                            '90-120': '#424949',
                                            '120+': '#FF5733'
                                        }
                            fig = px.bar(df_sorted, x='Lead time range', y='Percentage', title='Lead Time Range Distribution',text_auto=True,color='Lead time range',color_discrete_map=color_mapping)
                            fig1 = px.bar(los_counts, x='Lead time range', y='Percentage', title='Lead Time Range Distribution (Sorted)',text_auto=True,color='Lead time range',color_discrete_map=color_mapping)
                            fig.update_layout(xaxis_title='Lead Time Range', yaxis_title='Percentage')
                            fig1.update_layout(xaxis_title='Lead Time Range', yaxis_title='Percentage')
                            col1, col2 = st.columns(2)
                            col1.plotly_chart(fig,use_container_width=True)
                            col2.plotly_chart(fig1,use_container_width=True)
                    else:
                            st.write('---')

                    if st.button('Pie chart (LT)'):
                            los_counts = filtered_df1['Lead time range'].value_counts().reset_index()
                            los_counts.columns = ['Lead time range', 'Count']
                            los_counts = los_counts.sort_values('Lead time range')
                            fig = px.pie(los_counts, values='Count', names='Lead time range', 
                                title='Lead time range Distribution',
                                hole=0.4)
                            fig.update_traces(textposition='outside', textinfo='percent+label')
                            st.plotly_chart(fig,use_container_width=True)
                    else:
                            st.write('---')
                
                with LOS_t:
                    st.markdown('**Pivot table by LOS**')
                    channels = filtered_df1['Channel'].unique()
                    num_colors = len(channels)
                    existing_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#6392FF']
                    additional_colors = ['#FFD700', '#8B008B', '#00FF00']
                    combined_colors = existing_colors + additional_colors
                    colors = combined_colors
                    color_scale =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}

                    if st.button('ADR_LOS'):
                        col1, col2 = st.columns(2)
                        col1.markdown('**Average ADR by LOS and Room Type**')
                        adr_avg = filtered_df1.groupby(['Length of stay', 'Room Type'])['ADR'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Length of stay', y='ADR', color='Room Type',text_auto=True)
                        fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                        col1.plotly_chart(fig, use_container_width=True)
                        col2.markdown('**Average ADR by LOS**')
                        adr_avg = filtered_df1.groupby(['Length of stay'])['ADR'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Length of stay', y='ADR',text_auto=True)
                        col2.plotly_chart(fig, use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('**Count ADR by LOS**')
                            grouped = filtered_df1.groupby(['Length of stay', 'ADR']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Length of stay', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                        with col2:
                            ch,rt = st.tabs(['Count LOS by Channel','Count LoS by Room type'])
                            with ch:
                                st.markdown('**Count LOS by Channel**')
                                grouped = filtered_df1.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with rt:
                                st.markdown('**Count LOS by Room type**')
                                grouped = filtered_df1.groupby(['Length of stay', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Length of stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                    else:
                        st.write('---')

                    if st.button('LT_LOS'):
                        col1, col2 = st.columns(2)
                        col1.markdown('**Average LT by LOS and Room Type**')
                        adr_avg = filtered_df1.groupby(['Length of stay', 'Room Type'])['Lead time'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Length of stay', y='Lead time', color='Room Type',text_auto=True)
                        fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                        col1.plotly_chart(fig, use_container_width=True)
                        col2.markdown('**Average LT by LOS**')
                        adr_avg = filtered_df1.groupby(['Length of stay'])['Lead time'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Length of stay', y='Lead time',text_auto=True)
                        col2.plotly_chart(fig, use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('**Count LT by LOS**')
                            grouped = filtered_df1.groupby(['Length of stay', 'Lead time range']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Length of stay', y='counts', color='Lead time range',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                        with col2:
                            ch,rt = st.tabs(['Count LOS by Channel','Count LoS by Room type'])
                            with ch:
                                st.markdown('**Count LOS by Channel**')
                                grouped = filtered_df1.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with rt:
                                st.markdown('**Count LOS by Room type**')
                                grouped = filtered_df1.groupby(['Length of stay', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Length of stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                    else:
                        st.write('---')

                    if st.button('RN_LOS'):
                        col1, col2 = st.columns(2)
                        col1.markdown('**Average RN by LOS and Room Type**')
                        adr_avg = filtered_df1.groupby(['Length of stay', 'Room Type'])['RN'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Length of stay', y='RN', color='Room Type',text_auto=True)
                        fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                        col1.plotly_chart(fig, use_container_width=True)
                        col2.markdown('**Average RN by LOS**')
                        adr_avg = filtered_df1.groupby(['Length of stay'])['RN'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Length of stay', y='RN',text_auto=True)
                        col2.plotly_chart(fig, use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('**Count RN by LOS**')
                            grouped = filtered_df1.groupby(['Length of stay', 'RN']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Length of stay', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                        with col2:
                            ch,rt = st.tabs(['Count LOS by Channel','Count LoS by Room type'])
                            with ch:
                                st.markdown('**Count LOS by Channel**')
                                grouped = filtered_df1.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with rt:
                                st.markdown('**Count LOS by Room type**')
                                grouped = filtered_df1.groupby(['Length of stay', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Length of stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                    else:
                        st.write('---')

                    if st.button('Portion LOS'):
                        los_counts1 = filtered_df1['LOS range'].value_counts().reset_index()
                        custom_order1 = ['one', 'two', 'three', 'four', 'five', 'six','seven','eight', 'nine', 'ten', '14-30', '30-45', '60+']
                        los_counts1['sorting_order1'] = pd.Categorical(los_counts1['LOS range'], categories=custom_order1, ordered=True)
                        df_sorted1 = los_counts1.sort_values('sorting_order1')
                        df_sorted1 = df_sorted1.drop('sorting_order1', axis=1).reset_index(drop=True)
                        total_count1 = df_sorted1['count'].sum()
                        total_count1 = los_counts1['count'].sum()
                        color_mapping = {
                        'one': '#99f3bd',
                        'two': '#fbaccc',
                        'three': '#a8df65',
                        'four': '#ff7b54',
                        'five': '#FFC300',
                        'six': '#7FB3D5',
                        'seven': '#FF5733',
                        'eight': '#C70039',
                        'nine': '#900C3F',
                        'ten': '#581845',
                        '14-30': '#9C640C',
                        '30-45': '#154360',
                        '60+': '#512E5F'
                        }
                        los_counts1['Percentage'] = (los_counts1['count'] / total_count1) * 100
                        df_sorted1['Percentage'] = (df_sorted1['count'] / total_count1) * 100
                        los_counts1 = los_counts1[['LOS range','Percentage']]
                        fig = px.bar(df_sorted1, x='LOS range', y='Percentage', title='Length of stay Range Distribution',text_auto=True,color='LOS range',color_discrete_map=color_mapping)
                        fig1 = px.bar(los_counts1, x='LOS range', y='Percentage', title='Length of stay Range Distribution (Sorted)',text_auto=True,color='LOS range',color_discrete_map=color_mapping)
                        fig.update_layout(xaxis_title='Length of stay Range', yaxis_title='Percentage')
                        fig1.update_layout(xaxis_title='Length of stay Range', yaxis_title='Percentage')
                        col1, col2 = st.columns(2)
                        col1.plotly_chart(fig,use_container_width=True)
                        col2.plotly_chart(fig1,use_container_width=True)
                    else:
                        st.write('---')

                    if st.button('Pie chart (LOS)'):
                        los_counts = filtered_df1['Length of stay'].value_counts().reset_index()
                        los_counts.columns = ['Length of stay', 'Count']
                        los_counts = los_counts.sort_values('Length of stay')
                        fig = px.pie(los_counts, values='Count', names='Length of stay', 
                            title='Length of Stay Distribution',
                            hole=0.4)
                        fig.update_traces(textposition='outside', textinfo='percent+label')
                        st.plotly_chart(fig,use_container_width=True)
                    else:
                        st.write('---')

            with tab_stay:
                all3 =  perform(all)
                if selected_channels:
                    filtered_df = all3[all3['Channel'].isin(selected_channels)]
                    if selected_room_types:
                        if 'All' not in selected_room_types:
                            filtered_df = filtered_df[filtered_df['Room Type'].isin(selected_room_types)]
                    else:
                        if selected_room_types:
                            if 'All' not in selected_room_types:
                                filtered_df = all3[all3['Room Type'].isin(selected_room_types)]
                else:
                    filtered_df = all3
                table = filtered_df.copy()
                filtered_df['Stay'] = filtered_df.apply(lambda row: pd.date_range(row['Check-in'], row['Check-out']- pd.Timedelta(days=1)), axis=1)
                filtered_df = filtered_df.explode('Stay').reset_index(drop=True)
                filtered_df = filtered_df[['Stay','Check-in','Guest names','Channel','ADR','Length of stay','Lead time','Lead time range','RN','Quantity','Room Type','Room']]
                filtered_df['Day Name'] = filtered_df['Stay'].dt.strftime('%A')
                filtered_df['Week of Year'] = filtered_df['Stay'].dt.isocalendar().week

                col1,col2 = st.columns(2)
                with col1:
                    start_date = st.date_input('Select a start date ', value=filtered_df['Stay'].min())
                with col2:
                    end_date = st.date_input('Select an end date ', value=filtered_df['Stay'].max())
                filtered_df = filtered_df[(filtered_df['Stay'] >= pd.Timestamp(start_date)) & (filtered_df['Stay'] <= pd.Timestamp(end_date))]

                col1 , col2 = st.columns(2)
                with col2:
                    filter_LT = st.checkbox('Filter by LT')
                    if filter_LT:
                        min_val, max_val = int(filtered_df['Lead time'].min()), int(filtered_df['Lead time'].max())
                        LT_min, LT_max = st.slider('Select a range of LT', min_val, max_val, (min_val, max_val))
                        filtered_df = filtered_df[(filtered_df['Lead time'] >= LT_min) & (filtered_df['Lead time'] <= LT_max)]
                    else:
                        filtered_df = filtered_df.copy()
                with col1:
                    filter_LOS = st.checkbox('Filter by LOS')
                    if filter_LOS:
                        min_val, max_val = int(filtered_df['Length of stay'].min()), int(filtered_df['Length of stay'].max())
                        LOS_min, LOS_max = st.slider('Select a range of LOS', min_val, max_val, (min_val, max_val))
                        filtered_df = filtered_df[(filtered_df['Length of stay'] >= LOS_min) & (filtered_df['Length of stay'] <= LOS_max)]
                    else:
                        filtered_df = filtered_df.copy()
                
                if st.button('Overview  (Stay)'):
                    tab1, tab2, tab3 ,tab4, tab5 , tab6 ,tab7,tab8,tab9= st.tabs(["Average", "Median", "Statistic",'Data'
                                                                        ,'Bar Chart','Room roomnight by channel'
                                                                        ,'Room revenue by channel','Flexible/NRF','RO/ABF'])
                    with tab1:
                        col0,col00, col1, col2, col4 = st.columns(5)
                        filtered_df['ADR discount'] = filtered_df["ADR"]*filtered_df["Length of stay"]*filtered_df["Quantity"]
                        min_s = filtered_df["Stay"].min()
                        max_s = filtered_df["Stay"].max()
                        per_period = (max_s - min_s).days
                        col00.metric('**Revenue per number of period(Stay)**',f'{round((filtered_df["ADR discount"].sum()/per_period),1)}')
                        col0.metric('**Revenue**',f'{round(filtered_df["ADR discount"].sum(),0)}')
                        col4.metric('**ADR with discount commission and ABF**',f'{round(filtered_df["ADR"].mean(),1)}',)
                        col1.metric("**A.LT**", f'{round(filtered_df["Lead time"].mean(),1)}')
                        col2.metric("**A.LOS**", f'{round(filtered_df["Length of stay"].mean(),1)}')
                    with tab2:
                        col1, col2, col3 = st.columns(3)
                        col3.metric('ADR with discount commission',f'{round(filtered_df["ADR"].median(),1)}')
                        col1.metric("A.LT", f'{round(filtered_df["Lead time"].median(),1)}')
                        col2.metric("A.LOS", f'{round(filtered_df["Length of stay"].median(),1)}')
                    with tab3:
                        st.write(filtered_df.describe())
                    with tab4:
                        st.write(filtered_df)
                    with tab5:
                        tab11, tab12, tab13, tab14 = st.tabs(['A.LT','A.LOS','A.RN','ADR by month'])
                        with tab14:
                            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Stay'].dt.month_name()])['ADR'].mean().reset_index()
                            mean_adr_by_month['Stay'] = pd.Categorical(mean_adr_by_month['Stay'], categories=month_order)
    
                            bar_chart = px.bar(mean_adr_by_month, x='Stay', y='ADR', color='Room Type',category_orders={'Stay': month_order},
                                        text='ADR')
                            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                            st.plotly_chart(bar_chart, use_container_width=True)
                        with tab11:
                            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Stay'].dt.month_name()])['Lead time'].mean().reset_index()
                            mean_adr_by_month['Stay'] = pd.Categorical(mean_adr_by_month['Stay'], categories=month_order)
    
                            bar_chart = px.bar(mean_adr_by_month, x='Stay', y='Lead time', color='Room Type',category_orders={'Stay': month_order},
                                        text='Lead time')
                            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                            st.plotly_chart(bar_chart, use_container_width=True)
                        with tab12:
                            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Stay'].dt.month_name()])['Length of stay'].mean().reset_index()
                            mean_adr_by_month['Stay'] = pd.Categorical(mean_adr_by_month['Stay'], categories=month_order)
    
                            bar_chart = px.bar(mean_adr_by_month, x='Stay', y='Length of stay', color='Room Type',category_orders={'Stay': month_order},
                                    text='Length of stay')
                            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                            st.plotly_chart(bar_chart, use_container_width=True)
                        with tab13:
                            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Stay'].dt.month_name()])['RN'].mean().reset_index()
                            mean_adr_by_month['Stay'] = pd.Categorical(mean_adr_by_month['Stay'], categories=month_order)
    
                            bar_chart = px.bar(mean_adr_by_month, x='Stay', y='RN', color='Room Type',category_orders={'Stay': month_order},
                                        text='RN')
                            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
                            st.plotly_chart(bar_chart, use_container_width=True)
                    with tab6:
                        counts = filtered_df[['Channel', 'Room Type','RN']].groupby(['Channel', 'Room Type']).sum().reset_index()
                        fig = px.treemap(counts, path=['Channel', 'Room Type','RN'], values='RN', color='RN',color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig, use_container_width=True)
                    with tab7:
                        counts = filtered_df[['Channel', 'Room Type','ADR discount']].groupby(['Channel', 'Room Type']).sum().reset_index()
                        fig = px.treemap(counts, path=['Channel', 'Room Type','ADR discount'], values='ADR discount', color='ADR discount',color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig, use_container_width=True)
                    with tab8:
                        counts = all2[['Channel','F/NRF']].groupby(['Channel', 'F/NRF']).size().reset_index(name='Count')
                        total_count = counts['Count'].sum()
                        fig = px.treemap(counts, path=['Channel', 'F/NRF'], values='Count', color='Count',color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig, use_container_width=True)
                    with tab9:
                        counts = all2[['Channel','RO/ABF']].groupby(['Channel', 'RO/ABF']).size().reset_index(name='Count')
                        total_count = counts['Count'].sum()
                        fig = px.treemap(counts, path=['Channel', 'RO/ABF'], values='Count', color='Count',color_continuous_scale='YlOrRd')
                        st.plotly_chart(fig, use_container_width=True)
                    bb,ss = st.tabs(['**ADR by Room type and channel (Stay)**','**ADR by Room type and channel (Booked)**'])
                    with bb:
                        ADR_S,LT_S,LOS_S = st.tabs(['**ADR by channel and room type**','**LT by channel and room type**','**LOS by channel and room type**'])
                        with ADR_S:
                            st.markdown('**avg ADR without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                            df_january = filtered_df[['Stay','Channel','Room Type','ADR']]
                            avg_adr = df_january.groupby(['Channel', 'Room Type'])['ADR'].mean()
                            result = avg_adr.reset_index().pivot_table(values='ADR', index='Channel', columns='Room Type', fill_value=np.nan)
                            avg_adr_all_room_type = df_january.groupby(['Channel'])['ADR'].mean()
                            result['ALL ROOM TYPE'] = avg_adr_all_room_type
                            result.loc['GRAND TOTAL'] = result.mean()  # Calculate the grand total row
                            result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                            st.write(result, use_container_width=True)
                        with LOS_S:
                            st.markdown('**avg LOS without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                            df_january = filtered_df[['Stay','Channel','Room Type','Length of stay']]
                            avg_adr = df_january.groupby(['Channel', 'Room Type'])['Length of stay'].mean()
                            result = avg_adr.reset_index().pivot_table(values='Length of stay', index='Channel', columns='Room Type', fill_value=np.nan)
                            avg_adr_all_room_type = df_january.groupby(['Channel'])['Length of stay'].mean()
                            result['ALL ROOM TYPE'] = avg_adr_all_room_type
                            result.loc['GRAND TOTAL'] = result.mean()  # Calculate the grand total row
                            result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                            st.write(result, use_container_width=True)
                        with LT_S:
                            st.markdown('**avg LT without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                            df_january = filtered_df[['Stay','Channel','Room Type','Lead time']]
                            avg_adr = df_january.groupby(['Channel', 'Room Type'])['Lead time'].mean()
                            result = avg_adr.reset_index().pivot_table(values='Lead time', index='Channel', columns='Room Type', fill_value=np.nan)
                            avg_adr_all_room_type = df_january.groupby(['Channel'])['Lead time'].mean()
                            result['ALL ROOM TYPE'] = avg_adr_all_room_type
                            result.loc['GRAND TOTAL'] = result.mean()  # Calculate the grand total row
                            result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                            st.write(result, use_container_width=True)
                        with ss:
                            ADR_S,LT_S,LOS_S = st.tabs(['**ADR by channel and room type**','**LT by channel and room type**','**LOS by channal and room type**'])
                            with ADR_S:
                                st.markdown('**avg ADR without comm and ABF by channal and room type (if you do not filter month, it would be all month)**')
                                df_january = table[['Booked','Channel','Room Type','ADR']]
                                avg_adr = df_january.groupby(['Channel', 'Room Type'])['ADR'].mean()
                                result = avg_adr.reset_index().pivot_table(values='ADR', index='Channel', columns='Room Type', fill_value=np.nan)
                                result.loc['Grand Total'] = result.mean()
                                result.at['Grand Total', 'Channel'] = 'Grand Total'
                                avg_adr_all_room_type = df_january.groupby(['Channel'])['ADR'].mean()
                                result['ALL ROOM TYPE'] = avg_adr_all_room_type
                                result = result.drop(columns='Channel')
                                result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                                st.write(result, use_container_width=True)
                            with LOS_S:
                                st.markdown('**avg LOS without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                                df_january = table[['Booked','Channel','Room Type','Length of stay']]
                                avg_adr = df_january.groupby(['Channel', 'Room Type'])['Length of stay'].mean()
                                result = avg_adr.reset_index().pivot_table(values='Length of stay', index='Channel', columns='Room Type', fill_value=np.nan)
                                result.loc['Grand Total'] = result.mean()
                                result.at['Grand Total', 'Channel'] = 'Grand Total'
                                avg_adr_all_room_type = df_january.groupby(['Channel'])['Length of stay'].mean()
                                result['ALL ROOM TYPE'] = avg_adr_all_room_type
                                result = result.drop(columns='Channel')
                                result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                                st.write(result, use_container_width=True)
                            with LT_S:
                                st.markdown('**avg LT without comm and ABF by channel and room type (if you do not filter month, it would be all month)**')
                                df_january = table[['Booked','Channel','Room Type','Lead time']]
                                avg_adr = df_january.groupby(['Channel', 'Room Type'])['Lead time'].mean()
                                result = avg_adr.reset_index().pivot_table(values='Lead time', index='Channel', columns='Room Type', fill_value=np.nan)
                                result.loc['Grand Total'] = result.mean()
                                result.at['Grand Total', 'Channel'] = 'Grand Total'
                                avg_adr_all_room_type = df_january.groupby(['Channel'])['Lead time'].mean()
                                result['ALL ROOM TYPE'] = avg_adr_all_room_type
                                result = result.drop(columns='Channel')
                                result = result.applymap(lambda x: int(x) if not pd.isna(x) else np.nan)
                                st.write(result, use_container_width=True)
    
                    st.markdown('**You can zoom in**')
    
                    channels = filtered_df['Channel'].unique()
                    num_colors = len(channels)
                    existing_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#6392FF']
                    additional_colors = ['#FFD700', '#8B008B', '#00FF00']
                    combined_colors = existing_colors + additional_colors
                    colors = combined_colors
                    color_scale =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}
    
                    ch,rt = st.tabs(['Count Stay by Channel','Count Stay by Room type'])
                    with ch:
                        st.markdown('**Count Stay by Channel**')
                        grouped = filtered_df.groupby(['Stay', 'Channel']).size().reset_index(name='counts')
                        fig = px.bar(grouped, x='Stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                        st.plotly_chart(fig,use_container_width=True)
                    with rt:
                        st.markdown('**Count Stay by Room type**')
                        grouped = filtered_df.groupby(['Stay', 'Room Type']).size().reset_index(name='counts')
                        fig = px.bar(grouped, x='Stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                        st.plotly_chart(fig,use_container_width=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        ch,rt = st.tabs(['Count LOS by Channel','Count LOS by Room type'])
                        with ch:
                            st.markdown('**Count LOS by Channel**')
                            grouped = filtered_df.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                        with rt:
                            st.markdown('**Count LOS by Room type**')
                            grouped = filtered_df.groupby(['Length of stay', 'Room Type']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Length of stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                    with col2:
                        ch,rt = st.tabs(['Count LT by Channel','Count LT by Room type'])
                        with ch:
                            st.markdown('**Count LT by Channel**')
                            grouped = filtered_df.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                        with rt:
                            st.markdown('**Count LT by Room type**')
                            grouped = filtered_df.groupby(['Lead time range', 'Room Type']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Lead time range', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('**count Stay in week of Year (calendar)**')
                        pt = filtered_df.pivot_table(index='Week of Year', columns='Day Name', aggfunc='size')
                        if set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).issubset(filtered_df['Day Name'].unique()):
                            pt = filtered_df.pivot_table(index='Week of Year', columns='Day Name', aggfunc='size', fill_value=0)
                            pt = pt[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
                            st.write(pt.style.background_gradient(cmap='coolwarm', axis=1))
                        else:
                            st.write('Not enough data to create a pivot table')
                    with col2:
                        st.markdown('**A.LT that Check-in in week of Year (calendar)**')
                        grouped = filtered_df.groupby(['Week of Year', 'Day Name'])
                        averages = grouped['Lead time'].mean().reset_index()
                        pt = pd.pivot_table(averages, values='Lead time', index=['Week of Year'], columns=['Day Name'])
                        if set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).issubset(filtered_df['Day Name'].unique()):
                            pt = pt.loc[:, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
                            st.write(pt.style.format("{:.2f}").background_gradient(cmap='coolwarm', axis=1))
                        else:
                            st.write('Not enough data to create a pivot table')
                else :
                    st.write('---')

                if st.button('Insight (Stay)'):
                    st.markdown('**Pivot table by Stay**')
                    channels = filtered_df['Channel'].unique()
                    num_colors = len(channels)
                    existing_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#6392FF']
                    additional_colors = ['#FFD700', '#8B008B', '#00FF00']
                    combined_colors = existing_colors + additional_colors
                    colors = combined_colors
                    color_scale =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}
                    t1,t2,t3,t4 = st.tabs(['ADR','LT','LOS','RN'])
                    with t1:
                        col1, col2 = st.columns(2)
                        col1.markdown('**Average ADR by Stay and Room Type**')
                        adr_avg = filtered_df.groupby(['Stay', 'Room Type'])['ADR'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Stay', y='ADR', color='Room Type',text_auto=True)
                        fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                        col1.plotly_chart(fig, use_container_width=True)
                        col2.markdown('**Average ADR by Stay**')
                        adr_avg = filtered_df.groupby(['Stay'])['ADR'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Stay', y='ADR',text_auto=True)
                        col2.plotly_chart(fig, use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('**Count ADR by Stay**')
                            grouped = filtered_df.groupby(['Stay', 'ADR']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Stay', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                        with col2:
                            ch,rt = st.tabs(['Count Stay by Channel','Count Stay by Room type'])
                            with ch:
                                st.markdown('**Count Stay by Channel**')
                                grouped = filtered_df.groupby(['Stay', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with rt:
                                st.markdown('**Count Stay by Room type**')
                                grouped = filtered_df.groupby(['Stay', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
    
                    with t2:
                        col1, col2 = st.columns(2)
                        col1.markdown('**Average LT by Stay and Room Type**')
                        adr_avg = filtered_df.groupby(['Stay', 'Room Type'])['Lead time'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Stay', y='Lead time', color='Room Type',text_auto=True)
                        fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                        col1.plotly_chart(fig, use_container_width=True)
                        col2.markdown('**Average LT by Stay**')      
                        adr_avg = filtered_df.groupby(['Stay'])['Lead time'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Stay', y='Lead time',text_auto=True)
                        col2.plotly_chart(fig, use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('**Count LT by Stay**')
                            grouped = filtered_df.groupby(['Stay', 'Lead time range']).size().reset_index(name='counts')            
                            fig = px.bar(grouped, x='Stay', y='counts', color='Lead time range',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                            
                        with col2:
                            ch,rt = st.tabs(['Count Stay by Channel','Count Stay by Room type'])
                            with ch:
                                st.markdown('**Count Stay by Channel**')
                                grouped = filtered_df.groupby(['Stay', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with rt:
                                st.markdown('**Count Stay by Room type**')
                                grouped = filtered_df.groupby(['Stay', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                    with t3:
                        col1, col2 = st.columns(2)
                        col1.markdown('**Average LOS by Stay and Room Type**')
                        adr_avg = filtered_df.groupby(['Stay', 'Room Type'])['Length of stay'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Stay', y='Length of stay', color='Room Type',text_auto=True)
                        fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                        col1.plotly_chart(fig, use_container_width=True)
                        col2.markdown('**Average LOS by Stay**')
                        adr_avg = filtered_df.groupby(['Stay'])['Length of stay'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Stay', y='Length of stay',text_auto=True)
                        col2.plotly_chart(fig, use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('**Count LOS by Stay**')
                            grouped = filtered_df.groupby(['Stay', 'Length of stay']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Stay', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                        with col2:
                            ch,rt = st.tabs(['Count Stay by Channel','Count Stay by Room type'])
                            with ch:
                                st.markdown('**Count Stay by Channel**')
                                grouped = filtered_df.groupby(['Stay', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with rt:
                                st.markdown('**Count Stay by Room type**')
                                grouped = filtered_df.groupby(['Stay', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                    with t4:
                        col1, col2 = st.columns(2)
                        col1.markdown('**Average RN by Stay and Room Type**')
                        adr_avg = filtered_df.groupby(['Stay', 'Room Type'])['RN'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Stay', y='RN', color='Room Type',text_auto=True)
                        fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                        col1.plotly_chart(fig, use_container_width=True)
                        col2.markdown('**Average RN by Stay**')
                        adr_avg = filtered_df.groupby(['Stay'])['RN'].mean().reset_index()
                        fig = px.bar(adr_avg, x='Stay', y='RN',text_auto=True)
                        col2.plotly_chart(fig, use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown('**Count RN by Stay**')
                            grouped = filtered_df.groupby(['Stay', 'RN']).size().reset_index(name='counts')
                            fig = px.bar(grouped, x='Stay', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
                            st.plotly_chart(fig,use_container_width=True)
                        with col2:
                            ch,rt = st.tabs(['Count Stay by Channel','Count Stay by Room type'])
                            with ch:
                                st.markdown('**Count Stay by Channel**')
                                grouped = filtered_df.groupby(['Stay', 'Channel']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                            with rt:
                                st.markdown('**Count Stay by Room type**')
                                grouped = filtered_df.groupby(['Stay', 'Room Type']).size().reset_index(name='counts')
                                fig = px.bar(grouped, x='Stay', y='counts', color='Room Type',color_discrete_map=color_scale, barmode='stack')
                                st.plotly_chart(fig,use_container_width=True)
                else:
                    st.write('---')
else:
    st.markdown("**No file uploaded.**")
    st.markdown('Upload the file from the **SiteMinder**, then select the Reservations and select the data type **Booked-on** or **Check-in** according to your purpose. And finally, **do not** forget to filter only **Booked.**')
    st.markdown('**GUIDE**')
    st.markdown('-You can multiselect Channels. If you do not select anything, It would be All Channels')
    st.markdown('-You can multiselect Room Type. If you do not select anything, It would be All Room Type')
    st.markdown('**-NOTE**: Rev and ADR discount **Commission** and **ABF**')
    st.markdown('')
