import os
import sys

sys.path.insert(0, os.getcwd())

import subprocess
from config import content_generation_llm


# Nested function to open a file in Notepad.
def OpenNotepad(File):
    default_text_editor = 'notepad.exe'  # Default text editor.
    subprocess.Popen([default_text_editor, File])  # Open the file in Notepad.

def content(Topic: str):
    content_generation_llm.messages = []
    ContentByAI = content_generation_llm.run(Topic)  # Generate content using AI.

    # Save the generated content to a text file.
    with open(rf"data\content\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)  # Write the content to the file.
        file.close()

    OpenNotepad(rf"data\content\{Topic.lower().replace(' ','')}.txt")  # Open the file in Notepad.
    return "I have opened the file in Notepad. You can check it out."


if __name__ == '__main__':
    content("write content about numbers")