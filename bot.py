import io
import os
import discord
from PIL import Image
from dotenv import load_dotenv
from scrape import Scraper

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

champions = set()
roles = {'jungle', 'top', 'bot', 'support', 'mid'}
# Strips the newline character
for line in open('champions.csv', 'r').readlines():
    champions.add(line.split("\t")[0])


@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:  # we do not want the bot to reply to itself
        return

    if message.content.startswith('!build'):
        keywords = message.content.split(" ")
        champion = keywords[1]
        role = keywords[2]

        if champion not in champions:
            await channel.send(f"Champion {champion} does not exist in the list -> " + str(list(champions)))
            return

        if role not in roles:
            await channel.send(f"Role {role} does not exist in the list -> " + str(list(roles)))
            return

        scraper = Scraper(f"https://www.op.gg/champion/{champion}/statistics/{role}/build")
        image = scraper.scrape(class_name="l-champion-statistics-content__main")
        image = Image.open(io.BytesIO(image))

        with io.BytesIO() as image_binary:
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await channel.send(file=discord.File(fp=image_binary, filename='image.png'))

client.run(TOKEN)
