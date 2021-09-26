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


def create_help_embed():
    embed = discord.Embed(title='**COMMANDS**', description='', colour=discord.Colour.green())
    embed.add_field(name='`!runes <champion> <role>`',
                    value='Shows runes for a champion for a role. Example: `!runes ezreal bot`.',
                    inline=False)
    embed.add_field(name='`!build <champion> <role>`',
                    value='Shows entire build for a champion for a role. Example: `!build ezreal bot`.',
                    inline=False)
    embed.add_field(name='`!items <champion> <role>`',
                    value='Shows items for a champion for a role. Example: `!items ezreal bot`.',
                    inline=False)
    embed.add_field(name='`!aram <champion>`',
                    value='Shows entire build for a champion in ARAM mode. Example: `!aram ezreal`.',
                    inline=False)
    return embed


async def send_image_response(channel, image):
    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await channel.send(file=discord.File(fp=image_binary, filename='image.png'))


@client.event
async def on_message(message):

    message_keywords = message.content.split(" ")

    if message.author == client.user:  # we do not want the bot to reply to itself
        return

    if message.content.startswith('!hippalus'):
        await message.channel.send(content=None, embed=create_help_embed())

    champion = message_keywords[1]

    if champion not in champions:
        await message.channel.send(f"**Champion {champion} does not exist in the list**\n" + str(list(champions)))

    if message.content.startswith('!aram'):
        scraper = Scraper(f"https://www.op.gg/aram/{champion}/statistics/")
        image = scraper.scrape(class_name="l-champion-statistics-content")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)

    try:
        role = message_keywords[2]
    except IndexError:
        await message.channel.send(f"**Please specify the role for {champion}**")

    if role not in roles:
        await message.channel.send(f"**Role {role} does not exist in the list**\n" + str(list(roles)))

    if message.content.startswith('!build'):
        scraper = Scraper(f"https://www.op.gg/champion/{champion}/statistics/{role}/build")
        image = scraper.scrape(class_name="l-champion-statistics-content__main")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)

    if message.content.startswith('!runes'):
        scraper = Scraper(f"https://www.op.gg/champion/{champion}/statistics/{role}/build")
        image = scraper.scrape(class_name="champion-overview__table.champion-overview__table--rune.tabItems")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)

    if message.content.startswith('!items'):
        scraper = Scraper(f"https://www.op.gg/champion/{champion}/statistics/{role}/build")
        image = scraper.scrape(xpath="(//table[@class='champion-overview__table'])[1]")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} with id {client.user.id}')
    await client.change_presence(activity=discord.Game('Type !hippalus for commands'))

client.run(TOKEN)
