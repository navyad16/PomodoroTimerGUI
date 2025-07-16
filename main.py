from gtts import gTTS

tts = gTTS("Time's up! Take a break.", lang="en")
tts.save("alert.mp3")
print("alert.mp3 created successfully!")
