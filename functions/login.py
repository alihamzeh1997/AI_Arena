import streamlit as st
from functions.gsheet import fetch_data

# Create a login function
def login_form():
    st.title("Login Form")

    with st.form(key='login_form'):
        email = st.text_input("Email")
        password_entry = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    # Check credentials
    if submit_button:
        user_data = fetch_data(worksheet="user_db", num_col=6, ttl=0)
        group_data = fetch_data(worksheet="group_db", num_col=7, ttl=0)
        competitions_data = fetch_data(worksheet="competition_db", num_col=7, ttl=0)
        user_name_data = user_data[user_data['email'] == email]
        group_id = user_name_data['group_id'].astype(str).iloc[0]
        group_data = group_data[group_data['group_id'] == group_id]
        group_name = group_data['group_name'].astype(str).iloc[0]
        password_database = user_name_data['password'].astype(str).iloc[0]
        user_name = user_name_data['username'].astype(str).iloc[0]
        user_role = user_name_data['user_role'].astype(str).iloc[0]

        # check if password is correct
        if not user_name_data.empty and password_database == str(password_entry): 
            st.session_state["logged_in"] = True
            st.session_state["email"] = email  
            st.session_state["group_id"] = group_id  # Store the group id
            st.session_state['group_name'] = group_name # Store the group name
            st.session_state['username'] = user_name # Store the username
            st.session_state['user_role'] = user_role # Store the user role
            st.session_state['competitions'] = competitions_data # Store the competitions list
            st.success("Login successful!")
            st.switch_page("pages/profile.py")
        
        # Invalid credentials
        else:
            st.error("Invalid password")

# Function to check if the user is logged in
def is_logged_in():
    return st.session_state["logged_in"]

# Function to get logged-in user
def get_username():
    return st.session_state["username"]

def get_groupname():
    return st.session_state["group_id"]


def show_login_form():
    with st.sidebar:
        # Initialize session state for login
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False

        # Show the login form if not logged in
        if not is_logged_in():
            login_form()
        else:
            # If logged in, show the main page
            st.title(f"Welcome, {get_username()}!")
            st.write("You are now logged in.")

        # Add a logout button
            if st.button("Logout"):
                st.session_state["logged_in"] = False
                del st.session_state["username"]
                st.switch_page("main.py")
