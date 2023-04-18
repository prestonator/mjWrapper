# MidjourneyWrapper Discord Bot

🤖 This is a fork of a Python app that interacts with Discord to prompt the Midjourney Bot commands. The original repository can be found [here](https://github.com/Debupt/MidjourneyWrapper).

## Prerequisites
Rename the file `.env.template` to `.env` and fill in the following fields:

- `USER_TOKEN` - Your Discord User Token, please refer to [How can I obtain my User Token?](https://www.androidauthority.com/get-discord-token-3149920/) to learn how to get it.
- `SERVER_ID` - The ID of the server you want to send the prompts to, refer to [How do I find my server ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) to learn how to get it.
- `CHANNEL_ID` - The ID of the channel you want to send the prompts to, see the above link to learn how to get it.


## Installation

To run the application, run the following commands:

> Unix/macOS
```
python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

> Windows
```
py -m venv env
.\env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Features

This fork includes the following additional features:

- Automatic image upscaling and sending the link to a webhook
- Removed the functionality of saving the image to a file
- Added Flask to send prompts to its endpoint using HTTP POST requests

## Usage

To use the MidjourneyWrapper API, you need to have access to your Discord credentials, e.g. User Token, Server ID, and Channel ID.

To interface with it, you can send the following example payload to the Flask endpoint "/prompt", using the HTTP POST method:

> Remember to not include /imagine in the prompt!
> "refId" is optional, but it is recommended to include it to automate uploading the image to Strapi.
```
{
    "prompt": "Some prompt, --v 5",
    "refId": "12"
}
```

## Build

This project was built with the following tools in mind:

- [n8n](https://n8n.io/)
- [gpt-3-turbo](https://platform.openai.com/docs/models/gpt-3-5)
- [Strapi v4](https://github.com/strapi/strapi)

## License

This project is licensed under the [MIT License](https://github.com/Debupt/MidjourneyWrapper/blob/main/LICENSE).