#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 08:47:29 2025

@author: user
"""

import streamlit as st
ss=st.session_state


import datetime as dt
import numpy as np
from num2words import num2words
import pandas as pd

import random
from st_keyup import st_keyup

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

random.seed(to_integer(dt.date.today()))

n_sonnet=random.randint(0, 153)

p=""

with open('sonnets.txt', 'r') as file:
    # Read each line in the file
    for i,line in enumerate(file):
        if i == n_sonnet:
            p=line
            break

def n_to_r(n):
    return (num2words(n,to='currency').replace('euro,','Rand,').title()).upper().replace('-',' ')

st.set_page_config(page_title="Small Utilities.", layout="wide")

st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:",
    ["Days Left Until...", "Numbers To Words", "Pro rata","Other"],
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

proratadf=pd.DataFrame(columns=['Company Name', 'Share in Rands', 'Share in Percentage'])
proratadf.set_index('Company Name', inplace=True)
proratadf.loc[f"Company {1}"] = [1.0,0.0]
proratadf.loc[f"Company {2}"] = [2.0,0.0]
proratadf.loc[f"Company {3}"] = [3.0,0.0]
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
    
    def write_n_to_r():
        st.write("Words:")
        s=(st.session_state['num_box']).replace('r','').replace('R','').replace(' ','')
        try:
            w=n_to_r(s)
        except:
            if s==None or s == '':
                w="Please Enter a number"
            else:
                w="Invalid Input"
        st.markdown(f"### {w}")
        
    
    st.markdown("Number:")
    
    s = st_keyup("Number to translate", value=None,type="number",  key="num_box",  on_change=write_n_to_r,debounce=300, args=None, kwargs=None,  placeholder=None, disabled=False, label_visibility="visible")
    
elif menu =="Pro rata":
    
    

    
    
    
    
    def update_df(proratadf):
        proratadf['Share in Percentage']=proratadf['Share in Rands']/proratadf['Share in Rands'].sum()*100.0
        
    sum_total=0.0
    
    data_col, pie_chart_col = st.columns(spec=[2,1])
    
    with data_col:
        st.header("Pro rata calculations")
        total_option=st.radio("Total",["Calculate Total","Specify Total"])
        if 'start_df' not in ss:
            ss.start_df = proratadf
        
        

        edited_df = st.data_editor(ss.start_df, num_rows='dynamic',column_config={
                                                                        "Company Name": st.column_config.TextColumn(
                                                                            width="medium",
                                                                        ),
                                                                        "Share in Percentage":  st.column_config.NumberColumn(
                                                                            format=" %.2f %%",width="medium"
                                                                        ),
                                                                        "Share in Rands":  st.column_config.NumberColumn(
                                                                            format="%.2f",width="medium",
                                                                        )
                                                                    })

        if not ss.start_df.equals(edited_df):
            ss.start_df = edited_df
            ss.start_df['Share in Percentage']= ss.start_df['Share in Rands']/ss.start_df['Share in Rands'].sum()*100.0
            st.rerun()
        
        sum_total=ss.start_df['Share in Rands'].sum()
        total_field=st.number_input("Total",value=sum_total,placeholder=sum_total,disabled=(total_option=="Calculate Total"))
    
    proratadf['Share in Percentage']=proratadf['Share in Rands']/proratadf['Share in Rands'].sum()*100.0
    
    with pie_chart_col:
        with st.container(border=True):
            st.header("Pie Chart")
            if total_option=="Calculate Total":
                if ss.start_df['Share in Rands'].sum()>0.01:
                    st.pyplot(ss.start_df.plot.pie(y='Share in Rands', figsize=(5, 5)).figure)
                else:
                    st.write("Could not plot values")
            else:
                unaccounted_for = total_field-float(ss.start_df['Share in Rands'].sum())
                
                if unaccounted_for >= 0.0:
                
                    df2=ss.start_df
                    df2.loc['UNACCOUNTED FOR']=[unaccounted_for,0.0]
                    df2['Share in Percentage']=df2['Share in Rands']/df2['Share in Rands'].sum()*100.0
                    if ss.start_df['Share in Rands'].sum()>0.01:
                        
                        st.pyplot(df2.plot.pie(y='Share in Rands', figsize=(5, 5)).figure)
                    else:
                        st.write("Could not plot values")
                else:
                    st.write("Please input a total that is equal to or greater than the sum of the columns")
elif menu=="Other":         

    st.markdown(f"## Sonnet {n_sonnet+1}")
    st.text(p.replace('\\n','\n'))

    


            
            
        
