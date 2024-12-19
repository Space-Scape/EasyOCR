import discord
import easyocr
import re
import os

# ---- Discord Bot Configuration ---- #
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = 1273094409432469605

# ---- EasyOCR Reader ---- #
reader = easyocr.Reader(['en'], gpu=False)

# ---- Discord Bot ---- #
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot is ready! Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.bot:
        return

    if message.attachments:
        await message.channel.send("Processing chatbox image... Please wait.")
        for attachment in message.attachments:
            if attachment.filename.endswith((".png", ".jpg", ".jpeg")):
                temp_image_path = f"temp_{attachment.filename}"
                await attachment.save(temp_image_path)

                try:
                    results = reader.readtext(temp_image_path)
                    extracted_text = set()
                    for _, text, _ in results:
                        matches = re.findall(r':\s*([^:()\n]+)\s*\(', text)
                        extracted_text.update(matches)

                    response = "**Extracted Text from Chatbox:**\n" + "\n".join(extracted_text) if extracted_text else "No matching text found."
                    await message.channel.send(response)

                except Exception as e:
                    await message.channel.send(f"Error: {e}")

                os.remove(temp_image_path)

if TOKEN:
    client.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN not found.")
