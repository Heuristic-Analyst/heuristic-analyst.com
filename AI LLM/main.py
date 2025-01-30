from OllamaWrapper import Ollama

# When running this file directly
if __name__ == "__main__":
    # Create connection to Ollama
    ollama = Ollama()  # Uses default localhost:11434

    # Start chat with 14B model (creates first conversation notebook)
    ai_agent_one = ollama.start_chat("deepseek-r1:14b")
    
    # First question with streaming response and auto-printing
    print("First response (streaming with auto-print):")
    ai_agent_one.chat("Can you explain quantum entanglement to a 5 year old?", stream=True, print_response=True)

    # Follow-up question with auto-printing (non-streaming)
    print("\n\nFollow-up (non-streaming with auto-print):")
    ai_agent_one.chat("I forgot what I said to you, what did I ask you? Simply repeat the question", print_response=True)

    # Switch to 1.5B model (creates new conversation notebook)
    print("\nSwitching to 14B model:")
    second_chat = ollama.start_chat("deepseek-r1:1.5b")  # Old chat remains but unused
    
    # Simple question to new model with auto-print
    print("Simple math question with auto-print:")
    second_chat.chat("What's 2+2?", print_response=True)

    # Streaming request with different model and auto-print
    print("\n1.5B model streaming response with auto-print:")
    second_chat.chat("Explain neural networks briefly", stream=True, print_response=True)
