import ollama
import timeimport ollama
import tkinter as tk
from tkinter import scrolledtext
import threading

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Chatbot")
        self.root.geometry("600x700")
        self.root.configure(bg='#2b2b2b')
        
        # Conversation history
        self.messages = [
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
        
        # Header
        header = tk.Label(root, text="💬 Personal AI Assistant", font=('Arial', 16, 'bold'), 
                         bg='#1e1e1e', fg='#00d9ff', pady=10)
        header.pack(fill=tk.X)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Arial', 11),
                                                      bg='#1e1e1e', fg='#ffffff', 
                                                      padx=10, pady=10, state=tk.DISABLED)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Configure tags for styling
        self.chat_display.tag_config('user', foreground='#00d9ff', font=('Arial', 11, 'bold'))
        self.chat_display.tag_config('bot', foreground='#00ff88', font=('Arial', 11, 'bold'))
        self.chat_display.tag_config('message', foreground='#ffffff')
        
        # Input frame
        input_frame = tk.Frame(root, bg='#2b2b2b')
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.input_field = tk.Text(input_frame, height=3, font=('Arial', 11), 
                                   bg='#3c3c3c', fg='#ffffff', insertbackground='#ffffff')
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.input_field.bind('<Return>', self.send_message)
        self.input_field.bind('<Shift-Return>', lambda e: None)
        
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message,
                                    bg='#00d9ff', fg='#000000', font=('Arial', 11, 'bold'),
                                    cursor='hand2', width=8)
        self.send_button.pack(side=tk.RIGHT)
        
        # Welcome message
        self.display_message("Bot", "👋 Hello! I'm your personal AI assistant. How can I help you today?")
        
    def display_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", sender.lower())
        self.chat_display.insert(tk.END, f"{message}\n\n", 'message')
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def send_message(self, event=None):
        if event and not event.state & 0x1:  # Check if Shift is not pressed
            user_input = self.input_field.get("1.0", tk.END).strip()
            
            if user_input:
                self.display_message("You", user_input)
                self.input_field.delete("1.0", tk.END)
                self.send_button.config(state=tk.DISABLED)
                
                # Run in thread to avoid freezing GUI
                threading.Thread(target=self.get_bot_response, args=(user_input,), daemon=True).start()
            
            return 'break'
        
    def get_bot_response(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})
        
        try:
            response = ollama.chat(model='llama3', messages=self.messages)
            bot_message = response['message']['content']
            self.messages.append({'role': 'assistant', 'content': bot_message})
            
            self.root.after(0, self.display_message, "Bot", bot_message)
        except Exception as e:
            self.root.after(0, self.display_message, "Bot", f"❌ Error: {str(e)}")
        finally:
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()

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
