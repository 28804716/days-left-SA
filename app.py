
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 08:47:29 2025

@author: user
"""

import streamlit as st
import datetime as dt
import numpy as np
from num2words import num2words

st.set_page_config(page_title="Small Utilities.", layout="wide")

st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:",
    ["Days Left Until...", "Numbers To Words", "Other"],
)

public_holidays = [[1,1,"New Year’s Day"],
[21,3,"Human Rights Day"],
[18,4,"Good Friday"],
[21,4,"Family Day"],
[27,4,"Freedom Day"],
[1,5,"Workers' Day"],
[16,6,"Youth Day"],
[9,8,"National Women’s Day"],
[24,9,"Heritage Day"],
[16,12,"Day of Reconciliation"],
[25,12,"Christmas Day"],
[26,12,"Day of Goodwill"]]


if menu =="Days Left Until...":

    startdate = st.date_input("Start Date", value="today", min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, kwargs=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
    stopdate = st.date_input("End Date", value=dt.datetime(2026,1,4), min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, kwargs=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
    
    diff = np.busday_count(startdate,stopdate,weekmask= "Mon Tue Wed Thu Fri")
    n_ph = 0
    public_holidays_active=[]
    for year in range(startdate.year,stopdate.year+1):
        for ph in public_holidays:
            ph_date=dt.date(year,ph[1],ph[0])
            if ph_date > startdate and ph_date < stopdate:
                if ph_date.weekday() != 5:
                    n_ph=n_ph+1
                    public_holidays_active.append([ph_date,ph[2]])
    
    st.markdown(f"# *{diff-n_ph}!*")
    
    st.markdown(f"There are **{diff-n_ph}** business days between **{startdate.strftime('%A %d %B %Y')}** and **{stopdate.strftime('%A %d %B %Y')}**.")
    st.write(f"({n_ph} public holidays)")
    
    with st.expander("Public Holidays (South Africa)", expanded=False,icon=None):
        for ph in public_holidays_active:
            st.markdown(f"{ph[0].strftime('%Y/%m/%d')} : **{ph[1]}**")
elif menu =="Numbers To Words":
    st.markdown("Number")
    number = st.number_input("Number to translate", min_value=0.0, max_value=None, value=123456789.10, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  placeholder=None, disabled=False, label_visibility="visible")
    number_word=num2words(number,to='currency').replace('euro,','Rand, and').title().replace(',','').replace('-',' ').upper()
    st.write("Words:")
    st.write(f"{number_word}")
