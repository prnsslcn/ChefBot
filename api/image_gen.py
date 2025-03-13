import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = '')

# prompt = input("Prompt: ")
prompt = "A delicious creamy potato gratin dish in warm lighting"

response = client.images.generate(
  model="dall-e-3",
  prompt=prompt,
  size="1024x1024",
  quality="hd",
  n=1,
)

image_url = response.data[0].url
print(image_url)