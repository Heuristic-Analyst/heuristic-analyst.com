import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"),
)

model = os.environ.get("OPENAI_MODEL", "gpt-4o")
stream = os.environ.get("OPENAI_STREAM", "false").lower() in ("true", "1", "yes")


# ---------------------------------------------------------------------------
# STEP 1: Define your tools (the actual Python functions)
# ---------------------------------------------------------------------------


def get_weather(city: str) -> dict:
    """Simulate a weather lookup. In reality, you'd call a weather API here."""
    return {
        "city": city,
        "temperature_celsius": 22,
        "condition": "Sunny",
    }


# Map of function name -> callable, so we can look them up dynamically
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
}


# ---------------------------------------------------------------------------
# STEP 2: Describe the tools for the model (JSON Schema format)
# ---------------------------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. 'Berlin' or 'Tokyo'.",
                    },
                },
                "required": ["city"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# STEP 3: The tool-calling loop
# ---------------------------------------------------------------------------


def print_thinking(message):
    """Print thinking/reasoning content if present."""
    thinking = getattr(message, "reasoning_content", None) or getattr(
        message, "reasoning", None
    )
    if thinking:
        print("=== Thinking ===")
        print(thinking)
        print()


def execute_tool_call(tool_call) -> str:
    """Run a tool call and return the result as a JSON string."""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"  -> Calling: {name}({args})")

    func = TOOL_FUNCTIONS.get(name)
    if func:
        result = func(**args)
    else:
        result = {"error": f"Unknown tool: {name}"}

    return json.dumps(result)


def run_standard(messages):
    """Standard (non-streaming) loop with tool support."""
    while True:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message
        print_thinking(message)

        # STEP 4: Check if the model wants to call tools
        if message.tool_calls:
            print("=== Tool Calls ===")

            # Append the assistant's message (with tool_calls) to the conversation
            messages.append(message.model_dump())

            # STEP 5: Execute each tool and feed results back
            for tool_call in message.tool_calls:
                result = execute_tool_call(tool_call)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

            # STEP 6: Loop back so the model can respond with the tool results
            print("\n=== Sending tool results back to model... ===\n")
            continue

        # No tool calls — the model gave a final text response
        print("=== Response ===")
        print(message.content)
        break


def run_streaming(messages):
    """Streaming loop with tool support."""
    while True:
        stream_response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            stream=True,
        )

        # Collect streamed content
        thinking_parts = []
        content_parts = []
        tool_calls_map = {}  # index -> {id, name, arguments}
        in_thinking = False
        in_content = False

        for chunk in stream_response:
            delta = chunk.choices[0].delta if chunk.choices else None
            if not delta:
                continue

            # Thinking/reasoning
            reasoning = getattr(delta, "reasoning_content", None) or getattr(
                delta, "reasoning", None
            )
            if reasoning:
                if not in_thinking:
                    print("=== Thinking ===", flush=True)
                    in_thinking = True
                print(reasoning, end="", flush=True)
                thinking_parts.append(reasoning)

            # Regular content
            if delta.content:
                if not in_content:
                    if in_thinking:
                        print("\n")
                    print("=== Response ===", flush=True)
                    in_content = True
                print(delta.content, end="", flush=True)
                content_parts.append(delta.content)

            # Tool calls arrive in chunks — collect them
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

        # Check if we got tool calls
        if tool_calls_map:
            print("=== Tool Calls ===")

            # Reconstruct the assistant message for conversation history
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

            # Execute tools and feed results back
            for tc_data in assistant_tool_calls:

                class _ToolCall:
                    """Minimal wrapper to reuse execute_tool_call."""

                    def __init__(self, d):
                        self.id = d["id"]
                        self.function = type(
                            "F",
                            (),
                            {
                                "name": d["function"]["name"],
                                "arguments": d["function"]["arguments"],
                            },
                        )()

                result = execute_tool_call(_ToolCall(tc_data))
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc_data["id"],
                        "content": result,
                    }
                )

            print("\n=== Sending tool results back to model... ===\n")
            continue

        # No tool calls — done
        break


# ---------------------------------------------------------------------------
# STEP 7: Run it
# ---------------------------------------------------------------------------

messages = []
# system_prompt = os.environ.get("OPENAI_SYSTEM_PROMPT")
# if system_prompt:
#    messages.append({"role": "system", "content": system_prompt})
messages.append(
    {
        "role": "user",
        "content": "What's the weather in Berlin and Tokyo? First do a tool call for berlin, then aswer me, then do it for tokiyo.",
    }
)

if stream:
    run_streaming(messages)
else:
    run_standard(messages)

print(messages)
