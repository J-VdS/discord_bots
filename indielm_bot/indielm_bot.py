import discord
from discord.ext import commands

import ping_server #to ping all the servers
import asyncio

with open('token.txt', 'r') as infile:
    data = [i.strip('\n') for i in infile.readlines()]
    TOKEN = data[0] #first line in token.txt
    OWNERID = data[1] #second line in token.txt
    BOT_CHANNEL = data[2]

with open('servers.txt', 'r') as infile:
    #servername, ownerID
    SERVERS = [i.strip().split(', ') for i in infile.readlines()]
print(SERVERS)

client = commands.Bot(command_prefix = '!') 
offline_msg = None
emos = {}
channels = {}

async def isowner(ctx):
    return (ctx.message.author.id == OWNERID) 

@client.event
async def on_ready():
    print('Bot is ready')

    #gets all custom emojis
    for x in client.get_all_emojis():
        emos[x.name] = x
    print(emos)
    for x in client.get_all_channels():
        channels[x.name] = x
    print('channels:',channels)
    
    #await ping_server.check(channels[BOT_CHANNEL], client, SERVERS)
        
@client.event
async def on_message(message):
    content = message.content
    if 'router' in content or 'splitter' in content:
        await client.add_reaction(message, emos['router'])
    await client.process_commands(message)

@client.event
async def on_message_edit(before, after):
    await on_message(after)
   
@client.command(pass_context=True,
                brief='-> deletes messages',
                description='deletes 99 messages, server-owner only')
async def clear(ctx, number=99):
    if await isowner(ctx):
        number = 99 if (number > 99) else number
        channel = ctx.message.channel
        message = [msg async for msg in client.logs_from(channel, limit=int(number)+1)]
        await client.delete_messages(message)

@client.command(pass_context=True,
                brief='-> your id',
                description='your discord id')
async def my_id(ctx):
    await client.say('Your discord id: %s' %(ctx.message.author.id))
    


client.run(TOKEN)
