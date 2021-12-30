import asyncio
import subprocess
import time
import os
import shutil
from datetime import datetime
from subprocess import Popen

from pip._internal import main as pipmain

try:
   from google.cloud import texttospeech
except ImportError:
    pipmain(['install', 'google-cloud-texttospeech'])
    from google.cloud import texttospeech

try:
   from websockets import serve
except ImportError:
    pipmain(['install', 'websockets'])
    from websockets import serve

try:
   import yaml
except ImportError:
    pipmain(['install', 'pyyaml'])
    import yaml

voicePath = os.getcwd() + "\\Output"
configPath = os.getcwd() + "\\config.yml"
with open(configPath, "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cfg["MuteHelper"]["credentialPath"]
publicIP = cfg["MuteHelper"]["publicIP"]
region = cfg["MuteHelper"]["region"]
gender = cfg["MuteHelper"]["gender"]
genderNum = 0

try:
    os.makedirs(os.getcwd() + "\\Output\\")
except FileExistsError:
    shutil.rmtree(os.getcwd() + "\\Output\\")
    os.makedirs(os.getcwd() + "\\Output\\")

subprocess.Popen(["python", "-m", "http.server", "--directory", "Output"])

if (gender.upper() == "MALE"):
    genderNum = 1
elif (gender.upper() == "FEMALE"):
    genderNum = 2
elif (gender.upper() == "NEUTRAL"):
    genderNum = 3

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code = region, ssml_gender=texttospeech.SsmlVoiceGender(genderNum)
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

def get_time():
        time = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]:")
        return time

async def server(websocket, path):
    # this code runs for each connected client

    print (get_time(),'Client connected!')

    fileName = ""
    filePath = ""

    isWaiting = False
    
    async for message in websocket:
        try:

            # this runs for each message a client sends a message

            command = message.split("\b")[0]
            message = message.split("\b")[1]
            
            if command == "getSpeech" and not isWaiting:

                # Set the text input to be synthesized
                synthesis_input = texttospeech.SynthesisInput(text = message)

                # Perform the text-to-speech request on the text input with the selected
                # voice parameters and audio file type
                response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )

                # The response's audio_content is binary.
                fileName = str(int(time.time())) + ".wav"
                filePath = os.getcwd() + "\\Output\\"
                with open(filePath + fileName, "wb") as out:
                    # Write the response to the output file.
                    out.write(response.audio_content)
                    print(get_time() + 'Audio content written to file ' + fileName)
                await websocket.send("play" + publicIP + "/" + fileName)
                isWaiting = True

            elif command == "donePlaying":
                os.remove(filePath + fileName)
                await websocket.send("ready")
                
                isWaiting = False
        except:
            print (get_time(),'Client disconnected!')

async def main():
    async with serve(server, "localhost", 8766):
        await asyncio.Future()

asyncio.run(main())