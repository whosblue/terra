# terra
Terra is a Discord chatbot featuring Claude 3 Opus. You will need to provide your own Discord application API key (that's free) and your own Anthropic API key (that's not free). Have fun! Read the installation guide below on how to proceed. This will not provide instructions on how to create a Discord Application Key (it's fairly easy, watch a 5 minute YouTube video.) or how to get an Anthropic API key.

# Installation
You must have Python installed, the latest version works fine. (make sure you installed Python to PATH, otherwise just reinstall it.)
 - Open cmd.
 - Type: "pip install discord anthropic httpx pillow asyncio requests" without the quotes into cmd.

Once you've done that, you're almost done. You must now input your API keys into the right places.
If you haven't already, unzip the zip you downloaded from the releases page here.
Once you've done that, make sure the Python file and the two txt files are extracted to the same exact folder, otherwise the bot won't work.
Place your Anthropic key into the "anthropicAPIKey.txt" file.
Place your Discord Application API key the into "discordAPIKey.txt" file.

Finally, make a Discord server, invite your Discord bot to said server. MOST IMPORTANTLY, CREATE A CHANNEL CALLED terra.

You can now run the Python file! Please report back here and make an issue if you encounter any issues.
DO NOTE! I've found the Anthropic API very temperamental. It will sometimes throw an error saying something along the lines of "Overloaded." That's not caused by Terra, that's an Anthropic issue. Tell them to fix their servers!

# Features
Make sure to read the important commands second too.
- Claude 3 Opus text
- Claude 3 Opus vision (image recognition, can answer questions based on images)
- Large context (documents) support.
    By the way, to use this, simply input a .txt file into Discord as an attachment and Terra will handle it. You can also ask your question at the same time. Do not resend the txt over and over again!

# Usage
How do I use Terra, you ask? Once you've completed the installation guide AND INVITED YOUR DISCORD BOT A SERVER OF YOUR CHOICE, you need to chat in the #terra channel you created. You can send messages with images and text to Terra
and it will respond accordingly. That's it! Check back here for new releases and additions to the code.

# IMPORTANT COMMANDS
These are some pretty useful commands you can use while using Terra.
- !e-brake - This restarts the program, helpful when Claude might freeze up.
- !new-convo - This wipes the conversation history, as if you restarted the program. Brand new conversation!
- !hault - Stops the current generation in turn for a new one.
- !setSmart - Sets the current model to Claude 3 Opus. The model is already Claude 3 Opus on start, but this will switch it back if you've changed it previously.
- !setQuick - Sets the model to Claude 3 Sonnet, which is cheaper and slightly faster at responding than Opus.
- !setUltraQuick - Sets the model to claude-instant-1.2, who is sort of dumb but super, super, fast.
