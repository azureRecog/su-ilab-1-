# This program uses IBM watson API to convert speech to text and vice versa
# Program is used with faceRecognizer.py when the person has been recognized
#and we would like in what languages they want to be greeted
# Authors: Nancy Xiao & Ayumi Mizuno
import pyaudio
import wave
import json,os
import time
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1 

# greeting
text_to_speech = TextToSpeechV1(
    # Enter username and password here
    username='',
    password='',
    x_watson_learning_opt_out=True)  # Optional flag
speech = "Face recognized,   what language do you prefer?   English, German, French or Japanese.    Or say skip"

with open(join(dirname(__file__), 'greeting.mp3'),
      'wb') as audio_file:
    audio_file.write(
    text_to_speech.synthesize(speech, accept='audio/wav',
                              voice="en-US_MichaelVoice"))

os.startfile('greeting.mp3')

# the recording part starts only after the greeting.mp3 is done
time.sleep(7)

#recording part(we found this on the web, did not change any line)
CHUNK = 1024 
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2 
RATE = 44100 
RECORD_SECONDS = 4 # Enter how many seconds you want to record
WAVE_OUTPUT_FILENAME = "soundsound.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data) # 2 bytes(16 bits) per channel

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()



#speech to text
speech_to_text = SpeechToTextV1(
    username="",
    password="",
    x_watson_learning_opt_out=False
)

#print(json.dumps(speech_to_text.models(), indent=2))

#print(json.dumps(speech_to_text.get_model('en-US_BroadbandModel'), indent=2))

with open(join(dirname(__file__), './soundsound.wav'),
          'rb') as audio_file:
    report = (json.dumps(speech_to_text.recognize(
        audio_file, content_type='audio/wav', timestamps=False,
        word_confidence=False),
        indent=2))

#Extract what users have said in the recording
reportList = report.split("\"")
#print(reportList)
transcript =""
for i in range(len(reportList)-1):
    if "transcript" in reportList[i]:
        transcript += (reportList[i+2])

print(transcript)



