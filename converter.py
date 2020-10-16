from pydub import AudioSegment
import os

def convert_ogg_to_wav (ogg_path, result_path):
    ogg_file = AudioSegment.from_ogg(ogg_path)
    ogg_file.export(result_path, format='wav')