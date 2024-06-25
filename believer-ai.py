import os
import json
import streamlit as st
from dotenv import load_dotenv
from models import functions
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser, PydanticOutputFunctionsParser
from models import Goals,Goal
from database import insert_goal, fetch_goals
import streamlit as st
import matplotlib.pyplot as plt

# from visualizations import plot_hours_over_time_for_goal, plot_user_statements_for_goal

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI


model = ChatOpenAI(model="gpt-3.5-turbo")

# tip always give good system message
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly goal time logger, if not provided dont assume"),
    ("user", "{input}")
])

model_with_functions = model.bind(functions=functions)
#model_with_functions.with_structured_output(Goal)
chain = prompt | model_with_functions | JsonOutputFunctionsParser()

# try following which helps 
#chain = prompt | model_with_functions
#response = chain.with_structured_output(Goal).invoke({"input":"spent 2 hours on python programming then machine learning for 5 hours then slept for 2 hours"})

#Streamlit code
# Streamlit app layout
st.title("Believer AI 10,000 Hours Mastery Tracker: Your Journey to Expertise")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def log_activity(user_input):
    # Generate response from the model
    response = chain.invoke({"input": user_input})
    
    # Insert goals into the database
    for goal in response['goals']:
        insert_goal(goal)
    
    response_text = "Great! You've logged the following activities:\n"
    for goal in response['goals']:
        response_text += f"- {goal['title']}: {goal['hours_logged']} hours on {goal['date']}"
    

    # Return the response to display in chat
    return response_text

user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(role="user", content=user_input))
        
        # Log activity and get response
        response = log_activity(user_input)
        
        # Add assistant response to chat history
        st.session_state.messages.append(AIMessage(role="assistant", content=json.dumps(response, indent=2)))


# Display chat history
for message in st.session_state.messages:
    if message.role == "user":
        st.write(f"You: {message.content}")
    else:
        st.write(f"Assistant: {message.content}")


# Function to generate Matplotlib visualizations
def plot_hours_over_time_for_goal(goals, goal):
    goal_data = [g for g in goals if g.title.lower() == goal.lower()]
    if not goal_data:
        return
    
    dates = [g.date for g in goal_data]
    hours = [g.hours_logged for g in goal_data]

    fig, ax = plt.subplots()
    ax.plot(dates, hours, marker='o')
    ax.set_title(f"Hours Logged Over Time for {goal.capitalize()}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Hours Logged")
    st.pyplot(fig)

def plot_user_statements_for_goal(goals, goal):
    goal_data = [g for g in goals if g['title'].lower() == goal.lower()]
    if not goal_data:
        return
    
    dates = [g['date'] for g in goal_data]
    statements = [g['user_statement'] for g in goal_data]
    hours = [g['hours_logged'] for g in goal_data]

    fig, ax = plt.subplots()
    ax.bar(dates, hours)
    ax.set_title(f"User Statements for {goal.capitalize()}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Hours Logged")
    st.pyplot(fig)

# Sidebar for fetching and visualizing goals
if st.sidebar.button("Visualize"):
    goals = fetch_goals()
    st.write("Logged Hours on Goals:")
    total_hours = 0
    for goal in goals:
        st.write(f"Title: {goal.title}, Hours: {goal.hours_logged}, Date: {goal.date}, User statement: {goal.user_input}")
        total_hours += goal.hours_logged

    # Display total hours
    st.write(f"Total hours logged: {total_hours}")

    # Generate visualizations for each goal
    st.subheader("Visualizations")
    unique_goals = {g.title.lower() for g in goals}
    
    for goal in unique_goals:
        st.write(f"## {goal.capitalize()}")
        plot_hours_over_time_for_goal(goals, goal)
       # plot_user_statements_for_goal(goals, goal)


# Fetching and displaying goals
def display_goals():
    goals = fetch_goals()
    for goal in goals:
        print(f"Title: {goal.title}, Hours: {goal.hours_logged}, Date: {goal.date}, User statement: {goal.user_input}")

