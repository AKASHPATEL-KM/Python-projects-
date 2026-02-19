import ollama
import time
import sys

def typing_effect(text, delay=0.02):
    """Simulate typing effect for bot responses"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def chat():
    print("\n" + "="*50)
    print("🤖 Welcome to Your Personal AI Assistant!")
    print("="*50)
    print("I'm here to chat, help, and provide thoughtful insights.")
    print("Type 'quit', 'exit', or 'bye' to end our conversation.\n")
    
    # Conversation history with personality system prompt
    messages = [
        {
            'role': 'system',
            'content': '''You are a friendly, creative, and thoughtful AI assistant. 
            Your responses should be:
            - Warm and personable, like talking to a knowledgeable friend
            - Creative and engaging, using analogies or examples when helpful
            - Concise but insightful, avoiding overly long responses
            - Encouraging and positive in tone
            - Occasionally use emojis to add personality (but don't overdo it)
            Remember previous context in the conversation and reference it naturally.'''
        }
    ]
    
    while True:
        user_input = input("\n💬 You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['quit', 'exit', 'bye']:
            typing_effect("\n👋 It was great chatting with you! Take care and come back anytime!")
            break
        
        # Add user message to history
        messages.append({'role': 'user', 'content': user_input})
        
        # Get response with conversation context
        response = ollama.chat(model='llama3', messages=messages)
        bot_message = response['message']['content']
        
        # Add bot response to history
        messages.append({'role': 'assistant', 'content': bot_message})
        
        # Display with typing effect
        print("\n🤖 Bot: ", end="")
        typing_effect(bot_message)

if __name__ == "__main__":
    chat()
