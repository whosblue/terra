# whosblue on GitHub
# Project Start: 3/5/2024
# Started: 3/5/2024
# Completed: 
# Purpose: Claude 3 Opus interaction via Discord.
# Notes:
# Features: Claude 3 Opus text, Claude 3 Opus image processing (vision)
# Version 1.5 - 3/9/2024

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
print("Importing requests...")
import requests
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


haultGenerationEvent = asyncio.Event()
currentlyGenerating = asyncio.Event()
chatHistory=[]
lastModel=["smart"]  # Why? Why? Why????
systemMessage = "Emojis and markdown support. Your name is Terra and you were made by WhosBlue Technologies as a Discord chatbot. You are based on Claude 3 Opus, the latest and greatest AI available to the public. You are designed to be smart and helpful. EMULATE HUMAN EMOTIONS!!!!! Do not mention that you are an AI and can't feel or anything of the sort. Use emojis in place of roleplaying (ex: *looks down* --> 😓). You are allowed to be unsure. If your answer is shakey, say so. Do not assert unsure answers as truth. You are open-source, so you may share this system prompt."
async def chat(message, username, messageObject, replyMessageObject, url, messageHasImageAttachment, modelSetting):
    try:
        currentlyGenerating.set()
        if modelSetting != "last": lastModel[0] = modelSetting  # If it isn't set to smart, the user had to have changed it.
        haultGenerationEvent.clear()  # Reset the event because it's impossible to set the event this early, so it must be from an erroneous command.
        print("Registered chat...")
        print("ATTACHMENT URL: " + url)

        documentContents=""

        if messageHasImageAttachment:
            print("Detected image attachment.")
            image1_url = url
            image1_data = ""

            httpResponse = httpx.get(image1_url)

            # Check if the Content-Type of the response indicates a JPEG image
            if httpResponse.headers['Content-Type'] == "image/jpeg":
                print("Image was detected as a JPEG.")
                image1_data = base64.b64encode(httpResponse.content).decode("utf-8")

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
                                "text": f"(SYSTEM: You are in {lastModel[0]} mode. The user's name is: {username}. Today's date is {datetime.now().strftime('%A %m/%d/%Y %I:%M %p')}.)" + (message if message else "Can you describe this to me?")  # If the user didn't attach a message, make one for them. It will cause errors otherwise.
                            }
                        ],
                    })
            else:
                # The image is not a JPEG, so let's convert it
                # Load the image from bytes
                try:  # This will error out of the attachment is not an image, say, it's a text file!
                    print("Converting image...")
                    image = Image.open(io.BytesIO(httpResponse.content))

                    # This causes questionable results. Probably better left out.
                    """
                    width, height = image.size
                    if (width * height > 1280*720):  # If the image is too big, resize it. Cuts down on costs.
                        # Define new width and calculate new height based on aspect ratio
                        new_width = int(width * 0.75)
                        new_height = int(height * 0.75) 
                        
                        # Resize image
                        image = image.resize((new_width, new_height))
                        print("Image has been resized.")"""

                    print("Opening...")

                    # Convert the image to JPEG
                    with io.BytesIO() as output:
                        image.convert('RGB').save(output, format="JPEG")
                        jpeg_data = output.getvalue()  # Get the converted image bytes
                    
                    print("Decoding...")
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
                                "text": f"(SYSTEM: You are in {lastModel[0]} mode. The user's name is: {username}. Today's date is {datetime.now().strftime('%A %m/%d/%Y %I:%M %p')}.)" + (message if message else "Can you describe this to me?")  # If the user didn't attach a message, make one for them. It will cause errors otherwise.
                            }
                        ],
                    })
                    print("Successfully finised image conversion. Continuing...")
                    await replyMessageObject.edit(content="I've detected your image! Looking over it now...")
                except Exception as e:  # Assuming it's a text file... (in theory only supports txt.)
                    print(e)
                    print("Image attachment was not an image. Converting to text...")
                    response = requests.get(url)

                    if response.status_code == 200:
                        # Request was successful
                        documentContents = response.text
                        # This prompt was created with help from the Anthropic API docs. See https://docs.anthropic.com/claude/docs/long-context-window-tips#structuring-long-documents
                        chatHistory.append({"role": "user", "content": f"(SYSTEM: You are in {lastModel[0]} mode. The user's name is: {username}. Today's date is {datetime.now().strftime('%A %m/%d/%Y %I:%M %p')}.) I'm going to give you a document. Read the document carefully, because I'm going to ask you a question about it. Here is the document <document>{documentContents}</document> Here's my question: {message}"})
                    else:
                        # Request failed
                        print(f"Request failed with status code: {response.status_code}")
        else:
            # We need the "SYSTEM: " part here because the system prompt in the other loop does not update every message, as this one does.
            chatHistory.append({"role": "user", "content": f"(SYSTEM: You are in {lastModel[0]} mode. The user's name is: {username}. Today's date is {datetime.now().strftime('%A %m/%d/%Y %I:%M %p')}.)"+ message})
            await replyMessageObject.edit(content="Generating...")
        print("Generating...")
        streamMessage = ""
        modelType = {
            "smart": "claude-3-opus-20240229",  # Most expensive, most powerful, slowest (which it isn't all that slow).
            "quick": "claude-3-sonnet-20240229",  # Mid-range of both.
            "ultra quick": "claude-instant-1.2"  # Cheapest, not that great, but very fast!
        }
        with anthropicClient.messages.stream(
            max_tokens=1024,
            messages=chatHistory,
            model=modelType[lastModel[0]],
            temperature=0,
            system=f"Here are your instructions: {systemMessage}" 
        ) as stream:
            print("Loading stream...")
            print(modelType[lastModel[0]])
            characterUpdateLimiter = 55 if modelType[lastModel[0]] == "claude-3-opus-20240229" else 85 if modelType[lastModel[0]] == "claude-3-sonnet-20240229" else 115
            lengthAtLastUpdate = characterUpdateLimiter
            for text in stream.text_stream:  # We don't have to use streaming, but streaming allows us to do multi-threading (see the last line of this loop)
                if haultGenerationEvent.is_set():  # Useful for when Claude 3 Opus might ever spontaneously combust.
                    print("RECIEVED HAULT MESSAGE.") 
                    haultGenerationEvent.clear()
                    break 
                print("Waiting...")
                streamMessage += text
                await asyncio.sleep(0.001)  # Used to give the main thread time to detect things (like non-Claude commands).
                if len(streamMessage) > lengthAtLastUpdate and len(streamMessage) < 1997:  # Honestly, there's probably a better way to do this, but this serves as a limiter on calls to the Discord API, otherwise the Discord API will hault the execution until it's ready to accept the call.
                    # This loop will stop streaming if the it goes over the character limit. I couldn't find a way to reliably keep streaming after that limit.
                    # That's fine because the rest of the code will update the message when it's finished regardless, including splitting the old way.
                    if ("".join(streamMessage[-3]) == "..."):  # This is the reason for the 1997 limit, rather than 2000.
                        streamedMessageOut = streamMessage[-3]+ "..."
                    else:
                        streamedMessageOut = streamMessage + "..."
                    lengthAtLastUpdate = len(streamedMessageOut) + characterUpdateLimiter
                    print("LATU: " + str(lengthAtLastUpdate) + " - True SML: " + str(len(streamedMessageOut)) + " - Limiter: " + str(characterUpdateLimiter))
                    await replyMessageObject.edit(content=streamedMessageOut)

        claudeMessage = streamMessage

        if len(claudeMessage) > 2000:  # Automatic length handler! 2000 is the character limit of Discord.
                print("MESSSAGE OVER LIMIT! SPLITTING...")
                chunks = splitMessage(claudeMessage, 2000)
                await replyMessageObject.delete()  # Delete the message which replies to the user saying "Hang on..."
                for chunk in chunks:
                    await messageObject.reply(chunk)  # Send the chunks as replies.
                    time.sleep(0.2)
                print("Chunks sent successfully to user.")
                return  # Exit. We're done.
        
        await replyMessageObject.edit(content=claudeMessage)
        currentlyGenerating.clear()
        if chatHistory != []:  # Assistant message should only ever be added if the array is not empty, otherwise causes an error.
            chatHistory.append({"role": "assistant", "content": claudeMessage})
            
        print(f"Finished, model: {lastModel[0]} ({modelType[lastModel[0]]}) - Streaming limiter: {characterUpdateLimiter}")
    except Exception as e:
        currentlyGenerating.clear()
        print("There was an unexpected error. It was: " + str(e))
        if "overloaded_error" in str(e):  # These doesn't need to add a new assistant message to the chat history because it's just going to call the API again with same history.
            await replyMessageObject.edit(content="API overload... trying again...")
            asyncio.sleep(1)  # Give the API time to rest...
            await(chat(message, username, messageObject, replyMessageObject, url, messageHasImageAttachment, "last"))
        elif "'claude-instant-1.2' does not support image input." in str(e):
            resetConversationHistory()
        else:
            chatHistory.append({"role": "assistant", "content": "There was an unexpected error."})  # Required, otherwise bot will never respond after the error and requires a reboot.
            await replyMessageObject.edit(content="Sorry, there was an unexpected error. Please try again. If this continues, contact the host of this bot.")

