import os

import streamsync as ss
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("API_KEY")

llm = ChatOpenAI(api_key=api_key, temperature=0, model_name="gpt-3.5-turbo")


def call_llm(prompt):
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=prompt)
    ]
    response = llm(messages)
    print(response)
    return response.content

def handle_user_input(payload):
    if payload == "":
        return "Please enter a message"
    else:
        gpt_response = call_llm(payload)
        return gpt_response

def handle_message_simple(payload):
    query = payload

    if query == "Hello":

		# You can simply return a string

        return "Hello, human."
    elif query == "Surprise me":

		# Or you can return a dict with actions, which are buttons
		# added to the conversation

        return {
            "text": "I can help you with that.",
            "actions": [{
            	"subheading": "Resource",
            	"name": "Surprise",
            	"desc": "Click to be surprised",
            	"data": "change_title" 
        	}]
        }
    else:
        return "I don't know"
    
# Initialise the state

initial_state = ss.init_state({
    "app": {
        "title": "Ask AI",
    },
    "message": None,
})
