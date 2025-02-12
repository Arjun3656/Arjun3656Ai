import asyncio
import pywhatkit

from .basic import (
    google_search,
    youtube_search,
    open_app_or_website,
    close_app
)
from .image_gen import generate_images_parallel
from .system import system
from .content import content

from typing import List, Callable, Awaitable, Union



async def process(command: str) -> Union[Callable[..., Awaitable], str]:
    func: Callable[..., Awaitable] = None

    
    if command.startswith("open "):  # Handle "open" commands.
        if "open it" in command:  # Ignore "open it" commands.
            pass

        if "open file" == command:  # Ignore "open file" commands.
            pass
        
        else:
            func = asyncio.to_thread(open_app_or_website, command.removeprefix("open "))  # Schedule app opening.

    elif command.startswith("general "):  # Placeholder for general commands.
        pass

    elif command.startswith("realtime "):  # Placeholder for real-time commands.
        pass
    
    elif command.startswith("generate image"):
        func = asyncio.create_task(generate_images_parallel(command.removeprefix("generate image")))
        
    elif command.startswith("close "):  # Handle "close" commands.
        func = asyncio.to_thread(close_app, command.removeprefix("close "))  # Schedule app closing.
        
    elif command.startswith("play "):  # Handle "play" commands.
        asyncio.to_thread(pywhatkit.playonyt, command.removeprefix("play "))  # Schedule YouTube playback.
        func = "I Play your Music, Enjoy your Song Sir"
    elif command.startswith("content "):  # Handle "content" commands.
        func = asyncio.to_thread(content, command.removeprefix("content "))  # Schedule content creation.

    elif command.startswith("google search "):  # Handle Google search commands.
        func = asyncio.to_thread(google_search, command.removeprefix("google search "))  # Schedule Google search.

    elif command.startswith("youtube search "):  # Handle YouTube search commands.
        func = asyncio.to_thread(youtube_search, command.removeprefix("youtube search "))  # Schedule YouTube search.

    elif command.startswith("system "):  # Handle system commands.
        func = asyncio.to_thread(system, command.removeprefix("system "))  # Schedule system command.

    return func

async def process_multiple(commands: List[str]):
    tasks = []
    
    for command in commands:
        func = await process(command)  # Ensure process is awaited to get the function.
        if func is not None:
            tasks.append(func)

    # Use asyncio.as_completed to handle responses as tasks complete.
    for completed_task in asyncio.as_completed(tasks):
        result = await completed_task
        yield result
