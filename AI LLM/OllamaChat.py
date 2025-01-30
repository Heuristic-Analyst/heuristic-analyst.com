"""
This code lets you chat with llm models run with Ollama - so a Ollama Wrapper
This code uses only the original Ollama API, using requests and json

It first creates a session with the Ollama server that should run in the background.
Then one create blank conversations by initializing the .start_chat function which takes the model name as a parameter
Then one can chat with the model by using the .chat function. If you want to stream the message from the llm, so that every word pops up after its generated, to not wait until the whole answer is been generated, 
  you need also to do stream=True
I also implemented a print param so it prints automatically for stream True and False accordingly!

Below you can see examples of how to do it.
"""

# Import necessary libraries
import requests  # Handles HTTP requests to communicate with the Ollama server
import json      # Converts Python objects to/from JSON format for API communication

# Main class to interact with Ollama
class Ollama:
    # Initialize connection to Ollama server
    def __init__(self, base_url='http://localhost:11434'):
        # Clean up the base URL and store it
        self.base_url = base_url.rstrip('/')  # Remove any trailing slash
        # Create a persistent HTTP connection
        self.session = requests.Session()     # Like keeping a phone line open

    # Inner class to manage individual chat conversations
    class ChatSession:
        def __init__(self, ollama, model):
            # Reference to the parent Ollama instance
            self.ollama = ollama  # Our connection to the server
            # Which AI model to use (like choosing a brain)
            self.model = model    # e.g. "deepseek-r1:1.5b"
            # Conversation history (memory of the chat)
            self.messages = []    # Stores all messages in order: user, AI, user, AI...
        
        # Main method to send messages to the AI
        def chat(self, message, stream=False, print_response=False, **kwargs):
            # Add user's message to history
            self.messages.append({"role": "user", "content": message})
            
            # Make the API call to Ollama
            response = self.ollama._request('/api/chat', {
                "model": self.model,       # Which model to use
                "messages": self.messages, # Full chat history
                "stream": stream,          # Stream response or wait for complete
                **kwargs                   # Any extra parameters
            }, stream)
            
            # Handle different response types
            if not stream:
                # For complete responses
                assistant_message = response['message']['content']
                # Save AI's response to history
                self.messages.append({"role": "assistant", "content": assistant_message})
                # Print if requested
                if print_response:
                    print(assistant_message)
                return assistant_message  # Return full text
            else:
                # For streaming responses (word by word)
                if print_response:
                    full_response = []
                    # Process generator and print chunks
                    for chunk in self._stream_handler(response):
                        print(chunk, end='', flush=True)
                        full_response.append(chunk)
                    print()  # Ensure newline after streaming
                    return ''.join(full_response)
                else:
                    return self._stream_handler(response)

        # Handles word-by-word streaming responses
        def _stream_handler(self, response):
            full_response = []  # Temporary storage for the complete response
            for chunk in response:
                # Extract text from each streaming chunk
                content = chunk.get('message', {}).get('content', '')
                full_response.append(content)  # Build complete response
                yield content  # Send each piece immediately to caller
                
            # After stream finishes, save complete response to history
            self.messages.append({
                "role": "assistant",
                "content": ''.join(full_response)  # Combine all chunks
            })

        # Reset conversation history
        def reset(self):
            self.messages = []  # Clear chat memory

    # Start a new chat session with specific model
    def start_chat(self, model):
        return self.ChatSession(self, model)  # Create new conversation notebook

    # Internal method to handle API requests
    def _request(self, endpoint, data, stream=False):
        # Build full API URL
        url = f"{self.base_url}{endpoint}"  # e.g. http://localhost:11434/api/chat
        # Send POST request
        response = self.session.post(url, json=data, stream=stream)
        # Check for HTTP errors
        response.raise_for_status()  # Crash if error (like 404)
        # Return appropriate response format
        return response.json() if not stream else self._handle_stream(response)

    # Process streaming response line by line
    def _handle_stream(self, response):
        # Read streaming response line by line
        for line in response.iter_lines():
            if line:  # Skip empty lines
                try:
                    # Convert JSON line to Python dictionary
                    yield json.loads(line.decode('utf-8'))
                except json.JSONDecodeError as e:
                    raise ValueError(f"Bad data received: {line}") from e

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
