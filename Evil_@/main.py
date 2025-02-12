import asyncio
import threading

from gui.main import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    SetMicrophoneStatus,
    GetMicrophoneStatus,
    GetAssistantStatus
)

from jarvis.chatbot.general_chat import general_chat
from jarvis.chatbot.real_time_chat import real_time_chat
from jarvis.model.dmm import dmm
from jarvis.vocalize.async_edgetts import text_to_speech, play_audio, textToSpeechBytes
from jarvis.vocalize.speach_to_text import SpeechRecognition
from jarvis.automation.controler import process_multiple
from modules.database.chat_history import ChatHistoryDB
from time import sleep

from config import sq_dict, Config


jarvis_chat_history = ChatHistoryDB("data/sql/chat_history.sql")
messages = jarvis_chat_history.getLastNMessages(
    Config.MAX_LLM_HISTORY, ["role", "content"]
)

default_chat = f"""
{Config.USER_NAME}: Hello {Config.ASSISTANT_NAME}, How are you?
{Config.ASSISTANT_NAME}: Welcome {Config.USER_NAME}. I am doing well. How may i help you?
""".strip()


def InitialExecution():
    SetMicrophoneStatus("False")
    SetAssistantStatus("Available...")
    
    if len(messages) != 0:
        ShowTextToScreen(default_chat)

    ChatLogIntegration()


def ChatLogIntegration():
    formatted_chatlog = ""
    for entry in messages:
        if entry["role"] == "user":
            formatted_chatlog += f"{Config.USER_NAME}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Config.ASSISTANT_NAME}: {entry['content']}\n"

    sq_dict["responses"] = formatted_chatlog.strip()


def add_message(role, content):
    messages.append({"role": role, "content": content})
    jarvis_chat_history.addMessage(role, content)


async def main_execution():

    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    
    ShowTextToScreen(f"{Config.USER_NAME}: {Query}")
    add_message("user", Query)
    
    SetAssistantStatus("Thinking...")

    decision: list[str] = dmm(Query)
    
    print("")
    print(f"Decision : {decision}")
    print("")

    general_query_flag = any([x for x in decision if x.startswith("general")])
    real_time_query_flag = any([x for x in decision if x.startswith("realtime")])

    mearged_query = " and ".join(
        [
            " ".join(i.split()[1:])
            for i in decision
            if i.startswith("general") or i.startswith("realtime")
        ]
    )

    funcs_response = process_multiple(decision)
    funcs_text = ""
    audios = []
    audio_playing_task = None
    async for response in funcs_response:
        if isinstance(response, str):
            funcs_text += response
        audios.append(asyncio.create_task(textToSpeechBytes(response)))
    
    if funcs_text:
        ShowTextToScreen(f"{Config.ASSISTANT_NAME}: {funcs_text}")

    if audios:
        audio_bytes = await asyncio.gather(*audios)

        def play_all_audios(audio_bytes):
            for audio in audio_bytes:
                play_audio(audio)

        audio_playing_task = asyncio.create_task(
            asyncio.to_thread(play_all_audios, audio_bytes)
        )

    llm_response = ""
    
    if real_time_query_flag or (general_query_flag and real_time_query_flag):
        SetAssistantStatus("Searching...")
        llm_response = real_time_chat(mearged_query, messages)
    
    elif general_query_flag:
        SetAssistantStatus("Thinking...")
        general_query = [
            x.removeprefix("general ") for x in decision if x.startswith("general")
        ]
        q = "".join(general_query)
        llm_response = general_chat(q, messages)
    
    if audio_playing_task:
        await audio_playing_task
    if funcs_text:
        add_message("assistant", funcs_text)
    if llm_response:
        add_message("assistant", llm_response)
        ShowTextToScreen(f"{Config.ASSISTANT_NAME}: {llm_response}")
        await text_to_speech(llm_response)

    if 'exit' in decision:
        exit(0)


async def main_loop():
    InitialExecution()
    while True:
        
        if GetMicrophoneStatus() == "True":
            await main_execution()
        else:
            
            if GetAssistantStatus() == "Available...":
                await asyncio.sleep(0.1)
            else:
                SetAssistantStatus("Available...")


def gui():
    sleep(3)
    GraphicalUserInterface()


if __name__ == "__main__":
    gui_thread = threading.Thread(target=gui, daemon=True)
    gui_thread.start()
    asyncio.run(main_loop())
