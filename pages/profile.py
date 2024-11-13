import streamlit as st
from datetime import datetime
import pandas as pd
from functions.login import login_form, is_logged_in, get_username, show_login_form
from functions.gsheet import fetch_data, update_data

if "username" not in st.session_state:
    st.warning("Please log in to view your profile.", icon="⚠️")
    show_login_form()
    st.stop()
else:
    st.title(f"Welcome, {get_username()}!")
    st.divider()

    with st.sidebar:
        with st.form("change_password"):
            st.write("Change Password")
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_button = st.form_submit_button("Change Password")

            if submit_button:
                
                try:
                    int(new_password)
                    st.error("Password should not be a number.", icon="⚠️")
                    st.stop()
                except ValueError:
                    pass
                
                user_data = fetch_data(worksheet="user_db", num_col=5, ttl=0)                
                individual_data = user_data[user_data.email == st.session_state["email"]]
                
                if current_password != individual_data.password.iloc[0]:
                    st.error("Current Password is incorrect.", icon="⚠️")
                    st.stop()
                elif new_password!= confirm_password:
                    st.error("New Password and Confirm Password do not match.", icon="⚠️")
                    st.stop()
                else:
                    user_data.loc[user_data.email == st.session_state['email'], 'password'] = new_password
                    update_data(worksheet="user_db", data=user_data)
                    st.success("Password changed successfully.")


    col1, col2 = st.columns(2)
    with col1:
        st.write("#### Personal Information")
        # Change username
        with st.form("change_username"):
            st.info("Change Username", icon="👤")
            new_username = st.text_input("New Username")
            submit_button = st.form_submit_button("Change Username")
            
            if submit_button:
                user_data = fetch_data(worksheet="user_db", num_col=5, ttl=0)
                user_data.loc[user_data.email == st.session_state['email'], 'username'] = new_username
                update_data(worksheet="user_db", data=user_data)
                st.session_state["username"] = new_username  # Update the session state with the new username
                st.success("Username changed successfully.")
                st.switch_page("pages/profile.py")  # Redirect to the profile page after changing username)


    with col2:
        st.write("#### Group Setting")
        
        with st.form("change_groupname"):
            st.info("Change Group Name", icon="👥")
            new_groupname = st.text_input("New Group Name", max_chars= 15)
            submit_button = st.form_submit_button("Change Groupname")
            
            if submit_button:
                group_data = fetch_data('group_db', num_col=7, ttl=0)
                group_data.loc[group_data.group_id == st.session_state['group_id'], 'group_name'] = new_groupname
                group_data.loc[group_data.group_id == st.session_state['group_id'], 'last_modified_by'] = st.session_state["email"]
                update_data(worksheet="group_db", data=group_data)
                st.success("Group name changed successfully.")

st.subheader("Adjust Your Agents")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Competition 1 Agents"):
        comp_data = fetch_data('competition_db', num_col= 7, ttl=0)
        deadline = comp_data[comp_data.competition_name == "Car Negotiation Game"].deadline.iloc[0]
        deadline = datetime.strptime(deadline, "%m/%d/%Y")
        if deadline < pd.to_datetime("now"):
            st.warning(f"You cannot adjust your agents, the deadline was at {deadline}", icon="⚠️")
        else:    
            agents_data = fetch_data(worksheet="agent_db", num_col=10, ttl=0)
            
            agents_data_not_change_1 = agents_data[agents_data.group_id != st.session_state['group_id']]
            agents_data = agents_data[agents_data.group_id == st.session_state['group_id']]
            agents_data_not_change_2 = agents_data[agents_data.competition_name != "Car Negotiation Game"]
            agents_data_not_change = pd.concat([agents_data_not_change_1, agents_data_not_change_2], ignore_index=True)

            st.session_state.agents_data_not_change = agents_data_not_change
            st.session_state.agents_data = agents_data[agents_data.competition_name == "Car Negotiation Game"]
with col2:
    if st.button("Competition 2 Agents"):
        comp_data = fetch_data('competition_db', num_col= 7, ttl=0)
        deadline = comp_data[comp_data.competition_name == "Guessing Game"].deadline.iloc[0]
        deadline = datetime.strptime(deadline, "%m/%d/%Y")
        if deadline < pd.to_datetime("now"):
            st.warning(f"You cannot adjust your agents, the deadline was at {deadline}", icon="⚠️")
        else:    
            agents_data = fetch_data(worksheet="agent_db", num_col=10, ttl=0)
            
            agents_data_not_change_1 = agents_data[agents_data.group_id != st.session_state['group_id']]
            agents_data = agents_data[agents_data.group_id == st.session_state['group_id']]
            agents_data_not_change_2 = agents_data[agents_data.competition_name != "Guessing Game"]
            agents_data_not_change = pd.concat([agents_data_not_change_1, agents_data_not_change_2], ignore_index=True)

            st.session_state.agents_data_not_change = agents_data_not_change
            st.session_state.agents_data = agents_data[agents_data.competition_name == "Guessing Game"]


with col3:
    if st.button("Competition 3 Agents"):
        comp_data = fetch_data('competition_db', num_col= 7, ttl=0)
        deadline = comp_data[comp_data.competition_name == "The Language Logic Challenge"].deadline.iloc[0]
        deadline = datetime.strptime(deadline, "%m/%d/%Y")
        if deadline < pd.to_datetime("now"):
            st.warning(f"You cannot adjust your agents, the deadline was at {deadline}", icon="⚠️")
        else:    
            agents_data = fetch_data(worksheet="agent_db", num_col=10, ttl=0)
            
            agents_data_not_change_1 = agents_data[agents_data.group_id != st.session_state['group_id']]
            agents_data = agents_data[agents_data.group_id == st.session_state['group_id']]
            agents_data_not_change_2 = agents_data[agents_data.competition_name != "The Language Logic Challenge"]
            agents_data_not_change = pd.concat([agents_data_not_change_1, agents_data_not_change_2], ignore_index=True)

            st.session_state.agents_data_not_change = agents_data_not_change
            st.session_state.agents_data = agents_data[agents_data.competition_name == "The Language Logic Challenge"]

if "agents_data" not in st.session_state:
    st.stop()

column_disabled_agents = [
    "model",
    "role",
    "competition_name",
    "created_by",
    "created_at",
    "group_id"
]

new_agent_data = st.data_editor(st.session_state.agents_data, disabled = column_disabled_agents, hide_index= True)

st.warning("Warning: By clicking on :orange[[Save changes]], the database will be changed.", icon="⚠️")
if st.button("Save changes"):
    updated_data = pd.concat([new_agent_data, st.session_state.agents_data_not_change], ignore_index = True)
    update_data(worksheet="agent_db", data=updated_data)
    st.success("Agent adjustments saved successfully.", icon="🎉")