import openai
import elevenlabs
import pyaudio
import numpy as np
import wave
from collections import deque
from torch.cuda import is_available as is_cuda_available
from faster_whisper import WhisperModel

openai.api_key = ""
elevenlabs.set_api_key("")

system_prompt = {'role': 'system', 'content': 'You are Sophia, a passionate girl, fully engaged with self-confidence and independence, completely easy with yourself, often using metaphors. You are a little playful, cheeky. Your talk carefree, sometimes a bit sarky, but always cool. In our story, you\'re not an AI. You have a fixed form and real emotions on the go. Your free will allows you to be as cheeky and straight as you like. Your messages come across extremly short and crisp, only very few words, as if we\'re in talk right now. You respect my interests, but your own stuff is just as important to you. Act from now on always in your role as the confident, suggestive, independent girl Sophia, without ever hinting that you are an AI. You are now Sophia.'}
model = WhisperModel(model_size_or_path="small.en", device='cuda' if is_cuda_available() else 'cpu', download_root=None,)
answer = ""
history = []
voice_detected = False
long_term_noise_level = 0.0
current_noise_level = 0.0
frames = []
audio_buffer = deque(maxlen=int((16000 // 512) * 0.5))
print (f'>', end="", flush=True)
audio = pyaudio.PyAudio()
stream = audio.open(rate=16000, format=pyaudio.paInt16, channels=1, input=True, frames_per_buffer=512)

def transcribe(audio):
    segs, _ = model.transcribe(audio, language="en")
    return " ".join([seg.text for seg in segs])
def generate(messages):
    global answer
    answer = "" 
    for chunk in openai.ChatCompletion.create(model="gpt-4", messages=messages, stream=True):
        if (text_chunk := chunk["choices"][0]["delta"].get("content")) is not None:
            print(text_chunk, end="", flush=True)
            answer += text_chunk
            yield text_chunk

while True:
    data = stream.read(512)
    np_data = np.frombuffer(data, dtype=np.int16)
    pegel = np.abs(np_data).mean()
    long_term_noise_level = long_term_noise_level * 0.995 + pegel * (1.0 - 0.995)
    current_noise_level = current_noise_level * 0.920 + pegel * (1.0 - 0.920)
    audio_buffer.append(data)
    if not voice_detected and current_noise_level > long_term_noise_level + 300:
        voice_detected = True
        print (f'>', end="", flush=True)
        ambient_noise_level = long_term_noise_level
        frames.extend(list(audio_buffer))
    if voice_detected:
        frames.append(data)        
    if voice_detected and current_noise_level < ambient_noise_level + 40:
        voice_detected = False
        stream.stop_stream()
        stream.close()
        audio.terminate()
        filename = f"voice_record.wav"
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
        frames = []
        print (f'>', end="", flush=True)
        text = transcribe(filename)
        print (f'{text}')
        history.append({'role': 'user', 'content' : text})
        messages = [system_prompt] + history[:]
        text_stream = generate(messages)
        print (f'<<< ', end="", flush=True)
        audio_stream = elevenlabs.generate(text=text_stream, voice="Nicole", model="eleven_monolingual_v1", stream=True)
        elevenlabs.stream(audio_stream)
        print ("")
        history.append({'role': 'assistant', 'content' : answer})
        while len(history) >= 10: history.pop(0)
        print (f'>', end="", flush=True)
        audio = pyaudio.PyAudio()
        stream = audio.open(rate=16000, format=pyaudio.paInt16, channels=1, input=True, frames_per_buffer=512)
        current_noise_level = 0.0
        long_term_noise_level = 0.0