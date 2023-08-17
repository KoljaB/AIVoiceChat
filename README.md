# Project

A full functional voice-based low latency AI talk companion.  

Uses faster_whisper and elevenlabs input streaming. 

Responds to spoken words in real-time.

📺 **[Watch a Demo Video](https://www.youtube.com/watch?v=lq_Q6y47iUU)** 

You may get this faster as I'm limited to a 10Mbit/s connection here - thank you, Telekom Germany.

### Modes of Operation:

1. **Hands-Free Mode** - Use `voice_talk_vad.py` to automatically detect speech. 
2. **Manual Mode** - Use `voice_talk.py` to toggle recording with the spacebar.

## Setup 🛠

### 1. API Keys:

Replace `your_openai_key` and `your_elevenlabs_key` with your OpenAI and ElevenLabs API key values in the code.

### 2. Dependencies:

Install the required Python libraries:
```bash
pip install openai elevenlabs pyaudio wave keyboard faster_whisper numpy torch 
```

### 3. Run the Script:

Execute the main script based on your mode preference:

```bash
python voice_talk_vad.py
```
or
```bash
python voice_talk.py
```

## Usage voice_talk_vad.py 🎙

Talk into your microphone.  
Listen to the reply.

## Usage voice_talk.py 🎙

1. Press the **space bar** to initiate talk.
2. Speak your heart out.
3. Hit the **space bar** again once you're done.
4. Listen to reply.

## Contribution 🤝

Feel free to fork, improve, and submit pull requests. For major changes, please open an issue first.

## Acknowledgements 💖

Huge shoutout to:
- The developers behind [faster_whisper](https://github.com/guillaumekln/faster-whisper).
- [ElevenLabs](https://www.elevenlabs.io/) for the fast, crystal-clear voice API.
- [OpenAI](https://www.openai.com/) for the GPT-4 model.
