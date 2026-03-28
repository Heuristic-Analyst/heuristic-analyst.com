import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOL_SCHEMAS, execute_tool_call

load_dotenv()

# ---------------------------------------------------------------------------
# Provider config — change these (or your .env) to switch providers
# ---------------------------------------------------------------------------

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"),
)

MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
STREAM = os.environ.get("OPENAI_STREAM", "false").lower() in ("true", "1", "yes")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _print_thinking(message):
    """Print thinking/reasoning content if present."""
    thinking = getattr(message, "reasoning_content", None) or getattr(
        message, "reasoning", None
    )  # returns extracted reasoning value or None
    if thinking:
        print("=== Thinking ===")
        print(thinking)
        print()


# ---------------------------------------------------------------------------
# Standard (non-streaming) loop
# ---------------------------------------------------------------------------


def run_standard(messages: list):
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        message = response.choices[0].message
        # If there is a reasoning/thinking, then it will be printed
        _print_thinking(message)

        if message.tool_calls:
            print("=== Tool Calls ===")
            messages.append(message.model_dump())

            for tool_call in message.tool_calls:
                result = execute_tool_call(
                    tool_call.function.name, tool_call.function.arguments
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

            print("\n=== Sending tool results back to model... ===\n")
            continue

        print("=== Response ===")
        print(message.content)
        messages.append({"role": "assistant", "content": message.content})
        break


# ---------------------------------------------------------------------------
# Streaming loop
# ---------------------------------------------------------------------------


def run_streaming(messages: list):
    while True:
        stream_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
            stream=True,
        )

        thinking_parts = []
        content_parts = []
        tool_calls_map = {}
        in_thinking = False
        in_content = False

        for chunk in stream_response:
            delta = chunk.choices[0].delta if chunk.choices else None
            if not delta:
                continue

            reasoning = getattr(delta, "reasoning_content", None) or getattr(
                delta, "reasoning", None
            )
            if reasoning:
                if not in_thinking:
                    print("=== Thinking ===", flush=True)
                    in_thinking = True
                print(reasoning, end="", flush=True)
                thinking_parts.append(reasoning)

            if delta.content:
                if not in_content:
                    if in_thinking:
                        print("\n")
                    print("=== Response ===", flush=True)
                    in_content = True
                print(delta.content, end="", flush=True)
                content_parts.append(delta.content)

            if delta.tool_calls:
                for tc_chunk in delta.tool_calls:
                    idx = tc_chunk.index
                    if idx not in tool_calls_map:
                        tool_calls_map[idx] = {"id": "", "name": "", "arguments": ""}
                    if tc_chunk.id:
                        tool_calls_map[idx]["id"] = tc_chunk.id
                    if tc_chunk.function and tc_chunk.function.name:
                        tool_calls_map[idx]["name"] = tc_chunk.function.name
                    if tc_chunk.function and tc_chunk.function.arguments:
                        tool_calls_map[idx]["arguments"] += tc_chunk.function.arguments

        if content_parts:
            print()

        if tool_calls_map:
            print("=== Tool Calls ===")

            assistant_tool_calls = []
            for idx in sorted(tool_calls_map.keys()):
                tc = tool_calls_map[idx]
                assistant_tool_calls.append(
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {"name": tc["name"], "arguments": tc["arguments"]},
                    }
                )

            messages.append(
                {
                    "role": "assistant",
                    "content": "".join(content_parts) if content_parts else None,
                    "tool_calls": assistant_tool_calls,
                }
            )

            for tc_data in assistant_tool_calls:
                result = execute_tool_call(
                    tc_data["function"]["name"], tc_data["function"]["arguments"]
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc_data["id"],
                        "content": result,
                    }
                )

            print("\n=== Sending tool results back to model... ===\n")
            continue
        messages.append({"role": "assistant", "content": "".join(content_parts)})
        break


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def chat(messages: list):
    """Send messages to the model. Picks streaming vs standard based on config."""
    if STREAM:
        run_streaming(messages)
    else:
        run_standard(messages)
