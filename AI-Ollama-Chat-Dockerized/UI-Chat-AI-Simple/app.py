from flask import Flask, render_template, request, jsonify, Response
from chat import Chat
from tools import _functions as available_functions, _schemas as tools
import inspect
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Load config
with open("config.json") as f:
    config = json.load(f)

CONVERSATIONS_DIR = config["conversations_dir"]
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

# In-memory chat instances keyed by conversation ID
active_chats = {}

# Metadata file for conversation names
METADATA_FILE = os.path.join(CONVERSATIONS_DIR, "_metadata.json")


def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE) as f:
            return json.load(f)
    return {}


def save_metadata(meta):
    with open(METADATA_FILE, "w") as f:
        json.dump(meta, f, indent=2)


def create_chat():
    """Create a fresh Chat instance from config."""
    opts = {}
    if config.get("num_ctx"):
        opts["num_ctx"] = config["num_ctx"]

    chat = Chat(
        host=config["ollama_host"],
        chat_model=config["chat_model"],
        tools=tools,
        available_functions=available_functions,
        think=config.get("think", True),
        keep_alive=config.get("keep_alive", -1),
        options=opts if opts else None,
    )
    system_prompt = config.get("system_prompt_path")
    if system_prompt and os.path.exists(system_prompt):
        chat.add_system_prompt(system_prompt)
    return chat


def get_chat(conv_id):
    """Get or restore a Chat instance for a conversation."""
    if conv_id in active_chats:
        return active_chats[conv_id]

    chat = create_chat()
    filepath = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
    if os.path.exists(filepath):
        chat.load_conversation(filepath)

    active_chats[conv_id] = chat
    return chat


def auto_title(messages):
    """Extract a title from the first user message."""
    for msg in messages:
        if msg.get("role") == "user":
            text = msg["content"].strip()
            return text[:60] + ("..." if len(text) > 60 else "")
    return "New Chat"


