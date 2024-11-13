import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def fetch_data(worksheet, num_col, ttl):
    existing_data = conn.read(worksheet=worksheet , usecols=list(range(num_col)), ttl=ttl)
    existing_data = existing_data.dropna(how="all")
    return existing_data


def update_data(worksheet, data):
    conn.update(worksheet=worksheet, data=data)

