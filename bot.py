import io
import os
import discord
from PIL import Image
from dotenv import load_dotenv
from scrape import Scraper

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PRODUCTION = os.getenv('PRODUCTION')

client = discord.Client()

champions = {}
roles = {'jungle', 'top', 'bot', 'support', 'mid'}

# Strips the newline character
for line in open('champions.csv', 'r').readlines():
    columns = line.split("\t")
    champion_name = columns[0]
    champion_image = columns[1]
    champions[champion_name] = champion_image


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
    embed.add_field(name='`!src`',
                    value='Check the source code at GitHub.',
                    inline=False)
    return embed


async def send_image_response(channel, image):
    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await channel.send(file=discord.File(fp=image_binary, filename='image.png'))


def construct_embed(msg, thumbnail_url):
    embed = discord.Embed(title='', description=msg)
    embed.set_thumbnail(url=thumbnail_url)
    return embed


@client.event
async def on_message(message):

    message_keywords = message.content.split(" ")

    if message.author == client.user:  # we do not want the bot to reply to itself
        return

    if message.content.startswith('!hippalus'):
        await message.channel.send(content=None, embed=create_help_embed())
        return

    if message.content.startswith('!src'):
        await message.channel.send("https://github.com/AlexandrosAlexiou/hippalus-discord-bot")
        return

    champion = message_keywords[1]

    if champion not in champions:
        champions_list_message = "```ini\n [" + ", ".join(list(champions)) + "] \n```"
        await message.channel.send(f"❗ **Champion __{champion}__ does not exist in the list** ❗\n" + champions_list_message)
        return

    if message.content.startswith('!aram'):
        await message.channel.send(
            embed=construct_embed(msg=f"✅ Aram build for __{champion}__ incoming ✅", thumbnail_url=champions[champion]))
        scraper = Scraper(f"https://www.op.gg/aram/{champion}/statistics/")
        image = scraper.scrape(class_name="l-champion-statistics-content__main.aram")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)
        return

    try:
        role = message_keywords[2]
    except IndexError:
        await message.channel.send(f"**Please specify the role for __{champion}__**")
        return

    if role not in roles:
        roles_list_message = "```ini\n [" + ", ".join(list(roles)) + "] \n```"
        await message.channel.send(f"❗ **Role __{role}__ does not exist in the list** ❗\n" + roles_list_message)
        return

    if message.content.startswith('!build'):
        await message.channel.send(
            embed=construct_embed(msg=f"✅ Build for {champion} {role} incoming ✅", thumbnail_url=champions[champion]))
        scraper = Scraper(f"https://www.op.gg/champion/{champion}/statistics/{role}/build")
        image = scraper.scrape(class_name="l-champion-statistics-content__main")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)
        return

    if message.content.startswith('!runes'):
        await message.channel.send(
            embed=construct_embed(msg=f"✅ Runes for {champion} {role} incoming ✅", thumbnail_url=champions[champion]))
        scraper = Scraper(f"https://www.op.gg/champion/{champion}/statistics/{role}/build")
        image = scraper.scrape(class_name="champion-overview__table.champion-overview__table--rune.tabItems")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)
        return

    if message.content.startswith('!items'):
        await message.channel.send(
            embed=construct_embed(msg=f"✅ Items for {champion} {role} incoming ✅", thumbnail_url=champions[champion]))
        scraper = Scraper(f"https://www.op.gg/champion/{champion}/statistics/{role}/build")
        image = scraper.scrape(xpath="(//table[@class='champion-overview__table'])[1]")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)
        return


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} with id {client.user.id}')
    await client.change_presence(activity=discord.Game('Type !hippalus for commands'))

client.run(TOKEN)
