import os

import requests
import streamsync as ss
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

# This is a placeholder to get you started or refresh your memory.
# Delete it or adapt it as necessary.
# Documentation is available at https://streamsync.cloud


# Its name starts with _, so this function won't be exposed
def _update_message(state):
    is_even = state["counter"] % 2 == 0
    message = ("+Even" if is_even else "-Odd")
    state["message"] = message

def decrement(state):
    state["counter"] -= 1
    _update_message(state)

def increment(state):
    state["counter"] += 1
    # Shows in the log when the event handler is run
    print("The counter has been incremented.")
    _update_message(state)

def call_gpt4(prompt):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        # 'model': 'gpt-4-turbo',  # Use the latest GPT-4 model ID
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 150
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

def handle_user_input(payload):
    gpt_response = call_gpt4(payload)
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

# "_my_private_element" won't be serialised or sent to the frontend,
# because it starts with an underscore

initial_state = ss.init_state({
    "my_app": {
        "title": "Ask GPT-4",
    },
    "_my_private_element": 1337,
    "message": None,
    "counter": 26,
})

_update_message(initial_state)