#Duckbot by turnt ducky
#Needs to have things downloaded which I havent listed yet
import discord
from discord.ext import commands
from discord.ext.commands import bot
from datetime import datetime
from plugin import Plugin
from decorators import command
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from collections import OrderedDict
import random
import asyncio
import chalk
import discord
import os
import html
import aiohttp

bot = commands.Bot(command_prefix="Duckbot ", description="This bot is always turnt")

starttime = datetime.now()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(starttime)
    print('------')

@bot.command()
async def uptime():
    """See how long the bot has been online"""
    await bot.say(datetime.now() - starttime)
    print("Someone wanted to see how long the bot has been online")

@bot.command(pass_context=True)
async def ping(ctx);
    """Ping the bot and see if there is a delay"""
	await bot.say(":ping_pong:Pong!!")
	print("Someone has pinged the bot")

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)
    print("Someone has roll a NdN format dice")

@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    """See some info on someone"""
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)
    print("Someone wanted to see info on someone")

@bot.command(pass_context=True)
async def serverinfo(ctx):
    """See info on the server"""
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's what I could find.", color=0x00ff00)
    embed.set_author(name="Turnt Ducky")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)
    print("Someone wanted to see info about the server")

@bot.command(pass_context=True)
@commands.has_role("ðŸ˜‚ðŸ‘Œ Friends")
async def kick(ctx, user: discord.Member):
    await bot.say(":boot: Cya, {}. Ya Bish!".format(user.name))
    await bot.kick(user)
    print("Someone has been kick from the server")

@bot.command(pass_context=True)
async def embed(ctx):
    """This is just a test for me"""
    embed = discord.Embed(title="test", description="Ducky was here", color=0x00ff00)
    embed.set_footer(text="this is a footer")
    embed.set_author(name="Turnt Ducky")
    embed.add_field(name="This is a field", value="no it isn't", inline=True)
    await bot.say(embed=embed)
    print("Someone used the test command for some reason")

@bot.command(pass_context=True)
async def helpme(ctx):
    """This is a command for if you need help"""
    embed = discord.Embed(title="**Commands**", description="==========", color=0x00ff00)
    embed.add_field(name="Duckbot uptime", value="See how many hours its been since Duckbot has been active", inline=True)
    embed.add_field(name="Duckbot ping", value="Does Duckbot have a bit of a delay", inline=True)
    embed.add_field(name="Duckbot roll", value="Cant decide what you should do. Roll a virtual die", inline=True)
    embed.add_field(name="Duckbot info [@ the person]", value="Get some basic info on someone", inline=True)
    embed.add_field(name="Duckbot serverinfo", value="Get basic info on this server", inline=True)
    embed.add_field(name="Duckbot helpme", value="Have this text popup", inline=True)
    embed.set_footer(text="Stay turnt everyone :)")
    await bot.say(embed=embed)
    print("Someone needed help with my commands")
   
#Search function

MAL_USERNAME = os.getenv('MAL_USERNAME')
MAL_PASSWORD = os.getenv('MAL_PASSWORD')

TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')

IMGUR_ID = os.getenv('IMGUR_ID')

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

NOT_FOUND = "I didn't find anything 😢..."


