from api_client import chat

messages = []

while True:
    user_input = input("You: ").strip()

    if user_input == "":
        continue
    elif user_input.startswith("/"):
        command = user_input.split(" ", 1)
        if command[0] == "/bye":
            break
    else:
        messages.append({"role": "user", "content": user_input})
        chat(messages)
        print("12345")
        for msg in messages:
            print(msg)
