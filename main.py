import os
from dotenv import load_dotenv
import time
from flask import Flask, request, jsonify
from midjourney_bot import MidjourneyBot
from waitress import serve

load_dotenv(dotenv_path=".env")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

midjourney_bot = MidjourneyBot()

app = Flask(__name__)

INVALID_PROMPT_ERROR = {"status": "error", "message": "Invalid prompt."}


def wait_for_image():
    while True:
        message = midjourney_bot.messages(1)[0]
        if midjourney_bot.validate_image_url(message):
            break
        print(midjourney_bot.content(message))
        midjourney_bot.wait()


@app.route("/prompt", methods=["POST"])
def receive_prompt():
    data = request.get_json()
    prompt = data.get("prompt", None)
    refId = data.get("refId", None)

    if not prompt:
        return jsonify(INVALID_PROMPT_ERROR)

    midjourney_bot.wait()
    midjourney_bot.ask(prompt)
    midjourney_bot.wait()

    headers = {}
    additional_data = {
        "refId": f"{refId}",
        "ref": "api::article.article",
        "field": "image",
    }

    # Wait for the original image to be generated
    wait_for_image()

    # Trigger the up_scale command
    original_message = midjourney_bot.messages(1)[0]
    print(original_message)
    up_scale_status = midjourney_bot.up_scale(1, original_message)
    print("Up_scale status:", up_scale_status)

    # Wait for the upscaled image to be generated
    wait_for_image()

    upscaled_message = midjourney_bot.messages(1)[0]
    image_url = midjourney_bot.get_image_url(upscaled_message)

    payload = midjourney_bot.save_image(
        image_url, WEBHOOK_URL, headers, additional_data
    )
    return jsonify(payload)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
