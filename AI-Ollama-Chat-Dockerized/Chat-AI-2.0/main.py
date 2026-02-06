from chat import Chat
from tools import _functions as available_functions, _schemas as tools
import ollama

client = ollama.Client(host="http://host.docker.internal:11434")

system_prompt_path = "./prompt_templates/system_prompt.md"
chat = Chat(system_prompt_path)

while True:
    user_input = input("Ask me anything (or type 'quit' or 'exit' to quit):\n")
    if user_input.lower() in ["quit", "exit"]:
        break

    # Save user message
    chat.add_message("user", user_input)

    # Tool loop - keeps going until model gives final response (no tool calls)
    while True:
        thinking_or_responding = "neither"
        assistant_thinking = ""
        assistant_content = ""
        tool_calls = None

        # Stream the response
        for chunk in client.chat(
            model="glm-4.7-flash:q8_0",
            messages=chat.conversation,
            tools=tools,
            stream=True,
            think=True,
            keep_alive=-1, #"30m" 30 minutes, "1h" 1 hour
        ):
            msg = chunk["message"]

            if msg.thinking:
                if thinking_or_responding != "thinking":
                    thinking_or_responding = "thinking"
                    print("\n\nThinking: ", end="\n", flush=True)
                print(msg.thinking, end="", flush=True)
                assistant_thinking += msg.thinking

            if msg.content:
                if thinking_or_responding != "responding":
                    thinking_or_responding = "responding"
                    print("\n\nResponse: ", end="\n", flush=True)
                print(msg.content, end="", flush=True)
                assistant_content += msg.content

            # Capture tool calls (usually in final chunk)
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                tool_calls = msg.tool_calls

        # Did model request tools?
        if tool_calls:
            print("\n\n🔧 Tool calls detected!")

            # Save assistant message WITH thinking and tool_calls
            chat.add_message(
                role="assistant",
                content=assistant_content,
                thinking=assistant_thinking,  # Preserve for context!
                tool_calls=tool_calls
            )

            # Execute each tool
            for tc in tool_calls:
                func_name = tc["function"]["name"]
                func_args = tc["function"]["arguments"]

                print(f"   Calling: {func_name}({func_args})")

                try:
                    func = available_functions[func_name]
                except KeyError:
                    result = f"Error: unknown tool '{func_name}'. Available: {list(available_functions.keys())}"
                else:
                    try:
                        result = func(**func_args)
                    except TypeError as e:
                        # Wrong/missing arguments
                        import inspect
                        expected = inspect.signature(func).parameters
                        result = (
                            f"Error calling {func_name}: {e}. "
                            f"Expected args: {list(expected.keys())}, "
                            f"got: {func_args}"
                        )
                    except Exception as e:
                        result = f"Error in {func_name}({func_args}): {type(e).__name__}: {e}"

                print(f"   Result: {result}")

                # Add tool result
                chat.add_tool_result(content=str(result), tool_name=func_name)

            # No tool calls - final response
        else:
            chat.add_message(
                role="assistant",
                content=assistant_content,
                thinking=assistant_thinking
            )
            break

    print("\n\n\n", end="")
