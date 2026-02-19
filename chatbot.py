import ollama

def chat():
    print("Chatbot started! Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
        
        response = ollama.chat(model='llama3', messages=[
            {'role': 'user', 'content': user_input}
        ])
        
        print(f"Bot: {response['message']['content']}\n")

if __name__ == "__main__":
    chat()
