import streamlit as st
from functions.gsheet import fetch_data
import autogen_agentchat as autogen
from autogen import GroupChatManager, ConversableAgent, GroupChat
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def AgentConfig(agent_name, agent_data):
    Agent_data = agent_data
    Agent_data = Agent_data[Agent_data.agent_name == agent_name]
    llm_config = {
    'model': str(Agent_data.model.iloc[0]),
    'api_key': st.secrets["model_auth"]["OPENAI_API_KEY"],
    'temperature': int(Agent_data.temperature.iloc[0])/100,
    'max_tokens': 200,
    'cache_seed': 42    
    }
    agent = ConversableAgent(
        name= str(Agent_data.agent_name.iloc[0]),
        system_message= str(Agent_data.prompt.iloc[0]),
        llm_config=llm_config,
        human_input_mode= "NEVER",
        description= str(Agent_data.description.iloc[0])
        )
    return agent

def GroupChatManagerConfig(agent_1, agent_2, Moderator, InitiateMessage):
    llm_config = {
    'model': "gpt-4o",
    'api_key': st.secrets["model_auth"]["OPENAI_API_KEY"],
    'temperature': 0.2
    }
    agent_list = [agent_1, agent_2, Moderator]

    chat_messages = []
    chat_group = GroupChat(
        agents=agent_list,
        messages=chat_messages,
        max_round = 20,
    )
    chat_group_manager = GroupChatManager(
        groupchat=chat_group,
        human_input_mode="NEVER",
        llm_config=llm_config
    )
    chat_result = Moderator.initiate_chat(
        chat_group_manager,
        message = InitiateMessage
        )   
    
    return chat_group_manager, chat_messages