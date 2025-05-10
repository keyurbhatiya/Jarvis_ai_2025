import datetime
import json
from groq import Groq
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# System prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

systemChatBot = [{"role": "system", "content": System}]
chatlog_path = r"Data/ChatLog.json"

# Load chat log or initialize
try:
    with open(chatlog_path, "r") as f:
        message = json.load(f)
except FileNotFoundError:
    message = []
    with open(chatlog_path, "w") as f:
        json.dump(message, f, indent=4)

# Function to return real-time information
def RealtimeInformation():
    now = datetime.datetime.now()
    return (
        "Please use this real-time information if needed,\n"
        f"Day: {now.strftime('%A')},\n"
        f"Date: {now.strftime('%d')},\n"
        f"Month: {now.strftime('%B')},\n"
        f"Year: {now.strftime('%Y')},\n"
        f"Time: {now.strftime('%I')} hours : {now.strftime('%M')} minutes : "
        f"{now.strftime('%S')} seconds {now.strftime('%p')}\n"
    )

# Answer cleaner
def AnswerModifier(answer):
    lines = answer.split("\n")
    return "\n".join([line.strip() for line in lines if line.strip()])

# Chat function
def ChatBot(query):
    try:
        # Reload messages every time
        with open(chatlog_path, "r") as f:
            message = json.load(f)

        message.append({"role": "user", "content": query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=systemChatBot + [{"role": "user", "content": RealtimeInformation()}] + message,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
        )

        answer = ""
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                answer += delta.content

        answer = answer.replace("</s>", "")
        message.append({"role": "assistant", "content": answer})

        with open(chatlog_path, "w") as f:
            json.dump(message, f, indent=4)

        return AnswerModifier(answer)

    except Exception as e:
        print(f"[ERROR] {e}")
        return "Sorry, an error occurred. Please try again."

# CLI interface
if __name__ == "__main__":
    while True:
        try:
            user_input = input("Enter your question: ")
            if user_input.strip().lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            response = ChatBot(user_input)
            print(response)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
