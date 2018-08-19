import discord
from discord.ext import commands

with open('token.txt', 'r') as infile:
    TOKEN = infile.readline()

client = commands.Bot(command_prefix = '!') 
emos = {}

@client.event
async def on_ready():
    print('Bot is ready')

    #gets all custom emojis
    for x in client.get_all_emojis():
        emos[x.name] = x
    print(emos)
        
@client.event
async def on_message(message):
    content = message.content
    if 'router' in content or 'splitter' in content:
        await client.add_reaction(message, emos['router'])
    print('rerout msg')
    await client.process_commands(message)

@client.event
async def on_message_edit(before, after):
    await on_message(after)
   
@client.command(pass_context=True)
async def clear(ctx, limit=100):
    channel = ctx.message.channel 
    message = [msg async for msg in client.logs_from(channel, limit=int(limit)+1)]
    await client.delete_messages(message)

client.run(TOKEN)
