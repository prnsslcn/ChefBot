import os
from flask import request, jsonify
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client(api_key = None)

def generate_image(prompt):
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )

        image_url = response.data[0].url
        return jsonify({"image_url": image_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
