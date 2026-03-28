import json

# ---------------------------------------------------------------------------
# Tool implementations (the actual Python functions)
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
# Tool schemas (JSON Schema format for the model)
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
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
# Tool execution helper
# ---------------------------------------------------------------------------


def execute_tool_call(name: str, arguments_json: str) -> str:
    """Run a tool by name with JSON arguments, return result as JSON string."""
    args = json.loads(arguments_json)
    print(f"  -> Calling: {name}({args})")

    func = TOOL_FUNCTIONS.get(name)
    if func:
        result = func(**args)
    else:
        result = {"error": f"Unknown tool: {name}"}

    return json.dumps(result)
