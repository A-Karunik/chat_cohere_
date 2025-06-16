import requests
import time
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize the LLM model with your API key
llm = ChatCohere(cohere_api_key)

# Create a prompt template with a system message and a placeholder for user input
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the person who is Creative, Problem-solving, and Informational. You have to answer the question asked in points so that the user can understand the content of the answer."),
    ("user", "{input}")  # Placeholder for user input
])

# Initialize the output parser
output_parsers = StrOutputParser()

# Combine the prompt, LLM model, and output parser into a chain
chain = prompt | llm | output_parsers

# Telegram bot API base URL and token
base_url = "https://api.telegram.org/"

def read_msg(offset):
    parameters = {"offset": offset}
    resp = requests.get(base_url + "/getUpdates", params=parameters)
    data = resp.json()

    if not data['ok']:
        print(f"Error: {data['error_code']} - {data['description']}")
        return offset

    for result in data.get("result", []):
        if "text" in result["message"]:
            # Get user input from Telegram message
            user_input = result["message"]["text"]
            # Check for specific questions and provide predefined answers
            if "who is the ceo of india" in user_input.lower():
                response = "Mr. Aman Karunik "
            else:
                # Invoke the chain with user input
                response = chain.invoke({"input": user_input})
            # Send the response back to the user
            send_msg(result["message"]["chat"]["id"], response)

    if data.get("result"):
        return data["result"][-1]["update_id"] + 1
    return offset

def send_msg(chat_id, message):
    parameters = {"chat_id": chat_id, "text": message}
    resp = requests.get(base_url + "/sendMessage", params=parameters)
    print(resp.text)

offset = 0
while True:
    offset = read_msg(offset)
    time.sleep(1)
