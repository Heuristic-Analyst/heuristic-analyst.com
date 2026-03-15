from pathlib import Path
import os
import json
import ollama
import inspect


class Chat:
    def __init__(self, host, chat_model, tools, available_functions, think, keep_alive, options=None):
        self.client = ollama.Client(host=host)
        self.chat_model = chat_model
        self.tools = tools
        self.available_functions = available_functions
        self.think = think
        self.keep_alive = keep_alive
        self.options = options
        self.conversation = []

    def add_system_prompt(self, system_prompt_path_md):
        system_prompt = Path(system_prompt_path_md).read_text(encoding="utf-8")
        self.conversation.append({"role": "system", "content": system_prompt})

    def load_conversation(self, filepath):
        """Load a conversation from a JSON file."""
        with open(filepath, 'r') as f:
            self.conversation = json.load(f)

    def add_message(self, role, content, thinking=None, tool_calls=None):
        """Add a user or assistant message."""
        msg = {"role": role, "content": content}
        if thinking is not None:
            msg["thinking"] = thinking
        if tool_calls is not None:
            msg["tool_calls"] = tool_calls
        self.conversation.append(msg)

    def add_tool_result(self, content, tool_name=None):
        """Add a tool result message."""
        msg = {"role": "tool", "content": content}
        if tool_name:
            msg["tool_name"] = tool_name
        self.conversation.append(msg)

    def get_assistant_response(self):
        """Run the tool loop until a final response. Returns (content, thinking).
        Used by the CLI version (main.py). The web app uses its own streaming logic."""

        while True:
            content = ""
            thinking = ""
            tool_calls = []

            try:
                stream = self.client.chat(
                    model=self.chat_model,
                    messages=self.conversation,
                    tools=self.tools,
                    stream=True,
                    think=self.think,
                    keep_alive=self.keep_alive,
                    options=self.options,
                )
            except Exception as e:
                print(f"\n⚠️  Could not connect to Ollama: {e}")
                return None, None

            thinking_started = False
            content_started = False

            for chunk in stream:
                msg = chunk["message"]

                if hasattr(msg, "thinking") and msg.thinking:
                    if not thinking_started:
                        print("\n💭 Thinking...\n", end="", flush=True)
                        thinking_started = True
                    print(msg.thinking, end="", flush=True)
                    thinking += msg.thinking

                if msg.content:
                    if not content_started:
                        if thinking_started:
                            print("\n\n📝 Response:\n", end="", flush=True)
                        content_started = True
                    print(msg.content, end="", flush=True)
                    content += msg.content

                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    tool_calls.extend(msg.tool_calls)

            prompt_tokens = chunk.get("prompt_eval_count", 0)
            output_tokens = chunk.get("eval_count", 0)

            if tool_calls:
                self.add_message("assistant", content, thinking=thinking, tool_calls=tool_calls)
                for tc in tool_calls:
                    name = tc["function"]["name"]
                    args = tc["function"]["arguments"]
                    print(f"\n🔧 Calling {name}({args})...", flush=True)

                    try:
                        func = self.available_functions[name]
                        result = str(func(**args))
                    except KeyError:
                        result = f"Error: unknown tool '{name}'"
                    except TypeError as e:
                        expected = inspect.signature(func).parameters
                        result = f"Error calling {name}: {e}. Expected: {list(expected.keys())}, got: {args}"
                    except Exception as e:
                        result = f"Error in {name}: {type(e).__name__}: {e}"

                    print(f"   ➜ {result}", flush=True)
                    self.add_tool_result(content=result, tool_name=name)
                # loop again so the model can respond with the tool results
            else:
                self.add_message("assistant", content, thinking=thinking)
                total_used = prompt_tokens + output_tokens
                num_ctx = (self.options or {}).get("num_ctx", 2048)  # default fallback
                pct = (total_used / num_ctx) * 100
                print(f"\n[{pct:.2f}% | {total_used} / {num_ctx} tokens]")
                return content, thinking

    def conversation_to_dict(self):
        """Convert conversation with ollama objects to JSON-serializable dict."""
        result = []
        for msg in self.conversation:
            msg_dict = {"role": msg["role"], "content": msg["content"]}

            if "thinking" in msg and msg["thinking"]:
                msg_dict["thinking"] = msg["thinking"]

            if "tool_calls" in msg and msg["tool_calls"]:
                msg_dict["tool_calls"] = [
                    {
                        "function": {
                            "name": tc["function"]["name"],
                            "arguments": tc["function"]["arguments"]
                        }
                    }
                    for tc in msg["tool_calls"]
                ]

            if "tool_name" in msg:
                msg_dict["tool_name"] = msg["tool_name"]

            result.append(msg_dict)
        return result

    def save_conversation(self, path):
        """Save conversation to JSON file, creating parent directories if needed."""
        # Get the directory from the path
        directory = os.path.dirname(path)
        # Create parent directories if they don't exist
        if directory:
            os.makedirs(directory, exist_ok=True)
        # Save the conversation
        with open(path, 'w') as f:
            json.dump(self.conversation_to_dict(), f, indent=2)