def sse_event(event, data):
    """Format a Server-Sent Event."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# ── Routes ──────────────────────────────────────────────────


@app.route("/")
def index():
    return render_template("index.html", stream_enabled=config.get("stream", True))


@app.route("/api/conversations")
def list_conversations():
    """Return all saved conversations (id + title), newest first."""
    meta = load_metadata()
    convos = []
    for fname in os.listdir(CONVERSATIONS_DIR):
        if not fname.endswith(".json") or fname.startswith("_"):
            continue
        filepath = os.path.join(CONVERSATIONS_DIR, fname)
        try:
            cid = fname.removesuffix(".json")
            with open(filepath) as fh:
                data = json.load(fh)
            convos.append({
                "id": cid,
                "title": meta.get(cid, {}).get("title") or auto_title(data),
                "modified": os.path.getmtime(filepath),
            })
        except Exception:
            pass
    convos.sort(key=lambda c: c["modified"], reverse=True)
    return jsonify(convos)


@app.route("/api/conversations/<conv_id>")
def get_conversation(conv_id):
    """Return full message history for a conversation."""
    filepath = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
    if not os.path.exists(filepath):
        return jsonify([])
    with open(filepath) as f:
        data = json.load(f)
    visible = [m for m in data if m["role"] != "system"]
    return jsonify(visible)


@app.route("/api/conversations/new", methods=["POST"])
def new_conversation():
    """Create a new conversation and return its ID."""
    conv_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
    chat = create_chat()
    active_chats[conv_id] = chat
    return jsonify({"id": conv_id})


@app.route("/api/conversations/<conv_id>/rename", methods=["POST"])
def rename_conversation(conv_id):
    """Rename a conversation."""
    data = request.json
    new_title = data.get("title", "").strip()
    if not new_title:
        return jsonify({"error": "Empty title"}), 400
    meta = load_metadata()
    meta.setdefault(conv_id, {})["title"] = new_title
    save_metadata(meta)
    return jsonify({"ok": True})


@app.route("/api/conversations/<conv_id>", methods=["DELETE"])
def delete_conversation(conv_id):
    """Delete a conversation."""
    filepath = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
    active_chats.pop(conv_id, None)
    meta = load_metadata()
    meta.pop(conv_id, None)
    save_metadata(meta)
    return jsonify({"ok": True})


# ── Shared tool execution ────────────────────────────────────


def _execute_tool(chat, func_name, func_args):
    """Execute a tool call and return the result string."""
    try:
        func = chat.available_functions[func_name]
    except KeyError:
        return f"Error: unknown tool '{func_name}'"
    try:
        return str(func(**func_args))
    except TypeError as e:
        expected = inspect.signature(func).parameters
        return f"Error calling {func_name}: {e}. Expected args: {list(expected.keys())}, got: {func_args}"
    except Exception as e:
        return f"Error in {func_name}: {type(e).__name__}: {e}"


def _call_ollama(chat):
    """Single Ollama streaming call, returns (content, thinking, tool_calls)."""
    content = ""
    thinking = ""
    tool_calls = []

    stream = chat.client.chat(
        model=chat.chat_model,
        messages=chat.conversation,
        tools=chat.tools,
        stream=True,
        think=chat.think,
        keep_alive=chat.keep_alive,
        options=chat.options,
    )

    for chunk in stream:
        msg = chunk["message"]
        if hasattr(msg, "thinking") and msg.thinking:
            thinking += msg.thinking
        if msg.content:
            content += msg.content
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tool_calls.extend(msg.tool_calls)

    return content, thinking, tool_calls


# ── Non-streaming chat endpoint ─────────────────────────────


@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    """Send a message and get the assistant response (non-streaming)."""
    data = request.json
    conv_id = data["conversation_id"]
    message = data["message"].strip()

    if not message:
        return jsonify({"error": "Empty message"}), 400

    chat = get_chat(conv_id)
    chat.add_message("user", message)

    try:
        content, thinking = _blocking_tool_loop(chat)
    except Exception as e:
        return jsonify({"error": f"Ollama error: {e}"}), 502

    chat.save_conversation(os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json"))

    return jsonify({
        "content": content,
        "thinking": thinking if thinking else None,
    })


def _blocking_tool_loop(chat):
    """Run the tool loop until a final response. Returns (content, thinking)."""
    while True:
        content, thinking, tool_calls = _call_ollama(chat)

        if tool_calls:
            chat.add_message("assistant", content, thinking=thinking, tool_calls=tool_calls)
            for tc in tool_calls:
                name = tc["function"]["name"]
                args = tc["function"]["arguments"]
                result = _execute_tool(chat, name, args)
                chat.add_tool_result(content=result, tool_name=name)
        else:
            chat.add_message("assistant", content, thinking=thinking)
            return content, thinking


# ── Streaming chat endpoint (SSE) ──────────────────────────


@app.route("/api/chat/stream", methods=["POST"])
def chat_stream():
    """Send a message and stream the response via Server-Sent Events."""
    data = request.json
    conv_id = data["conversation_id"]
    message = data["message"].strip()

    if not message:
        return jsonify({"error": "Empty message"}), 400

    chat = get_chat(conv_id)
    chat.add_message("user", message)

    def generate():
        try:
            for event_type, event_data in _stream_tool_loop(chat):
                yield sse_event(event_type, event_data)
        except Exception as e:
            yield sse_event("error", {"error": str(e)})

        # Save after completion
        chat.save_conversation(os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json"))
        yield sse_event("done", {})

    return Response(generate(), mimetype="text/event-stream")


def _stream_tool_loop(chat):
    """
    Generator that yields SSE events while running the tool loop.
    """
    while True:
        assistant_thinking = ""
        assistant_content = ""
        tool_calls = []

        try:
            stream = chat.client.chat(
                model=chat.chat_model,
                messages=chat.conversation,
                tools=chat.tools,
                stream=True,
                think=chat.think,
                keep_alive=chat.keep_alive,
                options=chat.options,
            )
        except Exception as e:
            yield ("error", {"error": f"Could not connect to Ollama: {e}"})
            return

        try:
            for chunk in stream:
                msg = chunk["message"]

                if hasattr(msg, "thinking") and msg.thinking:
                    assistant_thinking += msg.thinking
                    yield ("thinking", {"chunk": msg.thinking})

                if msg.content:
                    assistant_content += msg.content
                    yield ("content", {"chunk": msg.content})

                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    tool_calls.extend(msg.tool_calls)
        except Exception as e:
            yield ("error", {"error": f"Stream interrupted: {e}"})
            return

        if tool_calls:
            chat.add_message("assistant", assistant_content, thinking=assistant_thinking, tool_calls=tool_calls)

            for tc in tool_calls:
                name = tc["function"]["name"]
                args = tc["function"]["arguments"]
                yield ("tool_call", {"name": name, "arguments": args})

                result = _execute_tool(chat, name, args)
                yield ("tool_result", {"name": name, "result": result})
                chat.add_tool_result(content=result, tool_name=name)
        else:
            chat.add_message("assistant", assistant_content, thinking=assistant_thinking)
            return


if __name__ == "__main__":
    print(f"\n  Running on http://localhost:{config.get('port', 5000)}\n")
    app.run(debug=True, host="0.0.0.0", port=config.get("port", 5000))
