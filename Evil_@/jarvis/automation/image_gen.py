import os
import sys

sys.path.insert(0, os.getcwd())


import asyncio
import requests
import os
import random
from time import sleep
from PIL import Image
from config import Config



# API details for the Hugging Face Stable Diffusion model
API_URL = Config.IMAGE_GENERATION_API_URL
headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_API_KEY}"}

current_task = None

# Function to open and display images based on a given prompt
def open_images(prompt: str):
    folder_path = r"data"  # Folder where the images are stored
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores
    
    # Generate the filenames for the images
    Files = [f"{prompt}{i}.jpg" for i in range(1, Config.IMAGE_GENERATION_COUNT+1)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before showing the next image

        except IOError:
            print(f"Unable to open {image_path}")


# Async function to send a query to the Hugging Face API
async def query(payload: dict):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload, timeout=300)
    return response.content

# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []

    # Create 4 image generation tasks
    for _ in range(Config.IMAGE_GENERATION_COUNT):
        payload = {
            "inputs": f"{prompt}. seed = {random.randint(1, 1000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)

    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
            f.write(image_bytes)
    
    await asyncio.to_thread(open_images, prompt)

async def generate_images_parallel(prompt: str):
    global current_task
    current_task = asyncio.create_task(generate_images(prompt))
    await asyncio.sleep(1)
    return "Generating images may take some time, ranging from 10 seconds to 5 minutes."


if __name__ == "__main__":
    import asyncio
    # import time
    
    asyncio.run(generate_images("a cat"))
    # time.sleep(5)