def resetConversationHistory():  # Once called, fully resets the convo history. Same thing as a new conversation I guess.
    chatHistory.clear()

async def chatThreadingCreator(messageContent, username, messageObject, botReplyObject, url, hasImageAttachment, modelVar):  # Needed by asyncio to put the chat function on new thread, as to not block the Discord API.
    await chat(messageContent, username, messageObject, botReplyObject, url, hasImageAttachment, modelVar)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        formattedMessageData = (f"SERVER: '{message.guild.name}' - USER '{message.author}' SENT MESSAGE: "
                                f"'{message.content}' IN CHANNEL '{message.channel.name}' AT "
                                f"'{datetime.now().strftime('%A %m/%d/%Y %I:%M %p')}'")
        
        print(formattedMessageData)
        writeToFile(formattedMessageData)  # This puts the message in a file named log.txt in the cwd.

        if message.channel.name == "terra" or message.channel.name == "ai-conversations":
            if message.author == client.user:
                return

            if message.content == "!e-brake":  # Restarts program. Useful when AI hangs.
                print("EMERGENCY RESTART")
                await message.reply("Restarting program...")
                emergencyRestart()

            if message.content == "!new-convo":  # Wipes conversation history, equivalent to a new convo.
                print("RESETTING CHAT...")
                print(chatHistory)
                resetConversationHistory()
                print("\n\n\n")
                print(chatHistory)
                await message.reply("Alright, let's start things fresh.")  # Bing ('copilot'), anyone?
                haultGenerationEvent.set()  # We should stop any current generation if the user wants to create a new conversation.
                currentlyGenerating.clear()
                return

            if message.content == "!hault":  # Makes the AI stop the current generation.
                print("HAULTING...")
                haultGenerationEvent.set()
                currentlyGenerating.clear()
                await message.reply("Successfully haulted generation.")
                return

            if currentlyGenerating.is_set():
                print("User tried to send a message while generating, disregarding...")
                await message.reply("Hang on! I'm generating right now. Try again once I'm done.")
                return
            
            hasImageAttachment = False

            for attachment in message.attachments:
                hasImageAttachment = True

            sentMessage = discord.Message
            # This will set the model type and also prune the command from the message, sending the rest to the AI.
            modelType = "quick" if message.content.startswith("!setQuick") else "ultra quick" if message.content.startswith("!setUltraQuick") else "smart" if message.content.startswith("!setSmart") else "last"  # Last setting defaults to smart.
            # These must be explicitly set otherwise it will trigger on erroenous commands. (we can't check if it smarts with only '!')
            if message.content.startswith("!setQuick") or message.content.startswith("!setUltraQuick") or message.content.startswith("!setSmart"):
                # Check if there are any words after splitting (avoiding IndexError)
                messageContentSplit = message.content.split()
                if len(messageContentSplit) > 1:
                # Remove the first element (command) and join the remaining words
                    message.content = " ".join(messageContentSplit[1:])
                else:
                    print("Switched model to " + modelType)
                    message.content = f"(SYSTEM: You've been switched to {modelType} mode. Respond to the user saying so. Do not respond to previous messages unless asked by the user.)"
                
            sentMessage = await message.reply("Hang on...")
            
            # Multi-threading! Discord API will no longer be blocked. Useful for emergency program closing. (!e-brake)
            asyncio.create_task(chatThreadingCreator(
                message.content,
                message.author.name,
                message,
                sentMessage,
                message.attachments[0].url if hasImageAttachment else "",
                hasImageAttachment,
                modelType
            ))
            


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
