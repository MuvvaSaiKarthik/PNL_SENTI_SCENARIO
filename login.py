
import streamlit as st
import pandas as pd
# import streamlit_analytics
# from streamlit import runtime
# from streamlit.runtime.scriptrunner import get_script_run_ctx
import datetime

st.set_page_config(layout='wide')

st.title('PNL SENTI SCENARIO LOGIN')
# st.sidebar.success('Select a page')

PNL = pd.read_csv('dropcopy_Dealer_PNL_mar_pinpout_scenario_sqlview.csv')
teams = PNL['Team'].unique()
passwords = teams.copy()
passwords = passwords + '@321'

user_credentials = dict(zip(teams, passwords))

# NEW
user_credentials['ANG'] = 'ANG@1147'
user_credentials['DEL'] = 'DEL@5613'
user_credentials['GQO'] = 'GQO@61614'
user_credentials['KAR'] = 'KAR@13321'
user_credentials['KKD'] = 'KKD@992'
user_credentials['KLC'] = 'KLC@14156'
user_credentials['MUK'] = 'MUK@10188'
user_credentials['NAI'] = 'NAI@18513'
user_credentials['NIM'] = 'NIM@1059'
user_credentials['SHR'] = 'SHR@241323'
user_credentials['SIO'] = 'SIO@14410'
user_credentials['VIK'] = 'VIK@281517'
user_credentials['VIP'] = 'VIP@16310'
user_credentials['VIY'] = 'VIY@291632'

# EXISTING
user_credentials['JAI'] = 'LALIT@RAHUL'
user_credentials['JAS'] = 'HARSHIL@TEJAS'
user_credentials['VEO'] = 'SRINIVAS@CHINTAN'
user_credentials['HDO'] = 'HFT@987'
user_credentials['HEO'] = 'GAURAV@987'
user_credentials['KAL'] = 'KALPESH@123'
user_credentials['NAV'] = 'NAVNEET@456'
user_credentials['DIO'] = 'DINESH@321'


# user_credentials = {
#     "JAI": "LALIT@RAHUL",
#     "HDO": "HDO@321",
#     "DEL": "DEL@321",
#     "JAS": "HARSHIT@TEJAS",
#     "NAV": "NAV@321",
#     "JPT": "JPT@321",
#     "NAS": "NAS@321",
#     "VEO": "SRINIVAS@CHINTAN",
#     "KAL": "KAL@321",
#     "SIO": "SIO@321",
#     "VIK": "VIK@321",
#     "NAI": "NAI@321",
#     "KPT": "KPT@321",
#     "HDC": "HDC@321",
#     "MUK": "MUK@321",
#     "GQO": "GQO@321",
#     "SIC": "SIC@321",
#     "NAF": "NAF@321",
#     "VIY": "VIY@321",
#     "SHR": "SHR@321",
#     "VEC": "VEC@321",
#     "GQC": "GQC@321",
#     "KKD": "KKD@321",
#     "KKC": "KKC@321",
#     "VSS": "VSS@321",
#     "BKC": "BKC@321",
#     "SIA": "SIA@321",
#     "SIX": "SIX@321",
#     "RON": "RON@321",
#     "NIM": "NIM@321",
#     "KLC": "KLC@321",
#     "KAR": "KAR@321",
#     "HEO": "HEO@321",
#     "HEC": "HEC@321",
#     "VIP": "VIP@321",
#     "GQS": "GQS@321",
#     "LIC": "LIC@321",
#     "DIO": "DIO@321",
#     "ITT": "ITT@321"
#     # Add more entries as needed
# }


# # File to store access log
# log_file_all = "C:\\Users\\Administrator\\Documents\\streamlit_analytics\\pnl_senti_scenario_8000_access_all.log"
# log_file_tabs = "C:\\Users\\Administrator\\Documents\\streamlit_analytics\\pnl_senti_scenario_8000_access_tabs.log"


# # Function to log access
# def log_access_all(ip_address, my_input):
#     with open(log_file_all, "a") as f:
#         timestamp = datetime.datetime.now()
#         f.write(f"Timestamp: {timestamp}, IP Address: {ip_address}, USER ID: {my_input}\n")

# def log_access_tabs(ip_address, my_input):
#     with open(log_file_tabs, "a") as f:
#         timestamp = datetime.datetime.now()
#         f.write(f"Timestamp: {timestamp}, IP Address: {ip_address}, USER ID: {my_input}\n")

# def get_remote_ip() -> str:
#     """Get remote ip."""
#     try:
#         ctx = get_script_run_ctx()
#         if ctx is None:
#             return None

#         session_info = runtime.get_instance().get_client(ctx.session_id)
#         if session_info is None:
#             return None
#     except Exception as e:
#         return None

#     return session_info.request.remote_ip

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""


if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

username = st.text_input('Username')
password = st.text_input('Password', type='password')

my_input = username

login = st.button('Login')

# log_access_tabs(get_remote_ip(), my_input)

if login:
    if username in user_credentials and user_credentials[username] == password:
        st.success("Login successful!")
        st.markdown('<span style="color: blue;">Click on home in side menu to see the data</span>', unsafe_allow_html=True)
        st.session_state["my_input"] = my_input
        # log_access_all(get_remote_ip(), my_input)
        # st.write("You have entered: ", my_input)

    else:
        st.error("Invalid credentials. Please try again.")
