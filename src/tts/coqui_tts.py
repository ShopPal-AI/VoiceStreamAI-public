import torch
from TTS.api import TTS



# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False).to(device)

# Run TTS
tts.tts_to_file(text="Hi, how can I help you?", file_path="test.wav")
wav = tts.tts("hi, how can I help you?")
print(type(wav))
