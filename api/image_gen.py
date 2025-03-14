import os
from flask import request, jsonify
import openai
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

load_dotenv()

# 실행시 11번줄 #주석처리
client = openai.Client(api_key = None)

# 실행시 14번줄 #주석제거후 key 추가
# client = openai.Client(api_key = '')
memory = ConversationBufferMemory(memory_key="history")

response_schemas = [
    ResponseSchema(name="image_url"),
    ResponseSchema(name="style"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

def generate_image(prompt):
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    history = memory.load_memory_variables({})
    stored_style = history.get("history", [])

    style = stored_style[0] if isinstance(stored_style, list) and stored_style else "high-resolution, ultra-realistic, professional food photography, cinematic lighting"

    optimized_prompt = f"A high-quality image of {prompt}. Styled with {style}. Shot with a professional DSLR, soft lighting, ultra-realistic textures, and sharp details."

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=optimized_prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )

        image_url = response.data[0].url
        memory.save_context({"prompt": prompt}, {"history": [style]})
        json_string = f'{{"image_url": "{image_url}", "style": "{style}"}}'
        formatted_response = output_parser.parse(json_string)
        return jsonify(formatted_response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
