# whosblue on GitHub
# Project Start: 3/5/2024
# Started: 3/5/2024
# Completed: 
# Purpose: Claude 3 Opus interaction via Discord.
# Notes:
# Features: Claude 3 Opus text, Claude 3 Opus image processing (vision)

print("Importing packages...")
print("Importing discord...")
import discord
print("Importing anthropic...")
import anthropic
print("Importing asyncio...")
import asyncio
print("Importing sys...")
import sys
print("Importing os...")
import os
print("Importing datetime...")
from datetime import datetime
print("Importing time...")
import time
print("Importing base64...")
import base64
print("Importing httpx...")
import httpx
print("Importing pillow...")
from PIL import Image
print("Importing io...")
import io
print("Done.\n")

print("Getting API key from local files...")
anthropicAPIKey = ""
try:
    with open('anthropicAPIKey.txt', 'r') as file:
        anthropicAPIKey = file.readline()
    print("Done.\n")
    if anthropicAPIKey == "":  # Probably a really dumb way to do this.
        raise
except:
    print("Something went wrong. Make sure your Anthropic API key is in a file named 'anthropicAPIkey.txt' and your API key is on the first line inside that file. Also ensure said file is located alongside this Python file.")
    for i in range(10):  # Just to warn the user that their API key was not detected.
        time.sleep(0.5) # Five seconds
        

print("Creating Anthropic client...")
anthropicClient = anthropic.Anthropic(
        api_key=anthropicAPIKey,
    )
print("Done.\n")


def emergencyRestart():  # Restarts program. Useful when AI hangs.
    try:
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        print('Failed to restart program: ', e)


def splitMessage(content, limit):  # Splits a given string into multiple parts according to a numerical limiter.
    return [content[i:i+limit] for i in range(0, len(content), limit)]


def writeToFile(string):  # Intended to log messages from all Discord servers the bot is in to a file.
    file = open("log.txt", "a")
    file.write(string + "\n")
    file.close()



chatHistory=[]
systemMessage = "Emojis and markdown support. Your name is Terra and you were made by WhosBlue Technologies as a Discord chatbot. You are based on Claude 3 Opus, the latest and greatest AI available to the public. Important: EMULATE HUMAN EMOTIONS!"
async def chat(message, username, messageObject, replyMessageObject, url, messageHasImageAttachment):
    print("Registered chat...")

    if messageHasImageAttachment:

        image1_url = url
        image1_data = ""

        httpResponse = httpx.get(image1_url)

        # Check if the Content-Type of the response indicates a JPEG image
        if httpResponse.headers['Content-Type'] == "image/jpeg":
            image1_data = base64.b64encode(httpResponse.content).decode("utf-8")
        else:
            # The image is not a JPEG, so let's convert it
            # Load the image from bytes
            image = Image.open(io.BytesIO(httpResponse.content))
            
            # Convert the image to JPEG
            with io.BytesIO() as output:
                image.convert('RGB').save(output, format="JPEG")
                jpeg_data = output.getvalue()  # Get the converted image bytes
            
            # Encode the converted image to base64
            image1_data = base64.b64encode(jpeg_data).decode("utf-8")

            print("Image has been converted to JPEG and encoded to base64.")

        chatHistory.append({
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image1_data,
                    },
                },
                {
                    "type": "text",
                    "text": message
                }
            ],
        })
    else:
        chatHistory.append({"role": "user", "content": f"{username}: "+ message})
    print("Generating...")
    streamMessage = ""
    with anthropicClient.messages.stream(
        max_tokens=1024,
        messages=chatHistory,
        model="claude-3-opus-20240229",
        temperature=0.6
    ) as stream:
        for text in stream.text_stream:
            await asyncio.sleep(0.1)
            streamMessage += text
            print(text, end="", flush=True)
    print("Done.")

    claudeMessage = streamMessage
    chatHistory.append({"role": "assistant", "content": claudeMessage})
    if len(claudeMessage) > 2000:  # Automatic length handler! 2000 is the character limit of Discord.
            print("MESSSAGE OVER LIMIT! SPLITTING...")
            chunks = splitMessage(claudeMessage, 2000)
            await replyMessageObject.delete()  # Delete the message which replies to the user saying "Hang on..."
            for chunk in chunks:
                await messageObject.reply(chunk)  # Send the chunks as replies.
                time.sleep(0.2)
            print("Chunks sent successfully to user.")
            return  # Exit. We're done.
    
    print(claudeMessage)
    await replyMessageObject.edit(content=claudeMessage)

async def chatThreadingCreator(messageContent, username, messageObject, botReplyObject, url, hasImageAttachment):  # Needed by asyncio to put the chat function on new thread, as to not block the Discord API.
    await chat(messageContent, username, messageObject, botReplyObject, url, hasImageAttachment)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == client.user:
            return
        
        if message.content == "!e-brake":  # Restarts program. Useful when AI hangs.
            emergencyRestart()

        formattedMessageData = (f"SERVER: '{message.guild.name}' - USER '{message.author}' SENT MESSAGE: "
                                f"'{message.content}' IN CHANNEL '{message.channel.name}' AT "
                                f"'{datetime.now().strftime('%m/%d/%Y %I:%M %p')}'")

        print(formattedMessageData)
        writeToFile(formattedMessageData)  # This puts the message in a file named log.txt in the cwd.
        
        hasImageAttachment = False

        for attachment in message.attachments:
           hasImageAttachment = True

        if message.channel.name == "terra" or message.channel.name == "ai-conversations":
            sentMessage = discord.Message
            sentMessage = await message.reply("Hang on...")
            # Multi-threading! Discord API will no longer be blocked. Useful for emergency program closing. (!e-brake)
            if hasImageAttachment:
                asyncio.create_task(chatThreadingCreator(message.content, message.author.name, message, sentMessage, message.attachments[0].url, hasImageAttachment)) 
            else:
                asyncio.create_task(chatThreadingCreator(message.content, message.author.name, message, sentMessage, "", False))
            


intents = discord.Intents.all()
intents.message_content = True

client = MyClient(intents=intents)
print("Getting Discord API key from local files...")
discordKey = ""
with open('discordAPIKey.txt', 'r') as file:
    discordKey = file.readline()
if discordKey == "":  # Do not put Discord client creation in a try except, so do this instead.
    print("Sorry, your Discord application key was not detected. Make sure it's in a file named 'discordAPIKey.txt' and that your API key is on the first line. Also ensure said file is located alongside this Python file.")
    for i in range(10):
        time.sleep(0.5)
print("Done, running Discord client.")
client.run(discordKey)
