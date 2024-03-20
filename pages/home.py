import streamlit as st
import datetime
import pandas as pd
import time
from streamlit_option_menu import option_menu

import mysql.connector
import streamlit_analytics

st.set_page_config(layout='wide')

def fetch_data_PNL():
    try:
        df = pd.read_csv('dropcopy_Dealer_PNL_mar_pinpout_scenario_sqlview.csv')
        df[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL']] = df[
            ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL']].round(2)
        return df
    except Exception as e:
        print(f'Error fetching the data: {str(e)}')
        return None

def style_dataframe_PNL(df):
    return df.style.applymap(
        lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: black'),
        subset=['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5',
                'PL_U0.5D0.5', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']
    ).format(precision=2)

def style_dataframe_SENTI(df):
    return df.style.applymap(
        lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: black'),
        subset=['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI', 'Senti_NOI']
    ).format(precision=2)

def style_dataframe_SENTI_QTY(df):
    return df.style.applymap(
        lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: black'),
        subset=['SentiQty_BFI', 'SentiQty_BOI', 'SentiQty_FFI', 'SentiQty_FOI', 'SentiQty_MFI', 'SentiQty_MOI',
                'SentiQty_NFI', 'SentiQty_NOI']
    ).format(precision=0)


def style_dataframe_SCENARIO(df):
    return df.style.applymap(
        lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: black'),
        subset=['PL_D10U5', 'PL_D5U2', 'PL_D2U1.5', 'PL_D1U1',
                'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PL_U1U0', 'PL_U2U1', 'PL_U5U2', 'PL_U10U5']
    )

def assign_zero_columns(df, columns_to_check):
    for column in columns_to_check:
        if column not in df.columns:
            df[column] = 0
    return df

def style_dataframe_NET_POSITION(df):
    return df.style.applymap(
        lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: black'),
        subset=['NET_Position']
    )

def time_difference_in_minutes(dt1, dt2):
    timedelta = dt2 - dt1
    return (timedelta.total_seconds() // 60)

try:
    if st.session_state["my_input"]:

        logout = st.button('Logout')

        if logout:
            st.markdown('<span style="color: black;">Please go to login in the side menu</span>',
                        unsafe_allow_html=True)
            st.session_state["my_input"] = None
            # st.experimental_rerun()
            exit(0)

        selected = option_menu(
            menu_title=None,
            options=['PNL', 'SENTI', 'SENTI QUANTITY', 'SCENARIO', 'NET POSITION'],
            default_index=0,  # default selected navigation
            orientation='horizontal'
        )

        if selected == 'PNL':
            st.title("PNL DASHBOARD")

            # Create placeholders for dynamic data
            time_display_pnl = st.empty()
            time_delay_alert = st.empty()
            total_dataframe_placeholder_pnl = st.empty()
            pnl_team_placeholder_pnl = st.empty()
            pnl_dataframe_placeholder_pnl = st.empty()
            filtered_dataframe_placeholder_pnl = st.empty()

            while True:
                try:
                    pnl = fetch_data_PNL()

                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data_fetch_time = pnl['DT'].iloc[0]
                    del pnl['DT']

                    data_fetch_time = pd.to_datetime(data_fetch_time)
                    current_time_dt = pd.to_datetime(current_time)
                    time_diff_min = time_difference_in_minutes(current_time_dt, data_fetch_time)
                    time_diff_min = abs(time_diff_min)

                    # Update time_display placeholder
                    time_display_pnl.write(f'CT {current_time}   |   PNL Time {data_fetch_time}', format='md')


                    if pnl is not None:

                        if st.session_state['my_input'] == 'JAI':
                            pnl = pnl.loc[pnl['Team'].isin(['JAI', 'JAS', 'JPT'])]

                        elif st.session_state['my_input'] == 'VEO':
                            pnl = pnl.loc[pnl['Team'].isin(['VEO', 'VEC', 'VSS'])]

                        elif st.session_state['my_input'] == 'HEO':
                            pnl = pnl.loc[pnl['Team'].isin(['HEO', 'HEC'])]

                        elif st.session_state['my_input'] == 'HDO':
                            pnl = pnl.loc[pnl['Team'].isin(['HDO', 'HDC'])]

                        elif st.session_state['my_input'] == 'GQO':
                            pnl = pnl.loc[pnl['Team'].isin(['GQO', 'GQC', 'GQS'])]

                        elif st.session_state['my_input'] == 'KKD':
                            pnl = pnl.loc[pnl['Team'].isin(['KKC', 'KKD'])]

                        elif st.session_state['my_input'] == 'NAI':
                            pnl = pnl.loc[pnl['Team'].isin(['NAF', 'NAI', 'NAS'])]

                        elif st.session_state['my_input'] == 'SIO':
                            pnl = pnl.loc[pnl['Team'].isin(['SIA', 'SIC', 'SIO'])]

                        else:
                            pnl = pnl.loc[pnl['Team'].isin([st.session_state["my_input"]])]

                        # Team wise PNL
                        pnl_team = pnl[['Team', 'Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D0.5U0.5',
                                        'PL_U0.5D0.5', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']].groupby(
                            by=['Team']).sum().reset_index()


                        # total PNL(sum)
                        total_pnl = pnl_team.select_dtypes(include=['number']).sum().reset_index()

                        total_pnl = pd.pivot_table(total_pnl, columns='index', values=0)

                        pnl = pnl[['Team', 'Name', 'Mrg', 'Y_PNL', 'E_PNL', 'O_PNL',
                                   'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout', 'Actual',
                                   'ExpOptVal', 'With_Exch']]

                        # create dummy column with * to get same data frame column sizes
                        size_values = pnl['Name'].apply(lambda x: len(x))
                        filler_size = size_values.max() + 2
                        pnl_team['Name'] = '*' * filler_size

                        total_pnl['Team'] = 'Total'
                        total_pnl['Name'] = '*' * filler_size

                        total_pnl = total_pnl[['Team', 'Name', 'Mrg', 'Y_PNL', 'E_PNL', 'O_PNL',
                                               'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout', 'Actual',
                                               'ExpOptVal', 'With_Exch']]

                        pnl_team = pnl_team[['Team', 'Name', 'Mrg', 'Y_PNL', 'E_PNL', 'O_PNL',
                                             'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout', 'Actual',
                                             'ExpOptVal', 'With_Exch']]

                        pnl = pnl[['Team', 'Name', 'Mrg', 'Y_PNL', 'E_PNL', 'O_PNL',
                                   'I_PNL', 'T_PNL', 'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PinPout', 'Actual',
                                   'ExpOptVal', 'With_Exch']]


                        pnl_team = pnl_team.sort_values(by='Mrg', ascending=False)

                        # remove wrong index
                        pnl.reset_index(inplace=True)
                        del pnl['index']

                        # for the below teams display total frame also else no total frame.
                        if ((st.session_state['my_input'] == 'JAI') or (st.session_state['my_input'] == 'VEO')
                                or (st.session_state['my_input'] == 'HEO') or
                                (st.session_state['my_input'] == 'HDO') or (st.session_state['my_input'] == 'GQO')
                                or (st.session_state['my_input'] == 'KKD') or (st.session_state['my_input'] == 'NAI')
                                or (st.session_state['my_input'] == 'SIO')):
                            # Create styled Data Frames
                            total_styled_df = style_dataframe_PNL(total_pnl)
                            pnl_team_styled_df = style_dataframe_PNL(pnl_team)
                            pnl_styled_df = style_dataframe_PNL(pnl)

                            # Update dataframe placeholder
                            total_dataframe_placeholder_pnl.dataframe(total_styled_df, width=5000)
                            pnl_team_placeholder_pnl.dataframe(pnl_team_styled_df, width=5000)
                            pnl_dataframe_placeholder_pnl.dataframe(pnl_styled_df, width=5000)

                        else:
                            # Create styled Data Frames
                            # total_styled_df = style_dataframe_PNL(total_pnl)
                            pnl_team_styled_df = style_dataframe_PNL(pnl_team)
                            pnl_styled_df = style_dataframe_PNL(pnl)

                            # Update dataframe placeholder
                            # total_dataframe_placeholder_pnl.dataframe(total_styled_df, width=5000)
                            pnl_team_placeholder_pnl.dataframe(pnl_team_styled_df, width=5000)
                            pnl_dataframe_placeholder_pnl.dataframe(pnl_styled_df, width=5000)

                    # Sleep for 3 seconds before the next update
                    time.sleep(3)

                except Exception as e:
                    print('Issue:', e)
                    time.sleep(1)
                    pass

        if selected == 'SENTI':
            st.title('SENTI')

            # Create placeholders for dynamic content
            time_display_senti = st.empty()
            time_delay_alert = st.empty()
            todo_dataframe_placeholder_senti = st.empty()
            total_dataframe_placeholder_senti = st.empty()
            team_client_dataframe_placeholder_senti = st.empty()
            filtered_dataframe_placeholder_senti = st.empty()

            while True:
                try:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Fetch data
                    senti = pd.read_csv('Senti.csv')
                    time_frame = senti['DT'].iloc[0]
                    del senti['DT']

                    time_frame = pd.to_datetime(time_frame)
                    current_time_dt = pd.to_datetime(current_time)
                    time_diff_min = time_difference_in_minutes(current_time_dt, time_frame)
                    time_diff_min = abs(time_diff_min)

                    # Update time_display placeholder
                    time_display_senti.write(f'CT {current_time}   |   SENTI Time {time_frame}', format='md')

                    if st.session_state['my_input'] == 'JAI':
                        senti = senti.loc[senti['Team'].isin(['JAI', 'JAS', 'JPT'])]

                    elif st.session_state['my_input'] == 'VEO':
                        senti = senti.loc[senti['Team'].isin(['VEO', 'VEC', 'VSS'])]

                    elif st.session_state['my_input'] == 'HEO':
                        senti = senti.loc[senti['Team'].isin(['HEO', 'HEC'])]

                    elif st.session_state['my_input'] == 'HDO':
                        senti = senti.loc[senti['Team'].isin(['HDO', 'HDC'])]

                    elif st.session_state['my_input'] == 'GQO':
                        senti = senti.loc[senti['Team'].isin(['GQO', 'GQC', 'GQS'])]

                    elif st.session_state['my_input'] == 'KKD':
                        senti = senti.loc[senti['Team'].isin(['KKC', 'KKD'])]

                    elif st.session_state['my_input'] == 'NAI':
                        senti = senti.loc[senti['Team'].isin(['NAF', 'NAI', 'NAS'])]

                    elif st.session_state['my_input'] == 'SIO':
                        senti = senti.loc[senti['Team'].isin(['SIA', 'SIC', 'SIO'])]

                    else:
                        senti = senti.loc[senti['Team'].isin([st.session_state["my_input"]])]

                    # If no senti for given team, then display empty frames and pass to next iteration,
                    # until we get senti for given team it displays empty frames.
                    if not (len(senti) > 0):
                        todo_dataframe_placeholder_senti.dataframe(senti, width=5000)
                        total_dataframe_placeholder_senti.dataframe(senti, width=5000)
                        team_client_dataframe_placeholder_senti.dataframe(senti, width=5000)
                        filtered_dataframe_placeholder_senti.dataframe(senti, width=5000)
                        pass

                    # If senti available for given team.
                    if senti is not None:
                        # Calculate and append totals row
                        # select numeric type columns and sum them
                        totals_row = senti.select_dtypes(include=['number']).sum()
                        totals_df = pd.DataFrame()
                        totals_df = totals_df.append(totals_row, ignore_index=True)
                        totals_df.reset_index(inplace=True)
                        totals_df.rename(columns={'index': 'Name'}, inplace=True)
                        totals_df['Name'] = 'Total'
                        del totals_df['ClientCode']

                        team_client_df = senti.groupby(by=['Team', 'ClientCode']).sum().reset_index()

                        totals_df['AccountName'] = 'Total'
                        totals_df['Team'] = 'Total'
                        totals_df['Type'] = 'DC'
                        totals_df['ClientCode'] = 'Total'
                        totals_df['Index'] = 'Total'

                        team_client_df['AccountName'] = 'Total'
                        team_client_df['Type'] = 'DC'
                        team_client_df['Index'] = 'Total'

                        totals_df = totals_df[
                            ['AccountName', 'Index', 'Team', 'Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                             'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                             'Senti_NOI', 'Type', 'ClientCode']]

                        team_client_df = team_client_df[
                            ['AccountName', 'Index', 'Team', 'Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                             'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                             'Senti_NOI', 'Type', 'ClientCode']]


                        senti.reset_index(inplace=True)
                        del senti['index']

                        todo_df = totals_df.copy()

                        # add limits to todo_df based on given family
                        if st.session_state['my_input'] == 'NAV':
                            todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                     'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                                     'Senti_NOI']] = (-50) - todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                                                      'Senti_FOI', 'Senti_MFI', 'Senti_MOI',
                                                                      'Senti_NFI',
                                                                      'Senti_NOI']]
                        elif st.session_state['my_input'] == 'KAL':
                            todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                     'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                                     'Senti_NOI']] = (-50) - todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                                                      'Senti_FOI', 'Senti_MFI', 'Senti_MOI',
                                                                      'Senti_NFI',
                                                                      'Senti_NOI']]

                        elif st.session_state['my_input'] == 'DIO':
                            todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                     'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                                     'Senti_NOI']] = (-10) - todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                                                      'Senti_FOI', 'Senti_MFI', 'Senti_MOI',
                                                                      'Senti_NFI',
                                                                      'Senti_NOI']]

                        else:
                            todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                     'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                                     'Senti_NOI']] = (-300) - todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                                                       'Senti_FOI', 'Senti_MFI', 'Senti_MOI',
                                                                       'Senti_NFI',
                                                                       'Senti_NOI']]

                        todo_df['AccountName'] = 'Todo'
                        todo_df['Team'] = 'Todo'
                        todo_df['Type'] = 'Todo'
                        todo_df['ClientCode'] = 'Todo'
                        todo_df['Index'] = 'Todo'

                        # Style the frames
                        todo_styled_df = style_dataframe_SENTI(todo_df)
                        totals_styled_df = style_dataframe_SENTI(totals_df)
                        team_client_styled_df = style_dataframe_SENTI(team_client_df)
                        filtered_styled_df = style_dataframe_SENTI(senti)

                        # update placeholders
                        todo_dataframe_placeholder_senti.dataframe(todo_styled_df, width=5000)
                        total_dataframe_placeholder_senti.dataframe(totals_styled_df, width=5000)
                        team_client_dataframe_placeholder_senti.dataframe(team_client_styled_df, width=5000)
                        filtered_dataframe_placeholder_senti.dataframe(filtered_styled_df, width=5000)
                    # Sleep for 3 seconds before the next update
                    time.sleep(3)

                except Exception as e:
                    print('Issue:', e)
                    time.sleep(1)
                    pass

        if selected == 'SENTI QUANTITY':
            st.title('SENTI QUANTITY')

            # Create placeholders for dynamic content
            time_display_senti_qty = st.empty()
            time_delay_alert = st.empty()
            todo_dataframe_placeholder_senti_qty = st.empty()
            total_dataframe_placeholder_senti_qty = st.empty()
            team_client_dataframe_placeholder_senti_qty = st.empty()
            filtered_dataframe_placeholder_senti_qty = st.empty()

            while True:
                try:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Fetch data
                    senti_qty = pd.read_csv('sentiQty.csv')

                    all_columns = ['AccountName', 'Team', 'SentiQty_BFI', 'SentiQty_BOI', 'SentiQty_FFI',
                                   'SentiQty_FOI', 'SentiQty_MFI', 'SentiQty_MOI', 'SentiQty_NFI',
                                   'SentiQty_NOI', 'Type', 'ClientCode', 'DT']

                    # assign unavailable columns as 0
                    senti_qty = assign_zero_columns(senti_qty, all_columns)

                    time_frame = senti_qty['DT'].iloc[0]
                    del senti_qty['DT']

                    time_frame = pd.to_datetime(time_frame)
                    current_time_dt = pd.to_datetime(current_time)
                    time_diff_min = time_difference_in_minutes(current_time_dt, time_frame)
                    time_diff_min = abs(time_diff_min)

                    # Update time_display placeholder
                    time_display_senti_qty.write(f'CT {current_time}   |  SENTI QTY Time {time_frame}', format='md')

                    if st.session_state['my_input'] == 'JAI':
                        senti_qty = senti_qty.loc[senti_qty['Team'].isin(['JAI', 'JAS', 'JPT'])]

                    elif st.session_state['my_input'] == 'VEO':
                        senti_qty = senti_qty.loc[senti_qty['Team'].isin(['VEO', 'VEC', 'VSS'])]

                    elif st.session_state['my_input'] == 'HEO':
                        senti_qty = senti_qty.loc[senti_qty['Team'].isin(['HEO', 'HEC'])]

                    elif st.session_state['my_input'] == 'HDO':
                        senti_qty = senti_qty.loc[senti_qty['Team'].isin(['HDO', 'HDC'])]

                    elif st.session_state['my_input'] == 'GQO':
                        senti_qty = senti_qty.loc[senti_qty['Team'].isin(['GQO', 'GQC', 'GQS'])]

                    elif st.session_state['my_input'] == 'KKD':
                        senti_qty = senti_qty.loc[senti_qty['Team'].isin(['KKC', 'KKD'])]

                    elif st.session_state['my_input'] == 'NAI':
                        senti_qty = senti_qty.loc[senti_qty['Team'].isin(['NAF', 'NAI', 'NAS'])]

                    elif st.session_state['my_input'] == 'SIO':
                        senti_qty = senti_qty.loc[senti_qty['Team'].isin(['SIA', 'SIC', 'SIO'])]

                    else:
                        senti_qty = senti_qty.loc[senti_qty['Team'].isin([st.session_state["my_input"]])]

                    # If no senti for given team, then display empty frames and pass to next iteration,
                    # until we get senti for given team it displays empty frames.
                    if not (len(senti_qty) > 0):
                        todo_dataframe_placeholder_senti_qty.dataframe(senti_qty, width=5000)
                        total_dataframe_placeholder_senti_qty.dataframe(senti_qty, width=5000)
                        team_client_dataframe_placeholder_senti_qty.dataframe(senti_qty, width=5000)
                        filtered_dataframe_placeholder_senti_qty.dataframe(senti_qty, width=5000)
                        pass

                    # If senti available for given team.
                    if senti_qty is not None:

                        # Calculate and append totals row
                        totals_row = senti_qty.select_dtypes(include=['number']).sum()
                        totals_df = pd.DataFrame()
                        totals_df = totals_df.append(totals_row, ignore_index=True)
                        totals_df.reset_index(inplace=True)
                        totals_df.rename(columns={'index': 'Name'}, inplace=True)
                        totals_df['Name'] = 'Total'
                        del totals_df['ClientCode']

                        team_client_df = senti_qty.groupby(by=['Team', 'ClientCode']).sum().reset_index()

                        totals_df['AccountName'] = 'Total'
                        totals_df['Team'] = 'Total'
                        totals_df['Type'] = 'DC'
                        totals_df['ClientCode'] = 'Total'
                        totals_df['Index'] = 'Total'

                        team_client_df['AccountName'] = 'Total'
                        team_client_df['Type'] = 'DC'
                        team_client_df['Index'] = 'Total'

                        totals_df = totals_df[
                            ['AccountName', 'Index', 'Team', 'SentiQty_BFI', 'SentiQty_BOI', 'SentiQty_FFI',
                             'SentiQty_FOI', 'SentiQty_MFI', 'SentiQty_MOI', 'SentiQty_NFI',
                             'SentiQty_NOI', 'Type', 'ClientCode']]

                        team_client_df = team_client_df[
                            ['AccountName', 'Index', 'Team', 'SentiQty_BFI', 'SentiQty_BOI', 'SentiQty_FFI',
                             'SentiQty_FOI', 'SentiQty_MFI', 'SentiQty_MOI', 'SentiQty_NFI',
                             'SentiQty_NOI', 'Type', 'ClientCode']]


                        senti = pd.read_csv('Senti.csv')
                        # Read quantity_fetch_time.csv
                        # time_frame = senti['DT'].iloc[0]
                        del senti['DT']

                        if st.session_state['my_input'] == 'JAI':
                            senti = senti.loc[senti['Team'].isin(['JAI', 'JAS', 'JPT'])]

                        elif st.session_state['my_input'] == 'VEO':
                            senti = senti.loc[senti['Team'].isin(['VEO', 'VEC', 'VSS'])]

                        elif st.session_state['my_input'] == 'HEO':
                            senti = senti.loc[senti['Team'].isin(['HEO', 'HEC'])]

                        elif st.session_state['my_input'] == 'HDO':
                            senti = senti.loc[senti['Team'].isin(['HDO', 'HDC'])]

                        elif st.session_state['my_input'] == 'GQO':
                            senti = senti.loc[senti['Team'].isin(['GQO', 'GQC', 'GQS'])]

                        elif st.session_state['my_input'] == 'KKD':
                            senti = senti.loc[senti['Team'].isin(['KKC', 'KKD'])]

                        elif st.session_state['my_input'] == 'NAI':
                            senti = senti.loc[senti['Team'].isin(['NAF', 'NAI', 'NAS'])]

                        elif st.session_state['my_input'] == 'SIO':
                            senti = senti.loc[senti['Team'].isin(['SIA', 'SIC', 'SIO'])]

                        else:
                            senti = senti.loc[senti['Team'].isin([st.session_state["my_input"]])]

                        # Calculate and append totals row
                        totals_row_senti = senti.select_dtypes(include=['number']).sum()
                        totals_df_senti = pd.DataFrame()
                        totals_df_senti = totals_df_senti.append(totals_row_senti, ignore_index=True)
                        totals_df_senti.reset_index(inplace=True)
                        totals_df_senti.rename(columns={'index': 'Name'}, inplace=True)
                        totals_df_senti['Name'] = 'Total'
                        del totals_df_senti['ClientCode']

                        team_client_df_senti = senti.groupby(by=['Team', 'ClientCode']).sum().reset_index()

                        totals_df_senti['AccountName'] = 'Total'
                        totals_df_senti['Team'] = 'Total'
                        totals_df_senti['Type'] = 'DC'
                        totals_df_senti['ClientCode'] = 'Total'
                        totals_df_senti['Index'] = 'Total'
                        # totals_df['Name'] = 'DC'

                        team_client_df_senti['AccountName'] = 'Total'
                        team_client_df_senti['Type'] = 'DC'
                        team_client_df_senti['Index'] = 'Total'
                        # team_client_df['Name'] = 'DC'

                        # totals_df['AccountName', 'Team', 'Type' 'ClientCode'] = 'Total'
                        # team_client_df['AccountName', 'Team', 'Type' 'ClientCode'] = 'Total'

                        totals_df_senti = totals_df_senti[
                            ['AccountName', 'Index', 'Team', 'Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                             'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                             'Senti_NOI', 'Type', 'ClientCode']]

                        team_client_df_senti = team_client_df_senti[
                            ['AccountName', 'Index', 'Team', 'Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                             'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                             'Senti_NOI', 'Type', 'ClientCode']]

                        todo_df = totals_df_senti.copy()

                        if st.session_state['my_input'] == 'NAV':
                            todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                     'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                                     'Senti_NOI']] = (-50) - todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                                                      'Senti_FOI', 'Senti_MFI', 'Senti_MOI',
                                                                      'Senti_NFI',
                                                                      'Senti_NOI']]
                        elif st.session_state['my_input'] == 'KAL':
                            todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                     'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                                     'Senti_NOI']] = (-50) - todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                                                      'Senti_FOI', 'Senti_MFI', 'Senti_MOI',
                                                                      'Senti_NFI',
                                                                      'Senti_NOI']]

                        elif st.session_state['my_input'] == 'DIO':
                            todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                     'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                                     'Senti_NOI']] = (-10) - todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                                                      'Senti_FOI', 'Senti_MFI', 'Senti_MOI',
                                                                      'Senti_NFI',
                                                                      'Senti_NOI']]

                        else:
                            todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                     'Senti_FOI', 'Senti_MFI', 'Senti_MOI', 'Senti_NFI',
                                     'Senti_NOI']] = (-300) - todo_df[['Senti_BFI', 'Senti_BOI', 'Senti_FFI',
                                                                       'Senti_FOI', 'Senti_MFI', 'Senti_MOI',
                                                                       'Senti_NFI',
                                                                       'Senti_NOI']]

                        todo_df['AccountName'] = 'Todo'
                        todo_df['Team'] = 'Todo'
                        todo_df['Type'] = 'Todo'
                        todo_df['ClientCode'] = 'Todo'
                        todo_df['Index'] = 'Todo'

                        senti_price = pd.read_csv('Fut_Settle_Price.csv', header=None)
                        NIFTY_price = senti_price.loc[senti_price[0] == 'NIFTY', 1].iloc[0]
                        BANKNIFTY_price = senti_price.loc[senti_price[0] == 'BANKNIFTY', 1].iloc[0]
                        FINNIFTY_price = senti_price.loc[senti_price[0] == 'FINNIFTY', 1].iloc[0]
                        MIDCPNIFTY_price = senti_price.loc[senti_price[0] == 'MIDCPNIFTY', 1].iloc[0]

                        todo_df['Senti_BFI'] = (todo_df['Senti_BFI'] / BANKNIFTY_price) * 10000000
                        todo_df['Senti_BOI'] = (todo_df['Senti_BOI'] / BANKNIFTY_price) * 10000000
                        todo_df['Senti_FFI'] = (todo_df['Senti_FFI'] / FINNIFTY_price) * 10000000
                        todo_df['Senti_FOI'] = (todo_df['Senti_FOI'] / FINNIFTY_price) * 10000000
                        todo_df['Senti_MFI'] = (todo_df['Senti_MFI'] / MIDCPNIFTY_price) * 10000000
                        todo_df['Senti_MOI'] = (todo_df['Senti_MOI'] / MIDCPNIFTY_price) * 10000000
                        todo_df['Senti_NFI'] = (todo_df['Senti_NFI'] / NIFTY_price) * 10000000
                        todo_df['Senti_NOI'] = (todo_df['Senti_NOI'] / NIFTY_price) * 10000000

                        todo_df.rename(columns={'Senti_BFI': 'SentiQty_BFI', 'Senti_BOI': 'SentiQty_BOI',
                                                'Senti_FFI': 'SentiQty_FFI', 'Senti_FOI': 'SentiQty_FOI',
                                                'Senti_MFI': 'SentiQty_MFI', 'Senti_MOI': 'SentiQty_MOI',
                                                'Senti_NFI': 'SentiQty_NFI', 'Senti_NOI': 'SentiQty_NOI'},
                                       inplace=True)


                        senti_qty.reset_index(inplace=True)
                        del senti_qty['index']

                        todo_styled_df = style_dataframe_SENTI_QTY(todo_df)
                        totals_styled_df = style_dataframe_SENTI_QTY(totals_df)
                        team_client_styled_df = style_dataframe_SENTI_QTY(team_client_df)
                        senti_qty = style_dataframe_SENTI_QTY(senti_qty)

                        todo_dataframe_placeholder_senti_qty.dataframe(todo_styled_df, width=5000)
                        total_dataframe_placeholder_senti_qty.dataframe(totals_styled_df, width=5000)
                        team_client_dataframe_placeholder_senti_qty.dataframe(team_client_styled_df, width=5000)
                        filtered_dataframe_placeholder_senti_qty.dataframe(senti_qty, width=5000)
                    # Sleep for 3 seconds before the next update
                    time.sleep(3)

                except Exception as e:
                    print('Issue:', e)
                    time.sleep(1)
                    pass

        if selected == 'SCENARIO':
            st.title('SCENARIO')

            # Create placeholders for dynamic content
            time_display_scenario = st.empty()
            time_delay_alert = st.empty()
            total_dataframe_placeholder_scenario = st.empty()
            scenario_team_placeholder = st.empty()
            scenario_dataframe_placeholder = st.empty()
            filtered_dataframe_placeholder_scenario = st.empty()

            while True:
                try:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Read quantity_fetch_time.csv
                    scenario = pd.read_csv(
                        'Dealer_Data_All_PLdealer_dropcopy.csv')
                    fetch_time = pd.to_datetime(scenario['DT'].iloc[-1].split('_')[0])
                    del scenario['DT']

                    fetch_time = pd.to_datetime(fetch_time)
                    current_time_dt = pd.to_datetime(current_time)
                    time_diff_min = time_difference_in_minutes(current_time_dt, fetch_time)
                    time_diff_min = abs(time_diff_min)

                    # Update time_display placeholder
                    time_display_scenario.write(f'CT {current_time}   |   SCENARIO Time {fetch_time}',
                                                format='md')


                    if st.session_state['my_input'] == 'JAI':
                        scenario = scenario.loc[scenario['Team'].isin(['JAI', 'JAS', 'JPT'])]

                    elif st.session_state['my_input'] == 'VEO':
                        scenario = scenario.loc[scenario['Team'].isin(['VEO', 'VEC', 'VSS'])]

                    elif st.session_state['my_input'] == 'HEO':
                        scenario = scenario.loc[scenario['Team'].isin(['HEO', 'HEC'])]

                    elif st.session_state['my_input'] == 'HDO':
                        scenario = scenario.loc[scenario['Team'].isin(['HDO', 'HDC'])]

                    elif st.session_state['my_input'] == 'GQO':
                        scenario = scenario.loc[scenario['Team'].isin(['GQO', 'GQC', 'GQS'])]

                    elif st.session_state['my_input'] == 'KKD':
                        scenario = scenario.loc[scenario['Team'].isin(['KKC', 'KKD'])]

                    elif st.session_state['my_input'] == 'NAI':
                        scenario = scenario.loc[scenario['Team'].isin(['NAF', 'NAI', 'NAS'])]

                    elif st.session_state['my_input'] == 'SIO':
                        scenario = scenario.loc[scenario['Team'].isin(['SIA', 'SIC', 'SIO'])]

                    else:
                        scenario = scenario.loc[scenario['Team'].isin([st.session_state["my_input"]])]

                    # If no scenario for given team, then display empty frames and pass to next iteration,
                    # until we get scenario for given team it displays empty frames.
                    if not (len(scenario) > 0):
                        scenario_team_placeholder.dataframe(scenario, width=5000)
                        scenario_dataframe_placeholder.dataframe(scenario, width=5000)
                        pass

                    scenario_team = scenario[['Team', 'PL_D10U5', 'PL_D5U2', 'PL_D2U1.5', 'PL_D1U1',
                                              'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PL_U1U0', 'PL_U2U1', 'PL_U5U2',
                                              'PL_U10U5']].groupby(
                        by=['Team']).sum().reset_index()

                    scenario_team[['PL_D10U5', 'PL_D5U2', 'PL_D2U1.5', 'PL_D1U1',
                                   'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PL_U1U0', 'PL_U2U1', 'PL_U5U2', 'PL_U10U5']] = \
                    scenario_team[
                        ['PL_D10U5', 'PL_D5U2', 'PL_D2U1.5', 'PL_D1U1',
                         'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PL_U1U0', 'PL_U2U1', 'PL_U5U2', 'PL_U10U5']].astype(int)

                    total_scenario = scenario_team.select_dtypes(include=['number']).sum().reset_index()

                    total_scenario = pd.pivot_table(total_scenario, columns='index', values=0)

                    total_scenario['Team'] = 'Total'
                    total_scenario['Name'] = 'Total'

                    total_scenario = total_scenario[
                        ['Team', 'Name', 'PL_D10U5', 'PL_D5U2', 'PL_D2U1.5', 'PL_D1U1',
                         'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PL_U1U0', 'PL_U2U1', 'PL_U5U2', 'PL_U10U5']]

                    scenario = scenario[['Team', 'Name', 'PL_D10U5', 'PL_D5U2', 'PL_D2U1.5', 'PL_D1U1',
                                         'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PL_U1U0', 'PL_U2U1', 'PL_U5U2', 'PL_U10U5']]

                    # create dummy column with * to get same data frame column sizes
                    size_values = scenario['Name'].apply(lambda x: len(x))
                    filler_size = size_values.max() + 2
                    scenario_team['Name'] = '*' * filler_size

                    total_scenario['Name'] = '*' * filler_size

                    scenario_team = scenario_team[
                        ['Team', 'Name', 'PL_D10U5', 'PL_D5U2', 'PL_D2U1.5', 'PL_D1U1',
                         'PL_D0.5U0.5', 'PL_U0.5D0.5', 'PL_U1U0', 'PL_U2U1', 'PL_U5U2', 'PL_U10U5']]

                    # remove wrong index
                    scenario.reset_index(inplace=True)
                    del scenario['index']

                    # for the below teams display total frame also else no total frame.
                    if ((st.session_state['my_input'] == 'JAI') or (st.session_state['my_input'] == 'VEO')
                            or (st.session_state['my_input'] == 'HEO') or
                            (st.session_state['my_input'] == 'HDO') or (st.session_state['my_input'] == 'GQO')
                            or (st.session_state['my_input'] == 'KKD') or (st.session_state['my_input'] == 'NAI')
                            or (st.session_state['my_input'] == 'SIO')):

                        # Create styled Data Frames
                        total_styled_df = style_dataframe_SCENARIO(total_scenario)
                        scenario_team_styled_df = style_dataframe_SCENARIO(scenario_team)
                        scenario_styled_df = style_dataframe_SCENARIO(scenario)

                        # Update dataframe placeholder
                        total_dataframe_placeholder_scenario.dataframe(total_styled_df, width=5000)
                        scenario_team_placeholder.dataframe(scenario_team_styled_df, width=5000)
                        scenario_dataframe_placeholder.dataframe(scenario_styled_df, width=5000)

                    else:
                        # Create styled Data Frames
                        scenario_team_styled_df = style_dataframe_SCENARIO(scenario_team)
                        scenario_styled_df = style_dataframe_SCENARIO(scenario)

                        # Update dataframe placeholder
                        # total_dataframe_placeholder_scenario.dataframe(total_styled_df, width=5000)
                        scenario_team_placeholder.dataframe(scenario_team_styled_df, width=5000)
                        scenario_dataframe_placeholder.dataframe(scenario_styled_df, width=5000)


                except Exception as e:
                    print('Error:', e)
                    time.sleep(1)
                    pass

                # Sleep for 3 seconds before the next update
                time.sleep(3)

        if selected == 'NET POSITION':
            st.title('NET POSITION')

            # Create placeholders for dynamic content
            time_display_net_position = st.empty()
            time_delay_alert = st.empty()
            total_dataframe_placeholder_net_position = st.empty()
            net_position_team_placeholder = st.empty()
            net_position_dataframe_placeholder = st.empty()
            filtered_dataframe_placeholder_net_position = st.empty()

            while True:
                try:
                    # Read quantity_fetch_time.csv
                    net_position = pd.read_csv('pnl_sqlview_DT.csv')
                    net_position['DT'] = net_position['DT'].astype(str)
                    fetch_time = pd.to_datetime(net_position['DT'].iloc[0].split('_')[0])
                    del net_position['DT']

                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    fetch_time = pd.to_datetime(fetch_time)
                    current_time_dt = pd.to_datetime(current_time)
                    time_diff_min = time_difference_in_minutes(current_time_dt, fetch_time)
                    time_diff_min = abs(time_diff_min)

                    # Update time_display placeholder
                    time_display_net_position.write(f'CT {current_time}   |   NET POSITION time {fetch_time}',
                                                    format='md')


                    net_position['CFQty'] = net_position['Qty_Today'] + net_position['Qty_pvs']

                    net_position = \
                        net_position.groupby(by=['Team', 'Name', 'ScripName', 'ExpiryDate', 'StrikePrice', 'CPType'])[
                            ['CFQty']].sum()
                    net_position.reset_index(inplace=True)
                    net_position.rename(columns={'CFQty': 'NET_Position'}, inplace=True)

                    net_position['NET_Position'] = net_position['NET_Position'].astype(int)
                    net_position['StrikePrice'] = net_position['StrikePrice'].astype(int)

                    if st.session_state['my_input'] == 'JAI':
                        net_position = net_position.loc[net_position['Team'].isin(['JAI', 'JAS', 'JPT'])]

                    elif st.session_state['my_input'] == 'VEO':
                        net_position = net_position.loc[net_position['Team'].isin(['VEO', 'VEC', 'VSS'])]

                    elif st.session_state['my_input'] == 'HEO':
                        net_position = net_position.loc[net_position['Team'].isin(['HEO', 'HEC'])]

                    elif st.session_state['my_input'] == 'HDO':
                        net_position = net_position.loc[net_position['Team'].isin(['HDO', 'HDC'])]

                    elif st.session_state['my_input'] == 'GQO':
                        net_position = net_position.loc[net_position['Team'].isin(['GQO', 'GQC', 'GQS'])]

                    elif st.session_state['my_input'] == 'KKD':
                        net_position = net_position.loc[net_position['Team'].isin(['KKC', 'KKD'])]

                    elif st.session_state['my_input'] == 'NAI':
                        net_position = net_position.loc[net_position['Team'].isin(['NAF', 'NAI', 'NAS'])]

                    elif st.session_state['my_input'] == 'SIO':
                        net_position = net_position.loc[net_position['Team'].isin(['SIA', 'SIC', 'SIO'])]

                    else:
                        net_position = net_position.loc[net_position['Team'].isin([st.session_state["my_input"]])]

                    # If no net position for given team, then display empty frames and pass to next iteration,
                    # until we get net position for given team it displays empty frames.
                    if not (len(net_position) > 0):
                        net_position_team_placeholder.dataframe(net_position, width=5000)
                        pass

                    net_position = net_position.loc[net_position['NET_Position'] != 0]

                    # remove wrong index
                    net_position.reset_index(inplace=True)
                    del net_position['index']

                    net_position_styled_df = style_dataframe_NET_POSITION(net_position)

                    # Update dataframe placeholder
                    net_position_team_placeholder.dataframe(net_position_styled_df, width=5000)

                    name = net_position_dataframe_placeholder.selectbox('Select Name', net_position['Name'].unique())

                    if name:
                        net_position_filtered = net_position.loc[net_position['Name'] == name]
                        # remove wrong index
                        net_position_filtered.reset_index(inplace=True)
                        del net_position_filtered['index']

                        net_position_filtered_styled = style_dataframe_NET_POSITION(net_position_filtered)
                        filtered_dataframe_placeholder_net_position.dataframe(net_position_filtered_styled, width=5000)

                except Exception as e:
                    print('Error:', e)
                    time.sleep(1)
                    pass

                # Sleep for 3 seconds before the next update
                time.sleep(3)

except KeyError:
    # Handle the KeyError when the key is not found in session state
    st.error('User not Logged in')
    st.markdown('<span style="color: blue;">Please go to login in the side menu</span>', unsafe_allow_html=True)
    time.sleep(1)
    pass

except Exception as e:
    # Handle all other exceptions
    st.write(e)
    time.sleep(1)
    pass