class Search(Plugin):

    """
    @command(db_name='google',
             pattern='^Duckbot google (.*)',
             db_check=True,
             usage="Duckbot google search_value")
    async def google(self, message, args):
        pass
    """

    @command(db_name='youtube',
             pattern='^Duckbot youtube (.*)',
             db_check=True,
             usage="Duckbot youtube video_name")
    async def youtube(self, message, args):
        search = args[0]
        url = "https://www.googleapis.com/youtube/v3/search"
        with aiohttp.ClientSession() as session:
            async with session.get(url, params={"type": "video",
                                                "q": search,
                                                "part": "snippet",
                                                "key": GOOGLE_API_KEY}) as resp:
                data = await resp.json()
        if data["items"]:
            video = data["items"][0]
            response = "https://youtu.be/" + video["id"]["videoId"]
        else:
            response = NOT_FOUND

        await self.Duckbot.send_message(message.channel, response)


    @command(db_name='urban',
             pattern='Duckbot urban (.*)',
             db_check=True,
             usage="Duckbot urban dank_word")
    async def urban(self, message, args):
        search = args[0]
        url = "http://api.urbandictionary.com/v0/define"
        with aiohttp.ClientSession() as session:
            async with session.get(url, params={"term": search}) as resp:
                data = await resp.json()

        if data["list"]:
            entry = data["list"][0]
            response = "\n **{e[word]}** ```\n{e[definition]}``` \n "\
                       "**example:** {e[example]} \n"\
                       "<{e[permalink]}>".format(e=entry)
        else:
            response = NOT_FOUND
        await self.Duckbot.send_message(message.channel, response)

    """
    @command(db_name='gimg',
             pattern='^Duckbot gimg (.*)',
             db_check=True,
             usage="Duckbot gimg search_value")
    async def gimg(self, message, args):
        pass
    """

    @command(db_name='pokemon',
             pattern='^Duckbot pokemon (.*)',
             db_check=True,
             usage="Duckbot pokemon pokemon_name")
    async def pokemon(self, message, args):
        url = "http://veekun.com/dex/pokemon/search"
        search = args[0]
        with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   params={"name": search}) as resp:
                data = await resp.text()

        if "Nothing found" in data:
            response = NOT_FOUND
        else:
            soup = BeautifulSoup(data, "html.parser")
            tds = soup.find_all("td", class_="name")[0].parent.find_all("td")

            p = OrderedDict()
            p["name"] = tds[1].text
            p["types"] = ", ".join(map(lambda img: img["title"],
                                       tds[2].find_all("img")))
            p["abilities"] = ", ".join(map(lambda a: a.text,
                                       tds[3].find_all("a")))
            p["rates"] = tds[4].find("img")["title"]
            p["egg groups"] = tds[5].text[1:-1].replace("\n", ", ")
            p["hp"] = tds[6].text
            p["atk"] = tds[7].text
            p["def"] = tds[8].text
            p["SpA"] = tds[9].text
            p["SpD"] = tds[10].text
            p["Spd"] = tds[11].text
            p["total"] = tds[12].text
            p["url"] = "http://veekun.com" + tds[1].find("a")["href"]

            with aiohttp.ClientSession() as session:
                async with session.get(p["url"]) as resp:
                    data = await resp.text()

            soup2 = BeautifulSoup(data, "html.parser")
            img = soup2.find("div",
                             id="dex-pokemon-portrait-sprite").find("img")
            p["picture"] = "http://veekun.com" + img["src"]

            response = "\n"
            for k, v in p.items():
                response += "**" + k + ":** " + v + "\n"

        await self.Duckbot.send_message(message.channel, response)

    @command(db_name='twitch',
             pattern='^Duckbot twitch (.*)',
             db_check=True,
             usage="Duckbot twitch streamer_name")
    async def twitch(self, message, args):
        search = args[0]
        url = "https://api.twitch.tv/kraken/search/channels"
        with aiohttp.ClientSession() as session:
            params = {
                "q": search,
                "client_id": TWITCH_CLIENT_ID,
            }
            async with session.get(url, params=params) as resp:
                data = await resp.json()

        if data["channels"]:
            channel = data["channels"][0]
            response = "\n**" + channel["display_name"] + "**: " + channel["url"]
            response += " {0[followers]} followers & {0[views]} views".format(
                channel
            )
        else:
            response = NOT_FOUND

        await self.Duckbot.send_message(message.channel, response)

    @command(db_name='imgur',
             pattern='^Duckbot imgur (.*)',
             db_check=True,
             usage="Duckbot imgur some_dank_search_value")
    async def imgur(self, message, args):
        search = args[0]
        url = "https://api.imgur.com/3/gallery/search/viral"
        headers = {"Authorization": "Client-ID " + IMGUR_ID}
        with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   params={"q": search},
                                   headers=headers) as resp:
                data = await resp.json()

        if data["data"]:
            result = data["data"][0]
            response = result["link"]
        else:
            response = NOT_FOUND

        await self.Duckbot.send_message(message.channel, response)

    """
    @command(db_name='wiki',
             pattern='^Duckbot wiki (.*)',
             db_check=True,
             usage="Duckbot wiki search_value")
    async def wiki(self, message, args):
        pass
    """

    @command(db_name='manga',
             pattern='Duckbot manga (.*)',
             db_check=True,
             usage="Duckbot manga manga_name")
    async def manga(self, message, args):
        search = args[0]
        auth = aiohttp.BasicAuth(login=MAL_USERNAME, password=MAL_PASSWORD)
        url = 'https://myanimelist.net/api/manga/search.xml'
        params = {'q': search}
        with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(url, params=params) as response:
                data = await response.text()

        if data == "":
            await self.Duckbot.send_message(message.channel,
                                         "I didn't find anything :cry:...")
            return

        root = ElementTree.fromstring(data)
        if len(root) == 0:
            await self.Duckbot.send_message(message.channel,
                                         "Sorry, I didn't find anything :cry:"
                                         "...")
        elif len(root) == 1:
            entry = root[0]
        else:
            msg = "**Please choose one by giving its number**\n"
            msg += "\n".join(['{} - {}'.format(n+1, entry[1].text)
                              for n, entry in enumerate(root) if n < 10])

            await self.Duckbot.send_message(message.channel, msg)

            def check(m): return m.content in map(str, range(1, len(root)+1))
            resp = await self.Duckbot.wait_for_message(author=message.author,
                                                    check=check,
                                                    timeout=20)
            if resp is None:
                return

            entry = root[int(resp.content)-1]

        switcher = [
            'english',
            'score',
            'type',
            'episodes',
            'volumes',
            'chapters',
            'status',
            'start_date',
            'end_date',
            'synopsis'
            ]

        msg = '\n**{}**\n\n'.format(entry.find('title').text)
        for k in switcher:
            spec = entry.find(k)
            if spec is not None and spec.text is not None:
                msg += '**{}** {}\n'.format(k.capitalize()+':',
                                            html.unescape(spec.text.replace(
                                                '<br />',
                                                ''
                                            )))
        msg += 'https://myanimelist.net/manga/{}'.format(entry.find('id').text)

        await self.Duckbot.send_message(message.channel,
                                     msg)

    @command(db_name='anime',
             pattern='Duckbot anime (.*)',
             db_check=True,
             usage="Duckbot anime anime_name")
    async def anime(self, message, args):
        search = args[0]
        auth = aiohttp.BasicAuth(MAL_USERNAME, password=MAL_PASSWORD)
        url = 'https://myanimelist.net/api/anime/search.xml'
        params = {'q': search}
        with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(url, params=params) as response:
                data = await response.text()

        if data == "":
            await self.Duckbot.send_message(message.channel,
                                         "I didn't find anything :cry:...")
            return

        root = ElementTree.fromstring(data)
        if len(root) == 0:
            await self.Duckbot.send_message(message.channel,
                                         "Sorry, I didn't find anything :cry:"
                                         "...")
        elif len(root) == 1:
            entry = root[0]
        else:
            msg = "**Please choose one by giving its number**\n"
            msg += "\n".join(['{} - {}'.format(n+1, entry[1].text)
                              for n, entry in enumerate(root) if n < 10])

            await self.Duckbot.send_message(message.channel, msg)

            def check(m): return m.content in map(str, range(1, len(root)+1))
            resp = await self.Duckbot.wait_for_message(author=message.author,
                                                    check=check,
                                                    timeout=20)
            if resp is None:
                return

            entry = root[int(resp.content)-1]

        switcher = [
            'english',
            'score',
            'type',
            'episodes',
            'volumes',
            'chapters',
            'status',
            'start_date',
            'end_date',
            'synopsis'
            ]

        msg = '\n**{}**\n\n'.format(entry.find('title').text)
        for k in switcher:
            spec = entry.find(k)
            if spec is not None and spec.text is not None:
                msg += '**{}** {}\n'.format(k.capitalize()+':',
                                            html.unescape(spec.text.replace(
                                                '<br />',
                                                ''
                                            )))
        msg += 'https://myanimelist.net/anime/{}'.format(entry.find('id').text)

        await self.Duckbot.send_message(message.channel,
                                     msg)
    
    #Bot talking back to user
    
@bot.command(pass_context=True)
async def Boi(ctx):
	await bot.say("Wot BOi")

@bot.command(pass_context=True)
async def Yeet(ctx):
	await bot.say("YEET")  
  
@bot.command(pass_context=True)
async def thonk(ctx):
	await bot.say(":thonk:")
	
#Log in your bot
    
bot.run("BOT_TOKEN_HERE")
