# Speech to Text Bot
The project implements a [Telegram bot](https://github.com/python-telegram-bot/python-telegram-bot) that generates text from a voice message and replies it to the user.

## Implementation

The project uses [DeepSpeech](https://github.com/mozilla/DeepSpeech) as Speech-to-Text method. The code is derived from the [Python API Usage example](https://deepspeech.readthedocs.io/en/v0.8.2/Python-Examples.html).

## Run the application
In order to get the bot running, you need to create a file named *TOKEN.txt* and add the Bot Token. Also you need to download the DeepSpeech model and scorer and add it to the project. The German model used for this project can be downloaded [here](https://github.com/AASHISHAG/deepspeech-german#trained-models).