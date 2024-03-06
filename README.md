# terra
Terra is a Discord chatbot featuring Claude 3 Opus. You will need to provide your own Discord application API key (that's free) and your own Anthropic API key (that's not free). Have fun! Read the installation guide below on how to proceed. This will not provide instructions on how to create a Discord Application Key (it's fairly easy, watch a 5 minute YouTube video.) or how to get an Anthropic API key.

# Installation
You must have Python installed, the latest version works fine.
 - Open cmd.
 - Type: "pip install discord anthropic asyncio pillow" without the quotes into cmd.

Once you've done that, you're almost done. You must now input your API keys into the right places.
If you haven't already, unzip the zip you downloaded from the releases page here.
Once you've done that, make sure the Python file and the two txt files are extracted to the same exact folder, otherwise the bot won't work.
Place your Anthropic key into the "anthropicAPIKey.txt" file.
Place your Discord Application API key the into "discordAPIKey.txt" file.

You can now run the Python file! Please report back here and make an issue if you encounter any issues.
DO NOTE! I've found the Anthropic API very temperamental. It will sometimes throw an error saying something along the lines of "Overloaded." That's not caused by Terra, that's an Anthropic issue. Tell them to fix their servers!
