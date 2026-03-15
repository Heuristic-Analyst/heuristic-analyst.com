import os
import json
from chat import Chat
from tools import _functions as available_functions, _schemas as tools

# Load config (same file the web app uses)
with open("config.json") as f:
    config = json.load(f)

opts = {}
if config.get("num_ctx"):
    opts["num_ctx"] = config["num_ctx"]

chat = Chat(
    host=config["ollama_host"],
    chat_model=config["chat_model"],
    tools=tools,
    available_functions=available_functions,
    think=config.get("think", True),
    keep_alive=config.get("keep_alive", -1),
    options=opts if opts else None,
)

system_prompt_path = config.get("system_prompt_path")
if system_prompt_path:
    if os.path.exists(system_prompt_path):
        chat.add_system_prompt(system_prompt_path)
    else:
        print(f"⚠️  System prompt not found: {system_prompt_path}")

# Optionally load a previous conversation
# chat.load_conversation("saved_conversations/conversation.json")

print(f"Model: {config['chat_model']}")
print(f"Host:  {config['ollama_host']}\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["quit", "exit"]:
        break

    chat.add_message("user", user_input)
    content, thinking = chat.get_assistant_response()

    if content is None:
        print("\n⚠️  No response received. Is Ollama running?\n")
        continue

    print()

# Optionally save the conversation
# chat.save_conversation("saved_conversations/conversation.json")
