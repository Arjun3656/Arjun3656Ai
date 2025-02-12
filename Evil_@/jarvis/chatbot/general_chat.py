import os
import sys

sys.path.insert(0, os.getcwd())


from config import Config, general_chat_llm
from datetime import datetime
from typing import Dict, List

system_prompt = f"""
Hello, I am {Config.USER_NAME},
You are a very accurate and advanced AI chatbot named {Config.ASSISTANT_NAME}.
Which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""


system_prompt_dict = {"role": "system", "content": system_prompt}


def get_datetime_dict() -> Dict:
    return {
        "role": "system",
        "content": f'Please use this real-time information if needed,\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.',
    }


def general_chat(prompt: str, messages: List[Dict]) -> str:
    messages.insert(0, system_prompt_dict)
    messages.insert(1, get_datetime_dict())

    general_chat_llm.messages = messages

    return general_chat_llm.run(prompt)


if __name__ == "__main__":
    print(general_chat("what is 2+2? and tell me the date ", []))
