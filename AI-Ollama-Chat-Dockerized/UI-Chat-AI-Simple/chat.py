from pathlib import Path
import os
import json
import ollama


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

    def load_conversation(self, filepath):
        """Load a conversation from a JSON file."""
        with open(filepath, 'r') as f:
            self.conversation = json.load(f)

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
