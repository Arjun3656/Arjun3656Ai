import os
import sys

sys.path.insert(0, os.getcwd())


from googlesearch import search
from datetime import datetime
from textwrap import dedent
from typing import Dict, List
from config import Config, general_chat_llm

system_prompt = f"""
Hello, I am {Config.USER_NAME},\
You are a very accurate and advanced AI chatbot named {Config.ASSISTANT_NAME} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***
"""


system_prompt_dict = {"role": "system", "content": system_prompt}


def get_datetime_dict() -> Dict:
    return {
        "role": "system",
        "content": f'Please use this real-time information if needed,\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.',
    }


def google_search(query: str) -> str:
    results = list(
        search(query, advanced=True, num_results=Config.NUMBER_OF_SEARCH_RESULTS)
    )

    formated_results = []
    for index, result in enumerate(results, start=1):
        s = f"{index}. URL: {result.url}, Title: {result.title}, Description: {result.description}"
        formated_results.append(s)

    formated_string = "\n\n".join(formated_results)

    answer = dedent(f"""
    The search results for {repr(query)} are:
    
    [start]
    
    {formated_string}
    
    [end]
    """)
    return answer


def real_time_chat(prompt: str, messages: List[Dict]) -> str:
    messages.insert(0, system_prompt_dict)
    messages.insert(1, get_datetime_dict())
    messages.insert(2, {"role": "system", "content": google_search(prompt)})

    general_chat_llm.messages = messages

    return general_chat_llm.run(prompt)


if __name__ == "__main__":
    print(real_time_chat("what is 2+2? and tell me the date ", []))
