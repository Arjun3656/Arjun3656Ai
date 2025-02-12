import os
import requests
from dotenv import load_dotenv
from modules.llm._groq import Groq, LLAMA_31_70B_VERSATILE
from modules.llm._cohere import Cohere, COMMAND_R_PLUS
from modules.database.sq_dict import SQLiteDict


load_dotenv(dotenv_path=".env")


class Settings:
    USER_NAME = os.getenv("USER_NAME", "User")
    ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")
    INPUT_LANGUAGE = os.getenv("INPUT_LANGUAGE", "en")
    ASSISTANT_VOICE = os.getenv("ASSISTANT_LANGUAGE", "en-CA-LiamNeural")
    COHERE_API_KEY = os.environ["COHERE_API_KEY"]
    GROQ_API_KEY = os.environ["GROQ_API_KEY"]
    HUGGINGFACE_API_KEY = os.environ["HUGGINGFACE_API_KEY"]
 
    
    # Internal
    NUMBER_OF_SEARCH_RESULTS = 5 # for real time chat resource. Increase for more results more accurate.
    # Speak to text
    ENGLISH_TRANSLATION = True # turn of this to get results in your input language
    # Image Generation
    IMAGE_GENERATION_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
    IMAGE_GENERATION_COUNT = 1 # one image per query
    # max message memory
    MAX_LLM_HISTORY = 60
    
    


Config = Settings()



cohere_llm = Cohere(
    COMMAND_R_PLUS,
    apiKey=Config.COHERE_API_KEY,
    logFile=r"log/cohere_llm.log"
)

groq_llm = Groq(
    LLAMA_31_70B_VERSATILE,
    apiKey=Config.GROQ_API_KEY,
    logFile=r"log/groq_llm.log"
)
# llm for chat bot
general_chat_llm = groq_llm
real_time_chat_llm = groq_llm

# content generation llm
content_generation_llm = groq_llm

# model
dmm_llm = cohere_llm

# free session
free_requests_session = requests.session()


# sq_dict
sq_dict = SQLiteDict(r"data/sql/persistent_dict.sql")


if __name__ == "__main__":
    print(Config.USER_NAME)
    print(Config.ASSISTANT_NAME)
    print(Config.INPUT_LANGUAGE)
    print(Config.ASSISTANT_VOICE)