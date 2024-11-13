import streamlit as st
import ast
from functions.login import login_form, is_logged_in, get_username, show_login_form
from functions.gsheet import fetch_data, update_data
import pandas as pd
import numpy as np
from autogen import GroupChatManager, ConversableAgent, GroupChat
from functions.AutoGenFunc import AgentConfig, GroupChatManagerConfig

if "user_role" not in st.session_state:
    st.warning("Only admin can access to admin panel, Please log in first.", icon="⚠️")
    show_login_form()
    st.stop()
elif st.session_state["user_role"]!= "admin":
    st.error("Only admin can start a competition.", icon="⚠️")
    st.stop()

competition_data = st.session_state["competitions"]
Competition_names = competition_data.competition_name.unique()

st.subheader("Initiate the Competition")
with st.form(key="moderator_config_form"):
    moderator_name = st.text_input("Moderator Name")
    moderator_prompt = st.text_area("Moderator Prompt")
    InitiateMessage = st.text_area("Initiate Message")
    competition_name = st.selectbox(label="Competition Name", options = Competition_names, index=None)
    submit_button = st.form_submit_button("Start the competition")

if submit_button:
    admin_db = fetch_data(worksheet= "admin_db", num_col= 7, ttl=0)
    Moderator = ConversableAgent(
        name=moderator_name,
        system_message=moderator_prompt,
        llm_config={
            'model': 'gpt-4o',
            'api_key': st.secrets["model_auth"]["OPENAI_API_KEY"],
            'temperature': 0.1,
            'max_tokens': 200,
            'cache_seed': 42
        },
        human_input_mode="NEVER",
        is_termination_msg = lambda msg: "terminate" in msg['content'].lower()
        )

    new_initiate_data = pd.DataFrame(
            [
                {
                    "initiate_id": "init" + str(np.random.randint(1000, 100000)),
                    "moderator_name": moderator_name,
                    "moderator_prompt": moderator_prompt,
                    "initiate_message": InitiateMessage,
                    "competition_name": competition_name,
                    "created_by": get_username(),
                    "created_at": pd.to_datetime("now")
                }
            ]
    )
    # update admin_db
    final_initiate_data = pd.concat([admin_db,new_initiate_data], ignore_index=True)
    update_data(worksheet="admin_db", data=final_initiate_data)

    # Competition
    competitions = fetch_data(worksheet="agent_db", num_col= 10, ttl=0)
    competitions = competitions[competitions.competition_name == competition_name]

    comp_df = pd.DataFrame(columns=['agent_1', 'role_agent_1', 'agent_2', 'role_agent_2', 'agent_1_group_id', 'agent_2_group_id'])
    
    if competition_name == Competition_names[0]:                  
        competition_id = competition_data[competition_data.competition_name == Competition_names[0]].competition_id.iloc[0]
        roles = competition_data[competition_data.competition_name == Competition_names[0]].competition_roles.iloc[0]
        roles = ast.literal_eval(roles)
        first_agent = competitions[competitions.role == roles[0]]
        second_agent = competitions[competitions.role == roles[1]]

    elif competition_name == Competition_names[1]:
        competition_id = competition_data[competition_data.competition_name == Competition_names[1]].competition_id.iloc[0]
        roles = competition_data[competition_data.competition_name == Competition_names[1]].competition_roles.iloc[0]
        roles = ast.literal_eval(roles)
        first_agent = competitions[competitions.role == roles[0]]
        second_agent = competitions[competitions.role == roles[1]]

    else:
        competition_id = competition_data[competition_data.competition_name == Competition_names[2]].competition_id.iloc[0]
        roles = competition_data[competition_data.competition_name == Competition_names[2]].competition_roles.iloc[0]
        roles = ast.literal_eval(roles)
        first_agent = competitions[competitions.role == roles[0]]
        second_agent = competitions[competitions.role == roles[1]]
    

    for i in range(len(first_agent)):
        for j in range(len(second_agent)):
            new_row = {
                'agent_1': first_agent.agent_name.iloc[i],
                'role_agent_1': first_agent.role.iloc[i],
                'agent_2': second_agent.agent_name.iloc[j],
                'role_agent_2': second_agent.role.iloc[j],
                'agent_1_group_id': first_agent.group_id.iloc[i],
                'agent_2_group_id': second_agent.group_id.iloc[j]
            }
            comp_df=pd.concat([comp_df, pd.DataFrame([new_row])], ignore_index=True)

    st.dataframe(comp_df,width=1000,height=300, hide_index=True)
    
    # Fetching previous chat messages data
    chat_messages_data = pd.read_csv("/Users/alihamzeh/Documents/StreamLit/.files/Messages.csv")
    chat_messages_gsheet = fetch_data(worksheet="messages_db", num_col=11, ttl=0)

    # Creating a new chat group for each competition
    for i in range(len(comp_df)):
        agent_1 = AgentConfig(agent_name=str(comp_df.agent_1.iloc[i]), agent_data=competitions)
        agent_2 = AgentConfig(agent_name=str(comp_df.agent_2.iloc[i]), agent_data=competitions)

        chat_group_manager, chat_messages = GroupChatManagerConfig(agent_1=agent_1, agent_2=agent_2, Moderator=Moderator, InitiateMessage=InitiateMessage)

        new_message_list = pd.DataFrame(
            [
                {
                    'agent_1_name': comp_df.agent_1.iloc[i],
                    'agent_2_name': comp_df.agent_2.iloc[i],
                    'agent_1_group_id': comp_df.agent_1_group_id.iloc[i],
                    'agent_2_group_id': comp_df.agent_2_group_id.iloc[i],
                    'agent_1_role': comp_df.role_agent_1.iloc[i],
                    'agent_2_role': comp_df.role_agent_2.iloc[i],
                    'agent_1_point': 0.001,
                    'agent_2_point': 0.001,
                    'messages_list': chat_messages,
                    'competition_name': competition_name,
                    'competition_id': competition_id,
                    'created_at': pd.to_datetime("now")
                }
            ]
        )
        chat_messages_data = pd.concat([chat_messages_data, new_message_list], ignore_index=True)
        chat_messages_gsheet = pd.concat([chat_messages_gsheet, new_message_list], ignore_index=True)
        


        expander_name = f"**{comp_df.agent_1.iloc[i]}** as {comp_df.role_agent_1.iloc[i]} vs. **{comp_df.agent_2.iloc[i]}** as {comp_df.role_agent_2.iloc[i]}"
        with st.expander(expander_name, icon="🤖"):
            with st.container(height=300):
                for item in chat_messages:
                    st.markdown(f":blue[{item['name']}:]")
                    st.markdown(f"{item['content']}")
    
    # Save updated chat messages to Google Sheets.
    update_data(worksheet="messages_db", data=chat_messages_gsheet)
    chat_messages_data.to_csv("/Users/alihamzeh/Documents/StreamLit/.files/Messages.csv", index=False)

    st.success("The competition has finished successfully.")

