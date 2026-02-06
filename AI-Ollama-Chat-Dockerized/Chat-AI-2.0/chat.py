from pathlib import Path

class Chat:
    def __init__(self, system_prompt_path=""):
        if system_prompt_path != "":
            self.system_prompt = Path(system_prompt_path).read_text(encoding="utf-8")
            self.conversation = [{"role": "system", "content": self.system_prompt}]
        else:
            self.conversation = []

    def add_message(self, role, content, thinking=None, tool_calls=None):
        """Add a user or assistant message"""
        msg = {"role": role, "content": content}
        if thinking:
            msg["thinking"] = thinking
        if tool_calls:
            msg["tool_calls"] = tool_calls
        self.conversation.append(msg)

    def add_tool_result(self, content, tool_name=None):
        """Add a tool result message"""
        msg = {"role": "tool", "content": content}
        if tool_name:
            msg["tool_name"] = tool_name
        self.conversation.append(msg)
