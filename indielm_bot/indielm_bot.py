import discord
from discord.ext import commands

import ping_server #to ping all the servers
import sqlite_mindustry #database stuff
import asyncio

with open('token.txt', 'r') as infile:
    data = [i.strip('\n') for i in infile.readlines()]
    TOKEN = data[0] #first line in token.txt
    OWNERID = data[1] #second line in token.txt
    BOT_CHANNEL = data[2]
    DB = data[3]

with open('servers.txt', 'r') as infile:
    #servername, ownerID
    SERVERS = [i.strip().split(',') for i in infile.readlines()]
print('servers:\n', SERVERS)
print('Discord server data:')

client = commands.Bot(command_prefix = '!') 
offline_msg = None
emos = {}
channels = {}


async def isowner(ctx):
    return (ctx.message.author.id == OWNERID) 


@client.event
async def on_ready():
    #gets all custom emojis
    for x in client.get_all_emojis():
        emos[x.name] = x
    print(emos)
    #gets all the discord channels
    for x in client.get_all_channels():
        channels[x.name] = x
    print('channels:',channels)
    sqlite_mindustry.make_db(DB)    
    print('Bot is ready')
    await ping_server.check(channels[BOT_CHANNEL], client, SERVERS)
    
        
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
    

@client.command(pass_context=True,
                brief='-> make an account in DM',
                description='Press !signup followed by your username and password in DM')
async def signup(ctx, login=None, password=None):
    info = '''
    Press !signup followed by your username and password (in this chat).
You are able to change them with !changeLogin and see them with !showLogin.
**important:** The system isn't case sensitive.
    '''
    #channels safety
    ID = ctx.message.author.id
    if ctx.message.channel in channels.values():
        await client.delete_message(ctx.message)
        await client.say('Resume your sign up process in DM')
        await client.send_message(ctx.message.author, info)
    elif login==None or password==None:
        await client.say(info)
    elif len(ctx.message.content.split(' ')) > 3:
        await client.say('**Don\'t use spaces in your password or username**')
        await client.say(info)
    elif sqlite_mindustry.check(DB, ID, login):
        await client.say('already in database!')
    else:
        succes = sqlite_mindustry.insert(DB, ID, login.lower(), password.lower())
        await client.say('Success!' if succes else 'Sign up failed!')
        

@client.command(pass_context=True,
                brief='-> shows your username and login',
                description='Press !showLogin in DM')
async def showLogin(ctx):
    author = ctx.message.author
    if ctx.message.channel in channels.values():
        await client.delete_message(ctx.message)
    login, password = sqlite_mindustry.get_data(DB, author.id)[0]
    embed = discord.Embed(title='**Your account:**',
                          colour=123123                          
                          )
    embed.add_field(name='USERNAME:', value=login, inline=True)
    embed.add_field(name='PASSWORD:', value=password, inline=True)
    embed.set_footer(text='''If you see "error", something went wrong, contact us.
                     This message will destroy itself after 60 seconds.''')
    msg = await client.send_message(author, embed=embed)
    await asyncio.sleep(60)
    await client.delete_message(msg)
    

@client.command(pass_context=True,
                brief='-> change your username and password!',
                description='Press !changeLogin in DM')
async def changeLogin(ctx, login=None, password=None):
    info='''
    Press !changeLogin followed by your new username and new password (in this chat).
**important:** The system isn't case sensitive.
    '''
    author = ctx.message.author
    if ctx.message.channel in channels.values():
        await client.delete_message(ctx.message)
        await client.send_message(author, info)
    elif login==None or password==None:
        await client.say(info)
    else:
        succes = sqlite_mindustry.changeLogin(DB, author.id, login.lower(), password.lower())
        await client.say('Success!' if succes else 'Change login failed!')


@client.command(pass_context=True,
                brief='->deletes your data from database')
async def deleteLogin(ctx):
    if ctx.message.channel in channels.values():
        await client.delete_message(ctx.message)
    succes = sqlite_mindustry.delete(DB, ctx.message.author.id)
    await client.send_message(ctx.message.author, 'Data deleted' if succes else 'Failed')
    

client.run(TOKEN)
