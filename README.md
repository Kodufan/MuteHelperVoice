# MuteHelperVoice
Ever worried people won't read your message bubbles? Concerned that vision challenged people can't see what you say?

Introducing the TTS Mute Helper! Using Google's Text to Speech API, you can speak up without speaking.

Using a modified copy of the popular Mute Helper, your messages can be read out in a voice with nearly any accent both male and female. The system in Neos is also so simple, it is easy to hook it up with your custom system!

It is slightly involved to get this system working, so if you have any problems not discussed here, please message me on Discord at Kodufan#7558.

## Step 1: Configure the Google end

First, you'll want to head [here](https://cloud.google.com/text-to-speech/docs/libraries#windows) and follow the instructions under the "Setting up authentication" area. You'll need to create a new project instead of selecting one. Once you have that json file, store it in some dedicated folder where you won't lose it.
After that, you will need to enable the text to speech API [here](https://console.cloud.google.com/marketplace/product/google/texttospeech.googleapis.com). Doing this requires a billing account to be added. Fear not though, as you only begin needing to pay after surpassing 1,000,000 words in a month, where every additional 1,000,000 words is $16. Suffice it to say, you will likely never reach that. If that still concerns you, you can always use a visa gift card or some other form of card you can easily cancel. 

## Step 2: Configure the network end

The TTS mute helper uses a simple Python HTTP server to make the audio available for other users to hear. You will need to forward the 8000 port for others to hear your messages.

## Step 3: Configure the Python end

This is easy. Simply put the file path to your json file you downloaded earlier and your IP (which can be found by googling "what is my IP?" provided you're not using a VPN) followed by :8000. Save it and run the Python program. It will download all the packages needed to run the server and start automatically.

## Step 4: Configure the Neos end

If you're using the TTS mute helper in my public folder (neosrec:///U-Kodufan/R-da99344a-2bb4-4740-b159-a58a5122c018), simply spawn it out and link it to you. The text to the upper left side of the message box should say "TTS Connected". If not, give it at least 10 seconds. If it still doesn't connect, please send me a message so I can help you out. 

If you want to add the system to your own mute helper, follow these steps:

- Add a dynamic variable space to the root of your mute helper titled "MuteHelper"
- Add a dynamic reference user variable titled "MuteHelper/User", a dynamic string variable titled "MuteHelper/Message", and a dynamic bool variable titled "MuteHelper/Playing"
- Add a websocket client with the URL: ws://localhost:8766 and a dynamic reference variable driver from "MuteHelper/User" driving the user field of the websocket component.
- Make sure the user variable points to you when using the mute helper, most easily done with an "active user slot" node pointing to the mute helper which should be parented to you. When you send a message, you should first write the message to the dynamic string and then send an impulse to "MuteHelper/Send"
- Make sure "MuteHelper/Playing" is written to false when unlinking the mute helper, otherwise it will not speak when you re-link it
