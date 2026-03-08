from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI
import re

app = Flask(__name__)

# Hugging Face Router client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")  # Set your HF_TOKEN in environment
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message")
    try:
        # Strict system prompt to avoid <think> and internal reasoning
        system_prompt = (
            "You are a friendly AI assistant. ONLY reply with user-facing text in simple English Hindi. "
            "Do NOT generate any internal reasoning, thought process, or <think> tags. "
            "Never explain how you are thinking. "
            "Use short sentences, examples, and emojis when helpful. "
            "Your output should be clean, ready-to-show text."
        )
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",  # Free chat-compatible model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        reply = completion.choices[0].message.content
        # Strip any stray <think> blocks just in case
        reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL).strip()
    except Exception as e:
        reply = f"AI Error: {e}"
    return jsonify({"reply": reply})

