# tools.py
# Example at the bottom to understand whats going on here (without decorator function for simplicity)


# Registry
_functions = {}
_schemas = []


def tool(schema: dict):
    """Decorator that registers a function as a tool."""
    def decorator(func):
        _functions[func.__name__] = func
        _schemas.append({
            "type": "function",
            "function": {
                "name": func.__name__,
                **schema
            }
        })
        return func
    return decorator


# --- Define your tools below ---

@tool({
    "description": "Get current weather for a city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"}
        },
        "required": ["city"]
    }
})
def get_weather(city: str) -> str:
    return f"22°C sunny in {city}"


@tool({
    "description": "Get the current time in a timezone",
    "parameters": {
        "type": "object",
        "properties": {
            "timezone": {"type": "string", "description": "e.g. Europe/Berlin"}
        },
        "required": ["timezone"]
    }
})
def get_time(timezone):
    from datetime import datetime
    from zoneinfo import ZoneInfo
    return datetime.now(ZoneInfo(timezone)).strftime("%H:%M")




# #################################################
# EXAMPLE TO UNDERSTAND WTF IS GOING ON HERE
# something like this:
#
# # Your tools
#def get_weather(city: str) -> str:
#    return f"22°C sunny in {city}"
#
#available_functions = { #--------> this is "_functions" in this file
#    "get_weather": get_weather,
#
#
# tools = [ #----------> this is "_schemas" in this file
#    {
#        "type": "function",
#        "function": {
#            "name": "get_weather",
#            "description": "Get current weather for a city",
#            "parameters": {
#                "type": "object",
#                "properties": {
#                    "city": {"type": "string", "description": "City name"}
#                },
#                "required": ["city"]
#            }
#        }
#    }
#]
# #################################################
