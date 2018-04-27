#Duckbot by turnt ducky

import discord
from discord.ext import commands
from discord.ext.commands import bot
from datetime import datetime
import random
import asyncio
import chalk
import discord

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
    await bot.say(datetime.now() - starttime)

@bot.command(pass_context=True)
async def ping(message, current_shard):
    now = datetime.datetime.utcnow()
    msg_time_stamp = message.timestamp
    difference = now - msg_time_stamp
    return "**PONG**\nReply in {} s from **SHARD {}**".format(str(difference), str(current))

@bot.command()
async def restart():
    command = "/Documents/Duckbot/Duckbot.py shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]

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

@bot.command(pass_context=True)
async def clear(ctx):
    channel = ctx.message.channel
    to_delete = list()
    for message in bot.messages:
        if message.channel == channel:
            print(message.author)
            if message.author.name == 'turnt ducky':
                to_delete.append(message)
            elif message.content[0] == '?' and len(message.content) > 2:
                to_delete.append(message)
    await bot.delete_messages(to_delete)

@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's what I could find.", color=0x00ff00)
    embed.set_author(name="Turnt Ducky")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
@commands.has_role("ðŸ˜‚ðŸ‘Œ Friends")
async def kick(ctx, user: discord.Member):
    await bot.say(":boot: Cya, {}. Ya Bish!".format(user.name))
    await bot.kick(user)

@bot.command(pass_context=True)
async def embed(ctx):
    embed = discord.Embed(title="test", description="Ducky was here", color=0x00ff00)
    embed.set_footer(text="this is a footer")
    embed.set_author(name="Turnt Ducky")
    embed.add_field(name="This is a field", value="no it isn't", inline=True)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def helpme(ctx):
    embed = discord.Embed(title="**Commands**", description="==========", color=0x00ff00)
    embed.add_field(name="Duckbot uptime", value="See how many hours its been since Duckbot has been active", inline=True)
    embed.add_field(name="Duckbot ping", value="Does Duckbot have a bit of a delay", inline=True)
    embed.add_field(name="Duckbot roll", value="Cant decide what you should do. Roll a virtual die", inline=True)
    embed.add_field(name="Duckbot info [@ the person]", value="Get some basic info on someone", inline=True)
    embed.add_field(name="Duckbot serverinfo", value="Get basic info on this server", inline=True)
    embed.add_field(name="Duckbot helpme", value="Have this text popup", inline=True)
    embed.set_footer(text="Stay turnt everyone :)")
    await bot.say(embed=embed)

bot.run("process.env.BOY_TOKEN")
