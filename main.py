from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
import os


st.set_page_config(page_title='SQL QA system')
st.markdown('### :mag:🧙ChatEma: The one-stop-agent for all your queries')
st.markdown(
    "<h5 style='text-align: center; color: green;'>\nTired of navigating through multiple websites for retrieving information???</h5>",
    unsafe_allow_html=True)

st.markdown(
    "<h6 style='text-align: center; color: black;'>We got you covered, simply type your question in the textbox below and we will answer it for you!!</h6>",
    unsafe_allow_html=True)

openai_api_key = st.sidebar.text_input('Please enter your OpenAI API Key', type='password')
if openai_api_key:
    os.environ['OPENAI_API_KEY'] = openai_api_key
else:
    load_dotenv(override=True)

if "llm" not in st.session_state:
    st.session_state['llm'] = OpenAI(temperature=0, verbose=True)

if "db" not in st.session_state:
    st.session_state['db'] = SQLDatabase.from_uri("sqlite:///Chinook.db")

if "sql_executor" not in st.session_state:
    st.session_state['sql_executor'] = create_sql_agent(st.session_state['llm'], toolkit=SQLDatabaseToolkit(db=st.session_state['db'], llm=st.session_state['llm']),
                                      verbose=True, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
if "messages" not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


def generate_response(user_question):
    response = st.session_state['sql_executor'].run(user_question)
    return response


if prompt := st.chat_input('How can we help you today?'):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        output = generate_response(prompt)
        message_placeholder.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})



