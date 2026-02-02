import ollama

# Only cuz i have this script running in docker
client = ollama.Client(host="http://host.docker.internal:11434")

system_prompt = (
    "You are a calculations helper. Help the person with its calculations to do."
)
# Get input from you
user_input = input("You: ")

print("Thinking: ", end="", flush=True)
is_thinking = True

# Chat with streaming
for chunk in client.chat(
    model="glm-4.7-flash:q8_0",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ],
    stream=True,
):
    msg = chunk["message"]

    if msg.thinking:
        print(msg.thinking, end="", flush=True)
    if msg.content:
        if is_thinking:
            print("\n\nResponse: ", end="", flush=True)
            is_thinking = False
        print(msg.content, end="", flush=True)

print()
