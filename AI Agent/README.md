You need an LLM Provider, in my case a Ollama server via docker (podman to be specific).

You can then connect it using the Openai library - I did it so people can easily switch between providers/models, as many models are compatible with it.

It can use tools, agentically, meaning it could:
User input -> thinking -> decides to call multiple tools -> get the tool return -> thinks again (may decide to use a tool now, then wait and then another tool again) -> tool call -> print the output of the tool to the user -> think again -> toolcall -> think -> last output to user

This is really cool
