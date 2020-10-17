import numpy as np
import shlex
import subprocess
import sys
import wave
import os

from deepspeech import Model
from timeit import default_timer as timer

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

############ LOAD MODEL (source: https://github.com/AASHISHAG/deepspeech-german)
dir_path = os.path.abspath(os.path.dirname(__file__))
model_load_start = timer()
# sphinx-doc: python_ref_model_start
model_path = dir_path + '/output_graph.tflite'
ds = Model(model_path)
# sphinx-doc: python_ref_model_stop
model_load_end = timer() - model_load_start
print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

desired_sample_rate = ds.sampleRate()

scorer_load_start = timer()
scorer_path = dir_path + '/kenlm.scorer'
ds.enableExternalScorer(scorer_path)
scorer_load_end = timer() - scorer_load_start
print('Loaded scorer in {:.3}s.'.format(scorer_load_end), file=sys.stderr)
##########################


def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path), desired_sample_rate)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))

    return desired_sample_rate, np.frombuffer(output, np.int16)

def speech_to_text(audio_path):
    fin = wave.open(audio_path, 'rb')
    fs_orig = fin.getframerate()
    if fs_orig != desired_sample_rate:
        _, audio = convert_samplerate(audio_path, desired_sample_rate)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    fin.close()    
    result = ds.stt(audio)
    return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Running DeepSpeech inference.')
    parser.add_argument('--audio', required=False,
                        help='Path to the audio file to run (WAV format)', default='audio_2020-10-16_18-23-33.wav')
    args = parser.parse_args()

    text = speech_to_text(args.audio)
    print(text)
