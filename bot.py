import io
import os
import requests
import json
import discord
from PIL import Image
from dotenv import load_dotenv
from scrape import Scraper
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PRODUCTION = os.getenv('PRODUCTION')

client = discord.Client()
logging.basicConfig(level=logging.NOTSET)

champion_names = set()
roles = {'jungle', 'top', 'bot', 'support', 'mid'}
champions_endpoint = "https://ddragon.leagueoflegends.com/cdn/12.4.1/data/en_US/champion.json"


def get_champion_thumbnail_endpoint(champion_name):
    return f"https://ddragon.leagueoflegends.com/cdn/12.4.1/img/champion/{champion_name}.png"


def get_champion_endpoint(champion_name):
    return f"https://ddragon.leagueoflegends.com/cdn/12.4.1/data/en_US/champion/{champion_name}.json"


def create_help_embed():
    embed = discord.Embed(title='**COMMANDS**',
                          description='', colour=discord.Colour.green())
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
    logging.info(f"[Hippalus] Message: {message}")
    message_keywords = message.content.split(" ")

    if message.author == client.user:  # we do not want the bot to reply to itself
        return

    if message.content.startswith('!hippalus'):
        await message.channel.send(content=None, embed=create_help_embed())
        return

    if message.content.startswith('!src'):
        await message.channel.send("https://github.com/AlexandrosAlexiou/hippalus-discord-bot")
        return

    champion_name = message_keywords[1]

    if champion_name not in champion_names:
        champions_list_message = "```ini\n [" + \
            ", ".join(list(champion_names)) + "] \n```"
        await message.channel.send(f"❗ **Champion __{champion_name}__ does not exist in the list** ❗\n" + champions_list_message)
        return

    if message.content.startswith('!aram'):
        await message.channel.send(
            embed=construct_embed(
                msg=f"✅ Aram build for __{champion_name}__ incoming ✅", thumbnail_url=get_champion_thumbnail_endpoint(champion_name)))
        scraper = Scraper(
            f"https://www.op.gg/aram/{champion_name.lower()}/statistics/")
        image = scraper.scrape_opgg(
            class_name="main")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)
        return

    try:
        role = message_keywords[2]
    except IndexError:
        await message.channel.send(f"**Please specify the role for __{champion_name}__**")
        return

    if role not in roles:
        roles_list_message = "```ini\n [" + ", ".join(list(roles)) + "] \n```"
        await message.channel.send(f"❗ **Role __{role}__ does not exist in the list** ❗\n" + roles_list_message)
        return

    if message.content.startswith('!build'):
        await message.channel.send(
            embed=construct_embed(msg=f"✅ Build for {champion_name} {role} incoming ✅",
                                  thumbnail_url=get_champion_thumbnail_endpoint(champion_name)))
        scraper = Scraper(
            f"https://www.op.gg/champion/{champion_name.lower()}/statistics/{role}/build")
        image = scraper.scrape_opgg(
            class_name="main")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)
        return

    if message.content.startswith('!runes'):
        await message.channel.send(
            embed=construct_embed(msg=f"✅ Runes for {champion_name} {role} incoming ✅",
                                  thumbnail_url=get_champion_thumbnail_endpoint(champion_name)))
        scraper = Scraper(
            f"https://www.op.gg/champion/{champion_name.lower()}/statistics/{role}/build")
        image = scraper.scrape_opgg(
            class_name="css-80j10c.e10jawsm1")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)
        return

    if message.content.startswith('!items'):
        await message.channel.send(
            embed=construct_embed(msg=f"✅ Items for {champion_name} {role} incoming ✅",
                                  thumbnail_url=get_champion_thumbnail_endpoint(champion_name)))
        scraper = Scraper(
            f"https://www.op.gg/champion/{champion_name.lower()}/statistics/{role}/build")
        image = scraper.scrape_opgg(
            class_name="css-y6aqwj.e2uay8y0")
        image = Image.open(io.BytesIO(image))
        await send_image_response(channel=message.channel, image=image)
        return


@ client.event
async def on_ready():
    response = requests.get(champions_endpoint)
    champions_json_response = json.loads(response.text)
    global champion_names
    champion_names = set(champions_json_response["data"].keys())
    logging.info(
        f'[Hippalus] Logged in as {client.user.name} with id {client.user.id}')
    await client.change_presence(activity=discord.Game('Type !hippalus for commands'))

client.run(TOKEN)
