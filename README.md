# MidjourneyWrapper Discord Bot

🤖 This is a fork of a Python app that interacts with Discord to prompt the Midjourney Bot commands. The original repository can be found [here](https://github.com/Debupt/MidjourneyWrapper).

## Installation

To run the application, you need to fill out the secrets and run the following command:

```
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

```
{
    "prompt": "Some prompt, --v 5",
    "refId": "12"
}
```
### Remember to not include /imagine in the prompt!

## Build

This project was built with the following tools in mind:

- [n8n](https://n8n.io/)
- [gpt-3-turbo](https://platform.openai.com/docs/models/gpt-3-5)
- [Strapi v4](https://github.com/strapi/strapi)

## License

This project is licensed under the [MIT License](https://github.com/Debupt/MidjourneyWrapper/blob/main/LICENSE).