import streamlit as st
from functions.login import login_form, is_logged_in, get_username, show_login_form, get_groupname
from functions.gsheet import fetch_data, update_data
import pandas as pd
import ast

if "username" not in st.session_state:
    st.warning("Please log in to submit your Agents.", icon="⚠️")    
    show_login_form()
    st.stop()

# Display Title and Description
st.title("Agent Configuration")
st.markdown("Please select the competition in the sidebar.")


competition_data = st.session_state["competitions"]
Competition_names = competition_data.competition_name.unique()

with st.sidebar:
    with st.form(key='competition_filter_form'):
        st.write("### Please select the competition:")
        competition_name = st.selectbox("Competition", options=Competition_names, index=None)
        submit_button = st.form_submit_button("select competition")

        if submit_button:
            if competition_name == None:
                st.error("Please select a competition.", icon="⚠️")
                st.stop()
            else:
                Models = competition_data[competition_data["competition_name"] == competition_name].competition_models.iloc[0]
                st.session_state.Models = ast.literal_eval(Models)
                Roles = competition_data[competition_data["competition_name"] == competition_name].competition_roles.iloc[0]
                st.session_state.Roles = ast.literal_eval(Roles)
                st.session_state.max_num_agents = competition_data[competition_data["competition_name"] == competition_name].competition_max_agents.iloc[0]
                st.markdown(f"Maximum number of agents for this competition: `{int(st.session_state.max_num_agents)}` in roles: `{st.session_state.Roles}`")

if "Models" in st.session_state and competition_name != None:
    st.write("configure your agent settings below. Read **knowledge center** before submitting your agent.")
    with st.form(key='agent_config_form'):
        competition_id = st.selectbox(label="Competition",options=competition_name)
        agent_name = st.text_input(label="Agent Name*", max_chars= 20, placeholder= "Enter your agent's name.")
        model_choice = st.selectbox(label="Model*", options=st.session_state.Models, index=None)
        role = st.selectbox(label="Role*", options=st.session_state.Roles, index=None)
        temperature = st.slider("Your agent's temperature (0-100)",min_value= 0,max_value= 100,value=50, step= 10)
        prompt = st.text_area(label="System Message*", max_chars=1000)
        description = st.text_area(label="Description*", max_chars=60, placeholder= " Describe your agent, shortly.")
        # Mark mandatory fields
        st.markdown("**required*")
        submit_button_2 = st.form_submit_button("Submit")
        
        if submit_button_2:
            
            agent_data = fetch_data(worksheet="agent_db", num_col=10, ttl=0)
            num_agents = agent_data[agent_data["competition_name"] == competition_id]
            num_agents = num_agents[num_agents["group_id"] == get_groupname()].group_id.count()
            
            # Check if all mandatory fields are filled
            if not agent_name or not model_choice or not competition_id or not prompt or not description or not role:
                st.warning("Ensure all mandatory fields are filled.")
                st.write(num_agents)
                st.stop()
            elif agent_data["agent_name"].str.contains(agent_name).any():
                st.warning("An agent with this name already exists.")
                st.stop()
            elif num_agents >= st.session_state.max_num_agents:
                st.warning("You have reached to the maximum number of Agents for this competition.")
                st.stop()
            else:
                new_agent_data = pd.DataFrame(
                    [
                        {
                            "agent_name": agent_name,
                            "model": model_choice,
                            "competition_name": competition_id,
                            "temperature": temperature,
                            "prompt": prompt,
                            "group_id": get_groupname(),
                            "description": description,
                            "created_by": get_username(),
                            "created_at": pd.to_datetime("now"),
                            "role": role
                        }
                    ]
                )

                # Save new agent data to Google Sheets
                updated_agent_data = pd.concat([agent_data, new_agent_data], ignore_index=True)
                # updated_agent_data.to_csv("/Users/alihamzeh/Documents/StreamLit/.files/Agents.csv", index=False)
                update_data(worksheet="agent_db", data=updated_agent_data)
                st.success("Agent configuration submitted successfully!")
                st.write(f"The number of agents on your group for **{competition_id}** is now **{num_agents + 1}**.")