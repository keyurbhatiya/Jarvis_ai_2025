# import asyncio
# from random import randint
# from PIL import Image
# import requests
# from dotenv import get_key
# import os
# from time import sleep


# def open_images(prompt):
#     folder_path = r"Data/Images"
#     prompt = prompt.replace(" ", "_")

#     Files = [f"{prompt}{i}.jpg" for i in range(1,5)]

#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)

#         try:
#            img = Image.open(image_path)
#            print(f"Opening image: {image_path}")
#            img.show()
#            sleep(1)
#         except IOError:
#             print(f"Error opening image: {image_path}")
            
# API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-x1-base-1.0"
# headers = {"Authorization": f"Bearer {get_key('.env','HuggingFaceAPIKey')}"}

# async def query(payload):
#     response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
#     return response.content

# async def generate_images(promt:str):
#     task = []

#     for _ in range(4):
#         payload = {
#             "inputs":f"{promt},quality=4k, sharpness=maximum,Ultra High details, high resolution, seed= {randint(0,1000000)}",
#         }
#         task = asyncio.create_task(query(payload))
#         task.append(task)
    
#     image_bytes_list = await asyncio.gather(*task)

#     for i, image_bytes in enumerate(image_bytes_list):
#         with open(fr"Data\Images\{promt.replace(' ','_')}{i+1}.jpg", "wb") as f:
#             f.write(image_bytes)

# def GenerateImages(prompt):
#     asyncio.run(generate_images(prompt))
#     open_images(prompt)

# while True:

#     try:
#         with open(r"Frontend\Files\ImageGeneration.data","r") as f:
#             Data: str = f.read()
        
#         Prompt,Status = Data.split(",")

#         if Status == "True":
#             print("Generating images...")
#             ImageStatus = GenerateImages(prompt=Prompt)

#             with open(r"Frontend\Files\ImageGeneration.data","w") as f:
#                 f.write("False,False")
#                 break
#         else:
#             sleep(1)
#     except Exception as e:
#        pass







# new code

import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

def open_images(prompt):
    folder_path = "Data/Images"
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError as e:
            print(f"Error opening image: {image_path}, {e}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
try:
    headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}
except Exception as e:
    print(f"Error loading API key: {e}")
    exit(1)

async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.content
    except requests.RequestException as e:
        print(f"Error querying API: {e}")
        return None

async def generate_images(prompt: str):
    tasks = []
    os.makedirs("Data/Images", exist_ok=True)  # Ensure directory exists

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            file_path = f"Data/Images/{prompt.replace(' ', '_')}{i+1}.jpg"
            try:
                with open(file_path, "wb") as f:
                    f.write(image_bytes)
                print(f"Saved image: {file_path}")
            except IOError as e:
                print(f"Error saving image {file_path}: {e}")

def GenerateImages(prompt):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

def main():
    file_path = "Frontend/Files/ImageGeneration.data"
    
    while True:
        try:
            with open(file_path, "r") as f:
                data = f.read().strip()
                if not data:
                    print("Empty file, waiting...")
                    sleep(1)
                    continue
                
                prompt, status = data.split(",")
                if status.strip() == "True":
                    print("Generating images...")
                    GenerateImages(prompt.strip())
                    with open(file_path, "w") as f:
                        f.write("False,False")
                    break
                else:
                    print("Status is False, waiting...")
                    sleep(1)
        except FileNotFoundError:
            print(f"File {file_path} not found, waiting...")
            sleep(1)
        except ValueError as e:
            print(f"Error parsing file {file_path}: {e}")
            sleep(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sleep(1)

if __name__ == "__main__":
    main()