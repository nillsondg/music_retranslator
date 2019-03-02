import discord
import re
from config import TOKEN

client = discord.Client()

VOICE_CHANNEL_ID = 342012658687672330
ADMIN_BOTS_CHANNEL_ID = 341856656721838081
MUSIC_CHANNEL_ID = 550429090776088577
VOICE_MUSIC_CHANNEL_ID = 342406273016266752
USEBOTS_CHANNEL_ID = 341626998709551104


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return True

    return False


def soundcloud_url(url):
    soundcloud_regex = (
        r'(https?://)?(www\.)?'
        '(soundcloud)\.(com)/')
    soundcloud_regex_match = re.match(soundcloud_regex, url)
    if soundcloud_regex_match:
        return True
    return False


def check_is_connected(channel):
    for user in channel.members:
        if user == client.user:
            return True
    return False


@client.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    if message.author == client.user:
        return

    if message.channel.id != USEBOTS_CHANNEL_ID and message.channel.id != MUSIC_CHANNEL_ID:
        return
    if not discord.opus.is_loaded():
        discord.opus.load_opus('/usr/local/Cellar/opus/1.3')

    if youtube_url_validation(message.content) or soundcloud_url(message.content):
        print("got music link")
        if not check_is_connected(client.get_channel(VOICE_CHANNEL_ID)):
            await client.get_channel(VOICE_CHANNEL_ID).connect()
        await client.get_channel(USEBOTS_CHANNEL_ID).send(content="!play <" + message.content + ">")
        # check unicode 6.0 name at https://emojipedia.org
        await message.add_reaction(u"\N{Thumbs Up Sign}")

client.run(TOKEN)
