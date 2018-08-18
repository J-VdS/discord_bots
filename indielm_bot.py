import discord
from discord.ext import commands

with open('token.txt', 'r') as infile:
    TOKEN = infile.readline()

client = commands.Bot(command_prefix = '.%') #not used
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

@client.event
async def on_message_edit(before, after):
    await on_message(after)
   
client.run(TOKEN)
