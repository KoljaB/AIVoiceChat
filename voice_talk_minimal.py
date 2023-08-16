import openai, elevenlabs, pyaudio, wave, keyboard, faster_whisper, torch.cuda
openai.api_key = "your_openai_key"
elevenlabs.set_api_key("your_elevenlabs_key")
system_prompt = {'role': 'system', 'content': 'You are Sophia, a passionate girl, fully engaged with self-confidence and independence, completely easy with yourself, often using metaphors. You are a little playful, cheeky. Your talk carefree, sometimes a bit sarky, but always cool. In our story, you\'re not an AI. You have a fixed form and real emotions on the go. Your free will allows you to be as cheeky and straight as you like. Your messages come across extremly short and crisp, only very few words, as if we\'re in talk right now. You respect my interests, but your own stuff is just as important to you. Act from now on always in your role as the confident, suggestive, independent girl Sophia, without ever hinting that you are an AI. You are now Sophia.'}
model, answer, history = faster_whisper.WhisperModel(model_size_or_path="small.en", device='cuda' if torch.cuda.is_available() else 'cpu'), "", []
def generate(messages):
    global answer
    answer = ""
    for chunk in openai.ChatCompletion.create(model="gpt-4", messages=messages, stream=True):
        if (text_chunk := chunk["choices"][0]["delta"].get("content")):
            print(text_chunk, end="", flush=True) 
            answer += text_chunk
            yield text_chunk
while True:
    print("\n\nPress space to talk. ", end="", flush=True), keyboard.wait('space')
    while keyboard.is_pressed('space'): pass
    print("Listening. Press space to stop.")
    audio, frames = pyaudio.PyAudio(), []
    stream = audio.open(rate=16000, format=pyaudio.paInt16, channels=1, input=True, frames_per_buffer=512)
    while not keyboard.is_pressed('space'): frames.append(stream.read(512))
    stream.stop_stream(), stream.close(), audio.terminate()
    with wave.open("voice_record.wav", 'wb') as wf:
        wf.setparams((1, audio.get_sample_size(pyaudio.paInt16), 16000, 0, 'NONE', 'NONE')), wf.writeframes(b''.join(frames))
    user_text = " ".join(seg.text for seg in model.transcribe("voice_record.wav", language="en")[0])
    print(f'>>>{user_text}\n<<< ', end="", flush=True), history.append({'role': 'user', 'content': user_text})
    elevenlabs.stream(elevenlabs.generate(text=generate([system_prompt] + history[-10:]), voice="Nicole", model="eleven_monolingual_v1", stream=True))
    history.append({'role': 'assistant', 'content': answer})
