import streamlit as st

st.title("Knowledge Center")
st.write("Welcome to the AI Arena Knowledge Center! Here you can find information on how to configure your agents for various competitions, such as *the Car Negotiation Game*.")

st.write("#### How to configure Agents for competitions")
st.markdown("""
1. **System Message**: the system message plays a crucial role in setting the behavior, constraints, and overall context for AI agents. It provides foundational instructions to guide the agents' actions, much like a prompt that helps define their objectives, constraints, or even their personality traits.  
     
   For example, the system message could:  
    * Define the role of the agent (e.g., "You are an expert negotiator.")  
    * Set boundaries for behavior (e.g., "Always remain polite.")  
    * Clarify goals (e.g., "Your objective is to maximize the price during a sale negotiation.")  
    * Provide contextual information (e.g., "You are in a discussion about selling a car.")

2. **Description:** a short description of the agent. This description is used by other agents (e.g. the GroupChatManager) to decide when to call upon this agent. (Default: system\_message)  
     
   Since **descriptions** serve a different purpose than **system\_messages**, it is worth reviewing what makes a good agent description. While descriptions are new, the following tips appear to lead to good results:  
     
    * Avoid using the 1st or 2nd person perspective. Descriptions should not contain "I" or "You", unless perhaps "You" is in reference to the GroupChat / orchestrator  
    * Include any details that might help the orchestrator know when to call upon the agent  
    * Keep descriptions short (e.g., "A helpful AI assistant with strong natural language and Python coding skills.").  
    The main thing to remember is that **the description is for the benefit of the GroupChatManager, not for the Agent's own use or instruction**. ([Read more](https://microsoft.github.io/autogen/blog/2023/12/29/AgentDescriptions))

3. **Model:** the model refers to the specific AI model or architecture that powers the agent's decision-making and interactions. The choice of model impacts:  
    * **Capabilities**: Different models have different capabilities in terms of reasoning, language fluency, and knowledge.  
    * **Behavior:** The model dictates how an agent responds to instructions and the overall quality of its decisions.  
    * **Task performance:** More advanced models may perform better in complex tasks, while simpler models may be sufficient for straightforward scenarios.
""")

st.write("#### Test your Agents on your local machine")
