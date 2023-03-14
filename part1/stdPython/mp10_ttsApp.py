# TTS (Google Text to Speach)
# pip install gTTs
# pip install playsound

from gtts import gTTS
from playsound import playsound

text = '안녕하세요, gtt t t t t fragile입니다.'

tts = gTTS(text = text, lang='ko')
tts.save('./stdPython/output/hi.mp3')

print('생성완료!')

playsound('./stdPython/output/hi.mp3')

print('음성출력 완료!')