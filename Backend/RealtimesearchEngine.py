from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Initialize chat history
try:
    with open("Data/ChatLog.json", "r") as f:
        message = load(f)
except:
    message = []
    with open("Data/ChatLog.json", "w") as f:
        dump(message, f)

# Google Search Function
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    answer += "[end]\n"
    return answer

# Real-time info
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%I")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    am_pm = current_date_time.strftime("%p")

    data = "Use this real-time information if needed:\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes : {second} seconds {am_pm}\n"
    return data

# Clean answer formatting
def AnswerModifier(answer):
    lines = answer.split("\n")
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

# System Prompt and Init
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": f"Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which also has real-time up-to-date information from the internet."}
]

# Main chat function
def RealtimeSearchEngine(prompt):
    global SystemChatBot, message

    # Load previous chat log
    try:
        with open("Data/ChatLog.json", "r") as f:
            message = load(f)
    except:
        message = []

    message.append({"role": "user", "content": prompt})

    # Append search results temporarily
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Send to Groq
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "user", "content": Information()}] + message,
        max_tokens=2024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )

    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content

    answer = answer.strip().replace("</s>", "")
    message.append({"role": "assistant", "content": answer})

    # Save chat log
    with open("Data/ChatLog.json", "w") as f:
        dump(message, f, indent=4)

    # Remove the temporary Google search result from system message
    SystemChatBot.pop()

    return AnswerModifier(answer)

# REPL loop
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
