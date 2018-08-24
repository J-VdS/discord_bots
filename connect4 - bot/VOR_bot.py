# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 13:34:14 2018

@author: Jeroen VdS
"""

import VOR_functions as Vf

import discord
from discord.ext import commands

with open('token.txt', 'r') as infile:
    data = [i.strip() for i in infile.readlines()]
    TOKEN = data[0]
del data

client = commands.Bot('.4')
games = {}

@client.event
async def on_ready():
    print('Bot is ready')
    print('prefix = .4')

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.channel
    player = ctx.message.author
    if (channel in games):
        if len(games[channel])<3:
            
            msg = await client.say('''Let the game begin.
You are red and you are playing against %s.
%s you may start.
To make a move, type .4move followed by a number. The number needs to be between
1 and 7 (each number represents a column)                                
            ''' %(games[channel][1], games[channel][1].mention))
            games[channel] += [player,msg]
            
        else:
            await client.say('Wait till the current game is finished!')
    else:
        games[channel] = [42*'E', player]
        await client.say('waiting for other player\nYou are yellow.')

@client.command(pass_context=True)
async def move(ctx, spot):
    channel = ctx.message.channel
    player = ctx.message.author
    if not(channel in games):
        await client.say("You need to start a game first!")
        return
    elif not(player in games[channel]):
        await client.say("Player error, reported")
        return
    
    checker = Vf.move('Y' if (games[channel].index(player)==1) else 'R',
                      games[channel][0],
                      int(spot)-1)
    if len(checker) != 4:
        await client.say("Put your coin somewhere else, column full!")
    else:
        await client.delete_message(games[channel][-1])
        games[channel][-1] =await client.send_file(channel, checker[0])
        if not checker[2]:
            games[channel][0] = checker[1]
            await client.say('%s, it is your turn' %(games[channel][2].mention if (checker[3]=='Y') else games[channel][1].mention))
        else:
            #one line lol
            await client.say('%s won!' %(games[channel][1].mention if (checker[3]=='Y') else games[channel][2].mention))
            del games[channel]

client.run(TOKEN)