st.subheader("Messages History")
st.write("Please select the competition in the Sidebar.")

with st.sidebar:
    with st.form("Messages History Administration"):
        competition_history = st.selectbox(label="Message History", options = Competition_names, index=None)
        submit_button_history = st.form_submit_button("Select competition")


if submit_button_history:
    st.write(f"The results for **{competition_history}** is as follows:")
    chat_history_data = fetch_data(worksheet="messages_db", num_col=11, ttl=0)
    chat_history_data = chat_history_data[chat_history_data.competition_name == competition_history]
    for row in range(len(chat_history_data)):
        expander_name_history = f"Group **{chat_history_data.agent_1_group_id.iloc[row]}** as *{chat_history_data.agent_1_role.iloc[row]}* Vs. Group **{chat_history_data.agent_2_group_id.iloc[row]}** as *{chat_history_data.agent_2_role.iloc[row]}*. Created at *{chat_history_data.created_at.iloc[row]}*"
        with st.expander(expander_name_history, icon="➕"):
            with st.container(height=500):
                message = ast.literal_eval(chat_history_data.messages_list.iloc[row])
                for item in message:
                    st.markdown(f":blue[{item['name']}:]")
                    st.markdown(f"{item['content']}")

st.subheader("💬 Manage Message Database")
st.write("Please be careful all the changes will be saved to the database. You can just change the agents points below.")

if st.button("Adjust agent's points"):
    st.session_state.chat_histories = fetch_data(worksheet="messages_db", num_col=11, ttl=0)

if "chat_histories" in st.session_state:
    column_disabled = [
        "agent_1_name",
        "agent_2_name",
        "agent_1_group_id",
        "agent_2_group_id",
        "agent_1_role",
        "agent_2_role",
        "messages_list",
        "competition_name",
        "created_at"  
    ]

    chat_histories_data = st.session_state.chat_histories
    new_chat_history = st.data_editor(chat_histories_data,disabled=column_disabled ,hide_index=True)

    st.warning("By clicking on :blue[Save changes], the database will be changed.", icon="⚠️")
    if st.button("Save changes"):
        update_data(worksheet="messages_db", data=new_chat_history)
        del st.session_state.chat_histories
        st.rerun()



st.subheader("⚙️ Manage competition Database")
st.write("Please be careful all the changes will be saved to the database. You can change all the settings of the competition.")

if st.button("Adjust competition"):
    st.session_state.comp_setting = fetch_data(worksheet="competition_db", num_col=7, ttl=0)

if "comp_setting" not in st.session_state:
    st.stop()


comp_setting = st.session_state.comp_setting
new_comp_setting = st.data_editor(comp_setting,hide_index=True)

st.warning("By clicking on :blue[Save changes], the database will be changed.", icon="⚠️")
if st.button("Save changes"):
    update_data(worksheet="competition_db", data=new_comp_setting)
    mainpage_content = new_comp_setting.loc[:, ['competition_name','competition_description']]
    mainpage_content.to_csv("/Users/alihamzeh/Documents/StreamLit/.files/mainpage.csv", index=False)
    del st.session_state.comp_setting
    st.rerun()