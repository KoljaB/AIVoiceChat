# Project

A seamless and real-time voice interaction with AI.  
Uses faster_whisper and elevenlabs input streaming.  
Offers low latency responses to spoken input.

**[🎥 Watch a Demo Video](https://www.youtube.com/watch?v=lq_Q6y47iUU)** 
> **Note**: The demo is conducted on a 10Mbit/s connection, so actual performance might be more impressive on faster connections.

### Modes of Operation:
1. **Hands-Free Mode** - Automatically detects speech using `voice_talk_vad.py`.
2. **Manual Mode** - Toggle recording on/off with the spacebar using `voice_talk.py`.

## 🛠 Setup:

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
## 🎙 How to Use:

### For `voice_talk_vad.py`:

Talk into your microphone.  
Listen to the reply.

### For `voice_talk.py`:

1. Press the **space bar** to initiate talk.
2. Speak your heart out.
3. Hit the **space bar** again once you're done.
4. Listen to reply.

## 🤝 Contribute

Feel free to fork, improve, and submit pull requests. If you're considering significant changes or additions, please start by opening an issue.

## 💖 Acknowledgements

Huge shoutout to:
- The hardworking developers behind [faster_whisper](https://github.com/guillaumekln/faster-whisper).
- [ElevenLabs](https://www.elevenlabs.io/) for their cutting-edge voice API.
- [OpenAI](https://www.openai.com/) for pioneering with the GPT-4 model.
