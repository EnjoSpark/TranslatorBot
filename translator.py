import os
import discord
import translators as ts
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents(messages=True,
                          message_content=True,
                          reactions=True,
                          members=True,
                          guilds=True)
client = discord.Client(intents=intents)

lang_emoji = {
    'zh': {'🇨🇳'},
    'ru': {'🇷🇺', '🇧🇾', '🇰🇬', '🇰🇿'},
    'en': {'🇬🇧', '🇺🇸', '🇦🇺', '🇳🇿', '🇨🇦'},
    'es': {
        '🇪🇸', '🇲🇽', '🇧🇷', '🇨🇱', '🇨🇴', '🇧🇿', '🇨🇷', '🇨🇺', '🇩🇴', '🇪🇨', '🇸🇻', '🇬🇹',
        '🇭🇳', '🇦🇷', '🇧🇴', '🇵🇪', '🇵🇾', '🇺🇾', '🇻🇪'
    },
    'ja': {'🇯🇵'},
    'ko': {'🇰🇷', '🇰🇵'},
    'fr': {'🇫🇷'},
    'de': {'🇩🇪'}
}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('$translate'):
        wds = msg.content.split('$translate ', 1)[1]
        trans = ts.google(wds)
        await msg.channel.send('translated: ' + trans)


@client.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    lang = get_emoji_lang(emoji)
    if not lang:
        print('Not translation emoji, skipping.')
        return
    channel = await client.fetch_channel(payload.channel_id)
    if not channel:
        print('Channel is none!')
        return
    message = await channel.fetch_message(payload.message_id)
    member = payload.member
    if not (message and member):
        print('Missing info.')
        return
    print(f'Translation triggered for {member.name} ({emoji}).')
    translated = ts.google(message.content, to_language=lang)
    pm = f'"{message.content}"\n{translated} ({emoji})'
    await member.send(pm)


def get_emoji_lang(emoji):
    for k, v in lang_emoji.items():
        if emoji in v:
            return k
    return None

client.run(os.getenv('TOKEN'))
