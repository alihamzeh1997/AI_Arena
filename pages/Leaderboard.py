import streamlit as st
from functions.gsheet import fetch_data, update_data
from functions.login import login_form, is_logged_in, get_username, show_login_form, get_groupname


st.title("🏆 Leaderboard")
st.write("You can see the leaderboard here.")

if "username" not in st.session_state:
    st.warning("Please log in to view the leaderboards.", icon="⚠️")    
    show_login_form()
    st.stop()

competition_data = st.session_state["competitions"]
Competition_names = competition_data.competition_name.unique()

leaderboard_data = fetch_data(worksheet="group_db", num_col=7, ttl=0)
leaderboard_data.rename(columns={
    'group_name': "Group",
    'comp_1_point': "Car Negotiation Game",
    'comp_2_point': "Guessing Game",
    'comp_3_point': "Language Logic Challenge",
    'points': "Total"
}, inplace=True)

leaderboard_data = leaderboard_data.drop(columns=['group_id', 'last_modified_by'], axis=1)

st.dataframe(leaderboard_data, hide_index=True, width= 1000)