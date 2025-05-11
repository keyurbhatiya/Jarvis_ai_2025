from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import requests
import subprocess
import keyboard
import asyncio
import os

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = [
    "zCubwf", "hgKElc", "LTKOO", "SY7ric", "ZOLcW", "gsrt", "vk_bk", "FzvWSb", "YwPhnf",
    "pclqee", "tw-Data-text", "tw-text-small", "tw-ta", "IZ6rdc", "05uR6d", "vlzY6d",
    "webanswers-webanswers_table_webanswers-table", "dDoNo", "ikb48b", "sXLage",
    "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36'

client = Groq(api_key=GroqAPIKey)

professional_response = [
    "your satisfaction is my top priority; feel free to reach  out if there's anthing else i can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

messages = []

SystemChatBot = [
    {"role": "system", "content": f"Hello, I am {os.environ.get('Username')}, You are a very accurate and advanced AI chatbot named {os.environ.get('AssistantName')} which also has real-time up-to-date information from the internet."},
]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            # model = "mixtral-8x7b-32768",
            model="llama3-70b-8192",
            messages = SystemChatBot + messages,
            max_tokens = 2024,
            temperature = 0.7,
            top_p = 1,
            stream = True,
            stop = None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        return Answer
    Topic:str = Topic.replace("content ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()
    
    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True



def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(Topic):
    playonyt(Topic)
    return True

def OpenApp(app,sess=requests.Session()):
    try:
        appopen(app,match_closest=True,output=True,throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a',{'jsname':'UWckNb'})
            return [link.get('href') for link in links if link.get('href')]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Falied to retrieve search results.")
                return None
        
        html = search_google(app)

        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
        return True



def CloseApp(app):

    if "chrome" in app:
        pass
    else:
        try:
            close(app,match_closest=True,output=True,throw_error=True)
            return True
        except:
            return False

def System(command):

    def mute():
        keyboard.press_and_release("volumemute")

    def unmute():
        keyboard.press_and_release("volumemute")

    def volume_up():
        keyboard.press_and_release("volumeup")

    def volume_down():
        keyboard.press_and_release("volumedown")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        if command.startswith("open "):

            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.replace("open ", ""))
                funcs.append(fun)
        elif command.startswith("genereal "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.replace("close ", ""))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.replace("play ", ""))
            funcs.append(fun)
        
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.replace("content ", ""))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.replace("google search ", ""))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function found for {command}")
    
    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result,str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):
        pass

    return True
