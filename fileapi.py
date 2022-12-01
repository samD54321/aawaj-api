from flask import Flask, request, Response
import os
from os.path import join

import soundfile as sf
import numpy as np
import torch

import sys

sys.path.append('tacotron2')
sys.path.append('tacotron2/waveglow')

from hparams import create_hparams
from model import Tacotron2
from layers import TacotronSTFT
from audio_processing import griffin_lim
from text import text_to_sequence
from waveglow.denoiser import Denoiser



force_download_TT2 = True
#add the path to your Aawaj model and waveglow vocoder model
tacotron2_pretrained_model = '/home/sampanna/Desktop/MAJOR/assets/Aawaj'
waveglow_pretrained_model = '/home/sampanna/Desktop/MAJOR/assets/waveglow_256channels_ljs_v3.pt'#@param {type:"string"}





thisdict = {}
for line in reversed((open('merged.dict.txt', "r").read()).splitlines()):
    thisdict[(line.split(" ",1))[0]] = (line.split(" ",1))[1].strip()
def ARPA(text):
    out = ''
    for word_ in text.split(" "):
        word=word_; end_chars = ''
        while any(elem in word for elem in r"!?,.;") and len(word) > 1:
            if word[-1] == '!': end_chars = '!' + end_chars; word = word[:-1]
            if word[-1] == '?': end_chars = '?' + end_chars; word = word[:-1]
            if word[-1] == ',': end_chars = ',' + end_chars; word = word[:-1]
            if word[-1] == '.': end_chars = '.' + end_chars; word = word[:-1]
            if word[-1] == ';': end_chars = ';' + end_chars; word = word[:-1]
            else: break
        try: word_arpa = thisdict[word.upper()]
        except: word_arpa = ''
        if len(word_arpa)!=0: word = "{" + str(word_arpa) + "}"
        out = (out + " " + word + end_chars).strip()
    if out[-1] != ";": out = out + ";"
    return out

#torch.set_grad_enabled(False)


hparams = create_hparams()


# Loading Tacotron2 
hparams.sampling_rate = 22050 
hparams.max_decoder_steps = 1000 # How long the audio will be before it cuts off (1000 = 11 seconds)
hparams.gate_threshold = 0.1 # Model must be 90% sure the clip is over before ending generation (the higher this number is, the more likely that the AI will keep generating until it reaches the Max Decoder Steps)
model = Tacotron2(hparams)
model.load_state_dict(torch.load(tacotron2_pretrained_model)['state_dict'])
_ = model.cuda().eval().half()

# Load WaveGlow
waveglow = torch.load(waveglow_pretrained_model)['model']
waveglow.cuda().eval().half()
for k in waveglow.convinv:
    k.float()
denoiser = Denoiser(waveglow)


def synthesize(text):
    sigma = 0.8
    denoise_strength = 0.324
    raw_input = True # disables automatic ARPAbet conversion, useful for inputting your own ARPAbet pronounciations or just for testing.
                    # should be True if synthesizing a non-English language

    for i in text.split("\n"):
        if len(i) < 1: continue;
        print(i)
        if raw_input:
            if i[-1] != ";": i=i+";" 
        else: i = ARPA(i)
        print(i)
        with torch.no_grad(): # save VRAM by not including gradients
            sequence = np.array(text_to_sequence(i, ['english_cleaners']))[None, :]
            sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()
            mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
        

            audio = waveglow.infer(mel_outputs_postnet, sigma=sigma); 
            print(""); 
            sf.write("speech.wav", np.float32(audio[0].data.cpu().numpy()), 22050)

    return  join(os.getcwd(), "speech.wav")

app = Flask(__name__)

@app.route('/api', methods = ['GET'])
def returnAudio():
    d = {}
    inputchr = str(request.args['query'])
    if(inputchr[0]==" "):
        inputchr= inputchr[1:]
    path = synthesize(inputchr)
    d['output'] = path
    return Response(open(path, 'rb'), mimetype='audio/wav',)





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)