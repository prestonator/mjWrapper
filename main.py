import os
from dotenv import load_dotenv
import time
from flask import Flask, request, jsonify
from midjourney_bot import MidjourneyBot
from waitress import serve

load_dotenv(dotenv_path=".env")
STRAPI_API_TOKEN = os.environ.get("STRAPI_API_TOKEN")
STRAPI_API_UPLOAD_URL = os.environ.get("STRAPI_API_UPLOAD_URL")

midjourney_bot = MidjourneyBot()

app = Flask(__name__)


@app.route("/prompt", methods=["POST"])
def receive_prompt():
    data = request.get_json()
    prompt = data.get("prompt", None)
    refId = data.get("refId", None)
    time.sleep(2)
    if prompt:
        time.sleep(2)
        midjourney_bot.ask(prompt)
        time.sleep(2)

        headers = {"Authorization": f"Bearer {STRAPI_API_TOKEN}"}
        additional_data = {
            "refId": f"{refId}",  # Replace this with the actual refId
            "ref": "api::article.article",
            "field": "image",
        }
        external_url = STRAPI_API_UPLOAD_URL

        # Wait for the original image to be generated
        while True:
            message = midjourney_bot.messages(1)[0]
            if midjourney_bot.validate_image_url(message):
                break
            print(midjourney_bot.content(message))
            time.sleep(5)

        # Trigger the up_scale command
        original_message = midjourney_bot.messages(1)[0]
        up_scale_status = midjourney_bot.up_scale(1, original_message)
        print("Up_scale status:", up_scale_status)

        # Wait for the upscaled image to be generated
        while True:
            upscaled_message = midjourney_bot.messages(1)[0]
            if (
                midjourney_bot.validate_image_url(upscaled_message)
                and upscaled_message["id"] != original_message["id"]
            ):
                break
            print(midjourney_bot.content(upscaled_message))
            time.sleep(5)

        upscaled_message = midjourney_bot.messages(1)[0]
        image_url = midjourney_bot.get_image_url(upscaled_message)
        midjourney_bot.save_image(
            image_url, "test.png", external_url, headers, additional_data
        )

        return jsonify(
            {"status": "success", "message": "Prompt received and processed."}
        )
    else:
        return jsonify({"status": "error", "message": "Invalid prompt."})


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
