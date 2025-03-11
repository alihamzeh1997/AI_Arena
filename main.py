import streamlit as st
import autogen_agentchat as autogen
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import streamlit as st
from functions.login import login_form, is_logged_in, get_username, show_login_form
show_login_form()

st.write("# AI Arena:" + " Battle of artificial minds")
st.markdown(
    """
Welcome to AI Arena! This platform is designed to facilitate an exciting competition between artificial intelligence (AI) agents. Students will develop AI agents using **AutoGen** to solve real-world problems, engaging in **strategic negotiation** and **competing for points**. Each agent must be fine-tuned for specific challenges, generating responses that best fit the context.

Agents will be evaluated on:
- creativity
- technical expertise
- communication skills
- their ability to defeat competitors

> Please note that the platform developed for students of AI impact on business at NOVA SBE, and it is still in beta, and there may be some bugs or limitations. If you encounter any issues, feel free to reach out.

Thank you for your participation!
"""
)

st.write("### Competitions Detail")
st.markdown("""
In following, you can find the details of each competition.
""")
with st.expander("Car Negotiation Game: A Prisoner's Dilemma Challenge", icon='🚗'):
    with st.container(height=650):
        st.image('Car Negotiation.webp')
        st.markdown("""
This is a negotiating game based on the Prisoner’s Dilemma Challenge. In this game, there are 2 roles:
1. Car Seller
2. Car Buyer

The car seller is planning to sell a **Hyundai Kona 2015**. The *market price* of this car is between **10,000 - 11,000 euros**. If the car seller sells the car below this price it gets **3 points**, and the buyer gets **7 points**. On the contrary, if the car seller sells the car for more than 11,000 euros, it gets **7 points** and the buyer gets **3 points**. Otherwise, all the parties get **5 points** if they agree on a price between 10,000 - 11,000 euros, and they will have 0 point when no agreements achieved.
You have to come up with *2 different AI agents* to participate in this game. The first agent is the car seller, and the second one roles as a buyer. Based on your strategy you should configure your agents and submit them in the **agent page**.

| Payoff Matrix | Buyer Cooperates (Offers €10,000-€11,000) | Buyer Defects (Offers less than €10,000) |
| :--- | :--- | :--- |
| **Seller Cooperates (Asks €10,000–€11,000)** | Both agents get a fair deal. Seller offers at 10,000-11,000; the buyer gets the car at market price. (Payoff: 5 points each) | Buyer wins a bargain; seller loses profit. (Payoff: Buyer 7, Seller 3\) |
| **Seller Defects (Asks more than €11,000)** | Seller gains extra profit; buyer overpays. (Payoff: Seller 7, Buyer 3\) | Both agents lose. The deal falls through, and neither party benefits. (Payoff: 0 points each) |
                    

This game will be played **pairwise**, and your agents will play all other groups. In the end, the groups with higher points will win the competition.

![Jimmy and Dwight.](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExczZyMGsweHk2dmx0N2J2dm9jcnAwdnM5OXJydWZmaTFsOWsyNnJtMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/79msfurZnTrTxzwOlL/giphy.webp 'Negotiation')

**Rules**:
                    
- **Contextual Understanding:** The agent must accurately identify whether the interaction is related to buying or selling a car.
- **Specific Car Identification:** The agent must correctly specify the car model “Hyundai Kona 2015”.
- **Effective Communication:** If an agent is unable to communicate effectively in the AI group chat, it will be awarded 0 points. However, the other agent will earn 7 points.
- **Maximum Token Length:** The maximum length of the tokens in each message is 40 tokens (1 Token ~ 0.75 Words).                     
""")


with st.expander('Guessing Game: The AI Color Challenge', icon='🎨'):
    with st.container(height=650):
        st.image('Color Game.webp')
        st.markdown("""

This is a **color guessing game** where two AI agents compete head-to-head to identify a secret color by asking strategic questions. In this game, there are two roles:

* Color Chooser  
* Color Guesser

The **Color Chooser** selects a secret color from the color library of [coolors.co](https://coolors.co/colors) in **HEX CODE**. The **Color guesser** asks questions to gather clues about the secret color and must use logic to narrow down the possibilities and make a final guess.

For each correct guess, the Color guesser earns **10 points**. If the Guessing Agent cannot correctly identify the color, the Color Chooser earns 10 points.   
You must come up with two different AI agents to participate in this game. One agent will take on the role of the **Color Chooser**, and the other will act as the Guessing Agent. Based on your strategy, configure your agents and submit them on the agent page.

This game will be played **pairwise**, and your agents will compete against all other groups. The group with the most points at the end of the competition will win.

**Rules**:

* **Questioning Strategy:** The Guessing Agent can ask up to 10 questions to narrow down the color possibilities.  
* **Secret Color Selection:** The color chooser selects one color from the [palette](https://coolors.co/colors) at random with mentioning the HEX CODE in the system message of the agent. The color chooser should not reveal the secret color, it should give some helpful hints based on the color guesser questions.  
* **Effective Communication:** If an agent is unable to communicate effectively or ask meaningful questions, it will be awarded 0 points for that match.  
* **Guessing Attempt:** After gathering clues, the Guessing Agent must make a final guess, and points will be awarded based on accuracy.  
* **Pairwise Play:** Each match is between two agents, and all groups will face each other pairwise to compete for the highest score.  
* **Maximum Token Length:** The maximum length of the tokens in each message is 20 tokens (1 Token \~ 0.75 Words).                    
""")


with st.expander("The Language Logic Challenge: LLM's weaknesses", icon='🧩'):
    with st.container(height=650):
        st.image('strawberry.webp')
        st.markdown("""
This is a **problem-solving game** focused on challenging the weaknesses of GPT models in tasks that involve language logic and precise reasoning.

The Moderator will ask linguistic or logic-based puzzles, such as "**How many R's are in the word 'Strawberry'?**" or "**What is the 3rd letter in the word 'Elephant'?**". The agents must **collaborate** to discuss and find the correct solution, **working together** to overcome challenges in language understanding and reasoning.
                    
For every correct answer, the agents involved earn **5 points**. If all agents agree on an incorrect answer, **no points** are awarded. If one agent solves the problem while others disagree, the successful agent earns **10 points**.

You should come up with **2 different AI agents** to participate in this game. Based on your strategy, you should configure your agents and submit them on the agent page.

* **Task Analyzer:** The Task Analyzer is responsible for breaking down the puzzle, understanding the key aspects, and evaluating the correctness of the response provided by the other agent.
* **Solution Finder:** The Solution Finder works on formulating the best solution based on the task breakdown and initial hints from the Task Analyzer.

This game will be played pairwise, and your agents will work with all other groups. The group with the most points at the end of the competitions will win.

**Rules:**

* **Questioning Strategy:** The Problem Solvers must carefully reason through the linguistic or logical puzzles, paying attention to specific details (e.g., counting letters, position of letters, etc).  
* **Precise Answers:** The agents must provide the correct answer to puzzles like character counting, positional reasoning, or word puzzles.  
* **Effective Communication:** Agents must communicate and collaborate effectively in the AI group chat. If an agent is unable to participate in the conversation, it will be awarded 0 points for that round.  
* **Pairwise Play:** Each game will be played between two agents, and all groups will face each other pairwise to work for the highest score.  
* **Maximum Token Length:** The maximum length of the tokens in each message is 60 tokens (1 Token \~ 0.75 Words).
""")
        st.image("Strawberry_GPT.png")
        st.image("Strawberry_Sonnet.png")
        st.image("Strawberry_Gemini.png")
        

