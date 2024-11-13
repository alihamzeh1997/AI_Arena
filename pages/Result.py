import streamlit as st
import ast
import numpy as np
from functions.login import login_form, is_logged_in, get_username, show_login_form, get_groupname
from functions.gsheet import fetch_data, update_data
import pandas as pd

if "username" not in st.session_state:
    st.warning("Please log in to view the chat history.", icon="⚠️")
    show_login_form()
else:
    chat_history = fetch_data(worksheet="messages_db", num_col=11, ttl=0)
    competition_list = chat_history.competition_name.unique().tolist()
    st.title(f'{st.session_state.group_name} Results')
    st.write(f"{get_username()}, please select a competition on the sidebar to view the chat results.")
    with st.sidebar:
        with st.form(key="chat_history_form"):
            st.header("Chat History")
            st.write("Please select a competition to view the chat history.")
            competition_name = st.selectbox("Select a Competition", options=competition_list)
            submit_button = st.form_submit_button("Submit")

    if submit_button:
        agents_data = fetch_data(worksheet="agent_db", num_col=10, ttl=0)
        agents_data = agents_data[agents_data.group_id == get_groupname()]
        agents_data = agents_data[agents_data.competition_name == competition_name]
        agents_role = np.unique(agents_data.role.values)

        st.subheader(f'The results of the {competition_name}')
        for i in range(len(agents_role)):
            st.write(f"Role: {agents_role[i]}")
            agents_name = agents_data[agents_data.role == agents_role[i]].agent_name.values
            for j in range(len(agents_name)):
                        chat_messages_1 = chat_history[chat_history.agent_1_name == agents_name[j]]
                        chat_messages_2 = chat_history[chat_history.agent_2_name == agents_name[j]]
                        chat_messages = pd.concat([chat_messages_1, chat_messages_2], ignore_index=True)
                        chat_messages_list = chat_messages.messages_list # From database
                        for row in range(len(chat_messages)):
                            with st.expander(f":gray[{chat_messages.agent_1_name.iloc[row]}:] :blue[{chat_messages.agent_1_point.iloc[row]}] :gray[points] **///** :gray[{chat_messages.agent_2_name.iloc[row]}:] :blue[{chat_messages.agent_2_point.iloc[row]}] :gray[points]", icon="👾"):
                                message = ast.literal_eval(chat_messages_list[row])
                                for item in message:
                                    st.markdown(f":blue[{item['name']}:]")
                                    st.write(f"{item['content']}")


