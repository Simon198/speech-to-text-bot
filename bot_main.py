from speech_to_text import speech_to_text
from converter import convert_ogg_to_wav
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import os

dir_path = os.path.abspath(os.path.dirname(__file__))

class EmptyStringException(Exception):
    def __str__(self):
        return 'Keine Sprache bemerkt'

def audio(update: Update, context: CallbackContext):
    try:
        ogg_path = dir_path + '/tmp.ogg'
        wav_path = dir_path + '/tmp.wav'

        file = context.bot.getFile(update.message.voice.file_id)
        file.download(ogg_path)
        convert_ogg_to_wav(ogg_path, wav_path)
        result = speech_to_text(wav_path)
        if len(result) == 0:
            raise EmptyStringException()
        update.message.reply_text(result)
        
    except Exception as err:
        update.message.reply_text('Ein Fehler ist aufgetreten:\n' + str(err))

def main ():
    with open('TOKEN.txt', 'r') as file:
        token = file.read()
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.voice, audio))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__': 
    main()